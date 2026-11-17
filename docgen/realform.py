"""원본 서식 오버레이 — 하나은행 공개 서식 PDF 를 그대로 배경으로 깔고, 손님이 쓴 것처럼 값을 얹는다.

서식 모양을 HTML 로 다시 그리지 않으므로 이미지 속 서식은 원본과 똑같다. 값을 쓸 자리는
docgen/scripts/extract_form_layout.py 가 PDF 에서 뽑은 docgen/forms/hf<No>/layout.json 을 쓴다 (서식 폴더: docgen/formdir.py).

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

from . import freetext as FT
from . import keyrules as KR
from . import korean as K
from . import marks as M
from . import formkit as FK
from . import overrides as OV
from . import sources as SRC
from .entities import Profile

ROOT = Path(__file__).resolve().parent   # docgen/ (레이아웃의 "file" 은 원본을 내려받은 자리 기록. 파일은 formdir.original_pdf)
FT_MIN_SIZE = 9.0   # 자유 기재 글이 이보다 작게 줄어야 들어가는 칸이면 넣지 않는다 (px)
FONTS = ROOT / "fonts"
CACHE = Path.home() / ".cache" / "docgen" / "bg"
HOST = "https://docgen.local/"
PX = 96 / 72          # PDF pt → CSS px
BG_ZOOM = 2 * PX      # 배경 해상도 = 렌더러 device_scale_factor(2) 에 맞춘다
BANK = "하나은행"
# 손글씨 비율, 결재란 비율, 체크 모양·글꼴 목록은 docgen/marks.py (marks.json·풀) 에서 읽는다.
# 손글씨 글꼴마다 글자 몸집이 달라 같은 칸 높이에서 키우는 비율도 풀의 scale 이다.
INKS = ["#1b2a80", "#1a1a1a", "#222c55", "#0d3a8a", "#2b2b2b", "#183c9c"]
D = K.fmt_date


# ---------------------------------------------------------------------------
# 배경·글꼴 제공 (렌더러가 부른다)
# ---------------------------------------------------------------------------

# 서식 파일 자리는 docgen/formdir.py: hf### 은 docgen/forms/hf<번호>/(layout.json, look/original.pdf),
# 가져온 이미지 서식 img_* 는 docgen/forms/<ID>/ 또는 $DOCGEN_PRIVATE_FORMS/<ID>/ (layout.json, look/page_<쪽>.png).

def layout_path(no: int) -> Path | None:
    from . import formdir

    return formdir.hf_layout(no)


@lru_cache(maxsize=None)
def load_layout(no: int) -> dict:
    """자동 추출 레이아웃 그대로 (사람 수정 전)."""
    return json.loads(layout_path(no).read_text(encoding="utf-8"))


def form_no(doc_id: str) -> int | None:
    return int(doc_id[2:]) if re.fullmatch(r"hf\d{3}", doc_id) else None


def image_form_dir(doc_id: str) -> Path | None:
    """overlay(image) 서식 폴더 (layout.json 이 있는 곳)."""
    from . import formdir

    return formdir.image_dir(doc_id)


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
    """칸 목록(서식 폴더의 fields.json, 없으면 자동 추출 + 예전 사람 수정)에 미리보기 초안을 덧씌운 레이아웃과 못 찾은 수정 목록."""
    return OV.apply(OV.base(doc_id), OV.load(doc_id))


def _pdf_page_png(no: int, page: int) -> bytes:
    """서식 PDF 의 한 쪽을 PNG 로 (캐시)."""
    out = CACHE / f"{no:03d}_{page}.png"
    if not out.exists():
        import pymupdf

        from . import formdir

        out.parent.mkdir(parents=True, exist_ok=True)

        with pymupdf.open(formdir.original_pdf(no)) as doc:
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
    from . import formdir

    return formdir.page_png(doc_id, page).read_bytes()


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
    if m := re.fullmatch(r"fonts/([A-Za-z0-9_-]+\.(woff2|woff|ttf|otf))", path):
        f = FONTS / m.group(1)
        if f.exists():
            return f.read_bytes(), f"font/{m.group(2)}"
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


def _text_key(it: dict) -> tuple[str | None, str]:
    """글자 칸(표 행이 아닌 것)의 키와 값 종류: 칸 목록(fields.json)에 적힌 그대로 (모든 서식 공통 규칙은 없다).
    키가 없으면 None — 도장 자리(kind seal)이거나, 키 설명으로 키를 만든다 (build_form)."""
    return it.get("key"), it.get("kind") or "text"


def _uniq_fn():
    """서식 안에서 키가 겹치면 뒤에 번호 (name, name2 …). HTML 속성·JSON 경로에 쓸 수 있는 글자만."""
    used: dict[str, int] = {}

    def uniq(key: str) -> str:
        key = re.sub(r"[^\w.]", "", key) or "value"
        used[key] = used.get(key, 0) + 1
        return key if used[key] == 1 else f"{key}{used[key]}"
    return uniq


def _row_key(it: dict, i: int) -> str:
    """표 행 칸의 키: <묶음>_목록.<행>.<항목명> (사람이 정한 키면 {i} 자리에 행 번호)."""
    label = it.get("label") or ""
    if it.get("key"):
        return re.sub(r"[^\w.]", "", it["key"].replace("{i}", str(i)))
    key_base = f"{norm(it['group'])}_목록" if norm(it.get("group") or "") else "목록"
    return re.sub(r"[^\w.]", "", f"{key_base}.{i}.{norm(label) or 'value'}")


def _check_key(it: dict) -> str:
    texts = [o["text"] or f"보기{j + 1}" for j, o in enumerate(it["options"])]
    return it["key"] if it.get("key") else "check." + (norm(it.get("label") or "") or norm(texts[0])[:12] or "item")


def layout_keys(doc_id: str) -> dict[str, dict]:
    """영역(영역 편집기 id)마다 {t, label, keys}: 렌더링 정답에 나오는 칸 키 (서식의 키). build_form 과 같은 순서로 번호를 붙인다.
    도장·서명 자리는 seal.<자리> · sign.<자리>, 서명 칸의 이름은 <자리>.name."""
    lay, _ = form_layout(doc_id)
    uniq, out, row_idx, rows = _uniq_fn(), {}, {}, {}
    mark = lambda role: [f"seal.{role}", f"sign.{role}"]  # noqa: E731
    rkey = lambda it: (it["page"], it.get("group") or "", norm(it.get("label") or ""))  # noqa: E731
    for it in lay["items"]:
        if it["t"] == "text" and it.get("row"):
            rows[rkey(it)] = rows.get(rkey(it), 0) + 1
    for it in lay["items"]:
        t, label, ks = it["t"], it.get("label") or "", []
        if t == "text":
            i = row_idx[rkey(it)] = row_idx.get(rkey(it), -1) + 1
        if t == "text" and it.get("row") and rows[rkey(it)] > 1:   # 한 줄뿐인 표 행은 보통 칸처럼
            ks = [_row_key(it, i)]
        elif t == "text":
            skey, kind = _text_key(it)
            if kind == "seal" and not skey:
                ks = mark(uniq("signer"))
            else:
                ks = [uniq(skey or norm(label) or "value") if (it.get("source") or not skey) else uniq(skey)]
        elif t == "check" and it.get("options"):
            ks = [uniq(_check_key(it))]
        elif t == "date":
            ks = [uniq(it.get("key") or "date")]
        elif t == "sign":
            role = uniq(it["key"] if it.get("key") else "signer")
            ks = ([f"{role}.name"] if it.get("name") else []) + mark(role)
        elif t == "copy":
            ks = [uniq(it["key"] if it.get("key") else "handwritten")]
        elif t == "float":
            from . import floats as FL

            c = FL.preset(it)
            k = uniq(c["key"])
            ks = [f"seal.{k}"] + ([k] if c.get("answer") else []) if c["type"] == "stamp" else [k]
        out[it.get("_id") or f"item:{len(out)}"] = {"t": t, "label": label, "keys": ks}
    for pg in lay["pages"]:
        for c in pg.get("staff", []):
            out[c.get("_id") or f"staff:{len(out)}"] = {"t": "staff", "label": c["role"],
                                                        "keys": mark(uniq("staff." + (norm(c["role"]) or "결재")))}
    return out


def _acct(r: random.Random) -> str:
    return "".join(str(r.randint(0, 9)) if c == "#" else c for c in "###-######-#####")


class Values:
    """한 서류 안에서 값을 만든다. 같은 표준 키는 같은 값 (표에 두 번 나와도 일치)."""

    def __init__(self, p: Profile, r: random.Random, cls: str):
        self.not_profile: set[str] = set()
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
            "family.name": lambda: (p.spouse or p.father).name,
            "related.name": lambda: K.make_name(r, r.choice("MF"))[0],   # 보증인·공동: 이 서류 안에서 같은 사람
            "date": lambda: D(p.issue_date, r.choice(["kor", "dot"])),
        }.get(key)
        if v is None:   # key_rules.json 의 keys 에서 더한 키: 값 출처(프로필 경로) 또는 값 종류
            k = KR.load()["keys"].get(key)
            if not k or not (k.get("source") or k.get("kind")):
                self.not_profile.add(key)   # 고객 정보 키가 아님 (build_form 이 값 종류로 만든다)
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
        if kind == "other_person":   # 발급기관 담당자·은행 직원: 고객 이름이 나오면 안 되는 칸
            return K.make_name(r, r.choice("MF"))[0]
        if kind == "office_phone":
            return K.landline(r, r.choice([p.person.address.sido, p.employment.company.address.sido]))
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
        return KR.make_value(kind, p, r)  # key_rules.json 의 공통 값 종류. 그 밖의 뜻을 모르는 칸은 비워 둔다 (실제 서식도 빈 칸이 많다)


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
    uniq = _uniq_fn()

    # 표 행(같은 묶음·같은 항목명이 여러 줄): 묶음마다 채울 줄 수를 정한다
    rows: dict[tuple, int] = {}
    for it in lay["items"]:
        if it["t"] == "text" and it.get("row"):
            k = (it["page"], it.get("group") or "", norm(it["label"]))
            rows[k] = rows.get(k, 0) + 1
    cap: dict[tuple, int] = {}   # 묶음마다 인쇄된 줄 수
    for (pg, grp, _), n in rows.items():
        cap[(pg, grp)] = max(cap.get((pg, grp), 0), n)
    fill_rows: dict[tuple, int] = {}
    fills = {}   # 묶음마다 채우는 행 수 설정 (영역 편집기 표 칸의 fill: few·half·full·any)
    for it in lay["items"]:
        if it["t"] == "text" and it.get("row") and it.get("fill"):
            fills.setdefault((it["page"], it.get("group") or ""), it["fill"])
    pct_plan: dict[tuple, list[int]] = {}
    row_idx: dict[tuple, int] = {}
    row_cols: dict[tuple, dict] = {}   # 묶음마다 열(항목명 → 첫 줄 칸): 별지에 이어 적을 때 쓴다

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
                    fill_rows[gk] = _fill_count(fills.get(gk), n_rows, p, rng)
                    more = _more_rows(p, doc_id, gk, cap[gk])
                    if more:   # 인쇄된 줄을 다 채우고 남은 줄은 별지에 (extra_rows)
                        fill_rows[gk] = cap[gk] + more
                row_cols.setdefault(gk, {}).setdefault(norm(label), it)
                key = _row_key(it, i)
                kind = it.get("kind") or "text"
                if i >= fill_rows[gk]:
                    value = None
                else:
                    value = FK.fmt(_row_value(it, i, gk, p, rng, vals, cls, fill_rows, pct_plan), it.get("fmt"))
            else:
                skey, kind = _text_key(it)
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
                elif skey and it.get("std", True):   # 키가 고객 정보 키면 그 값 (customer.name …, Values.std)
                    value = vals.std(skey)
                    if value is None and skey in vals.not_profile:   # 고객 정보 키가 아니면 값 종류로 (배우자 없는 고객의 spouse.name 은 빈칸 그대로)
                        value = vals.by_kind(kind, label)
                    if skey == "customer.rrn" and re.search(r"앞\s*6|앞자리", label) and value:
                        value = value[:6]
                    key = uniq(skey)
                else:   # "std": false — 값 종류로 만드는 칸 (기타·비고·사유 칸은 자유 기재 글)
                    value = vals.by_kind(kind, label)
                    key = uniq(skey or norm(label) or "value")
                    x0, y0, x1, y1 = _px(it["rect"])   # 기타·비고·사유 칸 일부는 자유 기재 글 (docgen/freetext.py)
                    value = FT.fill(label, f"{p.seed}:{doc_id}:{page}:{it['rect']}", p.issue_date,
                                    lambda s: _fit(s, x1 - x0 - 6, y1 - y0, style["hand"], style["base"],
                                                   style.get("scale", 1.0)) >= FT_MIN_SIZE) or value
                value = FK.fmt(value, it.get("fmt"))
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
            value = _in_unit(value, it)
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
            key = uniq(_check_key(it))
            out.append({"t": "check", "page": page, "key": key, "label": label or texts[0],
                        "options": [{"text": texts[j], "box": _px(o["box"]), "rect": _px(o["rect"]),
                                     "on": j == sel} for j, o in enumerate(opts)],
                        "selected": texts[sel] if sel is not None else None,
                        "union": _px([min(o["box"][0] for o in opts), min(o["rect"][1] for o in opts),
                                      max(o["rect"][2] for o in opts), max(o["rect"][3] for o in opts)])})
        elif t == "date":
            d0 = _date_value(it, p, rng, vals, cls)
            pr = it["parts"]
            y = f"{d0.year % 100:02d}" if it.get("yy") else (
                str(d0.year) if (pr["y"][2] - pr["y"][0]) > 18 or rng.random() < 0.3 else f"{d0.year % 100:02d}")
            m, dd = (str(d0.month), str(d0.day)) if rng.random() < 0.6 else (f"{d0.month:02d}", f"{d0.day:02d}")
            key = uniq(it.get("key") or "date")
            union = [pr["y"][0], pr["y"][1], pr["d"][2] + 9, pr["d"][3]]
            out.append(_hidden(key, label or "작성일", union, f"{d0.year}년 {d0.month}월 {d0.day}일", page))
            for part, txt in (("y", y), ("m", m), ("d", dd)):
                out.append(_visible(None, txt, pr[part], page, style, rng, align="center"))
        elif t == "sign":
            role = uniq(it["key"] if it.get("key") else "signer")
            name = _signer_name(label, it, vals, rng)
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
    # 인쇄된 줄보다 많은 행: 별지(계속) 쪽에 같은 열로 이어 적는다 (_extra_rows.html.j2, 넘치면 paginate.js 가 쪽을 늘림)
    extra_rows = []
    for gk, total in fill_rows.items():
        if total <= cap[gk]:
            continue
        cols = sorted(row_cols[gk].values(), key=lambda c: c["rect"][0])
        body = []
        for i in range(cap[gk], total):
            cells = []
            for c in cols:
                v = _in_unit(FK.fmt(_row_value(c, i, gk, p, rng, vals, cls, fill_rows, pct_plan), c.get("fmt")), c)
                kind = c.get("kind") or "text"
                cells.append({"key": _row_key(c, i), "value": v, "label": c.get("label") or "",
                              "align": "right" if (c.get("unit") in ("원", "천원", "만원", "백만원") or kind == "amount") else "left"})
            body.append({"no": i + 1, "cells": cells})
        extra_rows.append({"page": gk[0], "title": gk[1] or "", "columns": [c.get("label") or "" for c in cols],
                           "units": [c.get("unit") or "" for c in cols], "rows": body})
    _adjust(doc_id, out, extra_rows, p, style)   # 서식 폴더 generate.py 의 adjust(d, p, rng): 칸끼리 관계 (합계·순서)
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
    out += _floats(doc_id, lay, S, p, vals, cls, style, pools, uniq)   # 자유 위치 도장·번호 (docgen/floats.py)
    pages = []
    for i, pg in enumerate(lay["pages"]):
        bg = f"{HOST}bg/{no}/{i}.png" if no is not None else f"{HOST}bgi/{doc_id}/{i}.png"
        if OV.erase_for(ov, i):   # 지운 배경은 주소가 달라야 브라우저가 예전 그림을 다시 쓰지 않는다
            bg += f"?e={OV.digest(OV.erase_for(ov, i))}"
        pages.append({"w": round(pg["width"] * PX, 1), "h": round(pg["height"] * PX, 1), "bg": bg})
    fonts = M.font_faces(pools)
    return {"no": no, "doc_id": doc_id, "pages": pages, "items": out, "style": style, "class": lay.get("class", ""),
            "name": lay.get("name", doc_id), "fonts": fonts, "extra_rows": extra_rows}


def script_path(doc_id: str) -> Path | None:
    """overlay 서식의 생성 스크립트: 서식 폴더의 generate.py (adjust 가 있는 것만. html 서식과 같은 약속)."""
    from . import formdir

    d = formdir.folder(doc_id)
    f = d / "generate.py" if d else None
    return f if f is not None and f.exists() and re.search(r"^def adjust\(", f.read_text(encoding="utf-8"), re.M) else None


def nest(flat: dict) -> dict:
    """{"customer.name": v, "deals.0.amount": w} → {"customer": {"name": v}, "deals": [{"amount": w}]}.
    숫자 마디는 표 행 목록 (행 번호 순서). 다른 키와 부딪히는 키는 점 경로 그대로 맨 위에 둔다."""
    d: dict = {}
    for key in sorted(flat, key=lambda k: [int(x) if x.isdigit() else -1 for x in k.split(".")]):
        parts, cur, ok = key.split("."), d, True
        for j, k in enumerate(parts[:-1]):
            nxt_list = parts[j + 1].isdigit()
            if isinstance(cur, list):
                i = int(k)
                while len(cur) <= i:
                    cur.append({})
                cur = cur[i]
                continue
            if k.isdigit() or (k in cur and not isinstance(cur[k], (list if nxt_list else dict))):
                ok = False
                break
            cur = cur.setdefault(k, [] if nxt_list else {})
        last = parts[-1]
        if ok and isinstance(cur, list) and last.isdigit():
            ok = False
        if ok and isinstance(cur, dict) and last not in cur:
            cur[last] = flat[key]
        else:
            d[key] = flat[key]
    return d


def flatten(d, prefix: str = "") -> dict:
    """nest 의 반대."""
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(flatten(v, f"{prefix}{k}."))
    elif isinstance(d, list):
        for i, v in enumerate(d):
            out.update(flatten(v, f"{prefix}{i}."))
    else:
        out[prefix[:-1]] = d
    return out


def _adjust(doc_id: str, out: list[dict], extra_rows: list[dict], p: Profile, style: dict) -> None:
    """generate.py 의 adjust(d, p, rng) 로 글자 칸 값을 다듬는다 (없으면 그대로). d 는 칸 키의 점 경로를 중첩한 dict —
    표 행은 목록 (formkit.rows(d, "<묶음>")). 값을 바꾼 칸은 글자 크기를 다시 맞춘다. 새 키는 정답에 없다 (검사 경고).
    난수는 따로 (rng 를 같이 쓰면 스크립트를 더하기만 해도 다른 칸 값이 바뀐다)."""
    path = script_path(doc_id)
    if path is None:
        return
    from . import htmlform as HF

    flat = {it["key"]: it["value"] for it in out if it["t"] == "text" and it.get("key")}
    for g in extra_rows:
        for row in g["rows"]:
            for c in row["cells"]:
                flat[c["key"]] = c["value"]
    new = flatten(HF.run_script(doc_id, nest(flat), p, random.Random(f"adjust:{p.seed}:{doc_id}"), path))
    for it in out:
        if it["t"] == "text" and it.get("key") and it["key"] in new and new[it["key"]] != it["value"]:
            v = new[it["key"]]
            it["value"] = None if v in (None, "") else str(v)
            x0, y0, x1, y1 = it["rect"]
            it["size"] = _fit(it["value"], x1 - x0 - 6, y1 - y0, style["hand"], style["base"], style.get("scale", 1.0)) if it["value"] else 10
    for g in extra_rows:
        for row in g["rows"]:
            for c in row["cells"]:
                if c["key"] in new and new[c["key"]] != c["value"]:
                    c["value"] = None if new[c["key"]] in (None, "") else str(new[c["key"]])


def adjust_skeleton(doc_id: str) -> str:
    """overlay 서식의 견본 generate.py: 이 서식의 칸(seed 0 으로 그린 값)을 d 의 꼴로 주석에 적고, 흔한 관계 예시."""
    from .entities import make_profile

    d0 = build_form(doc_id, make_profile(0), random.Random(0))
    flat = {it["key"]: it["value"] for it in d0["items"] if it["t"] == "text" and it.get("key")}
    d = nest(flat)
    tables = [k for k, v in d.items() if isinstance(v, list)]
    lines = [f"# {k} = {v!r}" for k, v in flatten({k: (v[:1] if isinstance(v, list) else v) for k, v in d.items()}).items()]
    t = tables[0] if tables else "<표 묶음>"
    return f'''"""{doc_id} 생성 스크립트: 칸끼리 관계를 맞춘다 (합계 = 행의 합, 시작일 ≤ 종료일, 잔액 …).

