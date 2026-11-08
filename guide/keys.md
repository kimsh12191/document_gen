# 키 이름 정하기 (새 서식·외주용)

새 서식에 칸을 그릴 때 칸마다 붙이는 **키**를 정하는 규칙입니다. 그림 위에 그려서 만드는 서식(studio 새 서식 추가 A, [new-forms.md 0절](new-forms.md#0-그림-위에-그려서-만들기-overlay))을 기준으로 씁니다.
키 사전의 구조·전체 목록은 [서식 공통 설명서](../docgen/forms/_common/README.md#키-이름-규칙), 키 사전 파일은 `docgen/forms/_common/dictionary/`.

**한 줄 요약:** 항목명을 먼저 적고 자동으로 붙은 키를 본다 → 같은 고객의 값이면 공통 키(초록 "공통")가 붙었는지 → 아니면 `누구의.무엇` 영어 키를 직접 적는다. 한글 키·번호 붙은 키(`name2`)는 남기지 않는다.

---

## 1. 키가 쓰이는 곳

| 어디 | 무엇 |
|---|---|
| 정답 JSON | kie·표·체크 문항의 `"key"` 가 이 키입니다. 모델이 이 이름으로 답을 배웁니다 |
| 다른 서류와 연결 | **공통 키**(`customer.name` 등)면 같은 고객의 다른 서류의 같은 값과 이어집니다 (서류 대조·구비 확인, 평가 세트 3.0) |
| 평가 비교 | 실험끼리 같은 키로 점수를 비교합니다 |

그래서 **데이터셋을 만든 뒤에는 키를 바꾸지 않습니다.** 바꾸면 이전 데이터·평가와 이어지지 않고 서식이 "재검수 필요"로 돌아갑니다.

## 2. 정하는 순서 (영역 편집)

1. **항목명만 적고 저장합니다.** 그림에 인쇄된 이름 그대로 (`성명`, `생년월일`). 많이 쓰는 항목명은 키가 자동으로 붙습니다.
2. **오른쪽 칸 목록의 키 열을 봅니다.**

   | 보이는 것 | 할 일 |
   |---|---|
   | 초록 **공통** + 영어 키 (`customer.name`) | 끝 |
   | **문서별** + 영어 키 (`account`, `employer.name`) | 3절 규칙에 맞으면 그대로. 같은 고객의 값(이름·생년월일·주소·직장 …)인데 공통이 아니면 → 칸을 누르고 오른쪽 **키** 패널에서 **누구의 · 무엇**을 고릅니다. 공통 키가 있으면 초록으로 바뀝니다 |
   | **한글 키** (`차량번호`, `거래_목록.0.적요`) | 검수 탭 경고 "한글 키". 칸 › **자세히 — 키를 직접 적기**에 영어 키를 적습니다 (3절) |
   | 번호 붙은 키 (`customer.name2`) | 검수 탭 경고 "같은 키를 여러 칸이 씁니다". 6절 |

3. **검수 탭 › 자동 검사**에 "한글 키", "같은 키를 여러 칸이 씁니다" 경고가 없어야 넘깁니다.

`누구의 · 무엇` 선택은 키 사전(`docgen/forms/_common/dictionary/form_keys.json`)에 저장됩니다. 서식 폴더와 함께 넘깁니다.
**새 공통 키를 만드는 것**(키 패널의 공통 키 만들기, studio 키 사전 화면)은 모든 서식에 영향을 주므로 사내 담당자에게 요청합니다.

## 3. 새 키를 지을 때

**형식:** 영어 소문자 snake_case, 점(`.`)으로 나눔, **`누구의.무엇`** 순서. 예: `customer.name`, `loan.amount`, `car.plate`.

### 누구의 (앞)

키 사전의 당사자를 먼저 씁니다 (`docgen/forms/_common/dictionary/parties.json`).

| 키 | 뜻 | 예 |
|---|---|---|
| `customer` | 고객 본인 (신청인·예금주·차주) | `customer.name`, `customer.birth` |
| `agent` | 대리인 | `agent.name`, `agent.relation` |
| `related` | 보증인·공동 명의 | `related.name`, `related.rrn` |
| `family` | 가족 | `family.name` |
| `employer` | 고객의 직장 | `employer.name`, `employer.hire_date` |
| `corp` | 법인·사업자 (고객이 사업자일 때) | `corp.biz_no`, `corp.ceo` |
| `counterparty` | 거래 상대방 | `counterparty.name` |
| `foreign` | 외국 거래 상대 | `foreign.swift` |
| `issuer` · `bank` | 발급기관 · 은행 쪽 | `issuer.name`, `bank.branch` |
| `property` | 담보·물건 | `property.location` |

당사자가 아니라 **거래·상품 자체의 값**이면 그 대상 이름을 앞에 둡니다: `loan.amount`, `loan.months`, `deposit.rate`, `car.plate`, `period.start`.
서식 전체에 하나뿐인 값은 앞을 생략해도 됩니다: `account`, `issue_date`, `apply_date`.

### 무엇 (뒤)

같은 뜻은 **늘 같은 이름**을 씁니다 (키 사전 `attributes.json` 에 있는 것 먼저).

| 뜻 | 이름 | 뜻 | 이름 |
|---|---|---|---|
| 성명 | `name` | 주민등록번호 | `rrn` |
| 생년월일 | `birth` | 성별 | `gender` |
| 주소 | `address` | 연락처 · 휴대전화 | `phone` · `mobile` |
| 이메일 | `email` | 사업자등록번호 | `biz_no` |
| 법인등록번호 | `corp_reg_no` | 대표자 | `ceo` |
| 금액 | `amount` | 금리·이율 | `rate` |
| 기간(개월) | `months` | 시작일 · 종료일 | `start` · `end` (`period.start`) |
| 발급일 · 신청일 · 작성일 | `issue_date` · `apply_date` · `date` | 발급번호 | `issue_no` |
| 은행 · 지점 | `bank` · `branch` | 관계 | `relation` |

### 항목명 → 키 예

| 그림의 항목명 | 키 | |
|---|---|---|
| 성명 · 예금주 · 차주 | `customer.name` | 자동 (공통) |
| 생년월일 | `customer.birth` | 자동 (공통) |
| 연락처 · 휴대전화 | `customer.phone` · `customer.mobile` | 자동 |
| 계좌번호 | `account` | 자동 |
| 직장명 | `employer.name` | 자동 |
| 대리인 성명 | `agent.name` | 자동이 아니면 직접 |
| 신청일 (년·월·일 칸) | `apply_date` | 날짜 칸 › 키 직접 (자동은 `date`) |
| 대출 신청금액 · 대출 기간 | `loan.amount` · `loan.months` | 직접 |
| 차량번호 · 차종 | `car.plate` · `car.model` | 직접 |
| 조회기간 (시작 ~ 종료) | `period.start` · `period.end` | 직접 |
| 합계 입금액 · 합계 출금액 | `total.in` · `total.out` | 직접 |

## 4. 표

표 그리기의 **영문 키**(선택)에 표 키와 열 키를 적습니다. 키는 `<표 키>.<행>.<열 키>` 가 됩니다 (`deals.0.date`).

- **표 키:** 행 하나가 무엇인지 복수형 영어 — `deals`(거래), `items`(품목), `payments`(납입), `members`(구성원).
- **열 키:** 3절 "무엇" 이름 — `date`, `memo`, `in`, `out`, `amount`, `name`.
- 비우면 `<표 묶음>_목록.<행>.<항목명>` (한글 키) 이 됩니다. 표도 영어 키로 정합니다.
- 칸에 직접 적을 때는 행 번호 자리에 `{i}` 를 씁니다: `deals.{i}.date` (`deals.0.date` 처럼 번호를 직접 쓰지 않음).

## 5. 체크 · 서명 · 결재란 · 날짜 칸

| 칸 | 자동 키 | 할 일 |
|---|---|---|
| 체크 보기 | `check.<항목명>` (한글) | **키를 직접 적기**에 영어로: 재발급 사유 → `reissue_reason`, 수령 방법 → `delivery_method` |
| 서명·도장 자리 | `seal.signer` · `sign.signer` | 누구의 자리인지 키에 적습니다: `customer` → `seal.customer`·`sign.customer` (대리인 `agent`, 보증인 `related`) |
| 결재란 | `seal.staff.<칸 이름>` | 그대로 둡니다 (은행 직원 칸) |
| 날짜 칸 (년·월·일) | 항목명 자동 또는 `date` | 뜻이 있으면 직접: `apply_date`, `issue_date`, `customer.birth` |

## 6. 같은 값이 두 칸에 나올 때 (`name2`)

같은 키가 붙는 칸이 둘이면 뒤 칸 키에 번호가 붙습니다 (`customer.name`, `customer.name2`). 정답에 뜻 없는 키가 남으므로 고칩니다.

- **뒤 칸은 그 자리의 역할로 키를 적습니다:** 아래 서명란의 "신청인 성명" → `applicant.name`, "예금주 확인" → `holder.name`.
  값은 생성 방법(고객 정보 › 고객 이름)이 같으면 같은 사람으로 나옵니다.
- 정말 같은 칸이 두 번 인쇄된 것(쪽마다 반복되는 머리글 등)이면 뒤 칸을 빼도 됩니다.

## 7. 하지 않는 것

- 한글·대문자·공백·하이픈 (`차량번호`, `Car.Plate`, `car-plate`)
- 서식 이름을 키에 넣기 (`passbook_reissue.name` → `customer.name`)
- 같은 뜻을 다른 이름으로 (`birthday`, `birth_date` → `birth`)
- 데이터셋을 만든 뒤 키 바꾸기 (1절)
- 공통 키 사전 파일을 직접 고치기 → 사내 담당자에게 요청

## 8. 넘기기 전 확인

```bash
python -m docgen.formdir check <서식ID>     # 형식 문제 (값 종류·박스·질문 설정 …) — 한글 키는 검수 탭이 잡음
python -m docgen.formdir card <서식ID>      # 카드 FORM.md: 칸마다 키·누구의·무엇·질문→답 예시
```

studio **검수 탭 › 자동 검사**: "한글 키", "같은 키를 여러 칸이 씁니다" 가 없을 것. **질문·답 › 실제 문항**에서 kie 질문의 키 줄이 뜻이 통하는지 봅니다.
