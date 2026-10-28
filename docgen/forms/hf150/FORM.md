# 《기업》근저당권유용합의서 (`hf150`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf150 · card-hash: 2b10be1b2bda -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 《기업》근저당권유용합의서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.150 (대출) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `근저당권설정내역` | 근저당권설정내역 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:73 | 묻기 |
| `채권최고액` | 채권최고액 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name` | 채무자 | text | 1쪽 [203, 293, 269, 305] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `근저당권설정자` | 근저당권설정자 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:106 | 묻기 |
| `date` | 작성일 | date | 1쪽 [75, 485, 268, 499] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:128 | 묻기 |
| `date2` | 작성일 | date | 1쪽 [360, 570, 571, 585] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:153 | 묻기 |
| `signer2.name` | 채무자 | text | 1쪽 [220, 636, 287, 647] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `signer3.name` | 후순위근저당권자 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:195 | 묻기 |
| `customer.birth` | 생년월일 | date | 1쪽 [615, 657, 740, 669] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:212 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [608, 682, 769, 687] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `signer4.name` | 근저당권자 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:234 | 묻기 |
| `signer5.name` | 주택임차인 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:251 | 묻기 |
| `customer.birth2` | 생년월일 | date | 1쪽 [611, 743, 736, 755] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:268 | 묻기 |
| `customer.address2` | 주소 | text | 1쪽 [611, 767, 771, 773] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `related.name` ← `signer6.name` | 근저당권설정자 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:290 | 묻기 |
| `customer.birth3` | 생년월일 | date | 1쪽 [161, 828, 284, 840] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:307 | 묻기 |
| `customer.address3` | 주소 | text | 1쪽 [162, 850, 514, 861] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 22칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 인 | seal | 1쪽 [466, 407, 523, 448] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:117 | 묻기 |
| `sign.customer` ← `sign.signer` | 인 | signature | 1쪽 [194, 418, 795, 437] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.signer2` | 채무자 | seal | 1쪽 [362, 636, 388, 648] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.signer2` | 채무자 | signature | 1쪽 [362, 636, 388, 648] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.signer3` | 후순위근저당권자 | seal | 1쪽 [850, 636, 877, 648] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:195 | 묻기 |
| `sign.signer3` | 후순위근저당권자 | signature | 1쪽 [850, 636, 877, 648] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.signer4` | 근저당권자 | seal | 1쪽 [359, 721, 385, 733] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:234 | 묻기 |
| `sign.signer4` | 근저당권자 | signature | 1쪽 [359, 721, 385, 733] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.signer5` | 주택임차인 | seal | 1쪽 [843, 722, 870, 734] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:251 | 묻기 |
| `sign.signer5` | 주택임차인 | signature | 1쪽 [843, 722, 870, 734] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.related` ← `seal.signer6` | 근저당권설정자 | seal | 1쪽 [356, 807, 382, 819] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:106 | 묻기 |
| `sign.related` ← `sign.signer6` | 근저당권설정자 | signature | 1쪽 [356, 807, 382, 819] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:290 | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [581, 34, 653, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [581, 34, 653, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [666, 40, 712, 72] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [653, 34, 725, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.대리` | 대리 | seal | 1쪽 [731, 35, 791, 78] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.대리` | 대리 | signature | 1쪽 [725, 34, 797, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.차장` | 차장 | seal | 1쪽 [803, 35, 862, 77] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.차장` | 차장 | signature | 1쪽 [797, 34, 868, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.점장` | 점장 | seal | 1쪽 [868, 34, 941, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.점장` | 점장 | signature | 1쪽 [868, 34, 941, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키 `a` ← `b`:** 질문·정답은 공통 키 a, 서식의 원래 키는 b (키 사전이 정함). **정한 곳:** 템플릿에서 그 칸 자리 (html·코드 서식) / 칸 목록의 그 칸 (원본 서식).

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 공통 `docgen/forms/_common/questions.json`.

### 서류 분류 `classify` · 채점 acc

질문:

```
이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. 설명 없이 서류명만 한 줄로 답하세요.
```

답:

```json
"《기업》근저당권유용합의서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "남궁예태",
 "1985년 3월 28일",
 "서울특별시 서초구 강남대로 357, 103동 1301호"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남궁예태"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서울특별시 서초구 강남대로 357, 103동 1301호"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- 근저당권설정내역: 근저당권설정내역
- 채권최고액: 채권최고액
- customer.name: 채무자 (고객 성명, 같은 항목명 중 1번째 칸)
- 근저당권설정자: 근저당권설정자 (같은 항목명 중 1번째 칸)
- date: 작성일 (같은 항목명 중 1번째 칸)
- date2: 작성일 (같은 항목명 중 2번째 칸)
- signer2.name: 채무자 (고객 본인의 성명, 같은 항목명 중 2번째 칸)
- signer3.name: 후순위근저당권자 (은행·직원의 성명)
- customer.birth: 생년월일 (고객 생년월일, 같은 항목명 중 1번째 칸)
- customer.address: 주소 (고객 주소, 같은 항목명 중 1번째 칸)
- signer4.name: 근저당권자 (은행·직원의 성명)
- signer5.name: 주택임차인 (은행·직원의 성명)
- customer.birth2: 생년월일 (같은 항목명 중 2번째 칸)
- customer.address2: 주소 (같은 항목명 중 2번째 칸)
- related.name: 근저당권설정자 (보증인·공동 성명, 같은 항목명 중 2번째 칸)
- customer.birth3: 생년월일 (같은 항목명 중 3번째 칸)
- customer.address3: 주소 (같은 항목명 중 3번째 칸)
```

답:

```json
[{"key": "근저당권설정내역", "value": null},
 {"key": "채권최고액", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [203, 293, 269, 305], "page": 1},
 {"key": "근저당권설정자", "value": null},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [75, 485, 268, 499], "page": 1},
 {"key": "date2", "value": "2025년 4월 1일", "bbox_2d": [360, 570, 571, 585], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [220, 636, 287, 647], "page": 1},
 {"key": "signer3.name", "value": null},
 {"key": "customer.birth", "value": "1985년 3월 28일", "bbox_2d": [615, 657, 740, 669], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [608, 682, 769, 687], "page": 1},
 {"key": "signer4.name", "value": null},
 {"key": "signer5.name", "value": null},
 {"key": "customer.birth2", "value": "1985년 3월 28일", "bbox_2d": [611, 743, 736, 755], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [611, 767, 771, 773], "page": 1},
 {"key": "related.name", "value": null},
 {"key": "customer.birth3", "value": "1985년 3월 28일", "bbox_2d": [161, 828, 284, 840], "page": 1},
 {"key": "customer.address3", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [162, 850, 514, 861], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.customer: 인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.signer2: 채무자 (고객 본인의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer2: 채무자 (고객 본인의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.signer3: 후순위근저당권자 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer3: 후순위근저당권자 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.signer4: 근저당권자 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer4: 근저당권자 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.signer5: 주택임차인 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer5: 주택임차인 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.related: 근저당권설정자 (보증인·공동 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.related: 근저당권설정자 (보증인·공동 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.본인확인: 본인확인 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.대리: 대리 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.대리: 대리 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.차장: 차장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.차장: 차장 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.점장: 점장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.점장: 점장 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.customer", "value": true, "bbox_2d": [466, 407, 523, 448], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [362, 636, 388, 648], "page": 1},
 {"key": "seal.signer3", "value": false},
 {"key": "sign.signer3", "value": false},
 {"key": "seal.signer4", "value": false},
 {"key": "sign.signer4", "value": false},
 {"key": "seal.signer5", "value": false},
 {"key": "sign.signer5", "value": false},
 {"key": "seal.related", "value": false},
 {"key": "sign.related", "value": false},
 {"key": "seal.staff.본인확인", "value": false},
 {"key": "sign.staff.본인확인", "value": true, "bbox_2d": [581, 34, 653, 79], "page": 1},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [666, 40, 712, 72], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.대리", "value": true, "bbox_2d": [731, 35, 791, 78], "page": 1},
 {"key": "sign.staff.대리", "value": false},
 {"key": "seal.staff.차장", "value": true, "bbox_2d": [803, 35, 862, 77], "page": 1},
 {"key": "sign.staff.차장", "value": false},
 {"key": "seal.staff.점장", "value": false},
 {"key": "sign.staff.점장", "value": true, "bbox_2d": [868, 34, 941, 79], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기·위치·항목명 | studio ① 서식 › 영역 편집 (저장하면 `fields.json` items) | 재검수 → 카드 다시 만들기 |
| 값이 이상함 | 영역 편집에서 그 칸의 값 출처·값 종류 | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf150 --show` · `python -m docgen.preview hf150 --out work/hf150`
