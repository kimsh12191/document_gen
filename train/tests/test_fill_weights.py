"""합친 모델에 빠진 가중치 채우기 (train/fill_weights.py): 출발 모델에만 있는 묶음(MTP 머리 mtp.*)을 바이트 그대로 채우고,
config 의 빠진 칸을 더하며, 원본 폴더는 건드리지 않는다. 이름 규칙이 바뀐 것 같으면 채우지 않는다. torch 없이 가짜 safetensors 로."""
import json
import struct

import pytest

from train import fill_weights as FW
from train import serve as S


def write_st(path, tensors: dict[str, bytes]):
    """가짜 safetensors: 이름 → 바이트 (BF16, 1차원)."""
    head, data, off = {}, b"", 0
    for k, v in tensors.items():
        head[k] = {"dtype": "BF16", "shape": [len(v) // 2], "data_offsets": [off, off + len(v)]}
        data += v
        off += len(v)
    raw = json.dumps(head).encode()
    path.write_bytes(struct.pack("<Q", len(raw)) + raw + data)


def read_st(path) -> dict[str, bytes]:
    h, start = FW._header(path)
    blob = path.read_bytes()
    return {k: blob[start + v["data_offsets"][0]:start + v["data_offsets"][1]] for k, v in h.items()}


@pytest.fixture
def models(tmp_path):
    base, merged = tmp_path / "base", tmp_path / "merged"
    base.mkdir()
    merged.mkdir()
    write_st(base / "model-00001-of-00002.safetensors", {"model.a.weight": b"AAAA", "model.b.weight": b"BBBB"})
    write_st(base / "model-00002-of-00002.safetensors", {"mtp.layers.0.w": b"MTP0MTP0", "mtp.fc.weight": b"FCFC"})
    (base / FW.INDEX).write_text(json.dumps({"metadata": {"total_size": 20}, "weight_map": {
        "model.a.weight": "model-00001-of-00002.safetensors", "model.b.weight": "model-00001-of-00002.safetensors",
        "mtp.layers.0.w": "model-00002-of-00002.safetensors", "mtp.fc.weight": "model-00002-of-00002.safetensors"}}))
    (base / "config.json").write_text(json.dumps({"model_type": "qwen3_5", "text_config": {"hidden_size": 8, "mtp_num_hidden_layers": 1}}))
    write_st(merged / "model.safetensors", {"model.a.weight": b"aaaa", "model.b.weight": b"bbbb"})   # 학습으로 바뀐 값
    (merged / "config.json").write_text(json.dumps({"model_type": "qwen3_5", "text_config": {"hidden_size": 8}}))
    return base, merged


def test_plan_finds_dropped_group_and_config(models):
    base, merged = models
    p = FW.plan(base, merged)
    assert p["missing"] == {"mtp": 2} and p["extra"] == {} and sorted(p["fill"]) == ["mtp.fc.weight", "mtp.layers.0.w"]
    assert p["config"] == {"text_config.mtp_num_hidden_layers": 1}
    r = FW.fill(base, merged)   # --out 없이는 보기만
    assert r["written"] is None and r["filled"] == 2 and sorted(p.name for p in merged.iterdir()) == ["config.json", "model.safetensors"]


def test_fill_into_new_folder_keeps_the_original(models, tmp_path):
    base, merged = models
    before = {p.name: p.read_bytes() for p in merged.iterdir()}
    out = tmp_path / "filled"
    r = FW.fill(base, merged, out=out)
    assert r["written"] == str(out) and r["filled"] == 2
    assert {p.name: p.read_bytes() for p in merged.iterdir()} == before   # 원본 폴더는 그대로
    assert (out / "model.safetensors").is_symlink() and not (out / FW.INDEX).is_symlink() and not (out / "config.json").is_symlink()
    assert read_st(out / FW.FILLED) == {"mtp.layers.0.w": b"MTP0MTP0", "mtp.fc.weight": b"FCFC"}   # 출발 모델 바이트 그대로
    idx = json.loads((out / FW.INDEX).read_text())
    assert idx["weight_map"] == {"model.a.weight": "model.safetensors", "model.b.weight": "model.safetensors",
                                 "mtp.layers.0.w": FW.FILLED, "mtp.fc.weight": FW.FILLED}
    assert idx["metadata"]["total_size"] == 8 + 12
    assert FW.weight_map(out) == idx["weight_map"] and FW.plan(base, out)["missing"] == {}
    cfg = json.loads((out / "config.json").read_text())
    assert cfg["text_config"] == {"hidden_size": 8, "mtp_num_hidden_layers": 1}
    rec = json.loads((out / FW.RECORD).read_text())
    assert rec["groups"] == {"mtp": 2} and rec["config"] == {"text_config.mtp_num_hidden_layers": 1}
    with pytest.raises(FileExistsError):
        FW.fill(base, merged, out=out)   # 덮어쓰지 않음


def test_renamed_weights_block_unless_prefix_given(models, tmp_path):
    base, merged = models
    write_st(merged / "model.safetensors", {"model.a.weight": b"aaaa", "model.b.weight": b"bbbb", "lm_head.weight": b"LLLL"})
    p = FW.plan(base, merged)
    assert p["fill"] == [] and p["blocked"] and p["extra"] == {"lm_head": 1}
    assert FW.fill(base, merged, out=tmp_path / "x")["written"] is None and not (tmp_path / "x").exists()
    r = FW.fill(base, merged, out=tmp_path / "y", prefixes=["mtp"])
    assert r["filled"] == 2 and read_st(tmp_path / "y" / FW.FILLED)["mtp.fc.weight"] == b"FCFC"


def test_in_place_and_cli(models, capsys):
    base, merged = models
    FW.main([str(base), str(merged)])
    assert json.loads(capsys.readouterr().out)["missing"] == {"mtp": 2}
    FW.main([str(base), str(merged), "--in-place"])
    assert FW.plan(base, merged)["missing"] == {} and (merged / FW.RECORD).exists()
    assert read_st(merged / "model.safetensors") == {"model.a.weight": b"aaaa", "model.b.weight": b"bbbb"}   # 합친 가중치는 그대로


def test_pipeline_fills_after_merge_and_never_fails(models, tmp_path, capsys):
    base, merged = models
    S.fill_from_base(str(base), merged)
    assert FW.plan(base, merged)["missing"] == {} and "2개를 채움" in capsys.readouterr().out
    S.fill_from_base(str(tmp_path / "nothing"), merged)   # 출발 모델을 못 읽어도 평가는 계속
    assert "WARNING" in capsys.readouterr().out
    assert S.EVAL_DEFAULTS["fill_from_base"] is True
