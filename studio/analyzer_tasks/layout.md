# 작업: 서식 이미지 → 값 영역 초안 (overlay 서식)

`input/page_<쪽>.png` 는 서식 한 장(또는 여러 쪽)의 그림이다. 고객이 손으로 적거나 체크하는 **값 자리**를 찾아 `output/layout.json` 에 쓴다.
작업 폴더 밖의 파일은 바꾸지 않는다.

{target}

## 형식

```json
{"items": [
  {"t": "text",  "page": 0, "label": "성명",     "rect": [x0, y0, x1, y1], "key": "customer.name"},
  {"t": "check", "page": 0, "label": "주택소유", "rect": [x0, y0, x1, y1], "options": [{"text": "자가", "box": [x0, y0, x1, y1]}]},
  {"t": "sign",  "page": 1, "label": "신청인",   "rect": [x0, y0, x1, y1]}
]}
```

- 좌표는 **그 쪽 그림의 픽셀** (왼쪽 위 0,0). `rect` 는 값이 들어갈 빈 칸 (항목명 칸이 아니라 그 옆·아래의 빈 곳).
- `t`: `text`(글자 칸), `check`(□ 보기들, `options` 에 보기 글자와 □ 위치), `sign`(서명·날인 자리), `date`(년·월·일 칸 묶음).
- `label` 은 서식에 적힌 항목명 그대로. `key` 는 `input/keys.json` 의 표준 키 중 맞는 것이 있으면 쓰고 없으면 뺀다.
- 이미 인쇄된 글자(견본 값 포함)는 값 자리가 아니다. 표의 반복 행은 행마다 하나씩.
{ocr_hint}

{feedback}
