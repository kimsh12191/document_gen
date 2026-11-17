"""임시 변환: 그림 + 라벨 json 쌍이 든 폴더 → ms-swift .jsonl (kie). 그림은 그대로 두고 경로만 적는다.

폴더 안의 쌍: 같은 이름(확장자만 다름) — 007009.json ↔ 007009.jpg/.jpeg/.png/.tif/.tiff/.bmp/.webp
라벨 json: {"항목명": "값", …} 평평한 객체 (예: {"성명(상호명)": "주식회사 …", "귀속월": "2023년 5월분", …})
  - 값이 빈 글("")·공백·null → 정답 null (문서에 비어 있는 칸)
  - 숫자는 글로 바꾼다. 안쪽 객체는 '바깥.안쪽' 키로 편다. 목록 값은 그 키를 건너뛰고 수를 알려 준다 (표는 아직 안 다룸)
  - 같은 키가 두 번 나오면 두 번째부터 '키#2' (같은 항목명 중 2번째 칸) — 합성 kie·v3 와 같은 표기

한 줄: {"messages": [{"role": "user", "content": "<image>질문"}, {"role": "assistant", "content": "[{\"key\": …, \"value\": …}, …]"}],
        "images": ["/절대/경로.jpg"]}
  질문: --prompt value (기본, 학습용) 값만 묻는 kie 문장 + '- 키: 항목명' 줄
        --prompt synthetic 합성 kie 문장(docgen/bench/prompts.py 의 P_KIE, 위치까지 물음) 그대로 — temp/swift_to_kie_v3_tmp.py 와 같은 꼴
        (라벨에 위치가 없으므로 학습 데이터에는 value 를 쓴다. synthetic 으로 학습하면 '위치도 답하라'는 질문에 위치 없는 답을 가르친다)
  정답: [{"key": 키, "value": 값 또는 null}, …]  항목이 40개를 넘으면 40개씩 나눠 여러 줄 (합성 kie 와 같음)
  채점: train/scorers/kie_list_scorer.py (값 채점, 주 지표 f1) — 평가 세트로 쓸 때
        {"id": "real-<이름>", "format": "swift-fields", "gt": "reviewed", "paths": ["<출력.jsonl>"], "scorer": "../scorers/kie_list_scorer.py:score"}

  python temp/pairs_to_swift_kie_tmp.py <폴더> <출력.jsonl> [--prompt value|synthetic] [--labels labels.json] [--recursive]
  python temp/pairs_to_swift_kie_tmp.py keys <폴더> [--recursive] > labels.json     키 목록·나온 횟수 (항목명을 따로 붙일 때)

- --labels: {"키": "항목명"} 표. 없으면 항목명 = 키 (라벨 키가 이미 한국어 항목명이면 그대로 둬도 된다).
- 짝이 없는 그림·json, 읽을 수 없는 json 은 건너뛰고 수와 예를 알려 준다. 출력 파일이 이미 있으면 멈춘다 (덮어쓰지 않음).
- 같은 그림의 줄은 이어서 쓴다. 학습/평가를 나눌 때는 그림 단위로 나눈다 (한 그림의 줄이 양쪽에 들어가지 않게).
- 실서류 그림은 이 컴퓨터 안에서만 읽는다 (어디에도 보내지 않음).
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # 저장소 최상위 (docgen)

from docgen.bench.prompts import P_KIE  # noqa: E402

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}
MAX_ITEMS = 40
P_VALUE = ('이 문서에서 아래 항목의 값을 찾아 JSON 목록으로 답하세요. 항목마다 {{"key": 키, "value": 문서에 적힌 값 그대로}} 를 쓰세요. '
           '키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {{"key": 키, "value": null}} 로 답하세요.\n'
           '항목 (키: 서식의 항목명)\n{items}')
PROMPTS = {"value": P_VALUE, "synthetic": P_KIE}


def pairs(folder, recursive=False):
    """→ ([(그림, json)], 짝 없는 파일 목록). 같은 폴더·같은 이름끼리 짝."""
    files = sorted(p for p in (Path(folder).rglob("*") if recursive else Path(folder).iterdir()) if p.is_file())
    images = {}
    for p in files:
        if p.suffix.lower() in IMAGE_EXT:
            images.setdefault(p.with_suffix(""), []).append(p)
    out, alone, used = [], [], set()
    for p in files:
        if p.suffix.lower() != ".json":
            continue
        imgs = images.get(p.with_suffix(""), [])
        if len(imgs) != 1:
            alone.append(f"{p.name} (그림 {len(imgs)}개)")
            continue
        out.append((imgs[0].resolve(), p))
        used.add(imgs[0])
    alone += [f"{q.name} (json 없음)" for qs in images.values() for q in qs if q not in used]
    return out, alone


def _numbered(pairs_):
    """[(키, 값)] → 같은 키 두 번째부터 '키#2'."""
    seen, out = Counter(), []
    for k, v in pairs_:
        seen[k] += 1
        out.append((k if seen[k] == 1 else f"{k}#{seen[k]}", v))
    return out


def fields(path):
    """라벨 json → ([(키, 값 또는 None)], 건너뛴 목록 값 키)."""
    obj = json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=lambda kv: kv)   # 같은 키도 남긴다
    if not isinstance(obj, list) or (obj and not isinstance(obj[0], tuple)):
        raise ValueError("라벨이 {키: 값} 객체가 아닙니다")
    out, lists = [], []

    def walk(kv, prefix=""):
        for k, v in kv:
            key = f"{prefix}{str(k).strip()}"
            if isinstance(v, list) and v and isinstance(v[0], tuple):   # 안쪽 객체
                walk(v, key + ".")
            elif isinstance(v, list):
                lists.append(key)
            elif v is None or (isinstance(v, str) and not v.strip()):
                out.append((key, None))
            else:
                out.append((key, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)))
    walk(obj)
    return _numbered(out), lists


def label_of(key, labels):
    base, _, n = key.partition("#")
    lab = labels.get(key) or labels.get(base) or base
    return f"{lab} (같은 항목명 중 {n}번째 칸)" if n else lab


def records(image, kv, labels, prompt):
    out = []
    for i in range(0, len(kv), MAX_ITEMS):
        part = kv[i:i + MAX_ITEMS]
        items = "\n".join(f"- {k}: {label_of(k, labels)}" for k, _ in part)
        gold = [{"key": k, "value": v} for k, v in part]
        out.append({"messages": [{"role": "user", "content": "<image>" + prompt.format(items=items)},
                                 {"role": "assistant", "content": json.dumps(gold, ensure_ascii=False)}],
                    "images": [str(image)]})
    return out


def cmd_convert(folder, dst, prompt="value", labels_path=None, recursive=False):
    if Path(dst).exists():
        sys.exit(f"{dst} 가 이미 있습니다 (덮어쓰지 않습니다)")
    labels = {k: v for k, v in json.loads(Path(labels_path).read_text(encoding="utf-8")).items() if v} if labels_path else {}
    found, alone = pairs(folder, recursive)
    out, bad, lists, n_doc, n_null, n_field = [], [], Counter(), 0, 0, 0
    for image, js in found:
        try:
            kv, skipped = fields(js)
        except (ValueError, UnicodeDecodeError) as exc:
            bad.append(f"{js.name}: {exc}")
            continue
        lists.update(skipped)
        if not kv:
            bad.append(f"{js.name}: 항목 없음")
            continue
        out += records(image, kv, labels, PROMPTS[prompt])
        n_doc += 1
        n_field += len(kv)
        n_null += sum(v is None for _, v in kv)
    if not out:
        sys.exit(f"바꾼 쌍이 없습니다 (짝 {len(found)}, 짝 없음 {len(alone)}, 읽기 실패 {len(bad)}"
                 + (f", 예: {(bad or alone)[0]}" if bad or alone else "") + ")")
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")
    print(f"그림 {n_doc}장 → {len(out)}줄 {dst} (질문 {prompt}, 항목 {n_field}개 중 null {n_null}개 {n_null / n_field:.1%})")
    if alone:
        print(f"짝 없어 건너뜀 {len(alone)}개 (예: {', '.join(alone[:5])})")
    if bad:
        print(f"읽지 못해 건너뜀 {len(bad)}개 (예: {bad[0]})")
    if lists:
        print(f"목록 값이라 건너뛴 키 {len(lists)}종 (예: {', '.join(k for k, _ in lists.most_common(5))}) — 표는 아직 안 다룸")


def cmd_keys(folder, recursive=False):
    count = Counter()
    for _, js in pairs(folder, recursive)[0]:
        try:
            count.update(k.partition("#")[0] for k, _ in fields(js)[0])
        except (ValueError, UnicodeDecodeError):
            pass
    print(json.dumps({k: "" for k, _ in count.most_common()}, ensure_ascii=False, indent=1))
    print(f"키 {len(count)}종 (많이 나온 순, 횟수: {dict(count.most_common(5))} …). 값 칸에 항목명을 채워 --labels 로 넘기세요.",
          file=sys.stderr)


def main(argv):
    recursive = "--recursive" in argv
    argv = [a for a in argv if a != "--recursive"]
    if len(argv) == 2 and argv[0] == "keys":
        return cmd_keys(argv[1], recursive)
    opts = dict(zip(argv[2::2], argv[3::2]))
    if len(argv) >= 2 and len(argv) % 2 == 0 and set(opts) <= {"--prompt", "--labels"} \
            and opts.get("--prompt", "value") in PROMPTS:
        return cmd_convert(argv[0], argv[1], opts.get("--prompt", "value"), opts.get("--labels"), recursive)
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
