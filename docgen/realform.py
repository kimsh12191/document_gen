"""원본 서식 오버레이 — 하나은행 공개 서식 PDF 를 그대로 배경으로 깔고, 손님이 쓴 것처럼 값을 얹는다.

서식 모양을 HTML 로 다시 그리지 않으므로 이미지 속 서식은 원본과 똑같다. 값을 쓸 자리는
docgen/scripts/extract_form_layout.py 가 PDF 에서 뽑은 docgen/forms/layouts/<분류>/<No>.json 을 쓴다.

  text   빈 칸에 글자          → f(키)  값은 프로필(성명·주소·계좌…)이나 항목명으로 만든다
  check  □ 보기 묶음           → 고른 보기 □ 위에 손 V·■·○ (또는 풀 이미지) 표시, 정답은 고른 보기 글자
  date   "  년  월  일" 빈칸    → 숫자만 채우고 정답은 "2026년 1월 31일"
  sign   "(서명 또는 인)" 자리  → 이름 + 도장/서명/빈칸
  copy   자필 기재란            → 회색 안내 문구를 손글씨로 따라 쓴다
  staff  결재란 (담당·책임자 …)  → 은행이 접수·처리한 서류처럼 직원 이름 도장·확인 도장·서명 (일부는 빈칸)

글씨체는 서류마다 손글씨(기본 풀: 나눔손글씨 펜·붓, 하이멜로디, 감자꽃 — docgen/fonts/) 또는 인쇄체(전산 입력)에서
고른다. 비율과 글꼴·체크 모양 목록은 docgen/marks.py 가 정한다.
배경 이미지와 손글씨 글꼴은 렌더러(image.py)가 https://docgen.local/ 주소로 넘겨준다.

등록: docgen/docs/real_forms.py 가 register_all() 을 불러 hf<No>(그룹 hana) 로 등록한다. studio 가져오기에서 만든
이미지 배경 서식(img_*, 그룹 imported)도 같은 코드로 그린다 (register_images, layout.json 은 그 서식 폴더).
"""
from __future__ import annotations

import json
import random
import re
import unicodedata
from datetime import timedelta
from functools import lru_cache
from pathlib import Path

from . import keyrules as KR
from . import korean as K
from . import marks as M
from . import overrides as OV
from . import sources as SRC
from .entities import Profile

ROOT = Path(__file__).resolve().parent   # docgen/ (레이아웃의 "file" 은 이 폴더 기준: forms/하나은행_서식자료/…)
LAYOUTS = ROOT / "forms" / "layouts"
IMAGE_FORMS = ROOT / "forms" / "images"   # overlay(image): 스캔·사진 배경 서식 <ID>/layout.json + page_<쪽>.png
FONTS = ROOT / "fonts"
CACHE = Path.home() / ".cache" / "docgen" / "bg"
HOST = "https://docgen.local/"
PX = 96 / 72          # PDF pt → CSS px
BG_ZOOM = 2 * PX      # 배경 해상도 = 렌더러 device_scale_factor(2) 에 맞춘다
BANK = "하나은행"
# 손글씨 비율, 결재란 비율, 체크 모양·글꼴 목록은 docgen/marks.py (marks.json·풀) 에서 읽는다.
# 손글씨 글꼴마다 글자 몸집이 달라 같은 칸 높이에서 키우는 비율도 풀의 scale 이다.
HAND_FONTS = [f["id"] for f in M.DEFAULT_POOLS["hand_fonts"]]   # 템플릿이 @font-face 를 거는 기본 글꼴
INKS = ["#1b2a80", "#1a1a1a", "#222c55", "#0d3a8a", "#2b2b2b", "#183c9c"]
D = K.fmt_date


# ---------------------------------------------------------------------------
# 배경·글꼴 제공 (렌더러가 부른다)
# ---------------------------------------------------------------------------

def layout_path(no: int) -> Path | None:
    hits = list(LAYOUTS.glob(f"*/{no:03d}.json"))
    return hits[0] if hits else None


@lru_cache(maxsize=None)
def load_layout(no: int) -> dict:
    """자동 추출 레이아웃 그대로 (사람 수정 전)."""
    return json.loads(layout_path(no).read_text(encoding="utf-8"))


def form_no(doc_id: str) -> int | None:
    return int(doc_id[2:]) if re.fullmatch(r"hf\d{3}", doc_id) else None


def image_form_dir(doc_id: str) -> Path | None:
    """overlay(image) 서식 폴더: 저장소의 docgen/forms/images/<ID>/ 또는 private_forms_dir/<ID>/."""
    for root in [IMAGE_FORMS, *_private_roots()]:
        d = root / doc_id
        if (d / "layout.json").exists():
            return d
    return None


def _private_roots() -> list[Path]:
    import os

    p = os.environ.get("DOCGEN_PRIVATE_FORMS")
    return [Path(p)] if p else []


def raw_layout(doc_id: str) -> dict:
    """사람 수정 전 레이아웃 (pdf 서식은 자동 추출, image 서식은 그 폴더의 layout.json)."""
    no = form_no(doc_id)
    if no is not None:
        return load_layout(no)
    d = image_form_dir(doc_id)
    if d is None:
        raise KeyError(doc_id)
    return json.loads((d / "layout.json").read_text(encoding="utf-8"))


