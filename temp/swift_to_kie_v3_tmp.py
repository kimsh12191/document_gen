"""임시 변환 v3: 실서류 추출 jsonl 을 합성 kie 와 같은 꼴로 바꾼 새 jsonl 을 만든다. 그림은 그대로, 질문·정답의 꼴만 바뀐다.

모델은 합성 kie 꼴로만 추출을 배웠다 (질문 = docgen/bench/prompts.py 의 P_KIE, 답 = [{"key", "value", "bbox_2d", "page"}] 목록).
실서류 평가도 같은 꼴로 물으면 "처음 보는 질문 꼴" 탓에 틀리는 부분이 빠지고, 읽기·키 찾기만 잰다.
  질문: P_KIE 문장 그대로 + '- 키: 항목명' 줄 (항목명은 --labels 표, 없으면 키 그대로)
  정답: [{"key": 키, "value": 값 또는 null}, …]  (위치 정답이 없어 key·value 만)
  채점: train/scorers/kie_list_scorer.py — 합성 kie 와 같은 값 채점, 주 지표 f1 (위치 정답이 없으니 위치 점수는 뺀다)

  python temp/swift_to_kie_v3_tmp.py keys   <입력.jsonl> … > labels.json      (v2 와 같은 표를 써도 된다)
  python temp/swift_to_kie_v3_tmp.py convert <입력.jsonl> <출력.jsonl> [--labels labels.json]

- 입력은 swift 원본(질문에 'in order: [...]', 정답 값 배열), v1·v2 변환본(정답 {키: 값} 객체) 모두 받는다.
- 항목이 40개를 넘는 줄은 40개씩 나눠 여러 줄로 쓴다 (합성 kie 가 한 질문에 최대 40개로 학습).
- 같은 키가 두 번 나오는 '키#2' 는 항목명 뒤에 '(같은 항목명 중 2번째 칸)' — 합성 kie 와 같은 표기.
- 출력 파일이 이미 있으면 멈춘다 (덮어쓰지 않음). 바꿀 수 없는 줄은 건너뛰고 수를 알려 준다.
- 평가 세트는 새 id 로 (예: real-fx-po-v3) — v1·v2 점수와 같은 시험이 아니다.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # 같은 폴더의 v2 (키 읽기·항목명 표)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # 저장소 최상위 (docgen)

from swift_to_kie_v2_tmp import cmd_keys, lines, parse  # noqa: E402

from docgen.bench.prompts import P_KIE  # noqa: E402

MAX_ITEMS = 40


def label_of(key, labels):
    base, _, n = key.partition("#")
    lab = labels.get(key) or labels.get(base) or base
    return f"{lab} (같은 항목명 중 {n}번째 칸)" if n else lab


def convert(rec, labels):
    """한 줄 → v3 줄 목록 (항목 40개마다 한 줄)."""
    user, assistant = rec["messages"]
    images, keys, answer = parse(rec)
    out = []
    for i in range(0, len(keys), MAX_ITEMS):
        part = keys[i:i + MAX_ITEMS]
        items = "\n".join(f"- {k}: {label_of(k, labels)}" for k in part)
        gold = [{"key": k, "value": answer.get(k)} for k in part]
        out.append({**rec, "messages": [{**user, "content": images + P_KIE.format(items=items)},
                                        {**assistant, "content": json.dumps(gold, ensure_ascii=False)}]})
    return out


def cmd_convert(src, dst, labels_path=None):
    if Path(dst).exists():
        sys.exit(f"{dst} 가 이미 있습니다 (덮어쓰지 않습니다)")
    labels = {k: v for k, v in json.loads(Path(labels_path).read_text(encoding="utf-8")).items() if v} if labels_path else {}
    out, skipped, missing, n_in = [], [], set(), 0
    for n, rec in lines(src):
        n_in += 1
        try:
            out += convert(rec, labels)
            missing.update(k.partition("#")[0] for k in parse(rec)[1] if not (labels.get(k) or labels.get(k.partition("#")[0])))
        except (ValueError, KeyError, TypeError) as exc:
            skipped.append((n, str(exc)))
    Path(dst).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")
    print(f"{n_in - len(skipped)}줄 → {len(out)}줄 {dst}" + (f" (항목 {MAX_ITEMS}개 넘는 줄은 나눔)" if len(out) > n_in - len(skipped) else "")
          + (f", {len(skipped)}줄 건너뜀 (예: {skipped[0][0]}번째 줄 {skipped[0][1]})" if skipped else ""))
    if missing:
        print(f"항목명이 없어 키를 그대로 쓴 키 {len(missing)}개: {', '.join(sorted(missing)[:15])}")


def main(argv):
    if len(argv) >= 2 and argv[0] == "keys":
        return cmd_keys(argv[1:])
    if len(argv) in (3, 5) and argv[0] == "convert" and (len(argv) == 3 or argv[3] == "--labels"):
        return cmd_convert(argv[1], argv[2], argv[4] if len(argv) == 5 else None)
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
