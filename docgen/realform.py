"""원본 서식 오버레이 — 하나은행 공개 서식 PDF 를 그대로 배경으로 깔고, 손님이 쓴 것처럼 값을 얹는다.

서식 모양을 HTML 로 다시 그리지 않으므로 이미지 속 서식은 원본과 똑같다. 값을 쓸 자리는
scripts/extract_form_layout.py 가 PDF 에서 뽑은 add_template/layouts/<분류>/<No>.json 을 쓴다.

  text   빈 칸에 글자          → f(키)  값은 프로필(성명·주소·계좌…)이나 항목명으로 만든다
  check  □ 보기 묶음           → 고른 보기 □ 위에 V/✓/■ 표시, 정답은 고른 보기 글자
  date   "  년  월  일" 빈칸    → 숫자만 채우고 정답은 "2026년 1월 31일"
  sign   "(서명 또는 인)" 자리  → 이름 + 도장/서명/빈칸
  copy   자필 기재란            → 회색 안내 문구를 손글씨로 따라 쓴다

글씨체는 서류마다 손글씨(나눔손글씨 펜·붓, 하이멜로디, 감자꽃) 또는 인쇄체(전산 입력)에서 고른다.
배경 이미지와 손글씨 글꼴은 렌더러(image.py)가 https://docgen.local/ 주소로 넘겨준다.
"""
from __future__ import annotations

import json
import random
import re
import unicodedata
from datetime import timedelta
from functools import lru_cache
from pathlib import Path

from . import korean as K
from .entities import Profile

ROOT = Path(__file__).resolve().parent.parent
LAYOUTS = ROOT / "add_template" / "layouts"
FONTS = ROOT / "fonts"
CACHE = Path.home() / ".cache" / "docgen" / "bg"
HOST = "https://docgen.local/"
PX = 96 / 72          # PDF pt → CSS px
BG_ZOOM = 2 * PX      # 배경 해상도 = 렌더러 device_scale_factor(2) 에 맞춘다
BANK = "하나은행"

HAND_FONTS = ["NanumPen", "NanumBrush", "HiMelody", "GamjaFlower"]
# 손글씨 글꼴마다 글자 몸집이 달라 같은 칸 높이에서 키우는 비율
HAND_SCALE = {"NanumPen": 1.3, "NanumBrush": 1.3, "HiMelody": 1.05, "GamjaFlower": 1.0}
PRINT_FONTS = ["'Nanum Gothic'", "'NanumBarunGothic'", "'Noto Sans CJK KR'", "'Nanum Myeongjo'", "'NanumGothicCoding'"]
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
    return json.loads(layout_path(no).read_text(encoding="utf-8"))


def background_png(no: int, page: int) -> bytes:
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


def serve(url: str) -> tuple[bytes, str] | None:
    """https://docgen.local/bg/169/0.png, https://docgen.local/fonts/NanumPen.woff2 → (내용, MIME)."""
    if not url.startswith(HOST):
        return None
    path = url[len(HOST):].split("?")[0]
    if m := re.fullmatch(r"bg/(\d+)/(\d+)\.png", path):
        return background_png(int(m.group(1)), int(m.group(2))), "image/png"
    if m := re.fullmatch(r"fonts/([A-Za-z]+)\.woff2", path):
        f = FONTS / f"{m.group(1)}.woff2"
        if f.exists():
            return f.read_bytes(), "font/woff2"
    return None


# ---------------------------------------------------------------------------
# 항목명 → 키·값
# ---------------------------------------------------------------------------

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    s = re.sub(r"\([^)]*\)|\[[^\]]*\]", "", s)   # 괄호 설명 빼기: 매수비율(%) → 매수비율
    return re.sub(r"[\s:：*※·.,]+", "", s)