def form_layout(doc_id: str) -> tuple[dict, list[dict]]:
    """사람 수정(docgen/forms/overrides/<ID>.json)을 덧씌운 레이아웃과 못 찾은 수정 목록."""
    return OV.apply(raw_layout(doc_id), OV.load(doc_id))


def _pdf_page_png(no: int, page: int) -> bytes:
    """서식 PDF 의 한 쪽을 PNG 로 (캐시)."""
    out = CACHE / f"{no:03d}_{page}.png"
    if not out.exists():
        import pymupdf

        lay = load_layout(no)
        out.parent.mkdir(parents=True, exist_ok=True)
        with pymupdf.open(ROOT / lay["file"]) as doc:
            pix = doc[page].get_pixmap(matrix=pymupdf.Matrix(BG_ZOOM, BG_ZOOM), alpha=False)
            tmp = out.with_suffix(".tmp")
            pix.save(str(tmp), output="png")
            tmp.replace(out)
    return out.read_bytes()


def raw_background(doc_id: str, page: int) -> bytes:
    """지우기 전 배경 PNG (렌더러 배율 2 기준 해상도)."""
    no = form_no(doc_id)
    if no is not None:
        return _pdf_page_png(no, page)
    d = image_form_dir(doc_id)
    if d is None:
        raise KeyError(doc_id)
    return (d / f"page_{page}.png").read_bytes()


def background_png(doc_id: str | int, page: int) -> bytes:
    """배경 PNG. 사람 수정의 배경 지우기(erase)를 적용한다."""
    if isinstance(doc_id, int):
        doc_id = f"hf{doc_id:03d}"
    data = raw_background(doc_id, page)
    erases = OV.erase_for(OV.load(doc_id), page)
    if not erases:
        return data
    import io

    from PIL import Image

    img = OV.apply_erase(Image.open(io.BytesIO(data)), erases, BG_ZOOM)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def serve(url: str) -> tuple[bytes, str] | None:
    """https://docgen.local/bg/169/0.png, https://docgen.local/bgi/<ID>/0.png, https://docgen.local/fonts/NanumPen.woff2,
    https://docgen.local/marks/<풀 이미지> → (내용, MIME)."""
    if not url.startswith(HOST):
        return None
    path = url[len(HOST):].split("?")[0]
    if m := re.fullmatch(r"bg/(\d+)/(\d+)\.png", path):
        return background_png(int(m.group(1)), int(m.group(2))), "image/png"
    if m := re.fullmatch(r"bgi/([\w.-]+)/(\d+)\.png", path):
        return background_png(m.group(1), int(m.group(2))), "image/png"
    if m := re.fullmatch(r"fonts/([A-Za-z]+)\.woff2", path):
        f = FONTS / f"{m.group(1)}.woff2"
        if f.exists():
            return f.read_bytes(), "font/woff2"
    if path.startswith("marks/"):
        data = M.image(path[len("marks/"):])
        if data is not None:
            return data, "image/svg+xml" if path.endswith(".svg") else "image/png"
    return None


# ---------------------------------------------------------------------------
# 항목명 → 키·값
# ---------------------------------------------------------------------------

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    s = re.sub(r"\([^)]*\)|\[[^\]]*\]", "", s)   # 괄호 설명 빼기: 매수비율(%) → 매수비율
    return re.sub(r"[\s:：*※·.,]+", "", s)


# 항목명(norm) 정규식 → 표준 키, 항목명 → 값 종류: docgen/key_rules.json (studio 키 사전 화면이 고친다, docgen/keyrules.py).
# 위에서부터 처음 맞는 것. 아래 두 이름은 지금 파일 내용 (build_keys.py·studio editor 가 읽는다).
KEY_RULES: list[tuple[str, str]] = [tuple(x) for x in KR.load()["label_rules"]]

# 표준 키가 아닌 항목: 항목명 끝말로 값의 종류를 정한다
KIND_RULES: list[tuple[str, str]] = [tuple(x) for x in KR.load()["kind_rules"]]
_RX: dict = {}


def _compiled(name: str) -> list:
    """key_rules.json 의 규칙을 정규식으로 (파일이 바뀌면 다시)."""
    d = KR.load()
    if _RX.get(name, (None,))[0] is not d:
        _RX[name] = (d, [(re.compile(rx), k) for rx, k in d[name]])
    return _RX[name][1]

PRODUCTS = {
    "퇴직연금": ["정기예금 (1년)", "정기예금 (3년)", "이율보증형 보험(GIC) 1년", "하나 IRP 정기예금 3년",
              "하나 TDF 2045 증권투자신탁", "인덱스(KOSPI200) 증권자투자신탁", "국내채권형 증권자투자신탁",
              "미국S&P500 인덱스 증권투자신탁", "MMF 증권투자신탁", "하나 단기채 증권투자신탁", "원리금보장 ELB 1년"],
    "예금": ["하나 정기예금", "주거래하나 통장", "하나 적금", "급여하나 통장", "하나의정기예금", "청년도약계좌"],
    "신탁": ["특정금전신탁(정기예금형)", "ISA 중개형", "하나 지수연동 신탁", "MMT"],
    "기본": ["하나 정기예금", "하나 적금", "하나 TDF 2040", "하나 MMF", "하나 단기채 펀드"],
}
REASONS = ["생활자금", "주택구입", "사업자금", "학자금", "의료비", "만기 해지", "해외 이주", "타행 이체", "급여 수령",
           "본인 요청", "계좌 정리", "결혼자금", "전세자금", "투자 목적", "자녀 교육비"]
