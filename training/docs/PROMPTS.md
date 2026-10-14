# 질문·답변 가이드 (OCR 과제)

학습한 모델에게 **어떻게 물으면 어떤 형식으로 답하는지** 정리한 문서입니다. 모델은 아래 질문 문장으로 학습했으므로 같은 문장으로 물을 때 가장 정확합니다. 문장을 바꾸면 답 형식이 흐트러질 수 있습니다.

질문 문장은 `bank_ocr/tasks.py`의 `PROMPTS`와 같습니다. 테스트(`tests/test_prompts_doc.py`)가 이 문서와 코드가 같은지 확인합니다.

## 공통 규칙

| 항목 | 규칙 |
|---|---|
| 이미지 | 한 질문에 이미지 1장. 긴 변 2300·짧은 변 1600 이하로 줄여서 보냅니다(서버 `IMAGE_MAX_TOKEN_NUM=3600`). 더 크면 서버가 다시 줄이면서 작은 글씨를 잃습니다 |
| 좌표 | `[x1, y1, x2, y2]`, **보낸 이미지 기준 0~1000 정수** (왼쪽 위가 0,0). 픽셀이 아닙니다. 픽셀로 바꾸려면 `x × 너비 / 1000` |
| 박스 답 형식 | `[{"bbox_2d": [x1, y1, x2, y2], "label": "글자"}]` JSON 리스트. 없으면 `[]`. ```` ```json ```` 코드 블록으로 감싸 올 수 있으니 받는 쪽에서 벗겨 냅니다 |
| 글자 답 형식 | 설명 없이 읽은 글자만. 여러 줄이면 줄바꿈 |
| 언어 | 질문마다 영어·한국어 문장 두 가지로 학습했습니다. 둘 다 됩니다 |
| 생성 설정 | `temperature 0`, `enable_thinking false`, `max_tokens 2048` (`configs/inference.json`) |
| 읽는 순서 | 위→아래 줄, 줄 안에서 왼→오른쪽 (박스 위치 기준) |
| `{box}`, `{text}` 자리 | JSON 표기로 넣습니다. 좌표는 `[120, 340, 410, 372]`, 글자는 따옴표 포함 `"대출신청금액"` |

## 과제별

### crop_ocr — 잘라낸 글자 읽기

- **언제:** 단어·값 칸 하나만 잘라낸 작은 이미지를 읽을 때
- **질문**
  - `Read all text exactly as written. Do not correct or infer characters. Return only the text.`
  - `이미지의 글자를 보이는 그대로 읽으세요. 고치거나 추측하지 말고 글자만 답하세요.`
- **답:** `2025.03.14`
- **주의:** 틀린 글자도 고치지 않고 보이는 대로 옮기도록 배웠습니다.

### bbox_ocr — 박스 안 글자 읽기

- **언제:** 페이지 전체를 주고 특정 위치의 글자를 읽을 때
- **질문**
  - `Read the exact text inside bbox_2d={box}. Coordinates are 0-1000 relative to the image. Return only the text.`
  - `bbox_2d={box} 영역 안의 글자를 그대로 읽으세요. 좌표는 이미지 기준 0~1000입니다. 글자만 답하세요.`
- **예:** `bbox_2d=[512, 233, 640, 251] 영역 안의 글자를 …` → `홍길동`
- **주의:** 학습 박스는 단어 하나 크기입니다. 넓은 영역은 `region_ocr`을 쓰세요.

### region_ocr — 영역 안 글자 전부

- **언제:** 표 한 칸, 문단, 여러 줄 영역을 통째로 읽을 때
- **질문**
  - `Read all text inside bbox_2d={box} in reading order, one line per text line. Coordinates are 0-1000 relative to the image. Return only the text.`
  - `bbox_2d={box} 영역 안의 모든 글자를 읽는 순서대로 적으세요. 줄이 바뀌면 줄바꿈하세요. 좌표는 0~1000입니다. 글자만 답하세요.`
- **답:** 줄마다 줄바꿈한 글자
  ```
  서울특별시 서초구 강남대로 357
  103동 1301호
  ```

### grounding — 글자 위치 찾기

- **언제:** "이 글자가 어디 있나"를 찾을 때. 같은 글자가 여러 번 있으면 모두 찾습니다
- **질문**
  - `Find every occurrence of the exact text {text}. Coordinates are 0-1000 relative to the image. Return only a JSON list like [{"bbox_2d": [x1, y1, x2, y2], "label": "..."}]; return [] if it does not appear.`
  - `{text} 와 정확히 같은 글자가 있는 곳을 모두 찾으세요. 좌표는 이미지 기준 0~1000입니다. [{"bbox_2d": [x1, y1, x2, y2], "label": "..."}] 형식의 JSON 리스트만 답하고, 없으면 []로 답하세요.`
- **예:** `"성명" 와 정확히 같은 글자가 …` → `[{"bbox_2d": [88, 210, 131, 228], "label": "성명"}, {"bbox_2d": [88, 655, 131, 673], "label": "성명"}]`
- **주의:** 단어 단위(OCR이 나눈 단위)로 배웠습니다. 문장 전체를 찾으면 잘 안 될 수 있습니다. 약 10%는 없는 글자를 묻는 문항이라 없으면 `[]`라고 답합니다.

### spotting — 전체 글자와 위치

- **언제:** 이미지의 모든 글자를 위치와 함께 뽑을 때
- **질문**
  - `Detect every piece of text in the image in reading order. Coordinates are 0-1000 relative to the image. Return only a JSON list like [{"bbox_2d": [x1, y1, x2, y2], "label": "text"}].`
  - `이미지의 모든 글자를 읽는 순서대로 위치와 함께 찾으세요. 좌표는 0~1000입니다. [{"bbox_2d": [x1, y1, x2, y2], "label": "글자"}] 형식의 JSON 리스트만 답하세요.`
- **답:** 단어마다 한 항목인 JSON 리스트, 읽는 순서
- **주의:** 학습 이미지는 대부분 **페이지를 잘라낸 타일**이고 타일당 단어 40개 이하입니다(`spotting_max_items`). 글자가 많은 A4 한 장을 통째로 주면 답이 길어져 `max_tokens`에서 잘리거나 빠뜨립니다. 페이지를 몇 조각으로 나눠 묻는 편이 낫습니다.

### relation — 옆 글자 찾기

- **언제:** 항목명 옆(오른쪽·아래)의 값을 찾을 때. 예: "성명" 오른쪽 글자
- **질문** (`{direction}`: `to the right of` / `to the left of` / `below` / `above`, `{direction_ko}`: 오른쪽 / 왼쪽 / 아래 / 위)
  - `Find the text immediately {direction} {anchor}. Coordinates are 0-1000 relative to the image. Return only a JSON list with one entry like [{"bbox_2d": [x1, y1, x2, y2], "label": "text"}].`
  - `{anchor} 바로 {direction_ko}에 있는 글자를 찾으세요. 좌표는 0~1000입니다. [{"bbox_2d": [x1, y1, x2, y2], "label": "글자"}] 형식으로 하나만 답하세요.`
- **`{anchor}` 쓰는 법:** 페이지에 한 번만 나오는 글자면 `"성명"`, 아니면 박스로 `the text at bbox_2d=[88, 210, 131, 228]`(한국어 문장은 `bbox_2d=[88, 210, 131, 228] 글자`)
- **답:** 항목 하나짜리 JSON 리스트 `[{"bbox_2d": [140, 210, 198, 228], "label": "홍길동"}]`
- **주의:** "바로 옆 단어 하나"를 배웠습니다. 값이 여러 단어(주소 등)면 첫 단어만 나옵니다. 값 전체는 찾은 박스를 넓혀 `region_ocr`로 읽으세요.

### marked_ocr — 그린 박스 안 글자 읽기

- **언제:** 이미지에 빨강·파랑·초록 사각형을 직접 그려서 "여기 뭐라고 써 있나"를 물을 때
- **질문** (`{color}`: red / blue / green, `{color_ko}`: 빨간 / 파란 / 초록. `{coords}`는 보통 빈칸, 좌표를 함께 줄 때 ` at bbox_2d=[…]` / `(bbox_2d=[…])`)
  - `Read the text inside the {color} box drawn on the image{coords}. Return only the text.`
  - `이미지에 그려진 {color_ko} 박스{coords_ko} 안의 글자를 그대로 읽으세요. 글자만 답하세요.`
- **답:** `56,000,000`
- **주의:** 학습 박스는 단어 하나를 감싸고, 선 두께는 글자 높이의 약 8%, 색은 순수한 빨강(225,25,25)·파랑(25,75,235)·초록(15,165,55)입니다. 한 이미지에 최대 3개(색이 다름)입니다.

### marked_box — 그린 박스의 좌표

- **언제:** 그린 박스의 좌표 숫자가 필요할 때 (화면에서 표시한 위치를 좌표로 바꾸기)
- **질문**
  - `Give the position of the {color} box drawn on the image and the text inside it. Coordinates are 0-1000 relative to the image. Return only a JSON list with one entry like [{"bbox_2d": [x1, y1, x2, y2], "label": "text"}].`
  - `이미지에 그려진 {color_ko} 박스의 위치와 그 안의 글자를 답하세요. 좌표는 이미지 기준 0~1000입니다. [{"bbox_2d": [x1, y1, x2, y2], "label": "글자"}] 형식으로 하나만 답하세요.`
- **답:** `[{"bbox_2d": [301, 452, 389, 470], "label": "56,000,000"}]` (그린 선의 바깥 테두리 좌표)

## 하고 싶은 일 → 과제

| 하고 싶은 일 | 과제 |
|---|---|
| 작은 이미지 하나 읽기 | `crop_ocr` |
| 위치를 알고 글자를 읽기 | `bbox_ocr` (단어), `region_ocr` (여러 줄) |
| 글자를 알고 위치를 찾기 | `grounding` |
| 항목명 옆 값 찾기 | `relation` → 필요하면 `region_ocr` |
| 페이지 전체 글자+위치 | `spotting` (타일로 나눠서) |
| 화면에 표시한 곳 읽기 | `marked_ocr`, `marked_box` |

viewer(`viewer/README.md`)의 spotting·grounding·region·relation 버튼도 이 질문 문장을 그대로 씁니다.