# 항목명(norm) 정규식 → 표준 키. 위에서부터 처음 맞는 것.
KEY_RULES: list[tuple[str, str]] = [
    (r"^(영문(성명|이름|명)|성명영문|EnglishName|NameinEnglish)$", "customer.name_en"),
    (r"^(대리인|수임인)(성명|명)?$", "agent.name"),
    (r"^(성명|이름|고객명|성명또는상호|가입자|가입자명|가입자성명|신청인|신청인성명|신청인명|본인|본인성명|예금주|"
     r"예금주명|위임인|위임인성명|의뢰인|신고인|차주|차주성명|채무자|고객성명|명의인|Name)$", "customer.name"),
    (r"^(생년월일|DateofBirth)", "customer.birth"),
    (r"^(주민등록번호|실명번호|주민번호|실명확인번호)", "customer.rrn"),
    (r"^(휴대전화|휴대폰|휴대폰번호|핸드폰|핸드폰번호|휴대전화번호|HP|연락처|전화번호|연락전화|Tel|Mobile)$",
     "customer.phone"),
    (r"^(자택전화|자택전화번호|집전화)$", "customer.home_phone"),
    (r"^(이메일|이메일주소|E-?[Mm][Aa][Ii][Ll](주소|Address)?|e-?mail|전자우편|전자우편주소)$", "customer.email"),
    (r"^(자택주소|주소|현주소|주소지|거주지주소|Address)$", "customer.address"),
    (r"^(직장주소|회사주소|근무지주소)$", "employer.address"),
    (r"^(직장전화|회사전화|직장전화번호|근무처전화)$", "employer.phone"),
    (r"^(회사명|직장명|근무처|근무처명|직장|소속|사용자명)$", "employer.name"),
    (r"^(부서|부서명|소속부서)$", "employer.department"),
    (r"^(직위|직급|직책)$", "employer.position"),
    (r"^(입사일|입사일자|입사연월일)$", "employer.hire_date"),
    (r"^(직업|직업구분)$", "customer.job"),
    (r"^(국적|Nationality)$", "customer.nationality"),
    (r"^(우편번호)$", "customer.zipcode"),
    (r"^(상호|법인명|기업명|업체명|사업장명|상호명|기업체명|법인단체명|단체명|법인명칭|CompanyName)$", "company.name"),
    (r"^(사업자등록번호|사업자번호|고유번호)$", "company.biz_no"),
    (r"^(법인등록번호|법인번호)$", "company.corp_no"),
    (r"^(대표자|대표자명|대표자성명|대표이사)$", "company.ceo"),
    (r"^(소재지|사업장소재지|본점소재지|사업장주소|본점주소)$", "company.address"),
    (r"^(업태)$", "company.biz_type"),
    (r"^(업종|종목)$", "company.biz_item"),
    (r"^(설립일|설립연월일|개업일)$", "company.established"),
    (r"^(계좌번호|출금계좌|출금계좌번호|입금계좌|입금계좌번호|결제계좌|결제계좌번호|퇴직연금계좌번호|IRP계좌번호|"
     r"계좌|해지계좌번호|이전계좌번호|AccountNo)$", "account"),
    (r"^(관계|본인과의관계|위임인과의관계)$", "agent.relation"),
    (r"^(작성일|작성일자|신청일|신청일자|신고일|신고일자|일자|년월일|Date)$", "date"),
]
KEY_RX = [(re.compile(rx), key) for rx, key in KEY_RULES]

