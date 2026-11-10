# 키 이름 정하기 (새 서식·외주용)

새 서식에 칸을 그릴 때 칸마다 붙이는 **키**를 정하는 규칙입니다. 그림 위에 그려서 만드는 서식(studio 새 서식 추가, [new-forms.md 1절](new-forms.md#1-그림-위에-그려서-만들기))을 기준으로 씁니다.

**한 줄 요약:** 키는 **그 서식 안에서만** 정합니다. 영어 `누구의.무엇` 꼴로 직접 적고, 한글 키·번호 붙은 키(`name2`)는 남기지 않습니다.
모든 서식이 같이 쓰는 키 사전·공통 키는 없습니다. 다른 서식과 키를 맞출 필요도 없습니다.

---

## 1. 키가 쓰이는 곳

| 어디 | 무엇 |
|---|---|
| 질문 | kie·표·체크 질문의 항목 줄 `- 키: 키 설명` 에 그대로 나갑니다 |
| 정답 JSON | 문항의 `"key"` 가 이 키 그대로입니다 (바꿔 쓰는 규칙 없음). 모델이 이 이름으로 답을 배웁니다 |
| 평가 비교 | 실험끼리 같은 키로 점수를 비교합니다 |

그래서 **데이터셋을 만든 뒤에는 키를 바꾸지 않습니다.** 바꾸면 이전 데이터·평가와 이어지지 않고 서식이 "재검수 필요"로 돌아갑니다.

## 2. 정하는 순서 (영역 편집)

1. 칸을 고르고 오른쪽 **키 설명**에 그림에 인쇄된 이름을 그대로 적습니다 (`성명`, `생년월일`).
2. **키**에 영어 키를 적습니다 (3절). 비워 두면 키 설명이 그대로 키가 되어 **한글 키**가 됩니다 (`성명`).
3. 오른쪽 칸 목록의 **키** 열을 봅니다. 한글 키나 번호 붙은 키(`customer.name2`)가 없어야 합니다.
4. **그림·검수 › 검수**의 자동 검사에 "한글 키", "같은 키를 여러 칸이 씁니다" 경고가 없어야 넘깁니다.

**고객 정보 키를 적으면 값도 따라옵니다.** 생성 방법을 고르지 않은 칸(자동)은 키가 생성기가 아는 고객 정보 키면 그 고객의 값이 들어갑니다.
예: `customer.name`, `customer.birth`, `customer.rrn`, `customer.phone`, `customer.address`, `employer.name`, `company.biz_no`, `account`, `agent.name`.
전체 목록은 `docgen/realform.py` 의 `Values.std` 와 `docgen/forms/_common/key_rules.json` 의 `keys`. 그 밖의 키는 생성 방법을 꼭 고릅니다 ([generators.md](generators.md)).

## 3. 키를 지을 때

**형식:** 영어 소문자 snake_case, 점(`.`)으로 나눔, **`누구의.무엇`** 순서. 예: `customer.name`, `loan.amount`, `car.plate`.

### 누구의 (앞)

| 키 | 뜻 | 예 |
|---|---|---|
| `customer` | 고객 본인 (신청인·예금주·차주) | `customer.name`, `customer.birth` |
| `agent` | 대리인 | `agent.name`, `agent.relation` |
| `related` | 보증인·공동 명의 | `related.name` |
| `family` · `spouse` | 가족 · 배우자 | `family.name`, `spouse.name` |
| `employer` | 고객의 직장 | `employer.name`, `employer.hire_date` |
| `company` | 법인·사업자 (고객이 사업자일 때) | `company.biz_no`, `company.ceo` |
| `foreign` | 외국 거래 상대 | `foreign.name`, `foreign.swift` |
| `issuer` · `bank` | 발급기관 · 은행 쪽 | `issuer.name`, `bank.branch` |

당사자가 아니라 **거래·상품 자체의 값**이면 그 대상 이름을 앞에 둡니다: `loan.amount`, `loan.months`, `deposit.rate`, `car.plate`, `period.start`.
서식 전체에 하나뿐인 값은 앞을 생략해도 됩니다: `account`, `issue_date`, `apply_date`.

### 무엇 (뒤)

한 서식 안에서 같은 뜻은 **늘 같은 이름**을 씁니다. 아래 이름을 먼저 씁니다.

| 뜻 | 이름 | 뜻 | 이름 |
|---|---|---|---|
| 성명 | `name` | 주민등록번호 | `rrn` |
| 생년월일 | `birth` | 성별 | `gender` |
| 주소 | `address` | 연락처 · 휴대전화 | `phone` · `mobile` |
| 이메일 | `email` | 사업자등록번호 | `biz_no` |
| 법인등록번호 | `corp_no` | 대표자 | `ceo` |
| 금액 | `amount` | 금리·이율 | `rate` |
| 기간(개월) | `months` | 시작일 · 종료일 | `start` · `end` (`period.start`) |
| 발급일 · 신청일 · 작성일 | `issue_date` · `apply_date` · `date` | 발급번호 | `issue_no` |
| 은행 · 지점 | `bank` · `branch` | 관계 | `relation` |

### 키 설명 → 키 예

| 그림의 키 설명 | 키 |
|---|---|
| 성명 · 예금주 · 차주 | `customer.name` |
| 생년월일 | `customer.birth` |
| 연락처 · 휴대전화 | `customer.phone` |
| 계좌번호 | `account` |
| 직장명 | `employer.name` |
| 대리인 성명 | `agent.name` |
| 신청일 (년·월·일 칸) | `apply_date` (날짜 칸은 비우면 `date`) |
| 대출 신청금액 · 대출 기간 | `loan.amount` · `loan.months` |
| 차량번호 · 차종 | `car.plate` · `car.model` |
| 조회기간 (시작 ~ 종료) | `period.start` · `period.end` |
| 합계 입금액 · 합계 출금액 | `total.in` · `total.out` |

## 4. 표

표 그리기의 **영문 키**(선택)에 표 키와 열 키를 적습니다. 키는 `<표 키>.<행>.<열 키>` 가 됩니다 (`deals.0.date`).

- **표 키:** 행 하나가 무엇인지 복수형 영어 — `deals`(거래), `items`(품목), `payments`(납입), `members`(구성원).
- **열 키:** 3절 "무엇" 이름 — `date`, `memo`, `in`, `out`, `amount`, `name`.
- 비우면 `<표 묶음>_목록.<행>.<키 설명>` (한글 키) 이 됩니다. 표도 영어 키로 정합니다.
- 칸에 직접 적을 때는 행 번호 자리에 `{i}` 를 씁니다: `deals.{i}.date` (`deals.0.date` 처럼 번호를 직접 쓰지 않음).

## 5. 체크 · 서명 · 결재란 · 날짜 칸

| 칸 | 키를 비우면 | 할 일 |
|---|---|---|
| 체크 보기 | `check.<키 설명>` (한글) | 키에 영어로: 재발급 사유 → `reissue_reason`, 수령 방법 → `delivery_method` |
| 서명·도장 자리 | `seal.signer` · `sign.signer` | 누구의 자리인지 키에 적습니다: `customer` → `seal.customer`·`sign.customer` (대리인 `agent`, 보증인 `related`) |
| 결재란 | `seal.staff.<칸 이름>` · `sign.staff.<칸 이름>` | 그대로 둡니다 (은행 직원 칸) |
| 날짜 칸 (년·월·일) | `date` | 뜻이 있으면 직접: `apply_date`, `issue_date`, `customer.birth` |
| 자유 위치 도장·번호 | 종류의 기본 키: `stamp_received`(접수인)·`stamp_dated`(일부인)·`stamp_certified`·`ref_no`·`receipt_no` | 대개 그대로. 도장은 `seal.<키>`(찍혔는지), 글자를 정답에 켜면 `<키>`(도장 글자) |

## 6. 같은 값이 두 칸에 나올 때 (`name2`)

같은 키가 붙는 칸이 둘이면 뒤 칸 키에 번호가 붙습니다 (`customer.name`, `customer.name2`). 정답에 뜻 없는 키가 남으므로 고칩니다.

- **뒤 칸은 그 자리의 역할로 키를 적습니다:** 아래 서명란의 "신청인 성명" → `applicant.name`, "예금주 확인" → `holder.name`.
  값은 생성 방법(고객 정보 › 고객 이름)이 같으면 같은 사람으로 나옵니다.
- 정말 같은 칸이 두 번 인쇄된 것(쪽마다 반복되는 머리글 등)이면 뒤 칸을 빼도 됩니다.

## 7. 하지 않는 것

- 한글·대문자·공백·하이픈 (`차량번호`, `Car.Plate`, `car-plate`)
- 서식 이름을 키에 넣기 (`passbook_reissue.name` → `customer.name`)
- 한 서식 안에서 같은 뜻을 다른 이름으로 (`birthday`, `birth_date` → `birth`)
- 데이터셋을 만든 뒤 키 바꾸기 (1절)

## 8. 넘기기 전 확인

```bash
python -m docgen.formdir check <서식ID>     # 형식 문제 (값 종류·박스·질문 설정 …) — 한글 키는 검수 탭이 잡음
python -m docgen.formdir card <서식ID>      # 카드 FORM.md: 칸마다 키·키 설명·질문→답 예시
```

studio **검수 탭 › 자동 검사**: "한글 키", "같은 키를 여러 칸이 씁니다" 가 없을 것. **질문·답 › 실제 문항**에서 kie 질문의 키 줄이 뜻이 통하는지 봅니다.