COUNTRIES = ["미국", "일본", "중국", "베트남", "독일", "싱가포르", "캐나다", "호주", "영국", "필리핀"]
CURRENCIES = ["USD", "USD", "USD", "EUR", "JPY", "CNY", "GBP", "CAD", "AUD"]
BANKS = ["하나은행", "국민은행", "신한은행", "우리은행", "농협은행", "기업은행", "카카오뱅크"]


# 대리인 구역 (그 안의 성명·생년월일 … 은 대리인 값). '위임인'(본인) 구역은 아니다.
AGENT_SEC = re.compile(r"대리|수임|위임장|위임받|피위임")
FOREIGN_SEC = re.compile(r"받는|받으실|수취|Beneficiary|BENEFICIARY|상대방")


GOODS = ["전자부품", "반도체 소자", "자동차 부품", "의류 원단", "냉동 수산물", "화장품", "산업용 펌프", "LED 모듈",
         "플라스틱 원료", "커피 원두", "PCB 기판", "포장재", "식품 원재료", "기계 부품", "철강 코일"]
_CO_A = ["한빛", "대성", "미래", "세진", "동방", "새한", "청솔", "우진", "다온", "누리", "가온", "신영", "제일", "삼정", "유니온"]
_CO_B = ["전자", "산업", "무역", "상사", "테크", "물산", "정밀", "화학", "로지스", "시스템즈", "푸드", "메디칼"]


def _company(r: random.Random) -> str:
    name = r.choice(_CO_A) + r.choice(_CO_B)
    return r.choice([f"(주){name}", f"주식회사 {name}", f"{name}(주)", name])


def key_of(label: str) -> str | None:
    n = norm(label)
    for rx, key in _compiled("label_rules"):
        if rx.match(n):
            return key
    return next((k for lab, k in KR.label_index().items() if norm(lab).lower() == n.lower()), None)


def kind_of(label: str, unit: str | None, hint: str | None) -> str:
    if unit in ("원", "천원", "백만원", "만원", "억원", "원정"):
        return "amount"
    if unit == "%":
        return "percent"
    if unit in ("개월", "년", "회", "건", "명", "주", "개", "매", "좌", "세", "일간", "개년"):
        return "count"
    n = norm(label)
    for rx, k in _compiled("kind_rules"):
        if rx.search(n):
            return k
    return "text"


def _acct(r: random.Random) -> str:
    return "".join(str(r.randint(0, 9)) if c == "#" else c for c in "###-######-#####")


