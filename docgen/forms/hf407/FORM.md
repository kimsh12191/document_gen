# 본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(영문) (`hf407`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf407 · card-hash: 3abec28f9d6e -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 10 (seed 1000000 로 그린 것) · **분류 정답:** 본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.407 (기타) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 23칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `followingbusinesses` | followingbusinesses). | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:71 | 묻기 |
| `bankruptcy` | bankruptcy | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:82 | 묻기 |
| `RevenueCode` | RevenueCode | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:94 | 묻기 |
| `USbank` | (6)U.S.bank | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:106 | 묻기 |
| `FATCANonReporting` | FATCANon-Reporting | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:117 | 묻기 |
| `requirements` | requirements | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:129 | 묻기 |
| `Investment` | Investment | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:141 | 묻기 |
| `BActiveNFFEs` | B.ActiveNFFEs | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:153 | 묻기 |
| `Participation` | Participation | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:165 | 묻기 |
| `Retirement` | Retirement | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:177 | 묻기 |
| `Fund` | Fund | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:189 | 묻기 |
| `NonReportingFI` | Non-ReportingFI | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:201 | 묻기 |
| `Investment2` | Investment | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:213 | 묻기 |
| `Office` | Office | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:225 | 묻기 |
| `Retirement2` | Retirement | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:237 | 묻기 |
| `Fund2` | Fund | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:249 | 묻기 |
| `CRSNonReporting` | CRSNon-Reporting | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:261 | 묻기 |
| `Services` | Services | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:273 | 묻기 |
| `Commission` | Commission | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:285 | 묻기 |
| `Vehicle` | Vehicle | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:297 | 묻기 |
| `Office2` | Office | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:309 | 묻기 |
| `Retirement3` | Retirement | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:321 | 묻기 |
| `Fund3` | Fund | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:333 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키 `a` ← `b`:** 질문·정답은 공통 키 a, 서식의 원래 키는 b (키 사전이 정함).
- **키는·값은:** 어디서 정해지나. 원본 서식의 "규칙"·"항목명 자동" 은 키 사전(studio 키 사전 화면, `_common/key_rules.json`)이 항목명으로 정한 것 — 모든 서식에 같이 적용. 이 서식의 그 칸만 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
- **고칠 곳:** html·코드 서식은 템플릿 줄(칸 자리·키·항목명)과 fields.json 줄(값 출처·질문 설정 q), 원본 서식은 fields.json 의 그 칸(박스 `rect`·항목명·키·값·q). html·코드 서식에서 fields.json 에 줄이 없는 칸의 질문 설정은 fields.json 맨 위 `"q": {"키": {…}}` 묶음에.

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 공통 `docgen/forms/_common/questions.json`.

### 서류 분류 `classify` · 채점 acc

질문:

```
이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. 설명 없이 서류명만 한 줄로 답하세요.
```

답:

```json
"본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(영문)"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- followingbusinesses: followingbusinesses).
- bankruptcy: bankruptcy
- RevenueCode: RevenueCode
- USbank: (6)U.S.bank
- FATCANonReporting: FATCANon-Reporting
- requirements: requirements
- Investment: Investment (같은 항목명 중 1번째 칸)
- BActiveNFFEs: B.ActiveNFFEs
- Participation: Participation
- Retirement: Retirement (같은 항목명 중 1번째 칸)
- Fund: Fund (같은 항목명 중 1번째 칸)
- NonReportingFI: Non-ReportingFI
- Investment2: Investment (같은 항목명 중 2번째 칸)
- Office: Office (은행·직원, 같은 항목명 중 1번째 칸)
- Retirement2: Retirement (같은 항목명 중 2번째 칸)
- Fund2: Fund (같은 항목명 중 2번째 칸)
- CRSNonReporting: CRSNon-Reporting
- Services: Services
- Commission: Commission
- Vehicle: Vehicle
- Office2: Office (같은 항목명 중 2번째 칸)
- Retirement3: Retirement (같은 항목명 중 3번째 칸)
- Fund3: Fund (같은 항목명 중 3번째 칸)
```

답:

```json
[{"key": "followingbusinesses", "value": null},
 {"key": "bankruptcy", "value": null},
 {"key": "RevenueCode", "value": null},
 {"key": "USbank", "value": null},
 {"key": "FATCANonReporting", "value": null},
 {"key": "requirements", "value": null},
 {"key": "Investment", "value": null},
 {"key": "BActiveNFFEs", "value": null},
 {"key": "Participation", "value": null},
 {"key": "Retirement", "value": null},
 {"key": "Fund", "value": null},
 {"key": "NonReportingFI", "value": null},
 {"key": "Investment2", "value": null},
 {"key": "Office", "value": null},
 {"key": "Retirement2", "value": null},
 {"key": "Fund2", "value": null},
 {"key": "CRSNonReporting", "value": null},
 {"key": "Services", "value": null},
 {"key": "Commission", "value": null},
 {"key": "Vehicle", "value": null},
 {"key": "Office2", "value": null},
 {"key": "Retirement3", "value": null},
 {"key": "Fund3", "value": null}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf407` → `python -m docgen.formdir card hf407` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 규칙이 항목명으로 정함 — 모든 서식 공통 규칙은 studio 키 사전) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf407 --show` · `python -m docgen.preview hf407 --out work/hf407`
