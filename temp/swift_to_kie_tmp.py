"""임시 변환: swift 추출 jsonl 의 질문·답을 kie 꼴(한국어 질문, {키: 값} 객체 답)로 바꾼 새 jsonl 을 만든다.

  python swift_to_kie_tmp.py <입력.jsonl> <출력.jsonl>

- 키 목록은 각 줄 질문의 'in order: ["키", …]' 에서 자동으로 뽑는다.
- 답 배열을 그 순서대로 키에 짝지어 {"키": "값", …} 객체로. 빈 값("")은 null.
- 같은 키가 두 번 나오면 두 번째부터 '키#2' (JSON 객체는 같은 키를 두 번 못 쓴다).
- images 등 다른 칸은 그대로. 원본은 고치지 않는다. 바꿀 수 없는 줄은 건너뛰고 수를 알려 준다.
"""
import json
import re
import sys
from pathlib import Path

PROMPT = ("이 문서에서 아래 항목의 값을 찾아 JSON 객체로 답하세요. {{\"키\": \"문서에 적힌 값 그대로\", …}} 꼴로 쓰고, "
          "값이 여러 개면 줄바꿈으로 이어 한 문자열로 쓰세요. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 null 로 답하세요.\n"
          "항목 (키: 서식의 항목명)\n{items}")
ORDER = re.compile(r"in order:\s*(\[.*?\])", re.S)


def keys_of(prompt):
    m = ORDER.search(prompt)
    if not m:
        raise ValueError("질문에 'in order: [...]' 가 없습니다")
    seen, keys = {}, []
    for f in json.loads(m.group(1)):
        seen[f] = seen.get(f, 0) + 1
        keys.append(f if seen[f] == 1 else f"{f}#{seen[f]}")
    return keys


def convert(rec):
    user, assistant = rec["messages"]
    keys = keys_of(user["content"])
    values = json.loads(assistant["content"])
    if not isinstance(values, list) or len(values) != len(keys):
        raise ValueError(f"답 개수 {len(values) if isinstance(values, list) else '?'} ≠ 키 개수 {len(keys)}")
    answer = {k: (v if isinstance(v, str) and v.strip() else None) for k, v in zip(keys, values)}
    items = "\n".join(f"- {k}: -" for k in keys)
    images = "<image>" * user["content"].count("<image>")
    return {**rec, "messages": [{**user, "content": images + PROMPT.format(items=items)},
                                {**assistant, "content": json.dumps(answer, ensure_ascii=False)}]}


def main(src, dst):
    if Path(dst).exists():
        sys.exit(f"{dst} 가 이미 있습니다")
    out, skipped = [], []
    for n, line in enumerate(Path(src).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            out.append(convert(json.loads(line)))
        except (ValueError, KeyError, TypeError) as exc:
            skipped.append((n, str(exc)))
    Path(dst).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")
    print(f"{len(out)}줄 → {dst}" + (f", {len(skipped)}줄 건너뜀 (예: {skipped[0][0]}번째 줄 {skipped[0][1]})" if skipped else ""))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