class Values:
    """한 서류 안에서 값을 만든다. 같은 표준 키는 같은 값 (표에 두 번 나와도 일치)."""

    def __init__(self, p: Profile, r: random.Random, cls: str):
        self.p, self.r, self.cls = p, r, cls
        self.cache: dict[str, str] = {}
        self.home_phone = K.landline(r, p.person.address.sido)
        self.acct = p.accounts[0].number if p.accounts and p.accounts[0].bank == BANK else _acct(r)

    def std(self, key: str) -> str | None:
        p, r = self.p, self.r
        if key in self.cache:
            return self.cache[key]
        e = p.employment
        v = {
            "spouse.name": lambda: p.spouse.name if p.spouse else None,
            "spouse.rrn": lambda: p.spouse.rrn[:6] if p.spouse else None,
            "customer.name": lambda: p.person.name,
            "customer.name_en": lambda: p.person.name_en.upper(),
            "customer.birth": lambda: D(p.person.birth, r.choice(["dot", "dot", "kor_short", "dash"]))
            if r.random() < 0.8 else p.person.birth.strftime("%y%m%d"),
            "customer.rrn": lambda: K.mask_rrn(p.person.rrn) if r.random() < 0.4 else p.person.rrn,
            "customer.phone": lambda: p.person.mobile,
            "customer.home_phone": lambda: self.home_phone,
            "customer.email": lambda: p.person.email,
            "customer.address": lambda: p.person.address.road_short,
            "customer.job": lambda: e.job,
            "customer.nationality": lambda: p.person.nationality,
            "customer.zipcode": lambda: p.person.address.zipcode,
            "employer.address": lambda: f"{e.company.address.road_short} {e.company.name} {e.department}",
            "employer.phone": lambda: e.company.phone,
            "employer.name": lambda: e.company.name,
            "employer.department": lambda: e.department,
            "employer.position": lambda: e.position,
            "employer.hire_date": lambda: D(e.hire_date, "dot"),
            "company.name": lambda: p.corporation.name,
            "company.biz_no": lambda: p.corporation.biz_no,
            "company.corp_no": lambda: p.corporation.corp_no or K.corp_reg_no(r),
            "company.ceo": lambda: p.corporation.ceo.name,
            "company.address": lambda: p.corporation.address.road_short,
            "company.biz_type": lambda: p.corporation.biz_type,
            "company.biz_item": lambda: p.corporation.biz_item,
            "company.established": lambda: D(p.corporation.established, "dot"),
            "account": lambda: self.acct,
            "foreign.name": lambda: p.foreign.name,
            "foreign.address": lambda: p.foreign.address,
            "foreign.account": lambda: p.foreign.account,
            "foreign.phone": lambda: p.foreign.contact,
            "foreign.email": lambda: p.foreign.email,
            "foreign.nationality": lambda: p.foreign.country,
            "foreign.name_en": lambda: p.foreign.name,
            "agent.name": lambda: (p.spouse or p.father).name,
            "agent.birth": lambda: D((p.spouse or p.father).birth, r.choice(["dot", "kor_short"])),
            "agent.rrn": lambda: K.mask_rrn((p.spouse or p.father).rrn),
            "agent.phone": lambda: (p.spouse or p.father).mobile,
            "agent.address": lambda: p.person.address.road_short,
            "agent.email": lambda: (p.spouse or p.father).email,
            "agent.name_en": lambda: (p.spouse or p.father).name_en.upper(),
            "agent.home_phone": lambda: self.home_phone,
            "agent.relation": lambda: "배우자" if p.spouse else "부",
            "date": lambda: D(p.issue_date, r.choice(["kor", "dot"])),
        }.get(key)
        if v is None:   # 키 사전(key_rules.json)에서 더한 표준 키: 값 출처(프로필 경로) 또는 값 종류
            k = KR.load()["keys"].get(key)
            if not k or not (k.get("source") or k.get("kind")):
                return None
            v = (lambda: KR.resolve_source(p, k["source"])) if k.get("source") else (lambda: self.by_kind(k["kind"], key))
        self.cache[key] = v()
        return self.cache[key]

    def by_kind(self, kind: str, label: str) -> str | None:
        p, r = self.p, self.r
        if kind in ("skip", "seal"):
            return None
        if kind == "note":
            return (r.choice(REASONS) if r.random() < 0.15 else None) if p.extra.get("sparse_fields") else "해당 없음"
        if kind == "date":
            back = r.randint(0, 400) if not re.search(r"만기|기한|기일|종료|유효", label) else -r.randint(30, 1500)
            return D(p.issue_date - timedelta(days=back), r.choice(["dot", "dot", "kor_short", "dash"]))
        if kind == "biz_no":
            return p.corporation.biz_no if r.random() < 0.5 else K.biz_no(r)
        if kind == "passport":
            return f"M{r.randint(10000000, 99999999)}"
        if kind == "check_no":
            return f"{r.choice('가나다라마바사아자차')}{r.choice('가나다라마바')}{r.randint(10000000, 99999999)}"
        if kind == "goods":
            return r.choice(GOODS)
        if kind == "check_kind":
            return r.choice(["자기앞수표", "당좌수표", "가계수표", "약속어음"])
        if kind == "loan_subject":
            return r.choice(["일반자금대출", "운전자금대출", "시설자금대출", "가계일반자금대출", "주택담보대출", "무역금융"])
        if kind == "repay":
            return r.choice(["만기일시상환", "원리금균등분할상환", "원금균등분할상환", "혼합상환"])
        if kind == "branch":
            return p.bank_branch if p.bank_branch.endswith(("점", "지점")) else f"{p.bank_branch}점"
        if kind == "company":
            return p.corporation.name if r.random() < 0.3 else _company(r)
        if kind == "person":
            return K.make_name(r, r.choice("MF"))[0] if r.random() < 0.6 else p.person.name
        if kind == "amount":
            hi = r.choice([1e6, 1e7, 1e7, 5e7, 1e8, 3e8])
            n = K.round_to(r.uniform(hi / 20, hi), 10_000)
            return f"{n:,}" if r.random() < 0.8 else K.won(n)
        if kind == "fx_amount":
            return f"{r.choice(CURRENCIES)} {K.round_to(r.uniform(1e3, 2e5), 100):,}"
        if kind == "percent":
            if re.search(r"이율|금리|요율", label):
                return f"{r.uniform(2.5, 7.5):.2f}"
            return f"{r.choice([10, 20, 30, 40, 50, 60, 70, 100])}"
        if kind == "rate":
            return f"{r.uniform(1250, 1480):,.2f}"
        if kind == "currency":
            return r.choice(CURRENCIES)
        if kind == "account":
            return _acct(r)
        if kind == "number" and re.search(r"코드", label):
            return "".join(str(r.randint(0, 9)) for _ in range(r.choice([4, 5, 6])))
        if kind == "number":
            return "-".join("".join(str(r.randint(0, 9)) for _ in range(n)) for n in r.choice([[4, 4], [3, 6, 5], [6, 7]]))
        if kind == "count":
            if re.search(r"방수", label):
                return str(r.randint(1, 4))
            return str(r.choice([1, 2, 3, 6, 12, 24, 36, 60]))
        if kind == "product":
            pool = PRODUCTS.get(self.cls) or PRODUCTS["기본"]
            return r.choice(pool)
        if kind == "reason":
            return r.choice(REASONS) if not p.extra.get("sparse_fields") or r.random() < 0.7 else None
        if kind == "bank":
            return r.choice(BANKS)
        if kind == "country":
            return r.choice(COUNTRIES)
        if kind == "address":
            return p.person.address.road_short
        if kind == "email":
            return p.person.email
        if kind == "phone":
            return p.person.mobile if not re.search(r"팩스|FAX|직장|회사", label) else p.employment.company.phone
        return KR.make_value(kind, p, r)  # 키 사전에서 더한 종류. 그 밖의 뜻을 모르는 칸은 비워 둔다 (실제 서식도 빈 칸이 많다)


