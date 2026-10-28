"""임시 변환 v2: kie 질문을 고쳐 다시 쓴 새 jsonl 을 만든다. 그림·정답은 그대로, 질문 문장만 바뀐다.

v1(swift_to_kie_tmp.py) 질문에서 모델이 예시 '{"키": "문서에 적힌 값 그대로", …}' 를 그대로 베끼고(정답에 없는 키 → 감점),
항목명이 '-' 라 낯선 키(NEGO_CLCT, MAILTO …)는 어느 칸인지 몰라 포기하는 일이 있었다. v2 는
  1. 답 꼴 예시를 그 문항의 실제 키로 쓴다:  답 꼴: {"HSCODE": "…", "NO_EXPORT": "…"}   (따라 쓸 자리표시 글자가 없다)
  2. 키 옆에 한국어 항목명을 넣는다 (--labels 표, 없으면 '-' 그대로)

  python temp/swift_to_kie_v2_tmp.py keys   <입력.jsonl> … > labels.json      키 목록·나온 횟수 → 항목명을 채울 표 (빈 칸)
  python temp/swift_to_kie_v2_tmp.py convert <입력.jsonl> <출력.jsonl> [--labels labels.json]

- 입력은 v1 로 바꾼 파일(정답이 {키: 값} 객체)이나 swift 원본(질문에 'in order: [...]', 정답이 값 배열) 둘 다 받는다.
- labels.json: {"HSCODE": "HS 부호", "NO_EXPORT": "수출신고번호", …}. 표에 없는 키는 '-'.
  같은 키가 두 번 나오는 '키#2' 는 '키' 의 항목명 뒤에 ' (두 번째)'.
- 출력 파일이 이미 있으면 멈춘다 (덮어쓰지 않음). 바꿀 수 없는 줄은 건너뛰고 수를 알려 준다.
- 채점은 v1 과 같은 train/scorers/swift_kie_scorer.py (정답 {키: 값} 그대로, 질문의 '- 키: …' 줄에서 키 순서를 읽음).
  평가 세트는 새 id 로 (예: real-fx-po-v2) — 질문이 바뀌면 v1 점수와 같은 시험이 아니다.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

PROMPT = ("이 문서에서 아래 항목의 값을 찾아 JSON 객체 하나로 답하세요.\n"
          "아래 키를 그대로 쓰고, 값은 문서에 적힌 그대로 옮기세요. 값이 여러 개면 줄바꿈으로 이어 한 문자열로 쓰고, "
          "문서에 비어 있거나 없는 항목은 null 로 답하세요. 설명 없이 JSON 만 답하세요.\n"
          "답 꼴: {shape}\n"
          "항목 (키: 서식의 항목명)\n{items}")
ORDER = re.compile(r"in order:\s*(\[.*?\])", re.S)
V1_ITEM = re.compile(r"^- (.+): -\s*$", re.M)


def _numbered(keys):
    seen, out = {}, []
    for k in keys:
        seen[k] = seen.get(k, 0) + 1
        out.append(k if seen[k] == 1 else f"{k}#{seen[k]}")
    return out


def parse(rec):
    """한 줄 → (그림 표시 '<image>…', 키 목록, {키: 값} 정답)."""
    user, assistant = rec["messages"]
    images = "<image>" * user["content"].count("<image>")
    answer = json.loads(assistant["content"])
    m = ORDER.search(user["content"])
    if m:   # swift 원본: 질문의 in order 목록 + 값 배열
        keys = _numbered(json.loads(m.group(1)))
        if not isinstance(answer, list) or len(answer) != len(keys):
            raise ValueError(f"답 개수 {len(answer) if isinstance(answer, list) else '?'} ≠ 키 개수 {len(keys)}")
        answer = {k: (v if isinstance(v, str) and v.strip() else None) for k, v in zip(keys, answer)}
        return images, keys, answer
    if not isinstance(answer, dict):   # v1 변환본: {키: 값} 정답, 질문의 '- 키: -' 줄이 순서
        raise ValueError("정답이 {키: 값} 객체도 값 배열도 아닙니다")
    keys = V1_ITEM.findall(user["content"]) or list(answer)
    if set(keys) != set(answer):
        keys = list(answer)
    return images, keys, answer


def label_of(key, labels):
    base, _, n = key.partition("#")
    lab = labels.get(key) or labels.get(base)
    if not lab:
        return "-"
    return lab + (" (두 번째)" if n == "2" else f" ({n}번째)" if n else "")


def convert(rec, labels):
    user, assistant = rec["messages"]
    images, keys, answer = parse(rec)
    shape = "{" + ", ".join(f'"{k}": "…"' for k in keys) + "}"
    items = "\n".join(f"- {k}: {label_of(k, labels)}" for k in keys)
    return {**rec, "messages": [{**user, "content": images + PROMPT.format(shape=shape, items=items)},
                                {**assistant, "content": json.dumps({k: answer.get(k) for k in keys}, ensure_ascii=False)}]}


def lines(path):
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            yield n, json.loads(line)


def cmd_keys(paths):
    count = Counter()
    for p in paths:
        for _, rec in lines(p):
            try:
                count.update(k.partition("#")[0] for k in parse(rec)[1])
            except (ValueError, KeyError, TypeError):
                pass
    print(json.dumps({k: "" for k, _ in count.most_common()}, ensure_ascii=False, indent=1))
    print(f"키 {len(count)}개 (많이 나온 순). 값 칸에 한국어 항목명을 채워 --labels 로 넘기세요.", file=sys.stderr)


def cmd_convert(src, dst, labels_path=None):
    if Path(dst).exists():
        sys.exit(f"{dst} 가 이미 있습니다 (덮어쓰지 않습니다)")
    labels = {k: v for k, v in json.loads(Path(labels_path).read_text(encoding="utf-8")).items() if v} if labels_path else {}
    out, skipped, missing = [], [], Counter()
    for n, rec in lines(src):
        try:
            r = convert(rec, labels)
            out.append(r)
            missing.update(k for k in parse(rec)[1] if label_of(k, labels) == "-")
        except (ValueError, KeyError, TypeError) as exc:
            skipped.append((n, str(exc)))
    Path(dst).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")
    print(f"{len(out)}줄 → {dst}" + (f", {len(skipped)}줄 건너뜀 (예: {skipped[0][0]}번째 줄 {skipped[0][1]})" if skipped else ""))
    if missing:
        print(f"항목명이 없는 키 {len(missing)}개 ('-' 로 둠): {', '.join(k for k, _ in missing.most_common(15))}")


def main(argv):
    if len(argv) >= 2 and argv[0] == "keys":
        return cmd_keys(argv[1:])
    if len(argv) in (3, 5) and argv[0] == "convert" and (len(argv) == 3 or argv[3] == "--labels"):
        return cmd_convert(argv[1], argv[2], argv[4] if len(argv) == 5 else None)
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
