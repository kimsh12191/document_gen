"""swift 형식 실서류 추출 데이터(.jsonl)를 이 벤치마크의 정보 추출(kie) 과제 폴더로 바꾼다.

  python -m train.swift_to_kie <swift.jsonl> ... --out <과제 폴더> [--split test|train] [--labels 항목명.json]

- 들어오는 것: train/swift_import.py 와 같은 꼴. 질문에 'in order: ["필드", …]', 답은 같은 순서의 문자열 배열.
- 나가는 것: <out>/meta.json + <out>/tasks/kie.jsonl (studio 데이터셋과 같은 과제 폴더). data.benchmark(평가)나
  data.train(학습)에 폴더 경로로 넣는다 (format 은 적지 않음).
- 질문은 합성 kie 와 같은 꼴에서 위치만 뺀 것 (아래 P_KIE_VALUE), 답은 [{"key", "value"}, …].
  위치 정답이 없어 bbox_2d·page 는 없고, 채점은 값 점수(f1)만 (위치 정답 없는 문항은 evaluate 가 위치 점수를 내지 않음).
- 빈 값("")은 null (합성 kie 와 같음). 같은 필드가 두 번 나오면 두 번째부터 '필드#2'.
- --labels: {"필드": "항목명"} JSON. 주면 항목 줄이 '- NEGO_CLCT: 매입추심구분' 처럼, 없으면 '- NEGO_CLCT: -'.
- 그림은 원래 절대 경로를 그대로 쓴다 (복사하지 않음). 읽을 수 없는 줄은 건너뛰고 수를 알려 준다.
- 평가 세트로 쓸 것과 학습에 쓸 것은 다른 파일로 따로 만든다 (같은 그림이면 섞기 단계가 막는다).
"""
import argparse
import json
from pathlib import Path

from docgen.bench.ocr_data import read_jsonl, write_json, write_jsonl

from .swift_import import item_of

# 합성 kie 질문(docgen.bench.prompts.P_KIE)과 같은 목록 꼴에서 위치만 뺀 것
P_KIE_VALUE = ("이 문서에서 아래 항목의 값을 찾아 JSON 목록으로 답하세요. 항목마다 "
               '{{"key": 키, "value": 문서에 적힌 값 그대로}} 를 쓰세요. 값이 여러 개면 줄바꿈으로 이어 한 문자열로 쓰세요. '
               '키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {{"key": 키, "value": null}} 로 답하세요.\n항목 (키: 서식의 항목명)\n{items}')


def convert(rec, source, line, base, labels, split):
    """swift 한 줄 → kie 문항 (값만, 목록 답)."""
    it = item_of(rec, source, line, base)   # 꼴 검사·필드 순서·'#2' 는 평가용 swift 읽기와 같게
    keys = it["eval"]["order"]
    lines = "\n".join(f"- {k}: {labels.get(k.split('#')[0]) or '-'}" for k in keys)
    answer = [{"key": k, "value": v if v.strip() else None} for k, v in it["answer"].items()]
    return {"id": f"kie/{source}/{line:05d}", "task": "kie", "images": it["images"],
            "prompt": P_KIE_VALUE.format(items=lines), "answer": answer,
            "eval": {"fields": {k: {"type": "text"} for k in keys}},
            "meta": {**it["meta"], "split": split, "group": "real", "writing": "real"}}


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m train.swift_to_kie", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("inputs", nargs="+", help="swift .jsonl")
    p.add_argument("--out", required=True, help="만들 과제 폴더 (새 이름)")
    p.add_argument("--split", choices=["test", "train"], default="test", help="test: 평가 세트 (기본) | train: 학습 데이터")
    p.add_argument("--gt", choices=["reviewed", "pseudo"], default="reviewed", help="정답 출처: reviewed 사람 검수 · pseudo OCR·추론 그대로")
    p.add_argument("--labels", help='필드 → 항목명 JSON ({"NEGO_CLCT": "매입추심구분", …})')
    a = p.parse_args(argv)
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"{out} 가 이미 있습니다. 새 이름으로 만드세요")
    labels = json.loads(Path(a.labels).read_text(encoding="utf-8")) if a.labels else {}
    items, skipped = [], {}
    for path in map(lambda x: Path(x).resolve(), a.inputs):
        for line, rec in enumerate(read_jsonl(path), 1):
            try:
                items.append(convert(rec, path.stem, line, path.parent, labels, a.split))
            except (ValueError, KeyError, TypeError, AttributeError) as exc:
                skipped.setdefault(path.name, []).append({"line": line, "why": str(exc)})
    if not items:
        raise SystemExit(f"바꾼 문항이 없습니다: {skipped}")
    write_jsonl(out / "tasks" / "kie.jsonl", items)
    write_json(out / "meta.json", {"name": out.name, "split": a.split, "source": "swift", "real_data": True, "gt": a.gt,
                                   "made_by": "train.swift_to_kie", "inputs": [str(Path(x).resolve()) for x in a.inputs],
                                   "counts": {"kie": len(items)}, "documents": len({it["meta"]["document_id"] for it in items}),
                                   "skipped": skipped})
    print(f"kie {len(items)}문항 → {out}" + "".join(f"\n  {n}: {len(s)}줄 건너뜀 (예: {s[0]['line']}번째 줄 {s[0]['why']})"
                                                      for n, s in skipped.items()))


if __name__ == "__main__":
    main()