# ---------------------------------------------------------------------------
# 레이아웃 → 렌더링 지시 (템플릿 _real_form.html.j2 가 그린다)
# ---------------------------------------------------------------------------

def _px(rect) -> list[float]:
    return [round(v * PX, 1) for v in rect]


def _fit(text: str, w: float, h: float, hand: bool, base: float, scale: float = 1.0) -> float:
    """글자 크기(px): 칸 높이에 맞추고, 칸 너비를 넘으면 줄인다. scale: 손글씨 글꼴의 몸집 보정."""
    size = min(h * (0.78 if hand else 0.62), base) * scale
    size = min(size, h * 1.05)
    em = sum(1.0 if ord(c) > 0x2E80 else (0.62 if hand else 0.58) for c in text) or 1
    k = (0.86 if hand else 1.0) / scale
    if em * size * k > w * 0.96:
        size = w * 0.96 / (em * k)
    return round(max(size, 6.0), 1)


def _jitter(r: random.Random, hand: bool) -> str:
    if not hand:
        return ""
    return f"transform: translate({r.uniform(-1.5, 1.5):.1f}px, {r.uniform(-1.5, 1.2):.1f}px) rotate({r.uniform(-2.2, 2.2):.1f}deg);"


def build(no: int, p: Profile, rng: random.Random) -> dict:
    """서식 번호와 프로필로 렌더링 데이터(d)를 만든다."""
    return build_form(f"hf{no:03d}", p, rng)


def _pool(pools: dict, name: str) -> list[dict]:
    lst = M.expand(pools[name])
    return lst or M.expand(M.DEFAULT_POOLS[name])   # 다 꺼 두면 기본 풀