# 표준 키가 아닌 항목: 항목명 끝말로 값의 종류를 정한다
KIND_RULES = [
    # 값을 쓰지 않는 칸: 단위만 남은 라벨, 예/아니오 칸, 은행 칸, 동의서 표의 머리글
    (r"^(|년|월|일|원|금|소|매|갋|계|예|아니오|Yes|No|당행|타행|현금|수입|고정|전기|금기|전기말|금기말|은행사용란|"
     r"영업점장|점검자|점검일자|확인여부|대상여부|접수번호|접수일|처리일|처리기간|실행자아이디|담당자인|■.*|-.*)$", "skip"),
    (r"(인감|서명|날인|도장|^인$|인/서명)", "seal"),
    (r"(비고|특기사항|기타$|^기타|내용$|변경전|변경후|요청사항)", "note"),
    (r"(외화금액|외화|USD|US\$|^Amount$)", "fx_amount"),
    (r"(비율|이율|금리|요율|지분율|율$|률$)", "percent"),
    (r"(사업자(등록)?번호|BusinessRegistrationNo)", "biz_no"),
    (r"(여권번호|PassportNo)", "passport"),
    (r"(수표번호|어음번호|증서.*번호)", "check_no"),
    (r"(일자|년월일|만기일|개시일|종료일|시작일|날짜|기한|기일|만기|일$|Date)", "date"),
    (r"(금액|대금|가액|잔액|원금|이자|합계|수수료|보증금|한도|총액|부담금|급여액|월급|소득|매출|공급가|입금액|단가|이전액)", "amount"),
    (r"(환율)", "rate"),
    (r"(통화|Currency)", "currency"),
    (r"(계좌)", "account"),
    (r"(전화|연락처|휴대|팩스|FAX|PhoneNo|Tel)", "phone"),
    (r"(번호|No$|코드|ID$)", "number"),
    (r"(수량|건수|횟수|개수|매수$|기간\(월\))", "count"),
    (r"(품목|(?<!상)품명|제품명|모델명|규격|제조사|물품)", "goods"),
    (r"(상품명|펀드명|상품|예금종류|예금과목|예금종별|^종류$|^종별$)", "product"),
    (r"(수표종류|수표어음)", "check_kind"),
    (r"(과목)", "loan_subject"),
    (r"(상환방법)", "repay"),
    (r"(사유|목적|용도)", "reason"),
    (r"(은행|기관명|금융회사|금융기관|운용관리|자산관리)", "bank"),
    (r"(개설점|취급점|지점|지급지|영업점)", "branch"),
    (r"(국가|국명|Country)", "country"),
    (r"(이메일|E-?[Mm]ail|전자우편)", "email"),
    (r"(주소|소재지)", "address"),
    (r"(기업명|업체명|회사명|법인명|상호|거래처|차입처|지사명|사업자명|채권양도인|발행인|추심의뢰인|수취인|신고자|"
     r"Applicant|보증자|협력기업|명칭)", "company"),
    (r"(담당자|주주명|한글명|성명|이름|명의인)", "person"),
]
KIND_RX = [(re.compile(rx), k) for rx, k in KIND_RULES]

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
    for rx, key in KEY_RX:
        if rx.match(n):
            return key
    return None