값 하나하나는 영역 편집의 '생성 방법'이 만들고, 이 함수는 그 값을 받아 서로 맞게 고친다.
d = 이 서식의 칸 키(점 경로)를 중첩한 dict. 표 행은 목록: rows(d, "{t}") → [{{열: 값}}, …] (빈 행은 값이 None).
약속: 난수는 rng 만, 파일·네트워크·시간 금지, 새 키 금지 (정답에 없음). 확인: 영역 편집 › 수정 전후 비교, python -m docgen.formdir check {doc_id}
도우미: docgen/formkit.py (to_date·date_like·to_amount·amount_like·won_korean·rows·get·put·add_days)

seed 0 의 칸 (표는 첫 행만):
{chr(10).join(lines)}
"""
from docgen.formkit import add_days, amount_like, date_like, get, put, rows, to_amount, to_date  # noqa: F401


def adjust(d, p, rng):
    # 예: 표 금액 열의 합계 → 합계 칸
    # total = sum(to_amount(r.get("금액")) or 0 for r in rows(d, "{t}"))
    # put(d, "<합계 칸 키>", amount_like(total, get(d, "<합계 칸 키>") or "1,000"))
    #
    # 예: 시작일 ≤ 종료일
    # s, e = to_date(get(d, "<시작일 키>")), to_date(get(d, "<종료일 키>"))
    # if s and e and s > e:
    #     put(d, "<종료일 키>", date_like(add_days(s, rng.randint(30, 365)), get(d, "<종료일 키>")))
    return d
'''


def _spots(it: dict) -> list[list[float]]:
    """칸 하나가 차지하는 상자들 (pt): 값 자리·체크 보기·서명·날짜 칸."""
    out = [it[k] for k in ("rect", "mark", "name") if isinstance(it.get(k), list) and it["t"] != "float"]
    out += [v for v in (it.get("parts") or {}).values() if isinstance(v, list)]
    out += [o.get("rect") or o.get("box") for o in it.get("options") or [] if o.get("rect") or o.get("box")]
    return out


def _floats(doc_id: str, lay: dict, S: dict, p: Profile, vals: "Values", cls: str, style: dict, pools: dict, uniq) -> list[dict]:
    """자유 위치 요소 (docgen/floats.py): 서식의 float 칸 + 모든 서식 설정(marks.json floats). 요소마다 따로 난수
    (나올지·자리·회전·값) — 다른 칸의 값을 흔들지 않고, 요소가 없으면 결과가 예전과 같다."""
    from . import floats as FL

    els = [it for it in lay["items"] if it["t"] == "float"]
    els += [{**g, "page": None, "_global": True} for g in (S.get("floats") or [])]
    if not els:
        return []
    busy: dict[int, list] = {}
    for it in lay["items"]:
        busy.setdefault(it["page"], []).extend(_spots(it))
    out = []
    for j, el in enumerate(els):
        r = random.Random(f"float:{p.seed}:{doc_id}:{j}")
        c = FL.preset(el)
        page = el["page"] if el.get("page") is not None else r.randrange(len(lay["pages"]))
        pg = lay["pages"][page]
        if el.get("_global"):
            a = FL.AREAS[c.get("area") or "any"]
            area = [a[0] * pg["width"], a[1] * pg["height"], a[2] * pg["width"], a[3] * pg["height"]]
        else:
            area = el["rect"]
        show = r.random() < float(c.get("p", 0.5))
        key, label = uniq(c["key"]), el.get("label") or c["name"]
        if c["type"] == "stamp":
            size = float(c.get("size") or 50)
            rect = FL.place((size, size), area, busy.get(page, []), r) if show else [round(v, 1) for v in area]
            text = FL.stamp_text(c, p, r) if show else ""
            lines = [ln for ln in text.split("\n") if ln.strip()] or [""]
            spx = size * PX
            ems = max(sum(1.0 if ord(ch) > 0x2E80 else 0.56 for ch in ln) for ln in lines) or 1   # 숫자·점은 반 글자 폭
            fs = min(spx * 0.24, spx * 0.78 / ems, spx * 0.7 / (len(lines) * 1.12))
            mk = {"t": "mark", "page": page, "key": key, "label": label, "name": text, "seal": show, "sign": False,
                  "rect": _px(rect), "rot": round(r.uniform(-25, 25), 1), "square": c.get("shape") == "square",
                  "size": round(spx, 1), "fs": round(fs, 1), "no_sign": True, "float": True, "kind": c["name"].split(" ")[0]}
            if c.get("color"):
                mk["color"] = FL.COLORS[c["color"]]
            out.append(mk)
            if show and c.get("answer"):   # 도장 글자도 정답 (kie): 줄바꿈은 띄어쓰기로
                out.append(_hidden(key, label, rect, " ".join(text.split()), page))
        elif show:
            v = FL.text_value(c, p, r, el, cls, vals)
            if v in (None, ""):
                continue
            fs = r.uniform(8.5, 11.0)
            rect = FL.place(FL.text_size(str(v), fs), area, busy.get(page, []), r)
            st = c.get("style") or "print"
            hand = st == "hand"
            font = (style["font"] if style["hand"] else f"'{r.choice(_pool(pools, 'hand_fonts'))['id']}'") if hand \
                else r.choice(_pool(pools, "print_fonts"))["id"]
            item = _visible(key, str(v), rect, page, {**style, "hand": hand, "scale": 1.0}, r, label=label, align="left")
            item["font"] = font
            if st == "print":   # 전산으로 찍힌 번호는 검은색 (손글씨 서류의 펜 색이 아니라)
                item["color"] = "#1a1a1a"
            if st == "stamp":
                item["color"] = FL.COLORS[c.get("color") or "blue"]
                item["css"] = (item["css"] or "") + f"transform: rotate({r.uniform(-8, 8):.1f}deg);"
            out.append(item)
        else:
            continue
        busy.setdefault(page, []).append(rect)
    return out


def _date_value(it: dict, p: Profile, rng: random.Random, vals: "Values", cls: str):
    """년·월·일 칸의 날짜: 생성 방법(source)이 있으면 그 값을 날짜로 읽고, 없거나 못 읽으면 서류 날짜(발급·작성일)."""
    if it.get("source"):
        v = SRC.value(it["source"], p, rng, {**it, "class": cls}, vals)
        d = FK.to_date(v) or FK._compact_date(str(v or ""))
        if d:
            return d
    return p.issue_date


FILLS = {"few": "1~3행 (기본)", "half": "절반쯤", "full": "모든 행", "any": "1행 ~ 모든 행 고르게"}


def _fill_count(mode: str | None, n_rows: int, p: Profile, rng: random.Random) -> int:
    """표 묶음 하나에 채울 행 수. 기본(few)은 예전 그대로: 대개 1~3행, 15% 는 모든 행."""
    if mode == "full":
        return n_rows
    if mode == "half":
        return max(1, min(n_rows, round(n_rows * rng.uniform(0.35, 0.65))))
    if mode == "any":
        return rng.randint(1, n_rows)
    n = rng.choice([0, 1, 1, 2, 2, 3] if p.extra.get("sparse_fields") else [1, 1, 2, 2, 3]) if rng.random() < 0.85 else n_rows
    return min(n, n_rows)


MORE_ROWS = 0.15   # 표 하나가 인쇄된 줄을 넘쳐 별지로 이어지는 비율 (DOCGEN_HEAVY=1 이면 늘, 0 이면 없음 — 미리보기 '내용 많음')


def _more_rows(p: Profile, doc_id: str, gk: tuple, cap: int) -> int:
    """인쇄된 줄(cap)보다 더 적을 행 수 (0 이면 넘치지 않음). 다른 값의 난수를 흔들지 않게 따로 난수를 쓴다."""
    from .docs._common import heavy

    r = random.Random(f"rows:{p.seed}:{doc_id}:{gk}")
    return r.randint(1, max(4, 3 * cap)) if heavy(r, MORE_ROWS) else 0


def _row_value(it: dict, i: int, gk: tuple, p: Profile, rng: random.Random, vals: "Values", cls: str,
               fill_rows: dict, pct_plan: dict):
    """표 행 칸 하나의 값 (i 번째 줄)."""
    label = it.get("label") or ""
    kind = it.get("kind") or "text"
    if it.get("source"):
        return SRC.value(it["source"], p, rng, {**it, "class": cls}, vals, row=i)
    if kind == "percent":
        plan = pct_plan.setdefault(gk, _split100(rng, max(1, fill_rows[gk])))
        return str(plan[i])
    return vals.by_kind(kind, label)


def _in_unit(value, it: dict):
    """칸에 단위(천원·만원 …)가 인쇄돼 있으면 금액을 그 단위로 나눈 글자로."""
    unit = it.get("unit")
    if value is None or unit not in ("천원", "만원", "백만원", "억원") or it.get("source") == "rule:fixed":
        return value
    from .schema import korean_number

    amount = korean_number(str(value))
    if amount is None:
        try:
            amount = float(re.sub(r"[^0-9.+-]", "", str(value)))
        except ValueError:
            return value
    factor = {"천원": 1000, "만원": 10000, "백만원": 1000000, "억원": 100000000}[unit]
    return f"{amount / factor:,.4f}".rstrip("0").rstrip(".")


def _signer_name(label: str, it: dict, vals: "Values", rng: random.Random) -> str | None:
    """서명 칸에 쓰는 이름. 칸에 누구의 것인지(who: customer·agent·family·related·corp·bank, corp 면 what: ceo) 적었으면 그 사람
    (은행·직원 칸은 직원 이름이거나 빈칸), 없으면 키 설명으로 (대리인 칸은 대개 빈칸, 법인·상호 칸은 상호, 나머지는 고객)."""
    p = vals.p
    who, what = it.get("who"), it.get("what")
    if who == "bank":
        return K.make_name(rng, rng.choice("MF"))[0] if rng.random() < 0.5 else None
    if who == "corp":
        return p.corporation.ceo.name if what == "ceo" else p.corporation.name
    if who in ("agent", "family", "related"):
        return vals.std(f"{who}.name") if rng.random() < 0.6 else None   # 함께 오지 않으면 빈칸
    if who == "customer":
        return p.person.name
    n = norm(label)
    is_agent = bool(re.search(r"대리인|수임인|보호자|법정대리", n)) or bool(AGENT_SEC.search(norm(it.get("section") or "")))
    return None if is_agent and rng.random() < 0.85 else (p.corporation.name if re.search(r"법인|상호|회사", n) else p.person.name)


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
            if it.get("file"):   # 올린 도장 사진 (글자는 사진 그대로, 이름이 서류와 다를 수 있다)
                mk["seal_img"] = M.image_url(it)
            else:
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
    from . import formdir

    for path in formdir.hf_layouts():
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
    """overlay(image) 서식: docgen/forms/img_*/ 와 (설정했으면) DOCGEN_PRIVATE_FORMS/img_*/ 의 layout.json (docgen/formdir.py).
    studio 가져오기에서 견본 그림으로 만든 서식이다. 이미 등록된 ID 는 건너뛴다 (여러 번 불러도 된다)."""
    from . import formdir
    from .registry import REGISTRY, DocSpec

    n = 0
    for d in formdir.image_dirs():
        if d.name not in REGISTRY:
            REGISTRY[d.name] = image_spec(d)
            n += 1
    return n


def image_spec(d: Path):
    """이미지 서식 폴더 → 등록 정보 (layout.json 의 이름·쪽 방향)."""
    from .registry import DocSpec

    lay = json.loads((d / "layout.json").read_text(encoding="utf-8"))

    def generate(p: Profile, rng: random.Random, _id=d.name) -> dict:
        return build_form(_id, p, rng)

    pg = lay["pages"][0]
    page = "a4_landscape" if pg["width"] > pg["height"] else "a4"
    return DocSpec(d.name, lay.get("name") or d.name, "imported", "internal", "_real_form.html.j2",
                   generate, page, False,
                   f"가져온 서식 이미지 위에 기재 (묶음 {lay.get('from_batch', '-')}"
                   f"{', 내부 전용' if lay.get('private') else ''})")


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
