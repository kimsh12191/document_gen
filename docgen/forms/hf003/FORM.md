# 은행거래신청서 (`hf003`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf003 · card-hash: 519f9fb6820d -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 예금거래신청서 (다른 이름: 은행거래신청서)
- **질문·답:** 이 폴더의 `questions.json` 에서 바꾼 것이 있음 (아래 ← 바꿈)
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf003 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.3 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `questions.json` | 기본 과제의 질문 문장·답 틀 (기본과 다른 것만) |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 64칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `갋` | 갋 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:119 | 묻기 |
| `갋2` | 갋 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:133 | 묻기 |
| `갋3` | 갋 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:147 | 묻기 |
| `deposit_list_list.*.*.transfer_day` | 확정형연동형(개월) | text | 1쪽 [503, 449, 529, 469] (1행) | 늘 | 파일 key | 값 종류 `transfer_day` | fields.json:161 | 묻기 |
| `customer.name_en` | 영문명 | text | 1쪽 [480, 136, 699, 162] | 늘 | 파일 key | 고객 정보 (키 `customer.name_en`, 없으면 값 종류 `text`) | fields.json:248 | 묻기 |
| `customer.email` | 이메일 | text | 1쪽 [473, 191, 734, 219] | 늘 | 파일 key | 고객 정보 (키 `customer.email`, 없으면 값 종류 `email`) | fields.json:262 | 묻기 |
| `customer.address` | 자택 | text | 1쪽 [477, 223, 733, 242] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `text`) | fields.json:282 | 묻기 |
| `employer.address` | 직장 | text | 1쪽 [478, 252, 763, 268] | 늘 | 파일 key | 고객 정보 (키 `employer.address`, 없으면 값 종류 `text`) | fields.json:297 | 묻기 |
| `customer.home_phone` | 자택 | phone | 1쪽 [681, 275, 799, 296] | 늘 | 파일 key | 고객 정보 (키 `customer.home_phone`, 없으면 값 종류 `text`) | fields.json:313 | 묻기 |
| `employer.phone` | 직장 | phone | 1쪽 [687, 302, 791, 324] | 늘 | 파일 key | 고객 정보 (키 `employer.phone`, 없으면 값 종류 `text`) | fields.json:328 | 묻기 |
| `customer.payday` | 급여일 | text | 1쪽 [782, 193, 826, 218] | 늘 | 파일 key | 고객 정보 (키 `customer.payday`, 없으면 값 종류 `payday`) | fields.json:343 | 묻기 |
| `bank.auto_transfer_account` | 자동이체계좌번호 | account_no | 1쪽 [135, 923, 240, 939] | 늘 | 파일 key | 고객 정보 (키 `bank.auto_transfer_account`, 없으면 값 종류 `account`) | fields.json:373 | 묻기 |
| `bank.subject` | 과목명 | text | 1쪽 [335, 924, 412, 939] | 늘 | 파일 key | 고객 정보 (키 `bank.subject`, 없으면 값 종류 `product`) | fields.json:387 | 묻기 |
| `bank.contract_amount` | 계약(확인)금액 | amount | 1쪽 [572, 940, 635, 955] | 늘 | 파일 key | 고객 정보 (키 `bank.contract_amount`, 없으면 값 종류 `amount`) | fields.json:401 | 묻기 |
| `bank.pay_date` | 지급기일 | date | 1쪽 [819, 923, 881, 938] | 늘 | 파일 key | 고객 정보 (키 `bank.pay_date`, 없으면 값 종류 `date`) | fields.json:415 | 묻기 |
| `date` | 작성일 | date | 1쪽 [442, 715, 637, 726] | 늘 | 파일 key | 작성일 | fields.json:501 | 묻기 |
| `deposit.withdraw_account` | 출금계좌[ | account_no | 1쪽 [278, 662, 379, 677] | 늘 | 파일 key | `profile.accounts.0.number` (파일) | fields.json:572 | 묻기 |
| `customer.name` | 신청인 | text | 1쪽 [800, 698, 890, 723] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:588 | 묻기 |
| `account` | 계좌번호 | account_no | 1쪽 [104, 906, 220, 922] | 늘 | 파일 key | 고객 정보 (키 `account`, 없으면 값 종류 `account`) | fields.json:602 | 묻기 |
| `bank.first_trade_date` | 최초거래일 | date | 1쪽 [559, 907, 626, 920] | 늘 | 파일 key | 고객 정보 (키 `bank.first_trade_date`, 없으면 값 종류 `date`) | fields.json:616 | 묻기 |
| `bank.open_date` | 신규일 | date | 1쪽 [810, 904, 884, 921] | 늘 | 파일 key | 고객 정보 (키 `bank.open_date`, 없으면 값 종류 `date`) | fields.json:631 | 묻기 |
| `bank.deposit_amount` | 입금(수탁)액 | amount | 1쪽 [589, 923, 636, 939] | 늘 | 파일 key | 고객 정보 (키 `bank.deposit_amount`, 없으면 값 종류 `amount`) | fields.json:646 | 묻기 |
| `bank.kind` | 종별 | text | 1쪽 [90, 940, 175, 957] | 늘 | 파일 key | 고객 정보 (키 `bank.kind`, 없으면 값 종류 `product`) | fields.json:661 | 묻기 |
| `bank.staff_no` | 권유직원번호 | text | 1쪽 [838, 941, 902, 956] | 늘 | 파일 key | 고객 정보 (키 `bank.staff_no`, 없으면 값 종류 `number`) | fields.json:676 | 묻기 |
| `customer.name7` | 성명(업체명) | text | 1쪽 [154, 138, 246, 163] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `person`) | fields.json:1123 | 묻기 |
| `customer.birth` | 생년월일(사업자번호) | date | 1쪽 [788, 135, 894, 161] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`, 없으면 값 종류 `date`) | fields.json:1137 | 묻기 |
| `customer.phone` | 휴대폰 | phone | 1쪽 [485, 165, 627, 191] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:1151 | 묻기 |
| `customer.email2` | 계약서류수령E-mail또는휴대폰번호 | text | 1쪽 [638, 382, 754, 396] | 늘 | 파일 key | 고객 정보 (키 `customer.email`, 없으면 값 종류 `phone`) | fields.json:1165 | 묻기 |
| `date2` | 작성일(년월일) | date | 1쪽 [356, 716, 419, 726] | 늘 | 파일 key | 고객 정보 (키 `date`, 없으면 값 종류 `date`) | fields.json:1431 | 묻기 |
| `ebank.user_id` | 이용자ID | text | 2쪽 [127, 86, 221, 110] | 늘 | 파일 key | 고객 정보 (키 `ebank.user_id`, 없으면 값 종류 `user_id`) | fields.json:691 | 묻기 |
| `company.name` | 상호명 | text | 2쪽 [237, 441, 360, 463] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:706 | 묻기 |
| `company.biz_no` | 사업자등록번호 | biz_no | 2쪽 [540, 442, 655, 462] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:720 | 묻기 |
| `company.established` | 개업년월일 | date | 2쪽 [804, 443, 893, 463] | 늘 | 파일 key | 고객 정보 (키 `company.established`, 없으면 값 종류 `date`) | fields.json:734 | 묻기 |
| `account2` | 입금계좌 | account_no | 2쪽 [551, 521, 715, 544] | 늘 | 파일 key | 고객 정보 (키 `account`, 없으면 값 종류 `account`) | fields.json:749 | 묻기 |
| `agent.name` | 성명 | text | 2쪽 [198, 760, 272, 784] | 늘 | 파일 key | 고객 정보 (키 `agent.name`, 없으면 값 종류 `person`) | fields.json:762 | 묻기 |
| `agent.relation` | 본인과의관계 | text | 2쪽 [199, 783, 213, 806] | 늘 | 파일 key | 고객 정보 (키 `agent.relation`, 없으면 값 종류 `text`) | fields.json:776 | 묻기 |
| `agent.birth` | 생년월일 | date | 2쪽 [482, 762, 621, 784] | 늘 | 파일 key | 고객 정보 (키 `agent.birth`, 없으면 값 종류 `date`) | fields.json:790 | 묻기 |
| `agent.address` | 주소 | text | 2쪽 [481, 779, 823, 808] | 늘 | 파일 key | 고객 정보 (키 `agent.address`, 없으면 값 종류 `address`) | fields.json:804 | 묻기 |
| `agent.phone` | 전화번호 | phone | 2쪽 [744, 758, 881, 783] | 늘 | 파일 key | 고객 정보 (키 `agent.phone`, 없으면 값 종류 `phone`) | fields.json:819 | 묻기 |
| `bank.auto_transfer_account2` | 자동이체계좌번호 | text | 2쪽 [134, 922, 251, 939] | 늘 | 파일 key | 고객 정보 (키 `bank.auto_transfer_account`, 없으면 값 종류 `account`) | fields.json:834 | 묻기 |
| `bank.subject2` | 과목명 | text | 2쪽 [334, 923, 426, 939] | 늘 | 파일 key | 고객 정보 (키 `bank.subject`, 없으면 값 종류 `product`) | fields.json:848 | 묻기 |
| `bank.contract_amount2` | 계약(확인)금액 | amount | 2쪽 [566, 941, 631, 956] | 늘 | 파일 key | 고객 정보 (키 `bank.contract_amount`, 없으면 값 종류 `amount`) | fields.json:862 | 묻기 |
| `bank.pay_date2` | 지급기일 | date | 2쪽 [813, 922, 890, 938] | 늘 | 파일 key | 고객 정보 (키 `bank.pay_date`, 없으면 값 종류 `date`) | fields.json:876 | 묻기 |
| `ebank.phone_limit_once` | 원)(1회 | amount | 2쪽 [808, 119, 912, 145] | 늘 | 파일 key | 고객 정보 (키 `ebank.phone_limit_once`, 없으면 값 종류 `amount`) | fields.json:890 | 묻기 |
| `customer.name2` | 신청인 | text | 2쪽 [779, 161, 848, 181] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:906 | 묻기 |
| `customer.name3` | 신청인 | text | 2쪽 [783, 243, 852, 263] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:920 | 묻기 |
| `related.name` | 아니오(실제소유자성명 | text | 2쪽 [428, 344, 475, 361] | 늘 | 파일 key | 고객 정보 (키 `related.name`, 없으면 값 종류 `person`) | fields.json:934 | 묻기 |
| `customer.name4` | 신청인 | text | 2쪽 [784, 548, 853, 568] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:964 | 묻기 |
| `customer.name5` | 예금주 | text | 2쪽 [547, 714, 616, 733] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:978 | 묻기 |
| `agent.name2` | 대리인 | text | 2쪽 [781, 714, 839, 733] | 늘 | 파일 key | 고객 정보 (키 `agent.name`, 없으면 값 종류 `text`) | fields.json:992 | 묻기 |
| `customer.name6` | 위임인(예금주) | text | 2쪽 [751, 808, 820, 828] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:1006 | 묻기 |
| `account3` | 계좌번호 | account_no | 2쪽 [107, 905, 222, 921] | 늘 | 파일 key | 고객 정보 (키 `account`, 없으면 값 종류 `account`) | fields.json:1020 | 묻기 |
| `bank.first_trade_date2` | 최초거래일 | date | 2쪽 [558, 907, 623, 918] | 늘 | 파일 key | 고객 정보 (키 `bank.first_trade_date`, 없으면 값 종류 `date`) | fields.json:1034 | 묻기 |
| `bank.open_date2` | 신규일 | date | 2쪽 [806, 905, 876, 922] | 늘 | 파일 key | 고객 정보 (키 `bank.open_date`, 없으면 값 종류 `date`) | fields.json:1049 | 묻기 |
| `bank.deposit_amount2` | 입금(수탁)액 | amount | 2쪽 [581, 922, 632, 938] | 늘 | 파일 key | 고객 정보 (키 `bank.deposit_amount`, 없으면 값 종류 `amount`) | fields.json:1064 | 묻기 |
| `bank.kind2` | 종별 | text | 2쪽 [87, 940, 171, 956] | 늘 | 파일 key | 고객 정보 (키 `bank.kind`, 없으면 값 종류 `product`) | fields.json:1079 | 묻기 |
| `bank.staff_no2` | 권유직원번호 | text | 2쪽 [831, 941, 927, 953] | 늘 | 파일 key | 고객 정보 (키 `bank.staff_no`, 없으면 값 종류 `number`) | fields.json:1094 | 묻기 |
| `related.rrn` | 실명번호: | text | 2쪽 [811, 349, 853, 355] | 늘 | 파일 key | 고객 정보 (키 `related.rrn`, 없으면 값 종류 `number`) | fields.json:1109 | 묻기 |
| `ebank.internet_limit_day` | 인터넷/스마트폰뱅킹1일한도 | amount | 2쪽 [609, 90, 721, 116] | 늘 | 파일 key | 고객 정보 (키 `ebank.internet_limit_day`, 없으면 값 종류 `amount`) | fields.json:1445 | 묻기 |
| `ebank.internet_limit_once` | 인터넷/스마트폰뱅킹1회한도 | amount | 2쪽 [815, 93, 912, 115] | 늘 | 파일 key | 고객 정보 (키 `ebank.internet_limit_once`, 없으면 값 종류 `amount`) | fields.json:1459 | 묻기 |
| `ebank.phone_limit_day` | 폰뱅킹1일한도 | amount | 2쪽 [621, 121, 719, 143] | 늘 | 파일 key | 고객 정보 (키 `ebank.phone_limit_day`, 없으면 값 종류 `amount`) | fields.json:1473 | 묻기 |
| `ebank.passbook_memo` | 전자통장설명문구(한글6자) | text | 2쪽 [199, 237, 255, 252] | 늘 | 파일 key | `rule:free_text` (파일) | fields.json:1487 | 묻기 |
| `customer.name_en2` | 영문명(전자화폐발급시) | text | 2쪽 [521, 237, 648, 253] | 늘 | 파일 key | 고객 정보 (키 `customer.name_en`, 없으면 값 종류 `text`) | fields.json:1502 | 묻기 |
| `deposit.renew_count` | 갱신횟수 | number | 2쪽 [891, 521, 897, 540] | 늘 | 파일 key | 고객 정보 (키 `deposit.renew_count`, 없으면 값 종류 `count`) | fields.json:1516 | 묻기 |

## 표 `deposit_list` (표 과제 table·table_read·table_find·table_qa) — 8열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `deposit_list.*.interest_account` | 통장발행 | account_no | 1쪽 [72, 448, 221, 468] (1행) | 늘 | 파일 key | 값 종류 `account` | fields.json:23 | 묻기 |
| `deposit_list.*.tax_free_limit` | 연원가식 | amount | 1쪽 [744, 429, 812, 444] (1행) | 늘 | 파일 key | 고객 정보 (키 `deposit_list.0.tax_free_limit`, 없으면 값 종류 `amount`) | fields.json:527 | 묻기 |
| `deposit_list.*.product` | 상품명1 / 상품명2 / 상품명3 | text | 1쪽 [76, 428, 155, 449] (1행) | 늘 | 파일 key | 고객 정보 (키 `deposit_list.0.product`, 없으면 값 종류 `product`) | fields.json:1179 | 묻기 |
| `deposit_list.*.amount` | 가입금액1 / 가입금액2 / 가입금액3 | amount | 1쪽 [292, 431, 350, 445] (1행) | 늘 | 파일 key | 고객 정보 (키 `deposit_list.0.amount`, 없으면 값 종류 `amount`) | fields.json:1193 | 묻기 |
| `deposit_list.*.period` | 계약기간1 / 계약기간2 / 계약기간3 | text | 1쪽 [365, 430, 408, 447] (1행) | 늘 | 파일 key | 고객 정보 (키 `deposit_list.0.period`, 없으면 값 종류 `contract_period`) | fields.json:1207 | 묻기 |
| `deposit_list.*.transfer_amount` | 이체금액1 / 이체금액2 / 이체금액3 | amount | 1쪽 [620, 452, 681, 465] (1행) | 늘 | 파일 key | 고객 정보 (키 `deposit_list.0.transfer_amount`, 없으면 값 종류 `amount`) | fields.json:1221 | 묻기 |
| `deposit_list.*.transfer_end` | 이체기간(만료일)1 / 이체기간(만료일)2 / 이체기간(만료일)3 | date | 1쪽 [693, 451, 784, 465] (1행) | 늘 | 파일 key | 고객 정보 (키 `deposit_list.0.transfer_end`, 없으면 값 종류 `date`) | fields.json:1235 | 묻기 |
| `deposit_list.*.funding_amount` | 출금금액① / 출금금액② / 출금금액③ | amount | 1쪽 [606, 663, 650, 676] (1행) | 늘 | 파일 key | 고객 정보 (키 `deposit_list.0.funding_amount`, 없으면 값 종류 `amount`) | fields.json:1389 | 묻기 |

## 표 `자유_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `자유_목록.*.갋` | 갋 | text | - (1행) | 늘 | 파일 key | 값 종류 `skip` | fields.json:71 | 묻기 |