def kind_of(label: str, unit: str | None, hint: str | None) -> str:
    if unit in ("원", "천원", "백만원", "만원", "억원", "원정"):
        return "amount"
    if unit == "%":
        return "percent"
    if unit in ("개월", "년", "회", "건", "명", "주", "개", "매", "좌", "세", "일간", "개년"):
        return "count"
    n = norm(label)
    for rx, k in KIND_RX:
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
        if v is None:
            return None
        self.cache[key] = v()
        return self.cache[key]

    def by_kind(self, kind: str, label: str) -> str | None:
        p, r = self.p, self.r
        if kind in ("skip", "seal"):
            return None
        if kind == "note":
            return r.choice(REASONS) if r.random() < 0.15 else None
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
            return str(r.choice([1, 2, 3, 6, 12, 24, 36, 60]))
        if kind == "product":
            pool = PRODUCTS.get(self.cls) or PRODUCTS["기본"]
            return r.choice(pool)
        if kind == "reason":
            return r.choice(REASONS) if r.random() < 0.7 else None
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
        return None  # 뜻을 모르는 칸은 비워 둔다 (실제 서식도 빈 칸이 많다)


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
    lay = load_layout(no)
    cls = lay["class"].split("/")[0]
    vals = Values(p, rng, cls)
    hand = rng.random() < 0.72
    hf = rng.choice(HAND_FONTS)
    style = {
        "hand": hand,
        "scale": HAND_SCALE[hf] if hand else 1.0,
        "font": f"'{hf}'" if hand else rng.choice(PRINT_FONTS),
        "ink": rng.choice(INKS) if hand else rng.choice(["#111", "#1a1a1a", "#222"]),
        "base": rng.uniform(17, 22) if hand else rng.uniform(12, 14),
        "mark": rng.choice(["V", "V", "✓", "✔", "■", "O"]),
        "seal": rng.choice(["#d11", "#c00", "#e0312b", "#b22222"]),
        "fill": rng.uniform(0.75, 0.97),       # 선택 칸을 채울 확률
    }
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
                    fill_rows[gk] = rng.choice([0, 1, 1, 2, 2, 3]) if rng.random() < 0.85 else n_rows
                    fill_rows[gk] = min(fill_rows[gk], n_rows)
                key_base = f"{norm(it['group'])}_목록" if norm(it.get("group") or "") else "목록"
                key = re.sub(r"[^\w.]", "", f"{key_base}.{i}.{norm(label) or 'value'}")
                kind = kind_of(label, it.get("unit"), it.get("hint"))
                if i >= fill_rows[gk]:
                    value = None
                elif kind == "percent":
                    plan = pct_plan.setdefault(gk, _split100(rng, max(1, fill_rows[gk])))
                    value = str(plan[i])
                else:
                    value = vals.by_kind(kind, label) if kind != "reason" else vals.by_kind("product", label)
            else:
                skey = key_of(label)
                kind = kind_of(label, it.get("unit"), it.get("hint"))
                sec = norm(it.get("section") or "")
                if skey and AGENT_SEC.search(sec) and skey.startswith("customer."):
                    skey = "agent." + skey.split(".", 1)[1]   # 대리인 구역의 성명·생년월일 …
                elif skey and FOREIGN_SEC.search(sec) and (skey.startswith("customer.") or skey == "account"):
                    skey = "foreign." + (skey.split(".", 1)[1] if "." in skey else "account")  # 받는 분
                if kind == "seal" and not skey:   # '인감', '서명/날인' 칸 → 도장·서명 자리
                    x = rng.random()
                    nm = p.person.name
                    out.append({"t": "mark", "page": page, "key": uniq("signer"), "label": label, "name": nm,
                                "seal": x < 0.5, "sign": 0.5 <= x < 0.8, "rect": _px(it["rect"]),
                                "rot": round(rng.uniform(-12, 8), 1)})
                    continue
                if skey:
                    value = vals.std(skey)
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
            out.append(_visible(key, value, it["rect"], page, style, rng, label=label, align=align))
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
            key = uniq("check." + (norm(label) or norm(texts[0])[:12] or "item"))
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
            role = uniq("signer")
            if it.get("name"):
                out.append(_visible(f"{role}.name", name, it["name"], page, style, rng, label=label, align="center"))
            x = rng.random()
            seal = name is not None and x < 0.4
            sign = name is not None and not seal and x < 0.88
            out.append({"t": "mark", "page": page, "key": role, "label": label, "name": name or "",
                        "seal": seal, "sign": sign, "rect": _px(it["mark"]),
                        "rot": round(rng.uniform(-12, 8), 1), "sig_seed": rng.random()})
        elif t == "copy":
            filled = rng.random() < 0.85
            out.append(_visible(uniq("handwritten"), it["text"] if filled else None, it["rect"], page,
                                {**style, "hand": True, "font": f"'{hf}'", "scale": HAND_SCALE[hf]}, rng,
                                label=label or "자필기재", align="center"))
    pages = [{"w": round(pg["width"] * PX, 1), "h": round(pg["height"] * PX, 1),
              "bg": f"{HOST}bg/{no}/{i}.png"} for i, pg in enumerate(lay["pages"])]
    return {"no": no, "pages": pages, "items": out, "style": style, "class": lay["class"], "name": lay["name"]}


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


# 고객이 채우는 칸이 없는 인쇄물·내부 문서 (scripts/form_map.py 의 '제외' 판정과 같다)
EXCLUDE_KW = ["약관", "안내장", "체크리스트", "일반위험고지문", "상품설명서", "중요내용 설명서", "환전장부",
              "과목분류표", "관리대장", "제출서류 목록"]
# 22: 영문 통합제신고서 — PDF 글자 인코딩이 깨져(글자 코드가 밀려 있음) 항목명을 읽을 수 없다
EXCLUDE_NO = {12, 13, 14, 22, 40, 57, 143, 187, 200, 257, 404}


def fillable(lay: dict) -> int:
    return sum(1 for it in lay["items"] if it["t"] in ("text", "date", "sign", "copy")) + \
        sum(1 for it in lay["items"] if it["t"] == "check" and len(it["options"]) > 1)


def register_all() -> int:
    """레이아웃이 있는 서식을 모두 hf<No> 로 등록한다."""
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
    return n
