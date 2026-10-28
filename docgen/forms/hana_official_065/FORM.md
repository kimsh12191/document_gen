# 국토교통부 주택소유확인 시스템 등 이용 관련 [필수] 개인(신용)정보 수집·이용·제공 동의서 (`hana_official_065`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hana_official_065 · card-hash: f3b7ad720ac3 -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 국토교통부 주택소유확인 시스템 등 이용 관련 [필수] 개인(신용)정보 수집·이용·제공 동의서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 원문을 대조한 HTML. 국토교통부 주택소유확인 시스템 등 이용 관련 [필수] 개인(신용)정보 수집·이용·제공 동의서. 기존 hf065 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/06/13/5-06-0893.pdf

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `form.json` | 이름·그룹·출처 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 9칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `일반개인정보` | ■일반개인정보 | text | - | 늘 | - | - | 묻기 |
| `일반개인정보2` | ■일반개인정보 | text | - | 늘 | - | - | 묻기 |
| `customer.name` ← `signer.name` | 본인성명 | text | 2쪽 [761, 746, 849, 770] | 늘 | - | - | 묻기 |
| `family.name` ← `signer2.name` | 세대원성명 | text | 2쪽 [768, 771, 844, 796] | 늘 | - | - | 묻기 |
| `date` | 작성일 | date | 2쪽 [284, 801, 516, 819] | 늘 | - | - | 묻기 |
| `signer3.name` | 세대원성명 | text | 2쪽 [769, 797, 844, 820] | 늘 | - | - | 묻기 |
| `signer4.name` | 세대원성명 | text | - | 늘 | - | - | 묻기 |
| `signer5.name` | 세대원성명 | text | 2쪽 [766, 850, 842, 875] | 늘 | - | - | 묻기 |
| `signer6.name` | 세대원성명 | text | - | 늘 | - | - | 묻기 |

## 체크·도장·서명 (marks) — 22칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox (동의하지 않음 / 동의함) | 1쪽 [724, 765, 913, 779] | 늘 | - | - | 묻기 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox (동의하지 않음 / 동의함) | 1쪽 [849, 872, 913, 887] | 늘 | - | - | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [722, 38, 771, 72] | 늘 | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [711, 35, 782, 75] | 늘 | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [793, 39, 837, 71] | 늘 | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [782, 35, 847, 75] | 늘 | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [861, 38, 907, 71] | 늘 | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [847, 35, 921, 75] | 늘 | - | - | 묻기 |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox (동의하지 않음 / 동의함) | 2쪽 [725, 526, 837, 541] | 늘 | - | - | 묻기 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox (동의하지 않음 / 동의함) | 2쪽 [850, 629, 915, 644] | 늘 | - | - | 묻기 |
| `seal.customer` ← `seal.signer` | 본인성명 | seal | 2쪽 [898, 750, 926, 766] | 늘 | - | - | 묻기 |
| `sign.customer` ← `sign.signer` | 본인성명 | signature | 2쪽 [898, 750, 926, 766] | 늘 | - | - | 묻기 |
| `seal.signer2` | 세대원성명 | seal | 2쪽 [895, 765, 929, 802] | 늘 | - | - | 묻기 |
| `sign.signer2` | 세대원성명 | signature | 2쪽 [898, 776, 926, 792] | 늘 | - | - | 묻기 |
| `seal.signer3` | 세대원성명 | seal | 2쪽 [898, 802, 926, 818] | 늘 | - | - | 묻기 |
| `sign.signer3` | 세대원성명 | signature | 2쪽 [898, 802, 926, 818] | 늘 | - | - | 묻기 |
| `seal.signer4` | 세대원성명 | seal | 2쪽 [898, 828, 926, 844] | 늘 | - | - | 묻기 |
| `sign.signer4` | 세대원성명 | signature | 2쪽 [898, 828, 926, 844] | 늘 | - | - | 묻기 |
| `seal.signer5` | 세대원성명 | seal | 2쪽 [896, 844, 928, 880] | 늘 | - | - | 묻기 |
| `sign.signer5` | 세대원성명 | signature | 2쪽 [898, 854, 926, 870] | 늘 | - | - | 묻기 |
| `seal.signer6` | 세대원성명 | seal | 2쪽 [898, 880, 926, 896] | 늘 | - | - | 묻기 |
| `sign.signer6` | 세대원성명 | signature | 2쪽 [898, 880, 926, 896] | 늘 | - | - | 묻기 |

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
"국토교통부 주택소유확인 시스템 등 이용 관련 [필수] 개인(신용)정보 수집·이용·제공 동의서"
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
 "남궁찬윤"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남궁찬윤"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남궁찬윤"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- 일반개인정보: ■일반개인정보 (같은 항목명 중 1번째 칸)
