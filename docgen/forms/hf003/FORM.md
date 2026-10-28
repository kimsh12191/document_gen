# 은행거래신청서 (`hf003`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf003 · card-hash: 54f76ae21815 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 예금거래신청서 (다른 이름: 은행거래신청서)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.3 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 74칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `deposit_list.*.interest_account` | 통장발행 | account_no | 1쪽 [72, 448, 221, 468] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:26 | 묻기 |
| `목록.*.갋` | 갋 | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:74 | 묻기 |
| `갋` | 갋 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:87 | 묻기 |
| `갋2` | 갋 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:100 | 묻기 |
| `갋3` | 갋 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:113 | 묻기 |
| `deposit_list_list.*.*.transfer_day` | 확정형연동형(개월) | text | 1쪽 [501, 448, 532, 468] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name_en` | 영문명 | text | 1쪽 [478, 136, 698, 163] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:233 | 묻기 |
| `customer.email` | 이메일 | text | 1쪽 [473, 191, 734, 219] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:245 | 묻기 |
| `customer.address` | 자택 | text | 1쪽 [480, 221, 736, 242] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:265 | 묻기 |
| `employer.address` | 직장 | text | 1쪽 [479, 250, 764, 266] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:279 | 묻기 |
| `customer.home_phone` | 자택 | phone | 1쪽 [681, 275, 798, 296] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:294 | 묻기 |
| `employer.phone` | 직장 | phone | 1쪽 [686, 304, 789, 323] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:308 | 묻기 |
| `customer.payday` | 급여일 | text | 1쪽 [784, 195, 824, 217] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:322 | 묻기 |
| `bank.auto_transfer_account` | 자동이체계좌번호 | account_no | 1쪽 [139, 924, 244, 939] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:351 | 묻기 |
| `bank.subject` | 과목명 | text | 1쪽 [335, 922, 419, 939] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:365 | 묻기 |
| `bank.contract_amount` | 계약(확인)금액 | amount | 1쪽 [590, 940, 637, 955] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:379 | 묻기 |
| `bank.pay_date` | 지급기일 | date | 1쪽 [819, 923, 889, 938] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:393 | 묻기 |
| `date` | 작성일 | date | 1쪽 [442, 715, 637, 726] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:476 | 묻기 |
| `deposit_list.*.tax_free_limit` | 연원가식 | amount | 1쪽 [744, 429, 812, 444] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:501 | 묻기 |
| `deposit.withdraw_account` | 출금계좌[ | account_no | 1쪽 [278, 662, 379, 677] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name` | 신청인 | text | 1쪽 [800, 698, 890, 723] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:561 | 묻기 |
| `account` | 계좌번호 | account_no | 1쪽 [104, 906, 220, 922] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:573 | 묻기 |
| `bank.first_trade_date` | 최초거래일 | date | 1쪽 [559, 907, 626, 920] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:585 | 묻기 |
| `bank.open_date` | 신규일 | date | 1쪽 [810, 904, 884, 921] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:600 | 묻기 |
| `bank.deposit_amount` | 입금(수탁)액 | amount | 1쪽 [589, 923, 636, 939] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:615 | 묻기 |
| `bank.kind` | 종별 | text | 1쪽 [90, 940, 175, 957] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:630 | 묻기 |
| `bank.staff_no` | 권유직원번호 | text | 1쪽 [838, 941, 902, 956] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:645 | 묻기 |
| `customer.name7` | 성명(업체명) | text | 1쪽 [154, 138, 246, 163] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1060 | 묻기 |
| `customer.birth` | 생년월일(사업자번호) | date | 1쪽 [788, 135, 894, 161] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1073 | 묻기 |
| `customer.phone` | 휴대폰 | phone | 1쪽 [485, 165, 627, 191] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1086 | 묻기 |
| `customer.email2` | 계약서류수령E-mail또는휴대폰번호 | text | 1쪽 [638, 382, 754, 396] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `deposit_list.*.product` | 상품명1 / 상품명2 / 상품명3 | text | 1쪽 [76, 428, 155, 449] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1112 | 묻기 |
| `deposit_list.*.amount` | 가입금액1 / 가입금액2 / 가입금액3 | amount | 1쪽 [292, 431, 350, 445] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1126 | 묻기 |
| `deposit_list.*.period` | 계약기간1 / 계약기간2 / 계약기간3 | text | 1쪽 [365, 430, 408, 447] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1140 | 묻기 |
| `deposit_list.*.transfer_amount` | 이체금액1 / 이체금액2 / 이체금액3 | amount | 1쪽 [620, 452, 681, 465] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1154 | 묻기 |
| `deposit_list.*.transfer_end` | 이체기간(만료일)1 / 이체기간(만료일)2 / 이체기간(만료일)3 | date | 1쪽 [693, 451, 784, 465] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1168 | 묻기 |
| `deposit_list.*.funding_amount` | 출금금액① / 출금금액② / 출금금액③ | amount | 1쪽 [606, 663, 650, 676] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `date2` | 작성일(년월일) | date | 1쪽 [356, 716, 419, 726] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ebank.user_id` | 이용자ID | text | 2쪽 [127, 86, 221, 110] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:660 | 묻기 |
| `corp.name` ← `company.name` | 상호명 | text | 2쪽 [237, 441, 360, 463] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:675 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자등록번호 | biz_no | 2쪽 [540, 442, 655, 462] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:687 | 묻기 |
| `company.established` | 개업년월일 | date | 2쪽 [804, 443, 893, 463] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:699 | 묻기 |
| `account2` | 입금계좌 | account_no | 2쪽 [551, 521, 715, 544] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:713 | 묻기 |
| `agent.name` | 성명 | text | 2쪽 [198, 760, 272, 784] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `agent.relation` | 본인과의관계 | text | 2쪽 [199, 783, 213, 806] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `agent.birth` | 생년월일 | date | 2쪽 [482, 762, 621, 784] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:748 | 묻기 |
| `agent.address` | 주소 | text | 2쪽 [481, 779, 823, 808] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `agent.phone` | 전화번호 | phone | 2쪽 [744, 758, 881, 783] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:773 | 묻기 |
| `bank.auto_transfer_account2` | 자동이체계좌번호 | text | 2쪽 [134, 922, 251, 939] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:786 | 묻기 |
| `bank.subject2` | 과목명 | text | 2쪽 [334, 923, 426, 939] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:800 | 묻기 |
| `bank.contract_amount2` | 계약(확인)금액 | amount | 2쪽 [566, 941, 631, 956] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:814 | 묻기 |
| `bank.pay_date2` | 지급기일 | date | 2쪽 [813, 922, 890, 938] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:828 | 묻기 |
| `ebank.phone_limit_once` | 원)(1회 | amount | 2쪽 [808, 119, 912, 145] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name2` | 신청인 | text | 2쪽 [779, 161, 848, 181] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:858 | 묻기 |
| `customer.name3` | 신청인 | text | 2쪽 [783, 243, 852, 263] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:870 | 묻기 |
| `related.name` | 아니오(실제소유자성명 | text | 2쪽 [428, 344, 475, 361] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `redeposit_list.*.product` | [신청상품]1 / 신청상품② / 신청상품③ | text | 2쪽 [255, 544, 359, 562] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name4` | 신청인 | text | 2쪽 [784, 548, 853, 568] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:911 | 묻기 |
| `customer.name5` | 예금주 | text | 2쪽 [547, 714, 616, 733] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:923 | 묻기 |
| `agent.name2` | 대리인 | text | 2쪽 [781, 714, 839, 733] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:935 | 묻기 |
| `customer.name6` | 위임인(예금주) | text | 2쪽 [751, 808, 820, 828] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `account3` | 계좌번호 | account_no | 2쪽 [107, 905, 222, 921] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:959 | 묻기 |
| `bank.first_trade_date2` | 최초거래일 | date | 2쪽 [558, 907, 623, 918] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:971 | 묻기 |
| `bank.open_date2` | 신규일 | date | 2쪽 [806, 905, 876, 922] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:986 | 묻기 |
| `bank.deposit_amount2` | 입금(수탁)액 | amount | 2쪽 [581, 922, 632, 938] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1001 | 묻기 |
| `bank.kind2` | 종별 | text | 2쪽 [87, 940, 171, 956] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1016 | 묻기 |
| `bank.staff_no2` | 권유직원번호 | text | 2쪽 [831, 941, 927, 953] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1031 | 묻기 |
| `related.rrn` | 실명번호: | text | 2쪽 [811, 349, 853, 355] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ebank.internet_limit_day` | 인터넷/스마트폰뱅킹1일한도 | amount | 2쪽 [609, 90, 721, 116] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ebank.internet_limit_once` | 인터넷/스마트폰뱅킹1회한도 | amount | 2쪽 [815, 93, 912, 115] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ebank.phone_limit_day` | 폰뱅킹1일한도 | amount | 2쪽 [621, 121, 719, 143] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ebank.passbook_memo` | 전자통장설명문구(한글6자) | text | 2쪽 [199, 237, 255, 252] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name_en2` | 영문명(전자화폐발급시) | text | 2쪽 [521, 237, 648, 253] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1433 | 묻기 |
| `deposit.renew_count` | 갱신횟수 | number | 2쪽 [891, 521, 897, 540] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:1446 | 묻기 |

## 체크·도장·서명 (marks) — 11칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.signer` | 한도:₩..~.. | seal | 1쪽 [830, 428, 950, 468] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.signer` | 한도:₩..~.. | signature | 1쪽 [830, 428, 950, 468] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.signer2` | 한도:₩..~.. | seal | 1쪽 [830, 498, 950, 540] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.signer2` | 한도:₩..~.. | signature | 1쪽 [830, 498, 950, 540] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.signer3` | 한도:₩..~.. | seal | 1쪽 [863, 574, 917, 612] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.signer3` | 한도:₩..~.. | signature | 1쪽 [830, 572, 950, 613] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.signer4` | 고객정보변경없음 | seal | 1쪽 [830, 191, 950, 286] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.signer4` | 고객정보변경없음 | signature | 1쪽 [830, 191, 950, 286] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.비과세종합저축재형저축` | 비과세종합저축/재형저축/주택청약상품의계약금액/한도/중복 | checkbox (비과세종합저축 / 재형저축 / 주택청약상품의 계약금액 / 한도 / 중복 ) | 1쪽 [59, 694, 551, 702] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.귀행에대한제대출금보증채` | 귀행에대한제대출금,보증채무,신용카드채무에대하여변제기가도래하 | checkbox (귀행에 대한 제 대출금, 보증채무, 신용카드채무에 대하여 변제기가 도래하) | 1쪽 [59, 701, 625, 709] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.본인은금융지주회사법제4` | 본인은금융지주회사법제48조의2에근거하여하나금융그룹내지주사및자 | checkbox (본인은 금융지주회사법 제48조의2에 근거하여 하나금융그룹내 지주사 및 자) | 1쪽 [59, 708, 656, 716] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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
"예금거래신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "542-218001-62744",
 "361-231296-44138",
 "419-070303-12790",
 "10일",
 "25일",
 "5일",
 "NAMGOONG YETAE",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "부산광역시 해운대구 해운대로 326, 7층 주식회사 다온패션 고객지원팀",
 "02-6508-5072",
 "051-509-1176",
 "938-071891-16095",
 "하나 정기예금",
 "210,000",
 "2026.04.07",
 "32,900,000",
 "1,470,000",
 "6,180,000",
 "540-121210-96628",
 "남궁예태",
 "2024.04.25",
 "2024.07.07",
 "170,000",
 "3416-9930",
 "1985.03.28",
 "010-6144-1173",
 "yetae741@gmail.com",
 "하나 적금",
 "87,150,000",
 "12개월",
 "35,390,000",
 "2024년 12월 11일",
 "주거래하나 통장",
 "12,500,000",
 "80,000",
 "2024.11.13",
 "청년도약계좌",
 "690,000원",
 "8,220,000원",
 "2024년 12월 2일",
 "820,000",
 "93,070,000",
 "9,960,000",
 "2025년 04월 01일",
 "parkjy77",
 "(주)미래케미칼",
 "702-81-38348",
 "2020.06.15",
 "남궁찬윤",
 "부",
 "1952년 10월 28일",
 "010-7568-9115",
 "260-793845-43109",
 "51,830,000",
 "2028-02-25",
 "3,450,000",
 "이다태",
 "하나의정기예금",
 "2024년 5월 12일",
 "2024.06.17",
 "290,000",
 "949-556199-50243",
 "736-892734-06832",
 "4,240,000",
 "215,650,000",
 "116,430,000",
 "만기 해지",
 "1"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2024년 12월 2일"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"3,450,000"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- 목록.0.갋: 갋 (목록 1행)
- 목록.2.갋: 갋 (목록 3행)
- deposit_list_list.1.1.transfer_day: 확정형연동형(개월) (2행)
- customer.address: 자택 (고객 주소, 같은 항목명 중 1번째 칸)
- customer.home_phone: 자택 (고객 자택전화, 같은 항목명 중 2번째 칸)
- employer.phone: 직장 (직장 연락처, 같은 항목명 중 2번째 칸)
- bank.auto_transfer_account: 자동이체계좌번호 (같은 항목명 중 1번째 칸)
- bank.contract_amount: 계약(확인)금액 (같은 항목명 중 1번째 칸)
- deposit.withdraw_account: 출금계좌[
- account: 계좌번호 (같은 항목명 중 1번째 칸)
- bank.kind: 종별 (같은 항목명 중 1번째 칸)
- customer.birth: 생년월일(사업자번호) (고객 생년월일)
- customer.phone: 휴대폰 (고객 연락처)
- customer.email2: 계약서류수령E-mail또는휴대폰번호
- deposit_list.0.period: 계약기간1 (1행)
- deposit_list.1.product: 상품명2 (2행)
- deposit_list.1.amount: 가입금액2 (2행)
- deposit_list.1.transfer_end: 이체기간(만료일)2 (2행)
- deposit_list.2.product: 상품명3 (3행)
- deposit_list.2.period: 계약기간3 (3행)
- deposit_list.2.funding_amount: 출금금액③ (3행)
- ebank.user_id: 이용자ID
- corp.name: 상호명 (법인·사업자 상호)
- corp.biz_no: 사업자등록번호 (법인·사업자 사업자등록번호)
- account2: 입금계좌
- agent.relation: 본인과의관계 (대리인 관계)
- bank.auto_transfer_account2: 자동이체계좌번호 (같은 항목명 중 2번째 칸)
- bank.subject2: 과목명 (같은 항목명 중 2번째 칸)
- bank.pay_date2: 지급기일 (같은 항목명 중 2번째 칸)
- customer.name2: 신청인 (같은 항목명 중 2번째 칸)
- customer.name3: 신청인 (같은 항목명 중 3번째 칸)
- related.name: 아니오(실제소유자성명 (보증인·공동 성명)
- redeposit_list.0.product: [신청상품]1 (1행)
- customer.name4: 신청인 (같은 항목명 중 4번째 칸)
- agent.name2: 대리인
- account3: 계좌번호 (같은 항목명 중 2번째 칸)
- bank.first_trade_date2: 최초거래일 (같은 항목명 중 2번째 칸)
- related.rrn: 실명번호: (보증인·공동 주민등록번호)
- customer.name_en2: 영문명(전자화폐발급시)
- deposit.renew_count: 갱신횟수
```

답:

```json
[{"key": "목록.0.갋", "value": null},
 {"key": "목록.2.갋", "value": null},
 {"key": "deposit_list_list.1.1.transfer_day", "value": "25일", "bbox_2d": [499, 520, 537, 541], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [480, 221, 736, 242], "page": 1},
 {"key": "customer.home_phone", "value": "02-6508-5072", "bbox_2d": [681, 275, 798, 296], "page": 1},
 {"key": "employer.phone", "value": "051-509-1176", "bbox_2d": [686, 304, 789, 323], "page": 1},
 {"key": "bank.auto_transfer_account", "value": "938-071891-16095", "bbox_2d": [139, 924, 244, 939], "page": 1},
 {"key": "bank.contract_amount", "value": "210,000", "bbox_2d": [590, 940, 637, 955], "page": 1},
 {"key": "deposit.withdraw_account", "value": "540-121210-96628", "bbox_2d": [278, 662, 379, 677], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [104, 906, 220, 922], "page": 1},
 {"key": "bank.kind", "value": "하나 정기예금", "bbox_2d": [90, 940, 175, 957], "page": 1},
 {"key": "customer.birth", "value": "1985.03.28", "bbox_2d": [788, 135, 894, 161], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [485, 165, 627, 191], "page": 1},
 {"key": "customer.email2", "value": "yetae741@gmail.com", "bbox_2d": [638, 382, 754, 396], "page": 1},
 {"key": "deposit_list.0.period", "value": "12개월", "bbox_2d": [365, 430, 408, 447], "page": 1},
 {"key": "deposit_list.1.product", "value": "주거래하나 통장", "bbox_2d": [74, 499, 175, 518], "page": 1},
 {"key": "deposit_list.1.amount", "value": "12,500,000", "bbox_2d": [292, 502, 352, 516], "page": 1},
 {"key": "deposit_list.1.transfer_end", "value": "2024.11.13", "bbox_2d": [696, 522, 754, 536], "page": 1},
 {"key": "deposit_list.2.product", "value": "청년도약계좌", "bbox_2d": [76, 574, 189, 594], "page": 1},
 {"key": "deposit_list.2.period", "value": "12개월", "bbox_2d": [364, 574, 407, 591], "page": 1},
 {"key": "deposit_list.2.funding_amount", "value": "9,960,000", "bbox_2d": [825, 663, 879, 677], "page": 1},
 {"key": "ebank.user_id", "value": "parkjy77", "bbox_2d": [127, 86, 221, 110], "page": 2},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [237, 441, 360, 463], "page": 2},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [540, 442, 655, 462], "page": 2},
 {"key": "account2", "value": "540-121210-96628", "bbox_2d": [551, 521, 715, 544], "page": 2},
 {"key": "agent.relation", "value": "부", "bbox_2d": [199, 783, 213, 806], "page": 2},
 {"key": "bank.auto_transfer_account2", "value": "260-793845-43109", "bbox_2d": [134, 922, 251, 939], "page": 2},
 {"key": "bank.subject2", "value": "주거래하나 통장", "bbox_2d": [334, 923, 426, 939], "page": 2},
 {"key": "bank.pay_date2", "value": "2028-02-25", "bbox_2d": [813, 922, 890, 938], "page": 2},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [779, 161, 848, 181], "page": 2},
 {"key": "customer.name3", "value": "남궁예태", "bbox_2d": [783, 243, 852, 263], "page": 2},
 {"key": "related.name", "value": "이다태", "bbox_2d": [428, 344, 475, 361], "page": 2},
 {"key": "redeposit_list.0.product", "value": "하나의정기예금", "bbox_2d": [255, 544, 359, 562], "page": 2},
 {"key": "customer.name4", "value": "남궁예태", "bbox_2d": [784, 548, 853, 568], "page": 2},
 {"key": "agent.name2", "value": "남궁찬윤", "bbox_2d": [781, 714, 839, 733], "page": 2},
 {"key": "account3", "value": "540-121210-96628", "bbox_2d": [107, 905, 222, 921], "page": 2},
 {"key": "bank.first_trade_date2", "value": "2024년 5월 12일", "bbox_2d": [558, 907, 623, 918], "page": 2},
 {"key": "related.rrn", "value": "736-892734-06832", "bbox_2d": [811, 349, 853, 355], "page": 2},
 {"key": "customer.name_en2", "value": "NAMGOONG YETAE", "bbox_2d": [521, 237, 648, 253], "page": 2},
 {"key": "deposit.renew_count", "value": "1", "bbox_2d": [891, 521, 897, 540], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.signer: 한도:₩..~.. (같은 항목명 중 1번째 칸, 도장)
- sign.signer: 한도:₩..~.. (같은 항목명 중 2번째 칸, 서명)
- seal.signer2: 한도:₩..~.. (같은 항목명 중 3번째 칸, 도장)
- sign.signer2: 한도:₩..~.. (같은 항목명 중 4번째 칸, 서명)
- seal.signer3: 한도:₩..~.. (같은 항목명 중 5번째 칸, 도장)
- sign.signer3: 한도:₩..~.. (같은 항목명 중 6번째 칸, 서명)
- seal.signer4: 고객정보변경없음 (같은 항목명 중 1번째 칸, 도장)
- sign.signer4: 고객정보변경없음 (같은 항목명 중 2번째 칸, 서명)
- check.비과세종합저축재형저축: 비과세종합저축/재형저축/주택청약상품의계약금액/한도/중복 (체크박스, 보기: 비과세종합저축 / 재형저축 / 주택청약상품의 계약금액 / 한도 / 중복 )
- check.귀행에대한제대출금보증채: 귀행에대한제대출금,보증채무,신용카드채무에대하여변제기가도래하 (체크박스, 보기: 귀행에 대한 제 대출금, 보증채무, 신용카드채무에 대하여 변제기가 도래하)
- check.본인은금융지주회사법제4: 본인은금융지주회사법제48조의2에근거하여하나금융그룹내지주사및자 (체크박스, 보기: 본인은 금융지주회사법 제48조의2에 근거하여 하나금융그룹내 지주사 및 자)
```

답:

```json
[{"key": "seal.signer", "value": false},
 {"key": "sign.signer", "value": true, "bbox_2d": [830, 428, 950, 468], "page": 1},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [830, 498, 950, 540], "page": 1},
 {"key": "seal.signer3", "value": true, "bbox_2d": [863, 574, 917, 612], "page": 1},
 {"key": "sign.signer3", "value": false},
 {"key": "seal.signer4", "value": false},
 {"key": "sign.signer4", "value": true, "bbox_2d": [830, 191, 950, 286], "page": 1},
 {"key": "check.비과세종합저축재형저축", "value": null},
 {"key": "check.귀행에대한제대출금보증채", "value": "귀행에 대한 제 대출금, 보증채무, 신용카드채무에 대하여 변제기가 도래하", "bbox_2d": [59, 701, 69, 708], "page": 1},
 {"key": "check.본인은금융지주회사법제4", "value": "본인은 금융지주회사법 제48조의2에 근거하여 하나금융그룹내 지주사 및 자", "bbox_2d": [59, 708, 69, 716], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf003 --show` · `python -m docgen.preview hf003 --out work/hf003`
