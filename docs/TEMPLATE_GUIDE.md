# 서류 템플릿 작성 가이드

서류 한 종을 추가하려면 **생성 함수 1개 + 템플릿 1개**를 만든다.

```
docgen/docs/<그룹>.py                 @doc(...) 로 등록하는 생성 함수
templates/<그룹>/<서류ID>.html.j2      Jinja2 HTML 템플릿
```

예시: `docgen/docs/income.py`의 `employment_certificate`와 `templates/income/employment_certificate.html.j2`

## 1. 생성 함수

```python
from ..registry import doc
from ._common import *  # D, won, K, issue_no, district_office, tax_office, courthouse, rand_date, date, timedelta ...

@doc("employment_certificate", "재직증명서", "income")       # (id, 한글명, 그룹, category="external"|"internal", page="a4"|"a4_landscape"|"card"|"passport", sample_mark=False)
def employment_certificate(p: Profile, rng: random.Random) -> dict:
    """한 줄 설명."""
    return {"employee": {"name": p.person.name, ...}, "items": [{"name": ..., "amount": won(1000)}], ...}
```

- `p: Profile`에는 고객 1명의 일관된 정보가 들어 있다. 자세한 내용은 `docgen/entities.py`를 본다.
  - 본인·가족: `p.person`, `p.spouse`, `p.children`, `p.father`, `p.mother`, `p.address_history`
  - 근무처: `p.employment` (`.company`, `.annual_salary` 등)
  - 사업체: 개인사업체 `p.business`, 법인 `p.corporation`, 임원 `p.directors`, 주주 `p.shareholders`
  - 부동산: `p.property`
  - 금융: `p.accounts`, `p.bank`, `p.bank_branch`
  - 해외 거래처: `p.foreign`
  - 기준일: `p.issue_date`
- **은행 서식(`bank_form` 그룹)은 서식을 낸 은행 기준 프로필을 받는다.** `p.bank`가 외환은행·KEB하나은행 같은 옛 은행이면 `p.issue_date`를 포함한 모든 날짜가 그 시기로 옮겨져 있다(`docgen/banks.py`).
  - 시기에 따라 달라지는 제도(예금자보호한도, 금소법 문구 등)는 `banks.since(p.issue_date, "fsca")`처럼 날짜로 판단한다.
  - 템플릿에는 `bk`(은행명·법인명칭·영문명·`bk.rev()` 개정년월·시기 플래그)가 넘어온다. 표시 전용이며 GT가 아니다. 다른 그룹 템플릿에서는 `bk`가 `None`이다.
- **같은 고객의 다른 서류와 값이 맞아야 한다.** 예를 들어 소득금액증명원의 소득은 `p.employment.annual_salary`를 기준으로 계산한다. 이름, 주소, 주민번호, 회사 정보는 프로필 값을 그대로 쓴다.
- 서류에만 필요한 값(발급번호, 월별 내역, 세부 금액 등)은 `rng`로 만든다. 프로필의 `World.rng`는 쓰지 않는다.
- **반환 dict의 모든 값은 화면에 표시될 문자열**이다. 날짜와 금액은 함수 안에서 포맷한다.
  - 날짜: `D(date, "dot"|"dash"|"kor"|"kor_short"|"slash"|"en"|"en_long")`
  - 금액: `won(n)`는 `1,000원`, `won(n, "")`는 `1,000`, 한글 금액은 `K.won_korean(n)`
  - 서류마다 실제로 쓰는 표기를 따르고, 여러 표기가 쓰이면 `rng.choice`로 다양화한다.
- dict 키는 영어 snake_case를 쓴다. 이 키가 그대로 VLM 학습 정답(JSON)의 키가 된다.
  - 의미가 드러나게 짓는다(`applicant.name`, `loan.amount`).
  - 반복 항목은 리스트로 만든다(`items: [...]`).
- 생성한 값은 모두 템플릿에 표시한다. 표시하지 않은 값이 있으면 `check`가 경고한다.
- 개수가 변하는 리스트(거래내역, 가족 등)는 길이를 랜덤으로 하되 한 페이지 안에 들어가게 제한한다.

## 2. 템플릿

