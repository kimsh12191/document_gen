# 이사회의사록 (`board_minutes`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card board_minutes · card-hash: 25d2062dee87 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** corporate · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 이사회의사록
- **쓰이는 업무:** 법인 여신
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 은행 차입 승인 이사회의사록 (출석 이사 기명날인).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/corporate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 34칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `datetime` | 일시 | text | 1쪽 [186, 102, 372, 112] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:25 | 묻기 |
| `venue` | 장소 | text | 1쪽 [186, 118, 564, 128] | 늘 | 템플릿 | generate.py | look/template.html.j2:26 · fields.json:160 | 묻기 |
| `directors_total` | 이사총수 | text | 1쪽 [186, 134, 207, 144] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:35 | 묻기 |
| `directors_present` | 출석이사수 | text | 1쪽 [342, 134, 363, 144] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:30 | 묻기 |
| `remote_count` | 원격참석 | text | 1쪽 [371, 134, 486, 144] | 4/16 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:120 | 묻기 |
| `auditor_total` | 감사총수 | text | 1쪽 [186, 150, 207, 160] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:10 | 묻기 |
| `auditor_present` | 출석감사수 | text | 1쪽 [342, 150, 363, 160] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:5 | 묻기 |
| `remote_attendees` | 원격참석이사 | text | 1쪽 [98, 173, 308, 183] | 4/16 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:115 | 묻기 |
| `remote_method` | 원격참석방법 | text | 1쪽 [772, 173, 930, 183] | 4/16 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:125 | 묻기 |
| `chair` | 의장 | text | 1쪽 [249, 213, 305, 224] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:15 | 묻기 |
| `loan.lender` | 차입은행 | text | 1쪽 [143, 256, 199, 267] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:70 | 묻기 |
| `loan.bank` | 차입기관 | text | 1쪽 [264, 323, 384, 334] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:55 | 묻기 |
| `loan.kind` | 대출과목 | text | 1쪽 [264, 343, 351, 354] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:65 | 묻기 |
| `loan.amount` | 차입금액 | amount | 1쪽 [264, 363, 525, 375] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:50 | 묻기 |
| `loan.period` | 차입기간 | text | 1쪽 [264, 383, 446, 395] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:75 | 묻기 |
| `loan.purpose` | 자금용도 | text | 1쪽 [264, 403, 370, 415] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:80 | 묻기 |
| `loan.rate` | 적용금리 | text | 1쪽 [264, 424, 322, 435] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:85 | 묻기 |
| `loan.collateral` | 담보 | text | 1쪽 [264, 444, 399, 455] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:60 | 묻기 |
| `agendas.*.no` | 의안번호 | text | 1쪽 [65, 474, 132, 484] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:180 | 묻기 |
| `agendas.*.title` | 의안 | text | 1쪽 [144, 474, 329, 484] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:185 | 묻기 |
| `agendas.*.body` | 결의내용 | text | 1쪽 [65, 497, 935, 523] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:170 | 묻기 |
| `end_time` | 종료시각 | text | 1쪽 [730, 537, 814, 548] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:40 | 묻기 |
| `minutes_date` | 작성일 | date | 1쪽 [451, 605, 549, 616] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:90 | 묻기 |
| `corp.name` ← `company_name` | 상호 | text | 1쪽 [841, 632, 935, 643] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:20 | 묻기 |
| `head_office` | 본점 | text | 1쪽 [687, 649, 935, 658] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:45 | 묻기 |
| `signers.*.title` | 자격 | text | 1쪽 [431, 686, 523, 697] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:210 | 묻기 |
| `signers.*.name` | 성명 | text | 1쪽 [582, 686, 649, 697] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:200 | 묻기 |
| `signers.*.remote` | 비고 | text | 1쪽 [758, 729, 824, 739] (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:205 | 묻기 |
| `notary.reg_no` | 등부번호 | text | 2쪽 [566, 70, 668, 82] | 2/16 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:110 | 묻기 |
| `notary.date` | 인증일 | date | 2쪽 [537, 133, 628, 145] | 2/16 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:95 | 묻기 |
| `notary.office` | 공증인 | text | 2쪽 [582, 148, 670, 159] | 2/16 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:105 | 묻기 |
| `notary.lawyer` | 공증담당변호사 | text | 2쪽 [639, 172, 681, 183] | 2/16 | 템플릿 | generate.py | look/template.html.j2:71 · fields.json:100 | 묻기 |
| `agendas.*.detail` | 세부내용 | - | - (1행) | 7/16 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:175 | 묻기 |
| `agendas.*.votes` | 표결결과 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:190 | 묻기 |

## 체크·도장·서명 (marks) — 6칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.corp` | 법인인감 | seal | 1쪽 [693, 666, 768, 718] | 늘 | 템플릿 | generate.py | fields.json:130 | 묻기 |
| `seal.signer2` | 서명인2 | seal | 1쪽 [705, 715, 761, 755] | 늘 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `seal.signer3` | 서명인3 | seal | 1쪽 [705, 758, 761, 798] | 늘 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `seal.signer4` | 서명인4 | seal | 1쪽 [705, 801, 761, 840] | 12/16 | 템플릿 | generate.py | fields.json:150 | 묻기 |
| `seal.notary` | 공증인직인 | seal | 2쪽 [681, 158, 738, 198] | 2/16 | 템플릿 | generate.py | fields.json:135 | 묻기 |
| `seal.signer5` | 서명인5 | 도장 | - | 5/16 | 템플릿 | generate.py | fields.json:155 | 묻기 |

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
"이사회의사록"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2025년 3월 28일 오후 2시 00분",
 "회사 본점 회의실 (제주특별자치도 제주시 첨단로 381-19, 2층)",
 "4명",
 "3명",
 "원격 참석 2명 포함",
 "1명",
 "사내이사 노도수, 사내이사 원승호",
 "화상회의, Microsoft Teams",
 "남궁예태",
 "국민은행",
 "국민은행 센텀지점",
 "일반자금대출",
 "금 팔십구억칠천만원정 (₩8,970,000,000)",
 "3년 (2025.04.09 ~ 2028.04.08)",
 "원자재 구입자금",
 "고정금리",
 "기술보증기금 보증서",
 "제2호 의안",
 "차입 관련 제반 권한 위임의 건",
 "의장은 제1호 의안의 차입과 관련하여 여신거래약정서 등 제반 서류의 작성, 날인 및 제출 등 일체의 권한을 대표이사에게 위임할 것을 제안하고 그 가부를 물은바, 출석이사 전원의 찬성으로 원안대로 승인 가결하다.",
 "오후 2시 40분",
 "2025년 3월 28일",
 "(주)미래케미칼",
 "제주특별자치도 제주시 첨단로 381-19, 2층",
 "의장 대표이사",
 "사내이사",
 "노도수",
 "(원격 참석)",
 "원승호",
 "감사",
 "원순수",
 "2025년 제4380호",
 "2025년 4월 3일",
 "법무법인 동인",
 "장혜인"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"1명"
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

### 정보 추출 `kie` · 채점 vl_f1 (값+위치)

틀 (질문의 항목 한 줄 · 답 항목 하나 · 빈 칸일 때) — `questions.json` 의 `kie`:

```
item:         - {key}: {label}{note}
answer:       {"key": "{key}", "value": "{value}", "bbox_2d": "{bbox_2d}", "page": "{page}"}
answer_empty: {"key": "{key}", "value": null}
```

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- datetime: 일시
- venue: 장소
- directors_total: 이사총수
- directors_present: 출석이사수
- remote_count: 원격참석
- auditor_total: 감사총수
- auditor_present: 출석감사수
- remote_attendees: 원격참석이사
- remote_method: 원격참석방법
- chair: 의장
- loan.lender: 차입은행
- loan.bank: 차입기관
- loan.kind: 대출과목
- loan.amount: 차입금액
- loan.period: 차입기간
- loan.purpose: 자금용도
- loan.rate: 적용금리
- loan.collateral: 담보
- agendas.0.no: 의안번호 (1행)
- agendas.0.title: 의안 (1행)
- agendas.0.body: 결의내용 (1행)
- end_time: 종료시각
- minutes_date: 작성일
- corp.name: 상호 (법인·사업자 상호)
- head_office: 본점
- signers.0.title: 자격 (1행)
- signers.0.name: 성명 (1행)
- signers.1.title: 자격 (2행)
- signers.1.name: 성명 (2행)
- signers.1.remote: 비고 (2행)
- signers.2.title: 자격 (3행)
- signers.2.name: 성명 (3행)
- signers.2.remote: 비고 (3행)
- signers.3.title: 자격 (4행)
- signers.3.name: 성명 (4행)
- notary.reg_no: 등부번호
- notary.date: 인증일
- notary.office: 공증인
- notary.lawyer: 공증담당변호사
```

답:

```json
[{"key": "datetime", "value": "2025년 3월 28일 오후 2시 00분", "bbox_2d": [186, 102, 372, 112], "page": 1},
 {"key": "venue", "value": "회사 본점 회의실 (제주특별자치도 제주시 첨단로 381-19, 2층)", "bbox_2d": [186, 118, 564, 128], "page": 1},
 {"key": "directors_total", "value": "4명", "bbox_2d": [186, 134, 207, 144], "page": 1},
 {"key": "directors_present", "value": "3명", "bbox_2d": [342, 134, 363, 144], "page": 1},
 {"key": "remote_count", "value": "원격 참석 2명 포함", "bbox_2d": [371, 134, 486, 144], "page": 1},
 {"key": "auditor_total", "value": "1명", "bbox_2d": [186, 150, 207, 160], "page": 1},
 {"key": "auditor_present", "value": "1명", "bbox_2d": [342, 150, 363, 160], "page": 1},
 {"key": "remote_attendees", "value": "사내이사 노도수, 사내이사 원승호", "bbox_2d": [98, 173, 308, 183], "page": 1},
 {"key": "remote_method", "value": "화상회의, Microsoft Teams", "bbox_2d": [772, 173, 930, 183], "page": 1},
 {"key": "chair", "value": "남궁예태", "bbox_2d": [249, 213, 305, 224], "page": 1},
 {"key": "loan.lender", "value": "국민은행", "bbox_2d": [143, 256, 199, 267], "page": 1},
 {"key": "loan.bank", "value": "국민은행 센텀지점", "bbox_2d": [264, 323, 384, 334], "page": 1},
 {"key": "loan.kind", "value": "일반자금대출", "bbox_2d": [264, 343, 351, 354], "page": 1},
 {"key": "loan.amount", "value": "금 팔십구억칠천만원정 (₩8,970,000,000)", "bbox_2d": [264, 363, 525, 375], "page": 1},
 {"key": "loan.period", "value": "3년 (2025.04.09 ~ 2028.04.08)", "bbox_2d": [264, 383, 446, 395], "page": 1},
 {"key": "loan.purpose", "value": "원자재 구입자금", "bbox_2d": [264, 403, 370, 415], "page": 1},
 {"key": "loan.rate", "value": "고정금리", "bbox_2d": [264, 424, 322, 435], "page": 1},
 {"key": "loan.collateral", "value": "기술보증기금 보증서", "bbox_2d": [264, 444, 399, 455], "page": 1},
 {"key": "agendas.0.no", "value": "제2호 의안", "bbox_2d": [65, 474, 132, 484], "page": 1},
 {"key": "agendas.0.title", "value": "차입 관련 제반 권한 위임의 건", "bbox_2d": [144, 474, 329, 484], "page": 1},
 {"key": "agendas.0.body", "value": "의장은 제1호 의안의 차입과 관련하여 여신거래약정서 등 제반 서류의 작성, 날인 및 제출 등 일체의 권한을 대표이사에게 위임할 것을 제안하고 그 가부를 물은바, 출석이사 전원의 찬성으로 원안대로 승인 가결하다.", "bbox_2d": [65, 497, 935, 523], "page": 1},
 {"key": "end_time", "value": "오후 2시 40분", "bbox_2d": [730, 537, 814, 548], "page": 1},
 {"key": "minutes_date", "value": "2025년 3월 28일", "bbox_2d": [451, 605, 549, 616], "page": 1},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [841, 632, 935, 643], "page": 1},
 {"key": "head_office", "value": "제주특별자치도 제주시 첨단로 381-19, 2층", "bbox_2d": [687, 649, 935, 658], "page": 1},
 {"key": "signers.0.title", "value": "의장 대표이사", "bbox_2d": [431, 686, 523, 697], "page": 1},
 {"key": "signers.0.name", "value": "남궁예태", "bbox_2d": [582, 686, 649, 697], "page": 1},
 {"key": "signers.1.title", "value": "사내이사", "bbox_2d": [431, 729, 489, 740], "page": 1},
 {"key": "signers.1.name", "value": "노도수", "bbox_2d": [582, 729, 632, 740], "page": 1},
 {"key": "signers.1.remote", "value": "(원격 참석)", "bbox_2d": [758, 729, 824, 739], "page": 1},
 {"key": "signers.2.title", "value": "사내이사", "bbox_2d": [431, 772, 489, 783], "page": 1},
 {"key": "signers.2.name", "value": "원승호", "bbox_2d": [582, 772, 632, 783], "page": 1},
 {"key": "signers.2.remote", "value": "(원격 참석)", "bbox_2d": [758, 772, 824, 782], "page": 1},
 {"key": "signers.3.title", "value": "감사", "bbox_2d": [431, 815, 460, 825], "page": 1},
 {"key": "signers.3.name", "value": "원순수", "bbox_2d": [582, 815, 632, 825], "page": 1},
 {"key": "notary.reg_no", "value": "2025년 제4380호", "bbox_2d": [566, 70, 668, 82], "page": 2},
 {"key": "notary.date", "value": "2025년 4월 3일", "bbox_2d": [537, 133, 628, 145], "page": 2},
 {"key": "notary.office", "value": "법무법인 동인", "bbox_2d": [582, 148, 670, 159], "page": 2},
 {"key": "notary.lawyer", "value": "장혜인", "bbox_2d": [639, 172, 681, 183], "page": 2}]