- 일반개인정보2: ■일반개인정보 (같은 항목명 중 2번째 칸)
- customer.name: 본인성명 (고객 성명)
- family.name: 세대원성명 (가족 성명, 같은 항목명 중 1번째 칸)
- date: 작성일
- signer3.name: 세대원성명 (배우자·가족의 성명, 같은 항목명 중 2번째 칸)
- signer4.name: 세대원성명 (배우자·가족의 성명, 같은 항목명 중 3번째 칸)
- signer5.name: 세대원성명 (배우자·가족의 성명, 같은 항목명 중 4번째 칸)
- signer6.name: 세대원성명 (배우자·가족의 성명, 같은 항목명 중 5번째 칸)
```

답:

```json
[{"key": "일반개인정보", "value": null},
 {"key": "일반개인정보2", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [761, 746, 849, 770], "page": 2},
 {"key": "family.name", "value": "남궁찬윤", "bbox_2d": [768, 771, 844, 796], "page": 2},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [284, 801, 516, 819], "page": 2},
 {"key": "signer3.name", "value": "남궁찬윤", "bbox_2d": [769, 797, 844, 820], "page": 2},
 {"key": "signer4.name", "value": null},
 {"key": "signer5.name", "value": "남궁찬윤", "bbox_2d": [766, 850, 842, 875], "page": 2},
 {"key": "signer6.name", "value": null}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.위고유식별정보수집이용에동의하십니까: 위고유식별정보수집·이용에동의하십니까? (체크박스, 보기: 동의하지 않음 / 동의함)
- check.위개인정보수집이용에동의하십니까: 위개인(신용)정보수집·이용에동의하십니까? (체크박스, 보기: 동의하지 않음 / 동의함)
- seal.staff.본인확인: 본인확인 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
- check.위고유식별정보제공에동의하십니까: 위고유식별정보제공에동의하십니까? (체크박스, 보기: 동의하지 않음 / 동의함)
- check.위개인정보제공에동의하십니까: 위개인(신용)정보제공에동의하십니까? (체크박스, 보기: 동의하지 않음 / 동의함)
- seal.customer: 본인성명 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 본인성명 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.signer2: 세대원성명 (배우자·가족의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer2: 세대원성명 (배우자·가족의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.signer3: 세대원성명 (배우자·가족의 신청인, 같은 항목명 중 3번째 칸, 도장)
- sign.signer3: 세대원성명 (배우자·가족의 신청인, 같은 항목명 중 4번째 칸, 서명)
- seal.signer4: 세대원성명 (배우자·가족의 신청인, 같은 항목명 중 5번째 칸, 도장)
- sign.signer4: 세대원성명 (배우자·가족의 신청인, 같은 항목명 중 6번째 칸, 서명)
- seal.signer5: 세대원성명 (배우자·가족의 신청인, 같은 항목명 중 7번째 칸, 도장)
- sign.signer5: 세대원성명 (배우자·가족의 신청인, 같은 항목명 중 8번째 칸, 서명)
- seal.signer6: 세대원성명 (배우자·가족의 신청인, 같은 항목명 중 9번째 칸, 도장)
- sign.signer6: 세대원성명 (배우자·가족의 신청인, 같은 항목명 중 10번째 칸, 서명)
```

답:

```json
[{"key": "check.위고유식별정보수집이용에동의하십니까", "value": null},
 {"key": "check.위개인정보수집이용에동의하십니까", "value": "동의함", "bbox_2d": [849, 874, 865, 887], "page": 1},
 {"key": "seal.staff.본인확인", "value": true, "bbox_2d": [722, 38, 771, 72], "page": 1},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [793, 39, 837, 71], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [861, 38, 907, 71], "page": 1},
 {"key": "sign.staff.책임자", "value": false},
 {"key": "check.위고유식별정보제공에동의하십니까", "value": "동의하지 않음", "bbox_2d": [725, 528, 741, 540], "page": 2},
 {"key": "check.위개인정보제공에동의하십니까", "value": "동의함", "bbox_2d": [850, 631, 867, 644], "page": 2},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [898, 750, 926, 766], "page": 2},
 {"key": "seal.signer2", "value": true, "bbox_2d": [895, 765, 929, 802], "page": 2},
 {"key": "sign.signer2", "value": false},
 {"key": "seal.signer3", "value": false},
 {"key": "sign.signer3", "value": false},
 {"key": "seal.signer4", "value": false},
 {"key": "sign.signer4", "value": false},
 {"key": "seal.signer5", "value": true, "bbox_2d": [896, 844, 928, 880], "page": 2},
 {"key": "sign.signer5", "value": false},
 {"key": "seal.signer6", "value": false},
 {"key": "sign.signer6", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `fields.json` 의 `fields` 에 키·source | 미리보기로 확인 → 재검수 → 카드 다시 만들기 |
| 칸 키·항목명 바꾸기 | `look/template.html.j2` 의 `f("키", label=…)` + `fields.json` (질문만 바꾸려면 `questions.json`) | `questions … --check` |
| 값이 이상함 / 칸끼리 안 맞음 | `fields.json` 의 source / `generate.py` 의 `adjust(d, p, rng)` | 재검수 |
| 모양·표·문구 | `look/template.html.j2` (studio html 편집) | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hana_official_065 --show` · `python -m docgen.preview hana_official_065 --out work/hana_official_065`
