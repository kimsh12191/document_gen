# 원하는 값이 고르기 창에 없을 때

칸에 넣을 값은 영역 편집 › 칸 › **생성 방법 [고르기…]** 에서 고릅니다. 거기 원하는 것이 없을 때 이 문서를 봅니다.
그림 위에 그린 서식(overlay, [new-forms.md 1절](new-forms.md#1-그림-위에-그려서-만들기))을 기준으로 씁니다.

## 한눈에

| 하고 싶은 것 | 방법 | 코드 |
|---|---|---|
| 몇 개 중 하나 (`이체`·`입금`·`출금`), 정해진 꼴의 번호 (`HN-4821-B`) | **1. 고르기 창에서 적기** — 보기 중 하나 · 틀로 만들기 | 없음 |
| 계산이 들어간 값 하나 (가린 계좌번호, 행마다 `1회`·`2회`, 비율을 정한 보기) | **2. 값 하나를 만드는 함수** — `docgen/forms/_common/generators.py` | 함수 하나 |
| 여러 칸이 서로 맞아야 하는 것 (합계 = 행의 합, 시작일 ≤ 종료일, 잔액) | **3. 칸끼리 관계 맞추기** — 서식 폴더의 `generate.py` | 함수 하나 |

2 와 3 은 이렇게 다릅니다.

- **2 는 칸 하나**만 봅니다. 다른 칸의 값을 모릅니다. 만든 함수는 모든 서식의 고르기 창에 나옵니다.
- **3 은 그 서식 한 장의 값이 칸마다 다 만들어진 뒤** 마지막에 한 번 돌며 서로 안 맞는 값을 고칩니다. 그 서식에만 쓰입니다.

> 파일 이름이 비슷합니다: **`generators.py`** (2, 모든 서식이 같이 씀, 한 개) ≠ **`generate.py`** (3, 서식 폴더마다 하나).

두 코드 모두 데이터를 만들 때마다 실행됩니다. 사내 담당자가 읽고 확인한 뒤 넣습니다 (4절).

---

## 1. 고르기 창에서 적기 (코드 없음)

고르기 창 › **직접 정하기** 묶음:

| 고르는 것 | 적는 것 | 나오는 값 |
|---|---|---|
| 보기 중 하나 | 보기 목록, 한 줄에 하나 | `이체` / `입금` / `출금` 중 하나 |
| 틀로 만들기 | 틀: `#` 숫자, `A` 대문자, `a` 소문자, `{가\|나}` 하나 고르기 | `HN-####-{A\|B}` → `HN-4821-B` |
| 늘 같은 글자 · 늘 빈 칸 | 글자 | |

날짜·금액의 **꼴**만 바꾸고 싶으면(`900210`, `1,234,000원`) 생성 방법이 아니라 칸의 **표기**를 고릅니다.

보기·틀은 **그 칸에만** 저장됩니다 (서식마다 따로). 여러 서식에서 같은 값이 필요하면 2절(함수)로 만듭니다.
(예전에 공통으로 저장해 둔 값 종류는 고르기 창의 **"공통 값 종류"** 묶음에 그대로 나옵니다. 파일은 `docgen/forms/_common/key_rules.json` 의 `kinds`.)

---

## 2. 값 하나를 만드는 함수 (`docgen/forms/_common/generators.py`)

함수 하나 = 고르기 창의 카드 하나입니다.

### 순서

1. `docgen/forms/_common/generators.py` 를 엽니다. 예시 함수 3개가 들어 있습니다.
2. 아래 **빈 틀**을 파일 끝에 붙이고 이름·설명·`return` 만 고칩니다.
3. 저장합니다. studio 를 다시 띄우지 않아도 고르기 창 **"직접 만든 생성기"** 묶음에 예시 값과 함께 나옵니다.
   파일에 오류가 있으면 고르기 창 맨 위에 **몇 번째 줄**인지 나옵니다.
4. 칸에서 그 카드를 고르고 → **저장** → **생성 사례 › 미리보기**를 seed 몇 개로 넘겨 봅니다.

### 빈 틀

```python
@generator("화면에 보일 이름", note="짧은 설명 (예: 12가 3456 꼴)")
def my_value(p, rng, item, row):        # 함수 이름: 영어 소문자·숫자·밑줄, 다른 것과 안 겹치게
    return "글자"                        # 칸에 찍힐 글자. None 이나 "" 이면 빈 칸
```

함수가 받는 넷 중 대개 `rng` 하나만 씁니다.

| 받는 것 | 무엇 | 자주 쓰는 것 |
|---|---|---|
| `rng` | 난수 | `rng.randint(10, 99)`, `rng.choice(["가", "나"])`, `rng.choices(["입금", "출금"], weights=[6, 4])[0]`, `rng.random() < 0.3` |
| `p` | 이 서류의 가짜 고객 (서류 한 건마다 한 명) | `p.person.name`, `p.person.birth` (date), `p.person.rrn`, `p.person.mobile`, `p.employment.company.name`, `p.accounts[0].number`, `p.issue_date` (서류 날짜) |
| `row` | 표의 몇 번째 행인지 (0부터, 표가 아니면 0) | `f"{row + 1}회"` |
| `item` | 이 칸 정보 | `item["label"]` 키 설명 |

고객 정보 전체 경로는 [생성 방법 목록](../docgen/forms/_common/values.md)의 "고객 프로필" 절 (`profile.` 를 뺀 뒤가 `p.` 뒤). 날짜는 `date` 이므로 꼴은 직접: `f"{d:%Y.%m.%d}"`.

### 예

```python
@generator("차량번호", note="12가 3456 · 123가 4567 꼴")
def car_plate(p, rng, item, row):
    han = "가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주"
    front = str(rng.randint(10, 99)) if rng.random() < 0.4 else str(rng.randint(100, 399))
    return f"{front}{rng.choice(han)} {rng.randint(1000, 9999)}"


@generator("계좌번호 (가운데 가림)", note="123-****-5678 꼴, 고객의 첫 계좌")
def account_masked(p, rng, item, row):
    parts = p.accounts[0].number.split("-")
    return "-".join([parts[0], "*" * len(parts[1]), *parts[2:]]) if len(parts) > 2 else p.accounts[0].number


@generator("상환 회차", note="표 행마다 1회, 2회 …")
def repay_round(p, rng, item, row):
    return f"{row + 1}회"


@generator("거래 구분 (비율)", note="입금 60%, 출금 30%, 이체 10%")
def txn_kind(p, rng, item, row):
    return rng.choices(["입금", "출금", "이체"], weights=[6, 3, 1])[0]
```

### 지킬 것

- **난수는 `rng` 만.** `import random`·현재 시각·파일·네트워크를 쓰지 않습니다. 같은 seed 면 같은 값이 나와야 평가 세트를 다시 만들 수 있습니다.
- **고객 본인 값**(이름·주민번호·주소·직장 …)은 지어내지 말고 `p` 에서 꺼냅니다. 그래야 한 서류 안의 다른 칸(같은 고객의 이름·생년월일 …)과 맞습니다.
- 다른 칸 값이 필요하면(합계 등) 이 함수로는 안 됩니다 → 3절.

### 명령으로 확인

```bash
python -c "import random; from docgen import sources as S; from docgen.entities import make_profile; \
print([S.value('rule:car_plate', make_profile(s), random.Random(s)) for s in range(5)])"   # 값 5개
python -m docgen.formdir check <서식ID>                                                    # 그 함수를 쓰는 서식 검사
```

---

## 3. 칸끼리 관계 맞추기 (서식 폴더의 `generate.py`)

### 왜 필요한가

칸마다 값을 **따로** 만들기 때문에, 그대로 두면 이런 서류가 나옵니다.

```text
거래일 2025.11.02  입금 2,230,000
거래일 2025.11.05  입금   450,000
합계 입금        30,150,000        ← 행의 합(2,680,000)이 아님
조회기간 2025.12.01 ~ 2025.10.22   ← 시작일이 종료일보다 뒤, 거래일도 기간 밖
```

`generate.py` 의 `adjust` 는 값이 다 만들어진 뒤 마지막에 한 번 불려서, 이런 것을 맞게 고칩니다 (합계 = 2,680,000, 기간 = 거래일을 감싸게).
이런 관계가 없는 서식은 만들지 않습니다.

### 순서

1. 영역 편집 위 **칸끼리 관계: [견본 만들기]** (= `python -m docgen.formdir adjust <서식ID> --new`)
   → 서식 폴더에 `generate.py` 가 생깁니다. 맨 위 주석에 **이 서식의 칸 키와 예시 값**이 적혀 있어 어떤 키를 고칠 수 있는지 보입니다.
2. `adjust(d, p, rng)` 안을 채웁니다 (아래 예를 고쳐 씀).
3. 영역 편집 **수정 전후 비교**, **미리보기** 여러 seed 로 확인 → `python -m docgen.formdir check <서식ID>`.
   파일을 고치면 서식이 "재검수 필요"로 바뀝니다.

### `d` 는 이 서류의 값 전부

칸 키의 점(`.`)을 따라 중첩한 dict 이고, 표는 행 목록입니다. 값은 **서식에 찍힐 글자 그대로**, 빈 칸은 `None`.

```python
# 칸 키가 period.start, period.end, total.in, deals.0.date, deals.0.in, deals.1.date … 이면
d = {"period": {"start": "2025.12.01", "end": "2025.10.22"},
     "total": {"in": "30,150,000"},
     "deals": [{"date": "2025.11.02", "in": "2,230,000"}, {"date": "2025.11.05", "in": "450,000"}, …]}
```

글자를 숫자·날짜로 바꿔 계산하고 같은 꼴로 되돌리는 도우미가 `docgen/formkit.py` 에 있습니다.

| 도우미 | 하는 일 |
|---|---|
| `rows(d, "deals")` | 표 행 목록 (표 키 = 표 그리기의 영문 표 키) |
| `get(d, "period.start")` · `put(d, "period.start", 값)` | 점 경로로 읽기 · 쓰기 |
| `to_amount("1,234,000원")` → `1234000` · `amount_like(1234000, "1,000원")` → `"1,234,000원"` | 금액 글자 ↔ 숫자 (보기와 같은 꼴로) |
| `to_date("2025.11.02")` → date · `date_like(date, "2025.01.01")` · `add_days(글자, n)` | 날짜 글자 ↔ date |

### 예: 거래내역 확인서

```python
from datetime import timedelta

from docgen.formkit import amount_like, date_like, get, put, rows, to_amount, to_date


def adjust(d, p, rng):
    deals = [r for r in rows(d, "deals") if r.get("date")]          # 채운 행만

    for col in ("in", "out"):                                       # 합계 = 행의 합
        total = sum(to_amount(r.get(col)) or 0 for r in rows(d, "deals"))
        put(d, f"total.{col}", amount_like(total, "1,000"))

    days = sorted(x for x in (to_date(r["date"]) for r in deals) if x)   # 조회기간이 거래일을 감싸게
    if days:
        put(d, "period.start", date_like(days[0] - timedelta(days=rng.randint(0, 15)), get(d, "period.start")))
        put(d, "period.end", date_like(days[-1] + timedelta(days=rng.randint(0, 15)), get(d, "period.end")))
    return d
```

### 할 수 있는 것 · 없는 것

| 됨 | 안 됨 |
|---|---|
| 글자 칸의 값 바꾸기 (단독 칸, 표 칸, 별지로 넘친 행) | 체크 선택, 서명·도장, 결재란, 년·월·일 날짜 칸, 자유 위치 도장·번호 |
| 값 비우기 (`None`) | 표 행 수 바꾸기 (표 칸의 "채우는 행 수"로) |
| | **새 키 만들기** — 칸 목록에 없는 키는 정답에 안 들어갑니다 |

난수는 `rng` 만 (2절과 같은 약속). 바뀐 칸은 글자 크기가 다시 맞춰집니다.
`formdir check` 가 seed 몇 개로 돌려 **오류(몇 번째 줄)·같은 seed 인데 값이 다름·새 키**를 잡습니다 (studio 검수 탭에는 아직 안 나옴).

html 서식의 `generate.py` 도 같은 약속입니다 ([NEW_FORM_SPEC 8절](../docgen/manual/NEW_FORM_SPEC.md)).

---

## 4. 넘길 때

| 무엇 | 넘기는 것 | 볼 사람 |
|---|---|---|
| 1 | 없음 (서식 폴더에 저장됨) | |
| 2 | `docgen/forms/_common/generators.py` 에서 더한 함수 | 사내 담당자 (모든 서식에 영향 — 이름 겹침, 예시 값) |
| 3 | 서식 폴더의 `generate.py` + 확인한 seed 와 결과 | 사내 담당자, 서식은 다시 **검수 완료** |