```

### 체크·도장·서명 `marks` · 채점 vl_f1 (값+위치)

틀 (질문의 항목 한 줄 · 답 항목 하나 · 빈 칸일 때) — `questions.json` 의 `marks`:

```
item:         - {key}: {label}{note}
answer:       {"key": "{key}", "value": "{value}", "bbox_2d": "{bbox_2d}", "page": "{page}"}
answer_empty: {"key": "{key}", "value": null}
```

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.corp: 법인인감 (법인·사업자 도장, 도장)
- seal.signer2: 서명인2 (은행·직원의 신청인, 도장)
- seal.signer3: 서명인3 (은행·직원의 신청인, 도장)
- seal.signer4: 서명인4 (은행·직원의 신청인, 도장)
- seal.notary: 공증인직인 (도장)
```

답:

```json
[{"key": "seal.corp", "value": true, "bbox_2d": [693, 666, 768, 718], "page": 1},
 {"key": "seal.signer2", "value": true, "bbox_2d": [705, 715, 761, 755], "page": 1},
 {"key": "seal.signer3", "value": true, "bbox_2d": [705, 758, 761, 798], "page": 1},
 {"key": "seal.signer4", "value": true, "bbox_2d": [705, 801, 761, 840], "page": 1},
 {"key": "seal.notary", "value": true, "bbox_2d": [681, 158, 738, 198], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check board_minutes` → `python -m docgen.formdir card board_minutes` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` | 다시 |
| 답의 값 | `generate.py` (값 만드는 함수). 파이썬 대신 정하려면 `fields.json` 의 그 칸 `source` | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (studio html 편집). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions board_minutes --show` · `python -m docgen.preview board_minutes --out work/board_minutes`