def build_form(doc_id: str, p: Profile, rng: random.Random) -> dict:
    """overlay 서식(pdf·image) 하나의 렌더링 데이터(d). 사람 수정·표시 설정·풀을 반영한다."""
    lay, _ = form_layout(doc_id)
    no = form_no(doc_id)
    ov = OV.load(doc_id)
    S = M.settings(ov.get("marks"))
    pools = M.pools()
    cls = (lay.get("class") or "기본").split("/")[0]
    vals = Values(p, rng, cls)
    hand = rng.random() < S["hand"]
    hfont = rng.choice(_pool(pools, "hand_fonts"))
    hf = hfont["id"]
    style = {
        "hand": hand,
        "scale": hfont.get("scale", 1.0) if hand else 1.0,
        "font": f"'{hf}'" if hand else rng.choice(_pool(pools, "print_fonts"))["id"],
        "ink": rng.choice(INKS) if hand else rng.choice(["#111", "#1a1a1a", "#222"]),
        "base": rng.uniform(17, 22) if hand else rng.uniform(12, 14),
    }
    check = rng.choice(_pool(pools, "check"))
    style["mark"] = check["id"] if check.get("builtin") else "img"
    if not check.get("builtin"):
        style["mark_img"] = M.image_url(check)
    style["seal"] = rng.choice(["#d11", "#c00", "#e0312b", "#b22222"])
    style["fill"] = rng.uniform(0.75, 0.97) if p.extra.get("sparse_fields") else 1.0
    out: list[dict] = []
    used_keys: dict[str, int] = {}

    def uniq(key: str) -> str:
        key = re.sub(r"[^\w.]", "", key) or "value"   # HTML 속성·JSON 경로에 쓸 수 있는 글자만
        used_keys[key] = used_keys.get(key, 0) + 1
        return key if used_keys[key] == 1 else f"{key}{used_keys[key]}"

    # 표 행(같은 묶음·같은 항목명이 여러 줄): 묶음마다 채울 줄 수를 정한다
    rows: dict[tuple, int] = {}
    for it in lay["items"]:
        if it["t"] == "text" and it.get("row"):
            k = (it["page"], it.get("group") or "", norm(it["label"]))
            rows[k] = rows.get(k, 0) + 1
    fill_rows: dict[tuple, int] = {}
    pct_plan: dict[tuple, list[int]] = {}
    row_idx: dict[tuple, int] = {}

    for it in lay["items"]:
        t, page = it["t"], it["page"]
        label = it.get("label") or ""
        if t == "text":
            rk = (page, it.get("group") or "", norm(label))
            n_rows = rows.get(rk, 1) if it.get("row") else 1
            i = row_idx[rk] = row_idx.get(rk, -1) + 1
            gk = (page, it.get("group") or "")
            if n_rows > 1:
                if gk not in fill_rows:
                    fill_rows[gk] = rng.choice([0, 1, 1, 2, 2, 3] if p.extra.get("sparse_fields") else [1, 1, 2, 2, 3]) if rng.random() < 0.85 else n_rows
                    fill_rows[gk] = min(fill_rows[gk], n_rows)
                key_base = f"{norm(it['group'])}_목록" if norm(it.get("group") or "") else "목록"
                key = re.sub(r"[^\w.]", "", f"{key_base}.{i}.{norm(label) or 'value'}")
                kind = kind_of(label, it.get("unit"), it.get("hint"))
                if it.get("key"):   # 사람 수정: products.{i}.name 처럼 {i} 자리에 행 번호
                    key = re.sub(r"[^\w.]", "", it["key"].replace("{i}", str(i)))
                kind = it.get("kind") or kind
                if i >= fill_rows[gk]:
                    value = None
                elif it.get("source"):
                    value = SRC.value(it["source"], p, rng, {**it, "class": cls}, vals, row=i)
                elif kind == "percent":
                    plan = pct_plan.setdefault(gk, _split100(rng, max(1, fill_rows[gk])))
                    value = str(plan[i])
                else:
                    value = vals.by_kind(kind, label)
            else:
                skey = it.get("key") or key_of(label)
                kind = it.get("kind") or kind_of(label, it.get("unit"), it.get("hint"))
                # '연소득 / 본인 / 백만원'의 '본인'은 성명 칸이 아니다.
                if not it.get("key") and it.get("unit") in ("원", "천원", "만원", "백만원", "억원", "%", "명", "개", "건", "회"):
                    skey = None
                sec = norm(it.get("section") or "")
                if it.get("key"):
                    pass   # 사람이 정한 키는 구역(대리인·받는 분)으로 바꾸지 않는다
                elif skey and AGENT_SEC.search(sec) and skey.startswith("customer."):
                    skey = "agent." + skey.split(".", 1)[1]   # 대리인 구역의 성명·생년월일 …
                elif skey and FOREIGN_SEC.search(sec) and (skey.startswith("customer.") or skey == "account"):
                    skey = "foreign." + (skey.split(".", 1)[1] if "." in skey else "account")  # 받는 분
                if kind == "seal" and not skey:   # '인감', '서명/날인' 칸 → 도장·서명 자리
                    x = rng.random()
                    nm = p.person.name
                    sp = S["seal_spot"]
                    mk = {"t": "mark", "page": page, "key": uniq("signer"), "label": label, "name": nm,
                          "seal": x < sp["seal_below"], "sign": sp["seal_below"] <= x < sp["sign_below"],
                          "rect": _px(it["rect"]), "rot": round(rng.uniform(-12, 8), 1)}
                    out.append(_pooled(mk, pools, rng))
                    continue
                if it.get("source"):
                    value = SRC.value(it["source"], p, rng, {**it, "class": cls}, vals)
                    key = uniq(skey or norm(label) or "value")
                elif skey:
                    value = vals.std(skey)
                    if value is None and it.get("key"):   # 사람이 정한 키인데 프로필 규칙에 없는 키 → 값 종류로
                        value = vals.by_kind(kind, label)
                    if skey == "customer.rrn" and re.search(r"앞\s*6|앞자리", label) and value:
                        value = value[:6]
                    key = uniq(skey)
                else:
                    value = vals.by_kind(kind, label)
                    key = uniq(norm(label) or "value")
                if value is not None and rng.random() > style["fill"] and skey not in ("customer.name", "date"):
                    value = None
            if it.get("at") and value and "@" in value:
                local, domain = value.split("@", 1)
                at = it["at"]
                r0 = it["rect"]
                parts = [([r0[0], r0[1], at[0] - 1, r0[3]], local, "right"),
                         ([at[2] + 1, r0[1], r0[2], r0[3]], domain, "left")]
                out.append(_hidden(key, label, it["rect"], value, page))
                for rect, txt, align in parts:
                    out.append(_visible(None, txt, rect, page, style, rng, align=align))
                continue
            align = "right" if (it.get("unit") in ("원", "천원", "만원", "백만원") or kind == "amount") else \
                "center" if (it["rect"][2] - it["rect"][0]) < 70 or kind in ("percent", "count") else "left"
            unit = it.get("unit")
            if value is not None and unit in ("천원", "만원", "백만원", "억원") and it.get("source") != "rule:fixed":
                from .schema import korean_number

                amount = korean_number(str(value))
                if amount is None:
                    try:
                        amount = float(re.sub(r"[^0-9.+-]", "", str(value)))
                    except ValueError:
                        amount = None
                if amount is not None:
                    factor = {"천원": 1000, "만원": 10000, "백만원": 1000000, "억원": 100000000}[unit]
                    value = f"{amount / factor:,.4f}".rstrip("0").rstrip(".")
            out.append({**_visible(key, value, it["rect"], page, style, rng, label=label, align=align), "unit": unit})
        elif t == "check":
            opts = [o for o in it["options"]]
            if not opts:
                continue
            texts = [o["text"] or f"보기{j + 1}" for j, o in enumerate(opts)]
            if len(opts) == 1:
                sel = 0 if rng.random() < 0.5 else None
            elif rng.random() < 0.1 and it.get("pick") != "one":
                sel = None
            else:
                sel = rng.randrange(len(opts))
            key = uniq(it["key"] if it.get("key") else "check." + (norm(label) or norm(texts[0])[:12] or "item"))
            out.append({"t": "check", "page": page, "key": key, "label": label or texts[0],
                        "options": [{"text": texts[j], "box": _px(o["box"]), "rect": _px(o["rect"]),
                                     "on": j == sel} for j, o in enumerate(opts)],
                        "selected": texts[sel] if sel is not None else None,
                        "union": _px([min(o["box"][0] for o in opts), min(o["rect"][1] for o in opts),
                                      max(o["rect"][2] for o in opts), max(o["rect"][3] for o in opts)])})
        elif t == "date":
            d0 = p.issue_date
            pr = it["parts"]
            y = f"{d0.year % 100:02d}" if it.get("yy") else (
                str(d0.year) if (pr["y"][2] - pr["y"][0]) > 18 or rng.random() < 0.3 else f"{d0.year % 100:02d}")
            m, dd = (str(d0.month), str(d0.day)) if rng.random() < 0.6 else (f"{d0.month:02d}", f"{d0.day:02d}")
            key = uniq(key_of(label) or "date") if label else uniq("date")
            union = [pr["y"][0], pr["y"][1], pr["d"][2] + 9, pr["d"][3]]
            out.append(_hidden(key, label or "작성일", union, f"{d0.year}년 {d0.month}월 {d0.day}일", page))
            for part, txt in (("y", y), ("m", m), ("d", dd)):
                out.append(_visible(None, txt, pr[part], page, style, rng, align="center"))
        elif t == "sign":
            n = norm(label)
            is_agent = bool(re.search(r"대리인|수임인|보호자|법정대리", n)) or bool(AGENT_SEC.search(norm(it.get("section") or "")))
            name = None if is_agent and rng.random() < 0.85 else (
                p.corporation.name if re.search(r"법인|상호|회사", n) else p.person.name)
            role = uniq(it["key"] if it.get("key") else "signer")
            if it.get("name"):
                out.append(_visible(f"{role}.name", name, it["name"], page, style, rng, label=label, align="center"))
            x = rng.random()
            sp = S["sign_spot"]
            seal = name is not None and x < sp["seal_below"]
            sign = name is not None and not seal and x < sp["sign_below"]
            mk = {"t": "mark", "page": page, "key": role, "label": label, "name": name or "",
                  "seal": seal, "sign": sign, "rect": _px(it["mark"]),
                  "rot": round(rng.uniform(-12, 8), 1), "sig_seed": rng.random()}
            out.append(_pooled(mk, pools, rng))
        elif t == "copy":
            filled = rng.random() < 0.85
            out.append(_visible(uniq(it["key"] if it.get("key") else "handwritten"), it["text"] if filled else None,
                                it["rect"], page, {**style, "hand": True, "font": f"'{hf}'", "scale": hfont.get("scale", 1.0)}, rng,
                                label=label or "자필기재", align="center"))
    # 결재란: 은행이 접수·처리한 서류에는 직원 도장·서명이 있다. 같은 칸 이름은 서류 안에서 같은 직원.
    cells = [(i, c) for i, pg in enumerate(lay["pages"]) for c in pg.get("staff", [])]
    if cells:
        st, ss = S["staff"], S["staff_spot"]
        processed = rng.random() < st["processed"]
        staff: dict[str, str] = {}
        for page, c in cells:
            role = c["role"]
            name = staff.setdefault(role, K.make_name(rng, rng.choice("MF"))[0])
            on = processed and rng.random() < st["filled"]
            x = rng.random()
            square = x < ss["square_below"]               # 사각 도장: 직원 이름 또는 '확인'·'검인'
            text = rng.choice(["확인", "검인"]) if square and rng.random() < 0.4 else name
            rect = _px(c["rect"])
            size = max(22.0, min(44.0, min(rect[2] - rect[0], rect[3] - rect[1]) * rng.uniform(0.62, 0.85)))
            mk = {"t": "mark", "page": page, "key": uniq("staff." + (norm(role) or "결재")), "label": role,
                  "name": text, "seal": on and x < ss["seal_below"], "sign": on and x >= ss["seal_below"], "rect": rect,
                  "rot": round(rng.uniform(-12, 8), 1), "staff": True, "square": square, "size": round(size, 1)}
            out.append(_pooled(mk, pools, rng))
    pages = []
    for i, pg in enumerate(lay["pages"]):
        bg = f"{HOST}bg/{no}/{i}.png" if no is not None else f"{HOST}bgi/{doc_id}/{i}.png"
        if OV.erase_for(ov, i):   # 지운 배경은 주소가 달라야 브라우저가 예전 그림을 다시 쓰지 않는다
            bg += f"?e={OV.digest(OV.erase_for(ov, i))}"
        pages.append({"w": round(pg["width"] * PX, 1), "h": round(pg["height"] * PX, 1), "bg": bg})
    fonts = list(dict.fromkeys(HAND_FONTS + [f["id"] for f in pools["hand_fonts"]]))
    return {"no": no, "doc_id": doc_id, "pages": pages, "items": out, "style": style, "class": lay.get("class", ""),
            "name": lay.get("name", doc_id), "fonts": fonts}