```jinja
{% extends "_base.html.j2" %}
{% import "_macros.html.j2" as m with context %}
{% block style %} /* 이 서류 전용 CSS (선택) */ {% endblock %}
{% block content %}
  {{ m.title("재 직 증 명 서") }}
  {{ m.kv([["성　명", "employee.name"], ["주　소", "employee.address", True]], cols=2, label_w="110px") }}
  {{ m.grid(["항목", "금액"], "items", ["name", "amount"], num_cols=[1]) }}
  {{ f("issue_date", label="발급일") }}
{% endblock %}
```

**규칙: 데이터 값은 반드시 `f("경로", label="한글 라벨")`로 출력한다.** `{{ d.x }}`로 직접 출력하면 정답 데이터에서 빠진다.
- 리스트 항목은 `f("items." ~ i ~ ".name", label="품목")`처럼 출력한다.
- 레이아웃 분기에 값이 필요하면 `val("경로")`나 `d.xxx`를 쓴다.
- 라벨은 문서에 실제로 적힌 항목명으로 쓴다(공백은 자동 제거). 이 라벨은 GT의 `fields[].label`에 저장된다.

주요 매크로 (`templates/_macros.html.j2`):

| 매크로 | 용도 |
|---|---|
| `m.title(text, sub=None, boxed=False)` | 문서 제목 |
| `m.kv(rows, cols=1, label_w=None)` | 라벨/값 표. `[라벨, 경로, True]`는 한 줄 전체를 차지한다 |
| `m.grid(headers, list_path, keys, num_cols=[], widths=None, min_rows=0)` | 목록 표 |
| `m.choice(path, options, label=None)` | ■/□ 선택 항목 (선택된 값만 GT로 기록) |
| `m.agree(path, yes, no)` | 동의/미동의 체크 |
| `m.seal(text, square=False, size="sm"\|"lg", over=False)` | 도장 |
| `m.issuer(date_path, org_path=None, org_text=None, seal_text=None)` | 발급일 + 기관명 + 직인 |
| `m.sign(label, path, mark="(서명 또는 인)")` | 서명란 |
| `m.doc_no(path, label="발급번호")` | 상단 발급번호 |

`_base.html.j2`의 CSS 클래스:
- 배치: `row`, `between`
- 정렬·글자: `right`, `center`, `bold`, `small`, `tiny`, `muted`, `accent`
- 상자·안내문: `box`, `note`
- 간격: `mt`, `mb`, `mt-l`
- 표: `num`, `c`, `table.compact`, `table.outer`, `table.plain`
- 조항 목록: `ol.clauses`
- 사진 자리: `.photo`
- 공문서 상단 줄: `.gov-head`
- 글자가 많은 서류: `{% block page_class %} dense{% endblock %}`로 글자를 줄인다.

`style.*` 변수(폰트, 테두리, 배경색)는 샘플마다 랜덤으로 바뀐다. 색과 폰트는 하드코딩하지 말고 CSS 변수(`var(--accent)`, `var(--border)`, `var(--label-bg)`, `var(--seal)`)를 쓴다. 신분증류처럼 고유 디자인이 필요할 때만 예외로 한다.

## 3. 사실성 가이드
- 실제 서류의 **항목 구성, 순서, 표기 관행**을 최대한 따른다.
  - 예: 정부24·홈택스 발급본의 발급번호와 "이 증명서는 인터넷으로 발급되었으며..." 문구
  - 예: 등기부의 표제부·갑구·을구 구조
- 실제 기관 로고, 바코드, 위변조 방지 패턴, 공식 관인 이미지는 넣지 않는다. 도장은 `m.seal`의 텍스트 도장만 쓴다.
- 신분증, 인감증명서처럼 위조 위험이 큰 서류는 `sample_mark=True`로 등록한다. 그러면 "견본 SAMPLE" 워터마크가 항상 들어간다.
- 페이지는 한 장(A4 794×1123px, 카드 540×340px)에 들어가야 한다. 긴 서류(약정서, 정관 등)는 첫 페이지나 핵심 페이지만 표현한다.

## 4. 검증

```bash
python -m docgen check --types <서류ID,...> --png --tmp /tmp/check   # 예외, 미표시 값, 페이지 넘침 검사
python -m docgen generate --types <서류ID> --n 3 --out /tmp/out --png  # 실제 이미지 확인
```
