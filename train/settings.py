"""공통: 설정 읽기 (JSON, YAML 은 학습 설정만), 설정 겹치기, 로그, 이미지 토큰 계산, 파일 잠금 (여러 실행이 같은 캐시를 만들 때)."""
import json
import math
import os
import socket
import time
from contextlib import contextmanager
from pathlib import Path


def load_settings(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
    else:
        try:
            import yaml
        except ImportError as exc:
            raise ValueError("YAML training configs require PyYAML (pip install pyyaml)") from exc
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML config: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("Config must be an object/mapping")
    if any(not isinstance(key, str) for key in value):
        raise ValueError("Config keys must be strings")
    return value


def merged(base, override):
    """dict 칸은 칸마다 겹쳐 쓴다."""
    result = dict(base)
    for key, value in override.items():
        result[key] = merged(base[key], value) if isinstance(value, dict) and isinstance(base.get(key), dict) else value
    return result


def log(message):
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ") + message, flush=True)


def image_tokens(model_dir, max_size):
    """Visual tokens needed for an image of max_size, from the model's vision config."""
    config = json.loads((Path(model_dir) / "config.json").read_text(encoding="utf-8"))
    vision = config.get("vision_config", {})
    patch, merge = vision.get("patch_size"), vision.get("spatial_merge_size")
    if not patch or not merge:
        raise ValueError("config.json has no vision_config.patch_size/spatial_merge_size")
    factor = patch * merge
    return image_tokens_for(max_size, factor), factor


def image_tokens_for(max_size, factor):
    return math.ceil(max(max_size) / factor) * math.ceil(min(max_size) / factor)


def pixel_factor(model_dir):
    """그림 조각 한 변의 픽셀 (patch × merge). 못 읽으면 32."""
    try:
        return image_tokens(model_dir, [32, 32])[1]
    except (OSError, ValueError, TypeError, KeyError) as exc:
        log(f"WARNING: {exc}; assuming 32x32 pixels per visual token")
        return 32


def _stale(lock: Path) -> bool:
    """잠근 실행이 이 서버에서 이미 끝났는지 (다른 서버가 잠근 것은 알 수 없어 기다린다)."""
    try:
        host, pid = lock.read_text().split()
    except (OSError, ValueError):
        try:
            return time.time() - lock.stat().st_mtime > 60   # 쓰다 만 잠금
        except OSError:
            return True
    if host != socket.gethostname():
        return False
    try:
        os.kill(int(pid), 0)
        return False
    except ProcessLookupError:
        return True
    except (PermissionError, ValueError):
        return False


@contextmanager
def locked(target, what):
    """<target>.lock 을 잡는다. 다른 실행이 잡고 있으면 끝날 때까지 기다린다 (같은 평가 세트·답을 두 번 만들지 않게)."""
    lock = Path(str(target) + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    noted = False
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            if _stale(lock):
                lock.unlink(missing_ok=True)
                continue
            if not noted:
                log(f"{what}: 다른 실행이 만드는 중이라 끝나기를 기다립니다 ({lock}; 그 실행이 없는데 계속 기다리면 이 파일을 지우세요)")
                noted = True
            time.sleep(10)
            continue
        os.write(fd, f"{socket.gethostname()} {os.getpid()}".encode())
        os.close(fd)
        break
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)
