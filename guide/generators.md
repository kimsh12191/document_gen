# 값 만드는 코드 짜기 (생성기 · 칸끼리 관계)

칸에 넣을 값을 만드는 규칙이 화면에서 고를 수 있는 것으로 안 될 때 코드를 짜는 법입니다. 그림 위에 그린 서식(overlay, [new-forms.md 0절](new-forms.md#0-그림-위에-그려서-만들기-overlay))을 기준으로 씁니다.
html 서식의 `generate.py` 는 [NEW_FORM_SPEC 8절](../docgen/manual/NEW_FORM_SPEC.md) 이 같은 약속입니다.

## 0. 먼저: 코드 없이 되는지

| 하고 싶은 것 | 코드 없이 | 어디서 |
|---|---|---|
| 있는 종류의 값 (날짜·금액·계좌·회사명·고객 정보 …) | 생성 방법 **고르기** | 영역 편집 › 칸 › 값 만들기 › 생성 방법 [고르기…] |
| 몇 개 중 하나 (이체·입금·출금) | **보기 중 하나** | 같은 곳 |
| 정해진 꼴의 번호 (`HN-####-{A\|B}`) | **틀로 만들기** (`#` 숫자, `A` 대문자, `a` 소문자, `{가\|나}` 하나) | 같은 곳 |
| 위 둘을 다른 서식에서도 | **[값 종류로 저장]** → 키 사전의 값 종류 | 칸 패널, studio 키 사전 › 값 종류 |
| 날짜·금액의 꼴 (`900210`, `1,234,000원`) | **표기** | 칸 패널 › 표기 |
| 표의 날짜가 행마다 늘어남 | **행마다 늘어나는 날짜** | 생성 방법 |

이걸로 안 될 때만 아래 둘 중 하나를 짭니다.

| 무엇 | 파일 | 언제 |
|---|---|---|
| **생성기** — 칸 하나의 값 | `docgen/forms/_common/generators.py` (모든 서식이 같이 씀) | 보기·틀로 안 되는 값 (계산이 들어간 번호, 고객 정보를 섞은 글자 …) |
| **칸끼리 관계** — 여러 칸을 서로 맞춤 | 서식 폴더의 `generate.py` 의 `adjust` (그 서식만) | 합계 = 행의 합, 시작일 ≤ 종료일, 잔액, 조건에 따라 비우기 |

두 파일 모두 **데이터를 만들 때마다 실행되는 코드**입니다. 사내 담당자가 읽고 확인한 뒤 넣습니다.

---

## 1. 생성기 (`docgen/forms/_common/generators.py`)

함수 하나 = 생성 방법 하나. 파일을 저장하면 studio 를 다시 띄우지 않아도 생성 방법 고르기 창의 **"직접 만든 생성기"** 에 예시 값과 함께 나옵니다. 칸의 생성 방법은 `rule:<함수 이름>` 이 됩니다.

```python
from docgen.usergen import generator


@generator("차량번호", note="12가 3456 · 123가 4567 꼴")      # 화면에 보일 이름, 짧은 설명
def car_plate(p, rng, item, row):                           # 함수 이름 = 영어 소문자·숫자·밑줄
    han = "가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주"
    front = str(rng.randint(10, 99)) if rng.random() < 0.4 else str(rng.randint(100, 399))
    return f"{front}{rng.choice(han)} {rng.randint(1000, 9999)}"   # 글자를 돌려줌. None·"" 이면 빈 칸
```

### 함수가 받는 것

| 인자 | 무엇 | 예 |
|---|---|---|
| `p` | 이 서류의 고객 (한 묶음의 서류가 같은 고객) | `p.person.name` `'박찬연'`, `p.person.birth` (date), `p.person.rrn`, `p.person.mobile`, `p.person.address.road_short`, `p.employment.company.name`, `p.employment.annual_salary` (int), `p.employment.hire_date` (date), `p.issue_date` (서류 날짜, date), `p.bank`, `p.bank_branch`, `p.accounts[0].number` |
| `rng` | 이 서류·이 칸의 난수 (`random.Random`) | `rng.random()`, `rng.randint(a, b)`, `rng.choice(목록)`, `rng.choices(목록, weights=…)` |
| `item` | 칸 정보 | `item["label"]` 항목명, `item.get("choices")` 보기, `item.get("text")`, `item.get("pattern")` |
| `row` | 표 행 번호 (0부터, 표가 아니면 0) | 행마다 늘어나는 번호: `f"{1000 + row}"` |

고객 정보 전체 목록(경로와 예시 값)은 [값 출처 목록](../docgen/forms/_common/values.md)의 "고객 프로필" 절 (`profile.` 를 뺀 경로가 `p.` 뒤). 날짜는 `date` 이므로 꼴은 직접: `f"{d:%Y.%m.%d}"`.

### 약속

- **난수는 `rng` 만** 씁니다. `random`·시간·파일·네트워크를 읽지 않습니다 (같은 seed → 같은 값이어야 평가 세트가 다시 만들어집니다).
- 고객 본인 값(이름·주민번호·주소 …)은 지어내지 말고 `p` 에서 씁니다 (다른 서류와 맞아야 서류 대조 과제가 됩니다).
- 함수 이름이 이미 있는 값 종류(`date`, `amount`, 키 사전 값 종류 …)와 겹치면 안 됩니다. 오류가 나면 고르기 창 맨 위에 **몇 번째 줄**인지 나옵니다.

### 더 많은 예

```python
@generator("계좌번호 (가운데 가림)", note="123-****-5678 꼴, 고객의 첫 계좌")
def account_masked(p, rng, item, row):
    n = p.accounts[0].number
    parts = n.split("-")
    return "-".join([parts[0], "*" * len(parts[1]), *parts[2:]]) if len(parts) > 2 else n


@generator("상환 회차", note="표 행마다 1회, 2회 …")
def repay_round(p, rng, item, row):
    return f"{row + 1}회"


@generator("거래 구분 (가중치)", note="입금 60%, 출금 30%, 이체 10%")
def txn_kind(p, rng, item, row):
    return rng.choices(["입금", "출금", "이체"], weights=[6, 3, 1])[0]
```

### 확인

```bash
python -c "import random; from docgen import sources as S; from docgen.entities import make_profile; \
print([S.value('rule:car_plate', make_profile(s), random.Random(s)) for s in range(5)])"   # 값 몇 개
python -m docgen.formdir check <서식ID>                                                    # 그 생성기를 쓰는 서식 검사
```

studio: 생성 방법 고르기 창 › "직접 만든 생성기" 의 예시 값 → 칸에 고르고 **그림·검수 › 미리보기** (seed 여러 개).

---

## 2. 칸끼리 관계 (서식 폴더 `generate.py` 의 `adjust`)

값 하나하나는 생성 방법이 만들고, `adjust` 가 그 값을 받아 서로 맞게 고칩니다.

1. 영역 편집 위 **칸끼리 관계: [견본 만들기]** (= `python -m docgen.formdir adjust <ID> --new`) → 서식 폴더에 `generate.py` 가 생깁니다.
   맨 위 주석에 **이 서식의 칸 키와 seed 0 의 값**이 적혀 있습니다 (어떤 키를 고칠 수 있는지).
2. `adjust(d, p, rng)` 를 고칩니다.
3. 영역 편집 **수정 전후 비교**, **미리보기** 여러 seed 로 확인 → 사내 담당자 검토 → 서식 **재검수** (파일을 고치면 "재검수 필요" 로 바뀝니다).

### `d` 의 꼴

칸 키(점 경로)를 중첩한 dict. **값은 서식에 찍힐 글자** (`"2025.01.03"`, `"1,234,000원"`, 빈 칸은 `None`).

```python
# 칸 키 customer.name, period.start, period.end, total.in, deals.0.date, deals.0.in, deals.1.date … 이면
d = {"customer": {"name": "박찬연"}, "period": {"start": "2025.10.22", "end": "2025.11.18"},
     "total": {"in": "30,150,000"},
     "deals": [{"date": "2025.11.02", "in": "2,230,000", "out": None}, …]}   # 표 = 행 목록 (안 채운 행은 값이 None)
```

- 표는 `rows(d, "deals")` 로 행 목록 (표 키 = 표 그리기의 영문 표 키, 없으면 `<표 묶음>_목록`).
- 다른 키와 부딪히는 키(`date` 와 `date.x` 가 같이 있음)는 점 경로 그대로 맨 위에 (`d["date.x"]`).

### 고칠 수 있는 것 · 없는 것

| 고칠 수 있음 | 고칠 수 없음 (스크립트가 못 봄) |
|---|---|
| 글자 칸의 값 (단독 칸, 표 칸, 별지로 넘친 표 행) | 체크박스 선택, 서명·도장, 결재란 |
| 값을 비우기 (`None`) | 년·월·일 날짜 칸, 둘로 나뉜 이메일 칸 |
| | 자유 위치 도장·번호 |
| | 표 행 수 (채우는 행 수는 표 칸의 "채우는 행 수") |
| | **새 키** — 칸 목록에 없는 키를 만들면 정답에 안 들어갑니다 |

바뀐 칸은 글자 크기를 다시 맞춥니다. 난수는 `rng` 만 (생성기와 같은 약속, 다른 칸 값과 따로 뽑힘).

### 도우미 `docgen.formkit`

| 함수 | 하는 일 |
|---|---|
| `to_date(s)` / `date_like(date, 보기)` | 날짜 글자 → `date` / `date` → 보기와 같은 꼴의 글자 |
| `add_days(s, n)` | 날짜 글자에 n 일 더해 같은 꼴로 |
| `to_amount(s)` / `amount_like(n, 보기)` | `'1,234,000원'` → `1234000` / 정수 → 보기와 같은 꼴 (쉼표·원 유지) |
| `won_korean(n)` | `120000000` → `'일억이천만'` |
| `rows(d, "표 키")` · `get(d, "a.b")` · `put(d, "a.b", 값)` | 표 행 목록 · 점 경로로 읽기 · 쓰기 |
| `fmt(값, "date.yymmdd")` | 표기와 같은 꼴 바꾸기 (`docgen/formkit.py` 의 `FORMATS`) |

### 예: 거래내역 확인서

```python
from datetime import timedelta

from docgen.formkit import amount_like, date_like, get, put, rows, to_amount, to_date


def adjust(d, p, rng):
    deals = [r for r in rows(d, "deals") if r.get("date")]   # 채운 행만

    for r in deals:                                          # 한 행에는 입금·출금 중 하나만
        if rng.random() < 0.6:
            r["in"] = None
        else:
            r["out"] = None

    days = sorted(x for x in (to_date(r["date"]) for r in deals) if x)   # 조회기간 = 거래일 범위
    if days:
        put(d, "period.start", date_like(days[0] - timedelta(days=rng.randint(0, 15)), get(d, "period.start")))
        put(d, "period.end", date_like(days[-1] + timedelta(days=rng.randint(0, 15)), get(d, "period.end")))

    for col in ("in", "out"):                                # 합계 = 행의 합 (별지로 넘친 행 포함)
        put(d, f"total.{col}", amount_like(sum(to_amount(r.get(col)) or 0 for r in rows(d, "deals")), "1,000"))
    return d
```

### 확인

```bash
python -m docgen.formdir check <서식ID>          # 오류가 나면 "generate.py N번째 줄: …"
python - <<'EOF'                                  # 같은 seed 로 두 번 → 같은 값인지, 관계가 지켜지는지
import random
from docgen import realform as RF
from docgen.entities import make_profile
for s in range(5):
    a = RF.build_form("<서식ID>", make_profile(s), random.Random(s))
    b = RF.build_form("<서식ID>", make_profile(s), random.Random(s))
    assert a["items"] == b["items"]
    v = {i["key"]: i["value"] for i in a["items"] if i.get("key")}
    print(v.get("total.in"), [v.get(f"deals.{i}.in") for i in range(5)])
EOF
```

`formdir check` 가 그린 서식의 `generate.py` 를 seed 몇 개로 돌려 **오류(몇 번째 줄)·같은 seed 두 번 다름·새 키**를 문제로 보입니다.
studio 검수 탭의 자동 검사에는 아직 나오지 않으니 명령으로 확인합니다.

---

## 3. 넘길 때

- 생성기: `docgen/forms/_common/generators.py` 의 바뀐 함수 (모든 서식에 영향 — 이름이 겹치지 않는지, 고르기 창 예시 값).
- 칸끼리 관계: 서식 폴더의 `generate.py` + 확인한 seed 와 결과.
- 둘 다 사내 담당자가 코드를 읽고, 서식은 다시 **검수 완료**.