## 표 `redeposit_list` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `redeposit_list.*.product` | [신청상품]1 / 신청상품② / 신청상품③ | text | 2쪽 [255, 544, 359, 562] (1행) | 늘 | 파일 key | 고객 정보 (키 `redeposit_list.0.product`, 없으면 값 종류 `product`) | fields.json:949 | 묻기 |

## 체크·도장·서명 (marks) — 11칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.signer` | 한도:₩..~.. | seal | 1쪽 [830, 428, 950, 468] | 늘 | 키 설명 그대로 | 값 종류 `seal` | fields.json:206 | 묻기 |
| `sign.signer` | 한도:₩..~.. | signature | 1쪽 [830, 428, 950, 468] | 늘 | 키 설명 그대로 | 값 종류 `seal` | fields.json:206 | 묻기 |
| `seal.signer2` | 한도:₩..~.. | seal | 1쪽 [830, 498, 950, 540] | 늘 | 키 설명 그대로 | 값 종류 `seal` | fields.json:220 | 묻기 |
| `sign.signer2` | 한도:₩..~.. | signature | 1쪽 [830, 498, 950, 540] | 늘 | 키 설명 그대로 | 값 종류 `seal` | fields.json:220 | 묻기 |
| `seal.signer3` | 한도:₩..~.. | seal | 1쪽 [860, 572, 919, 614] | 늘 | 키 설명 그대로 | 값 종류 `seal` | fields.json:234 | 묻기 |
| `sign.signer3` | 한도:₩..~.. | signature | 1쪽 [830, 572, 950, 613] | 늘 | 키 설명 그대로 | 값 종류 `seal` | fields.json:234 | 묻기 |
| `seal.signer4` | 고객정보변경없음 | seal | 1쪽 [830, 191, 950, 286] | 늘 | 표 행 (묶음·키 설명 '고객정보 변경없음') | 값 종류 `seal` | fields.json:357 | 묻기 |
| `sign.signer4` | 고객정보변경없음 | signature | 1쪽 [830, 191, 950, 286] | 늘 | 표 행 (묶음·키 설명 '고객정보 변경없음') | 값 종류 `seal` | fields.json:357 | 묻기 |
| `check.비과세종합저축재형저축` | 비과세종합저축/재형저축/주택청약상품의계약금액/한도/중복 | checkbox (비과세종합저축 / 재형저축 / 주택청약상품의 계약금액 / 한도 / 중복 ) | 1쪽 [59, 694, 551, 702] | 늘 | 파일 key | 보기 중 고름: 비과세종합저축 / 재형저축 / 주택청약상품의 계약금액 / 한도 / 중복  | fields.json:429 | 묻기 |
| `check.귀행에대한제대출금보증채` | 귀행에대한제대출금,보증채무,신용카드채무에대하여변제기가도래하 | checkbox (귀행에 대한 제 대출금, 보증채무, 신용카드채무에 대하여 변제기가 도래하) | 1쪽 [59, 701, 625, 709] | 늘 | 파일 key | 보기 중 고름: 귀행에 대한 제 대출금, 보증채무, 신용카드채무에 대하여 변제기가 도래하 | fields.json:453 | 묻기 |
| `check.본인은금융지주회사법제4` | 본인은금융지주회사법제48조의2에근거하여하나금융그룹내지주사및자 | checkbox (본인은 금융지주회사법 제48조의2에 근거하여 하나금융그룹내 지주사 및 자) | 1쪽 [59, 708, 656, 716] | 늘 | 파일 key | 보기 중 고름: 본인은 금융지주회사법 제48조의2에 근거하여 하나금융그룹내 지주사 및 자 | fields.json:477 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
- **고칠 곳:** html·코드 서식은 템플릿 줄(칸 자리·키·항목명)과 fields.json 줄(값 출처·질문 설정 q), 원본 서식은 fields.json 의 그 칸(박스 `rect`·항목명·키·값·q). html·코드 서식에서 fields.json 에 줄이 없는 칸의 질문 설정은 fields.json 맨 위 `"q": {"키": {…}}` 묶음에.

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 이 폴더 `questions.json` 과 공통 `docgen/forms/_common/questions.json`.

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
 "5일",
 "NAMGOONG YETAE",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "부산광역시 해운대구 해운대로 326, 7층 주식회사 다온패션 고객지원팀",
 "02-6508-5072",
 "051-509-1176",
 "말일",
 "380-718911-60956",
 "급여하나 통장",
 "9,280,000",
 "2028.11.28",
 "32,900,000",
 "1,470,000",
 "6,180,000",
 "540-121210-96628",
 "남궁예태",
 "2024.04.25",
 "2024.07.07",
 "170,000",
 "하나 정기예금",
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
항목 (키: 설명 (몇 번째 행))
- 갋: 갋 (같은 설명 중 1번째 칸)
- 갋2: 갋 (같은 설명 중 2번째 칸)
- customer.name_en: 영문명
- customer.address: 자택 (같은 설명 중 1번째 칸)
- employer.phone: 직장 (같은 설명 중 2번째 칸)
- customer.payday: 급여일
- bank.pay_date: 지급기일 (같은 설명 중 1번째 칸)
- date: 작성일
- account: 계좌번호 (같은 설명 중 1번째 칸)
- bank.first_trade_date: 최초거래일 (같은 설명 중 1번째 칸)
- bank.deposit_amount: 입금(수탁)액 (같은 설명 중 1번째 칸)
- bank.kind: 종별 (같은 설명 중 1번째 칸)
- bank.staff_no: 권유직원번호 (같은 설명 중 1번째 칸)
- date2: 작성일(년월일)
- ebank.user_id: 이용자ID
- company.name: 상호명
- company.biz_no: 사업자등록번호
- company.established: 개업년월일
- account2: 입금계좌
- agent.relation: 본인과의관계
- agent.birth: 생년월일
- agent.address: 주소
- agent.phone: 전화번호
- bank.auto_transfer_account2: 자동이체계좌번호 (같은 설명 중 2번째 칸)
- bank.contract_amount2: 계약(확인)금액 (같은 설명 중 2번째 칸)
- bank.pay_date2: 지급기일 (같은 설명 중 2번째 칸)
- customer.name2: 신청인 (같은 설명 중 2번째 칸)
- related.name: 아니오(실제소유자성명
- customer.name4: 신청인 (같은 설명 중 4번째 칸)
- customer.name5: 예금주
- agent.name2: 대리인
- account3: 계좌번호 (같은 설명 중 2번째 칸)
- bank.deposit_amount2: 입금(수탁)액 (같은 설명 중 2번째 칸)
- bank.kind2: 종별 (같은 설명 중 2번째 칸)
- bank.staff_no2: 권유직원번호 (같은 설명 중 2번째 칸)
- related.rrn: 실명번호:
- ebank.internet_limit_day: 인터넷/스마트폰뱅킹1일한도
- ebank.internet_limit_once: 인터넷/스마트폰뱅킹1회한도
- ebank.phone_limit_day: 폰뱅킹1일한도
- ebank.passbook_memo: 전자통장설명문구(한글6자)
```

답:

```json
[{"key": "갋", "value": null},
 {"key": "갋2", "value": null},
 {"key": "customer.name_en", "value": "NAMGOONG YETAE", "bbox_2d": [480, 136, 699, 162], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [477, 223, 733, 242], "page": 1},
 {"key": "employer.phone", "value": "051-509-1176", "bbox_2d": [687, 302, 791, 324], "page": 1},
 {"key": "customer.payday", "value": "말일", "bbox_2d": [782, 193, 826, 218], "page": 1},
 {"key": "bank.pay_date", "value": "2028.11.28", "bbox_2d": [819, 923, 881, 938], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [442, 715, 637, 726], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [104, 906, 220, 922], "page": 1},
 {"key": "bank.first_trade_date", "value": "2024.04.25", "bbox_2d": [559, 907, 626, 920], "page": 1},
 {"key": "bank.deposit_amount", "value": "170,000", "bbox_2d": [589, 923, 636, 939], "page": 1},
 {"key": "bank.kind", "value": "하나 정기예금", "bbox_2d": [90, 940, 175, 957], "page": 1},
 {"key": "bank.staff_no", "value": "3416-9930", "bbox_2d": [838, 941, 902, 956], "page": 1},
 {"key": "date2", "value": "2025년 04월 01일", "bbox_2d": [356, 716, 419, 726], "page": 1},
 {"key": "ebank.user_id", "value": "parkjy77", "bbox_2d": [127, 86, 221, 110], "page": 2},
 {"key": "company.name", "value": "(주)미래케미칼", "bbox_2d": [237, 441, 360, 463], "page": 2},
 {"key": "company.biz_no", "value": "702-81-38348", "bbox_2d": [540, 442, 655, 462], "page": 2},
 {"key": "company.established", "value": "2020.06.15", "bbox_2d": [804, 443, 893, 463], "page": 2},
 {"key": "account2", "value": "540-121210-96628", "bbox_2d": [551, 521, 715, 544], "page": 2},
 {"key": "agent.relation", "value": "부", "bbox_2d": [199, 783, 213, 806], "page": 2},
 {"key": "agent.birth", "value": "1952년 10월 28일", "bbox_2d": [482, 762, 621, 784], "page": 2},
 {"key": "agent.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [481, 779, 823, 808], "page": 2},
 {"key": "agent.phone", "value": "010-7568-9115", "bbox_2d": [744, 758, 881, 783], "page": 2},
 {"key": "bank.auto_transfer_account2", "value": "260-793845-43109", "bbox_2d": [134, 922, 251, 939], "page": 2},
 {"key": "bank.contract_amount2", "value": "51,830,000", "bbox_2d": [566, 941, 631, 956], "page": 2},
 {"key": "bank.pay_date2", "value": "2028-02-25", "bbox_2d": [813, 922, 890, 938], "page": 2},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [779, 161, 848, 181], "page": 2},
 {"key": "related.name", "value": "이다태", "bbox_2d": [428, 344, 475, 361], "page": 2},
 {"key": "customer.name4", "value": "남궁예태", "bbox_2d": [784, 548, 853, 568], "page": 2},
 {"key": "customer.name5", "value": "남궁예태", "bbox_2d": [547, 714, 616, 733], "page": 2},
 {"key": "agent.name2", "value": "남궁찬윤", "bbox_2d": [781, 714, 839, 733], "page": 2},
 {"key": "account3", "value": "540-121210-96628", "bbox_2d": [107, 905, 222, 921], "page": 2},
 {"key": "bank.deposit_amount2", "value": "290,000", "bbox_2d": [581, 922, 632, 938], "page": 2},
 {"key": "bank.kind2", "value": "하나 정기예금", "bbox_2d": [87, 940, 171, 956], "page": 2},
 {"key": "bank.staff_no2", "value": "949-556199-50243", "bbox_2d": [831, 941, 927, 953], "page": 2},
 {"key": "related.rrn", "value": "736-892734-06832", "bbox_2d": [811, 349, 853, 355], "page": 2},
 {"key": "ebank.internet_limit_day", "value": "4,240,000", "bbox_2d": [609, 90, 721, 116], "page": 2},
 {"key": "ebank.internet_limit_once", "value": "215,650,000", "bbox_2d": [815, 93, 912, 115], "page": 2},
 {"key": "ebank.phone_limit_day", "value": "116,430,000", "bbox_2d": [621, 121, 719, 143], "page": 2},
 {"key": "ebank.passbook_memo", "value": "만기 해지", "bbox_2d": [199, 237, 255, 252], "page": 2}]
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
- seal.signer: 한도:₩..~.. (같은 설명 중 1번째 칸, 도장)
- sign.signer: 한도:₩..~.. (같은 설명 중 2번째 칸, 서명)
- seal.signer2: 한도:₩..~.. (같은 설명 중 3번째 칸, 도장)
- sign.signer2: 한도:₩..~.. (같은 설명 중 4번째 칸, 서명)
- seal.signer3: 한도:₩..~.. (같은 설명 중 5번째 칸, 도장)
- sign.signer3: 한도:₩..~.. (같은 설명 중 6번째 칸, 서명)
- seal.signer4: 고객정보변경없음 (같은 설명 중 1번째 칸, 도장)
- sign.signer4: 고객정보변경없음 (같은 설명 중 2번째 칸, 서명)
- check.비과세종합저축재형저축: 비과세종합저축/재형저축/주택청약상품의계약금액/한도/중복 (체크박스, 보기: 비과세종합저축 / 재형저축 / 주택청약상품의 계약금액 / 한도 / 중복 )
- check.귀행에대한제대출금보증채: 귀행에대한제대출금,보증채무,신용카드채무에대하여변제기가도래하 (체크박스, 보기: 귀행에 대한 제 대출금, 보증채무, 신용카드채무에 대하여 변제기가 도래하)
- check.본인은금융지주회사법제4: 본인은금융지주회사법제48조의2에근거하여하나금융그룹내지주사및자 (체크박스, 보기: 본인은 금융지주회사법 제48조의2에 근거하여 하나금융그룹내 지주사 및 자)
```

답:

```json
[{"key": "seal.signer", "value": false},
 {"key": "sign.signer", "value": false},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": false},
 {"key": "seal.signer3", "value": true, "bbox_2d": [860, 572, 919, 614], "page": 1},
 {"key": "sign.signer3", "value": false},
 {"key": "seal.signer4", "value": false},
 {"key": "sign.signer4", "value": true, "bbox_2d": [830, 191, 950, 286], "page": 1},
 {"key": "check.비과세종합저축재형저축", "value": null},
 {"key": "check.귀행에대한제대출금보증채", "value": "귀행에 대한 제 대출금, 보증채무, 신용카드채무에 대하여 변제기가 도래하", "bbox_2d": [59, 701, 69, 708], "page": 1},
 {"key": "check.본인은금융지주회사법제4", "value": "본인은 금융지주회사법 제48조의2에 근거하여 하나금융그룹내 지주사 및 자", "bbox_2d": [59, 708, 69, 716], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[72, 428, 879, 677] 위치의 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 설명)
- interest_account: 통장발행
- product: 상품명1
- amount: 가입금액1
- period: 계약기간1
- transfer_amount: 이체금액1
- funding_amount: 출금금액①
- transfer_end: 이체기간(만료일)1
- tax_free_limit: 연원가식
```

답:

```json
{
 "columns": [
  "interest_account",
  "product",
  "amount",
  "period",
  "transfer_amount",
  "funding_amount",
  "transfer_end",
  "tax_free_limit"
 ],
 "rows": [
  [
   "542-218001-62744",
   "하나 적금",
   "87,150,000",
   "12개월",
   "35,390,000",
   "820,000",
   "2024년 12월 11일",
   "32,900,000"
  ],
  [
   "361-231296-44138",
   "주거래하나 통장",
   "12,500,000",
   "12개월",
   "80,000",
   "93,070,000",
   "2024.11.13",
   "1,470,000"
  ],
  [
   "419-070303-12790",
   "청년도약계좌",
   "690,000원",
   "12개월",
   "8,220,000원",
   "9,960,000",
   "2024년 12월 2일",
   "6,180,000"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    72,
    428,
    812,
    676
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    74,
    499,
    809,
    676
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    72,
    572,
    879,
    677
   ],
   "page": 1
  }
 ]
}
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[{"columns": ["통장발행", "상품명1", "가입금액1", "계약기간1", "이체금액1", "출금금액①", "이체기간(만료일)1", "연원가식"], "bbox_2d": [72, 428, 879, 677], "page": 1, "n_rows": 3},
 {"columns": ["[신청상품]1"], "bbox_2d": [255, 542, 685, 565], "page": 2, "n_rows": 3}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '상품명1'·'출금금액①' 열이 있는 표를 보고 답하세요. 마지막 행의 '상품명1' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"청년도약계좌"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '상품명1'·'출금금액①' 열이 있는 표를 보고 답하세요. '통장발행' 칸이 '361-231296-44138'인 행의 '상품명1' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"주거래하나 통장"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf003 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf003` → `python -m docgen.formdir card hf003` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 키 설명이 그대로 키) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf003 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf003 --show` · `python -m docgen.preview hf003 --out work/hf003`