def _pooled(mk: dict, pools: dict, rng: random.Random) -> dict:
    """찍힌 도장·서명의 모양을 풀에서 고른다. 풀이 기본(코드가 그리는 모양 하나)이면 난수를 쓰지 않는다."""
    render = {}
    if mk["sign"]:
        it = M.pick(rng, pools["sign"])
        if it and not it.get("builtin"):
            mk["sign_img"] = M.image_url(it)
            render["sign"] = it["id"]
    if mk["seal"]:
        it = M.pick(rng, pools["seal"])
        if it and not it.get("builtin"):
            mk["seal_tpl"] = it
            render["seal"] = it["id"]
    if render:
        mk["render"] = render
    return mk


def _split100(r: random.Random, n: int) -> list[int]:
    if n == 1:
        return [100]
    if n >= 20:
        base = [100 // n] * n
        base[0] += 100 - sum(base)
        return base
    cuts = sorted(r.sample(range(1, 20), n - 1))
    parts = [b - a for a, b in zip([0] + cuts, cuts + [20])]
    return [x * 5 for x in parts]


def _hidden(key: str, label: str, rect, value: str | None, page: int) -> dict:
    """정답 위치만 기록하는 투명 칸 (값이 여러 조각으로 나뉘어 쓰일 때: 날짜, 이메일)."""
    return {"t": "hidden", "page": page, "key": key, "label": label, "value": value, "rect": _px(rect)}


def _visible(key, value, rect, page, style, r: random.Random, label: str = "", align: str = "left") -> dict:
    x0, y0, x1, y1 = _px(rect)
    w, h = x1 - x0, y1 - y0
    text = value or ""
    size = _fit(text, w - 6, h, style["hand"], style["base"], style.get("scale", 1.0)) if text else 10
    pad = r.uniform(2, 7) if align == "left" else 2
    return {"t": "text", "page": page, "key": key, "label": label, "value": value,
            "rect": [x0, y0, x1, y1], "size": size, "align": align, "pad": round(pad, 1),
            "css": _jitter(r, style["hand"])}


# ---------------------------------------------------------------------------
# 등록
# ---------------------------------------------------------------------------

def all_layouts() -> list[dict]:
    out = []
    for path in sorted(LAYOUTS.glob("*/*.json")):
        lay = json.loads(path.read_text(encoding="utf-8"))
        out.append(lay)
    return out


# 고객이 채우는 칸이 없는 인쇄물·내부 문서 (docgen/scripts/form_map.py 의 '제외' 판정과 같다)
EXCLUDE_KW = ["약관", "안내장", "체크리스트", "일반위험고지문", "상품설명서", "중요내용 설명서", "환전장부",
              "과목분류표", "관리대장", "제출서류 목록"]
# 22: 영문 통합제신고서 — PDF 글자 인코딩이 깨져(글자 코드가 밀려 있음) 항목명을 읽을 수 없다
EXCLUDE_NO = {12, 13, 14, 22, 40, 57, 143, 187, 200, 257, 404}


def fillable(lay: dict) -> int:
    return sum(1 for it in lay["items"] if it["t"] in ("text", "date", "sign", "copy")) + \
        sum(1 for it in lay["items"] if it["t"] == "check" and len(it["options"]) > 1)


def register_images() -> int:
    """overlay(image) 서식: docgen/forms/images/img_*/ 와 (설정했으면) DOCGEN_PRIVATE_FORMS/img_*/ 의 layout.json.
    studio 가져오기에서 견본 그림으로 만든 서식이다. 이미 등록된 ID 는 건너뛴다 (여러 번 불러도 된다)."""
    from .registry import REGISTRY, DocSpec

    n = 0
    for root in [IMAGE_FORMS, *_private_roots()]:
        if not root.is_dir():
            continue
        for d in sorted(root.glob("img_*")):
            if d.name in REGISTRY or not (d / "layout.json").exists():
                continue
            lay = json.loads((d / "layout.json").read_text(encoding="utf-8"))

            def generate(p: Profile, rng: random.Random, _id=d.name) -> dict:
                return build_form(_id, p, rng)

            pg = lay["pages"][0]
            page = "a4_landscape" if pg["width"] > pg["height"] else "a4"
            REGISTRY[d.name] = DocSpec(d.name, lay.get("name") or d.name, "imported", "internal", "_real_form.html.j2",
                                       generate, page, False,
                                       f"가져온 서식 이미지 위에 기재 (묶음 {lay.get('from_batch', '-')}"
                                       f"{', 내부 전용' if lay.get('private') else ''})")
            n += 1
    return n


def register_all() -> int:
    """레이아웃이 있는 서식을 모두 hf<No> 로 등록한다 (+ 가져온 이미지 서식)."""
    from .registry import REGISTRY, DocSpec

    n = 0
    for lay in all_layouts():
        no = lay["no"]
        if no in EXCLUDE_NO or any(k in lay["name"] for k in EXCLUDE_KW) or fillable(lay) < 2:
            continue
        doc_id = f"hf{no:03d}"
        if doc_id in REGISTRY:
            continue

        def generate(p: Profile, rng: random.Random, _no=no) -> dict:
            from .banks import bank_view
            return build(_no, bank_view(p, BANK), rng)

        page = "a4_landscape" if lay["pages"][0]["width"] > lay["pages"][0]["height"] else "a4"
        REGISTRY[doc_id] = DocSpec(doc_id, lay["name"], "hana", "internal", "_real_form.html.j2", generate, page,
                                   False, f"하나은행 공개 서식 No.{no} ({lay['class']}) 원본 위에 기재")
        n += 1
    return n + register_images()
