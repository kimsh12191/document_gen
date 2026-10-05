"""가족관계·주민등록 서류 (주민등록표 등본/초본, 가족관계등록부 증명서)."""
from ..registry import doc
from ._common import *  # noqa: F401,F403
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# 이 모듈 전용 헬퍼. 같은 프로필이면 서류가 달라도 같은 값이 나오도록
# (본, 등록기준지, 세대주, 혼인신고일 등) 프로필 seed 기반 Random 을 쓴다.
# ---------------------------------------------------------------------------

_BON = {
    "김": ["金海", "金海", "慶州", "光山", "金寧", "安東"], "이": ["全州", "全州", "慶州", "星州", "延安", "廣州"],
    "박": ["密陽", "密陽", "潘南", "咸陽"], "최": ["慶州", "全州", "海州", "江陵"], "정": ["東萊", "延日", "晋州", "慶州"],
    "강": ["晋州"], "조": ["漢陽", "白川", "咸安"], "윤": ["坡平", "海南"], "장": ["仁同", "安東", "玉山"],
    "임": ["羅州", "平澤", "醴泉"], "한": ["淸州"], "오": ["海州", "寶城"], "서": ["達城", "利川"],
    "신": ["平山", "高靈"], "권": ["安東"], "황": ["長水", "昌原"], "안": ["順興", "竹山"], "송": ["礪山", "恩津"],
    "류": ["文化", "豊山"], "전": ["旌善", "天安"], "홍": ["南陽", "豊山"], "고": ["濟州"], "문": ["南平"],
    "양": ["南原", "濟州"], "손": ["密陽", "慶州"], "배": ["盆城", "星山"], "백": ["水原"], "허": ["金海", "陽川"],
    "남": ["宜寧"], "심": ["靑松"], "노": ["光山", "交河"], "하": ["晋州"], "곽": ["玄風"], "성": ["昌寧"],
    "차": ["延安"], "주": ["新安"], "우": ["丹陽"], "구": ["綾城"], "민": ["驪興"], "진": ["驪陽"], "나": ["羅州"],
    "지": ["忠州"], "엄": ["寧越"], "채": ["平康"], "원": ["原州"], "천": ["潁陽"], "방": ["溫陽"], "공": ["曲阜"],
    "현": ["延州"], "함": ["江陵"], "변": ["草溪"], "염": ["坡州"], "여": ["咸陽"], "추": ["秋溪"], "도": ["星州"],
    "석": ["忠州"], "선": ["寶城"], "설": ["慶州"], "마": ["長興"], "길": ["海平"], "연": ["谷山"], "위": ["長興"],
    "표": ["新昌"], "명": ["西蜀"], "기": ["幸州"], "반": ["巨濟"], "왕": ["開城"], "금": ["奉化"], "옥": ["宜寧"],
    "남궁": ["咸悅"], "황보": ["永川"], "제갈": ["南陽"], "선우": ["太原"],
}
_BON_FALLBACK = ["金海", "慶州", "全州", "密陽", "晋州", "安東"]


def _surname(per) -> str:
    return per.name[:len(per.name) - 2]


def _bon(p: Profile, per, role: str) -> str:
    """본(本). 부계(본인·부·자녀는 부의 본)는 같은 값이 나온다."""
    r = random.Random(f"bon:{p.seed}:{role}:{_surname(per)}")
    return r.choice(_BON.get(_surname(per), _BON_FALLBACK))


def _husband(p: Profile) -> Person:
    return p.person if p.person.gender == "M" or p.spouse is None else p.spouse


def _bon_of(p: Profile, who: str) -> str:
    if who in ("person", "father"):
        return _bon(p, p.father, "paternal")
    if who == "mother":
        return _bon(p, p.mother, "mother")
    if who == "spouse":
        return _bon(p, p.spouse, "spouse")
    # 자녀: 아버지(남편)의 본
    return _bon(p, p.father, "paternal") if _husband(p) is p.person else _bon(p, p.spouse, "spouse")


def _reg_base(p: Profile) -> str:
    """등록기준지 (지번 주소)."""
    r = random.Random(f"regbase:{p.seed}")
    if r.random() < 0.35:
        a = p.address_history[0][1]
        return a.jibun_full
    sido, sigungu, _z, dongs, _roads = r.choice(K.REGIONS)
    jibun = f"{r.randint(1, 999)}" + (f"-{r.randint(1, 30)}" if r.random() < 0.5 else "")
    return " ".join(x for x in (sido, sigungu, r.choice(dongs), jibun) if x)


def _head(p: Profile) -> str:
    """세대주: 'person' 또는 'spouse'."""
    if p.spouse is None:
        return "person"
    return "spouse" if random.Random(f"head:{p.seed}").random() < 0.3 else "person"


def _marriage_date(p: Profile) -> date:
    r = random.Random(f"marriage:{p.seed}")
    lo = date(max(p.person.birth.year, p.spouse.birth.year) + 25, 1, 1)
    hi = p.issue_date - timedelta(days=200)
    if p.children:
        hi = min(hi, min(c.birth for c in p.children) - timedelta(days=300))
    lo = min(lo, hi - timedelta(days=30))
    return rand_date(r, lo, hi)


def _rrn(per, masked: bool) -> str:
    return K.mask_rrn(per.rrn) if masked else per.rrn


def _ymd(d: date) -> str:
    return f"{d.year}년 {d.month:02d}월 {d.day:02d}일"


def _member(p: Profile, per, who: str, label: str, masked: bool, bon: str | None = None,
            status: str | None = None) -> dict:
    """가족관계등록부 증명서의 인적사항 한 줄. 외국인(per.nationality 가 대한민국이 아님)은 주민등록번호·본 대신 국적."""
    out = {"relation": label, "name": per.name, "name_hanja": per.hanja, "birth": _ymd(per.birth)}
    foreign = getattr(per, "nationality", "대한민국") not in (None, "대한민국")
    if foreign:
        out["nationality"] = per.nationality
    else:
        out["rrn"] = _rrn(per, masked)
    out["gender"] = per.gender_ko
    if not foreign:
        out["bon"] = bon or _bon_of(p, who)
    if status:
        out["status"] = status
    if out["name_hanja"] is None:
        del out["name_hanja"]
    return out


# ---------------------------------------------------------------------------
# 한 고객의 '가족·주소 이력' (같은 프로필이면 등본·초본·가족관계 증명서가 모두 같은 이야기를 한다)
#   프로필(p.address_history, p.children ...)은 그대로 두고, 프로필 seed 기반 Random 으로
#   부모 사망·이혼/재혼·입양·개명·귀화·이사가 잦은 이력 등을 덧붙인다.
#   heavy()/special() 의 환경변수 강제(DOCGEN_HEAVY, DOCGEN_SPECIAL)도 그대로 따른다.
# ---------------------------------------------------------------------------

@dataclass
class _P:
    """서류에만 나오는 가족 (전 배우자, 전혼 자녀, 형제, 친생부모 등)."""
    name: str
    hanja: str | None
    birth: date
    rrn: str | None
    gender: str
    nationality: str = "대한민국"

    @property
    def gender_ko(self) -> str:
        return "남" if self.gender == "M" else "여"


def _yrs(d: date, n: int) -> date:
    try:
        return d.replace(year=d.year + n)
    except ValueError:
        return d.replace(year=d.year + n, day=28)


def _new_person(r: random.Random, gender: str, birth: date, surname_of=None) -> _P:
    name, hanja, _se, _ge = K.make_name(r, gender)
    if surname_of is not None:  # 성을 맞춘다 (자녀·형제)
        sur = _surname(surname_of)
        old = name[:len(name) - 2]
        name = sur + name[len(old):]
        hanja = surname_of.hanja[:len(sur)] + hanja[len(old):] if surname_of.hanja else hanja
    return _P(name, hanja, birth, K.rrn(r, birth, gender), gender)


def _new_addr(r: random.Random, near: Address | None = None) -> Address:
    """새 주소. near 를 주면 대개 같은 시·도 안에서 옮긴다."""
    regions = K.REGIONS
    if near is not None and r.random() < 0.65:
        regions = [x for x in K.REGIONS if x[0] == near.sido] or K.REGIONS
    sido, sigungu, zip2, dongs, roads = r.choice(regions)
    dong = r.choice(dongs)
    bno = str(r.randint(1, 650)) + (f"-{r.randint(1, 40)}" if r.random() < 0.3 else "")
    jibun = f"{r.randint(1, 1500)}" + (f"-{r.randint(1, 60)}" if r.random() < 0.6 else "")
    if r.random() < 0.55:
        bname = r.choice(K.APT_NAMES) + r.choice(K.APT_SUFFIX) + ("아파트" if r.random() < 0.5 else "")
        detail = f"{r.randint(101, 125)}동 {r.randint(1, 25)}{r.randint(1, 4):02d}호"
    else:
        bname = r.choice(["", "", "그린빌", "하이츠", "빌라", "맨션", "원룸", "주택"])
        detail = r.choice([f"{r.randint(1, 5)}0{r.randint(1, 4)}호", f"{r.randint(1, 5)}층", "", f"지하{r.randint(1, 2)}층"])
    return Address(sido, sigungu, dong, r.choice(roads), bno, jibun, detail, bname, f"{zip2}{r.randint(0, 999):03d}")


_FAMILY_COURT = {
    "서울특별시": "서울가정법원", "부산광역시": "부산가정법원", "대구광역시": "대구가정법원", "인천광역시": "인천가정법원",
    "광주광역시": "광주가정법원", "대전광역시": "대전가정법원", "울산광역시": "울산가정법원", "경기도": "수원가정법원",
    "세종특별자치시": "대전가정법원 세종지원", "강원특별자치도": "춘천지방법원", "충청북도": "청주지방법원",
    "충청남도": "대전가정법원 천안지원", "전북특별자치도": "전주지방법원", "전라남도": "광주가정법원 순천지원",
    "경상북도": "대구가정법원 포항지원", "경상남도": "창원지방법원", "제주특별자치도": "제주지방법원",
}

# 외국인 (전) 배우자: (한글 표기, 원지음 표기, 국적)
_FOREIGN_SPOUSE = {
    "F": [("응우옌티화", "NGUYEN THI HOA", "베트남"), ("쩐티란", "TRAN THI LAN", "베트남"), ("왕리나", "WANG LINA", "중국"),
          ("산토스마리아", "SANTOS MARIA", "필리핀"), ("다나카유키", "TANAKA YUKI", "일본"),
          ("이바노바안나", "IVANOVA ANNA", "러시아"), ("카리모바닐루파르", "KARIMOVA NILUFAR", "우즈베키스탄")],
    "M": [("스미스존", "SMITH JOHN", "미국"), ("다나카히로시", "TANAKA HIROSHI", "일본"), ("왕웨이", "WANG WEI", "중국"),
          ("응우옌반안", "NGUYEN VAN AN", "베트남"), ("밀러데이비드", "MILLER DAVID", "미국")],
}
_CN_BIRTHPLACE = ["중국 길림성 연길시", "중국 길림성 용정시", "중국 흑룡강성 하얼빈시", "중국 요녕성 심양시", "중국 길림성 도문시"]
_EMIGRATE_TO = ["미국", "캐나다", "호주", "뉴질랜드", "일본", "독일"]


def _alive(death: date | None, d: date) -> bool:
    return death is None or d < death


def _life(p: Profile) -> dict:
    """프로필 하나의 가족·주소 이야기 (결정론적)."""
    r = random.Random(f"life:{p.seed}")
    per = p.person
    L: dict = {"natur": None, "rename": None, "gender_fix": None, "adopted": None, "ex": None,
               "ex_children": [], "dead_child": None, "dead": {}, "siblings": []}
    hist_heavy = heavy(r, 0.3)            # 이사가 잦은 사람 (초본 20~40건)
    big = heavy(r, 0.25)                  # 세대원이 많은 세대 (부모·형제 동거 등)
    md = _marriage_date(p) if p.spouse else None
    L["married"] = md

    # --- 부모 사망 -------------------------------------------------------
    if special(r, "parent_deceased", 0.25 if per.age >= 45 else 0.1):
        who = r.choice(["father", "father", "mother", "both"])
        for w in (["father", "mother"] if who == "both" else [who]):
            par = getattr(p, w)
            hi = p.issue_date - timedelta(days=90)
            lo = min(max(_yrs(par.birth, 50), _yrs(per.birth, 3)), hi - timedelta(days=400))
            L["dead"][w] = rand_date(r, lo, hi)

    # --- 귀화 (중국 동포) ---------------------------------------------------
    first_home = p.address_history[0][0]
    if special(r, "naturalized", 0.03):
        L["natur"] = {"date": first_home - timedelta(days=r.randint(20, 300)), "prev": "중국",
                      "birthplace": r.choice(_CN_BIRTHPLACE)}
        L["natur"]["notified"] = L["natur"]["date"] + timedelta(days=r.randint(3, 20))

    # --- 입양 (본인이 일반입양된 경우: 프로필의 부모는 양부모, 친생부모는 같은 성의 친척) ----------
    if not L["natur"] and special(r, "adopted", 0.04):
        bf = _new_person(r, "M", rand_date(r, _yrs(per.birth, -36), _yrs(per.birth, -24)), surname_of=per)
        bm = _new_person(r, "F", rand_date(r, _yrs(per.birth, -34), _yrs(per.birth, -21)))
        L["adopted"] = {"father": bf, "mother": bm}

    # --- 개명 ------------------------------------------------------------
    if special(r, "name_change", 0.08):
        lo, hi = max(_yrs(per.birth, 20), date(1995, 1, 1)), p.issue_date - timedelta(days=200)
        if hi > lo:
            nm, hj, _a, _b = K.make_name(r, per.gender)
            old = _surname(per) + nm[len(nm) - 2:]
            old_hj = (per.hanja[:len(_surname(per))] + hj[len(hj) - 2:]) if per.hanja else None
            if old != per.name:
                permitted = rand_date(r, lo, hi)
                L["rename"] = {"old": old, "old_hanja": old_hj, "permitted": permitted,
                               "reported": min(permitted + timedelta(days=r.randint(3, 25)), p.issue_date - timedelta(days=150)),
                               "court": _FAMILY_COURT[p.address_history[-1][1].sido]}

    # --- 성별정정 (드묾) ----------------------------------------------------
    if special(r, "gender_correction", 0.015):
        lo, hi = max(_yrs(per.birth, 22), date(2006, 1, 1)), p.issue_date - timedelta(days=200)
        if hi > lo:
            permitted = rand_date(r, lo, hi)
            L["gender_fix"] = {"old_rrn": K.rrn(r, per.birth, "F" if per.gender == "M" else "M"), "permitted": permitted,
                               "reported": permitted + timedelta(days=r.randint(3, 20)),
                               "court": _FAMILY_COURT[per.address.sido]}

    # --- 이혼(전혼) / 재혼 ----------------------------------------------------
    if special(r, "divorce", 0.12):
        end = (md - timedelta(days=400)) if md else p.issue_date - timedelta(days=500)
        lo = _yrs(per.birth, 22)
        if L["natur"]:
            lo = max(lo, L["natur"]["date"])
        if end - lo > timedelta(days=800):
            m = rand_date(r, lo, end - timedelta(days=500))
            dv = rand_date(r, m + timedelta(days=400), end)
            g = "F" if per.gender == "M" else "M"
            eb = rand_date(r, _yrs(per.birth, -5), min(_yrs(per.birth, 6), _yrs(m, -19)))
            if special(r, "foreign_spouse", 0.25):
                ko, en, nat = r.choice(_FOREIGN_SPOUSE[g])
                ex = _P(ko, None, eb, None, g, nat)
                ex.original = en  # type: ignore[attr-defined]
            else:
                ex = _new_person(r, g, eb)
            kind = r.choice(["협의", "협의", "협의", "재판"])
            L["ex"] = {"person": ex, "married": m, "divorced": dv, "kind": kind,
                       "court": _FAMILY_COURT[r.choice(p.address_history)[1].sido],
                       "office": r.choice(p.address_history)[1].region,
                       "div_office": r.choice(p.address_history)[1].region}
            if special(r, "prev_marriage_child", 0.45) and dv - m > timedelta(days=500):
                # 자녀의 성: 본인이 부이면 본인의 성, 전 남편이 외국인이면 모(본인)의 성, 아니면 전 남편의 성
                sur = per if per.gender == "M" or ex.nationality != "대한민국" else ex
                for _ in range(r.choice([1, 1, 2])):
                    cb = rand_date(r, m + timedelta(days=300), dv - timedelta(days=60))
                    L["ex_children"].append(_new_person(r, r.choice("MF"), cb, surname_of=sur))

    # --- 사망한 자녀 (드묾) ----------------------------------------------------
    if md and special(r, "deceased_child", 0.03):
        lo, hi = md + timedelta(days=300), p.issue_date - timedelta(days=500)
        if hi > lo:
            cb = rand_date(r, lo, hi)
            c = _new_person(r, r.choice("MF"), cb, surname_of=_husband(p))
            L["dead_child"] = (c, rand_date(r, cb + timedelta(days=20), min(cb + timedelta(days=3650), p.issue_date - timedelta(days=60))))

    # --- 형제자매 (등본 부모 동거 세대용) ---------------------------------------
    mb = p.mother.birth
    for _ in range(r.choice([0, 1, 1, 1, 2, 2, 3])):
        lo = max(_yrs(mb, 20), _yrs(per.birth, -9))
        hi = min(_yrs(mb, 42), _yrs(per.birth, 9), p.issue_date - timedelta(days=400))
        if hi > lo:
            sb = rand_date(r, lo, hi)
            if abs((sb - per.birth).days) > 300:
                L["siblings"].append(_new_person(r, r.choice("MF"), sb, surname_of=p.father))
    L["siblings"].sort(key=lambda x: x.birth)

    # --- 세대 구성 ---------------------------------------------------------
    dead = L["dead"]
    H = p.address_history[-1][0]
    alive_now = [w for w in ("father", "mother") if w not in dead]
    mode, cores = "single", []
    if p.spouse is None:
        if big and alive_now and not L["natur"]:
            mode = "parents"
        elif big and L["siblings"]:
            mode = "siblings"
    else:
        mode = "family"
        if big:
            if _head(p) == "person":
                cores = [] if L["natur"] else alive_now
            else:
                cores = ["spouse_mother"]
    L["household"] = {"mode": mode, "co_parents": cores}
    if mode == "parents":
        F = rand_date(r, H - timedelta(days=5400), H - timedelta(days=60))
        L["household"]["formed"] = F
        fd = dead.get("father")
        if fd is None:
            head, chg = "father", None
        elif fd <= F:
            head, chg = "mother", None
        else:
            head, chg = "mother", fd + timedelta(days=r.randint(7, 60))
            chg = min(chg, p.issue_date - timedelta(days=5))
        L["household"].update(head=head, head_change=chg, father_until=fd)
    elif mode == "family" and _head(p) == "spouse" and md > H:
        # 혼인 전부터 살던 집에 배우자가 전입한 뒤 배우자로 세대주 변경
        jd = min(md + timedelta(days=r.randint(0, 40)), p.issue_date - timedelta(days=20))
        chg = min(jd + timedelta(days=r.choice([0, 0, r.randint(1, 90)])), p.issue_date - timedelta(days=10))
        L["household"].update(head="spouse", spouse_joined=jd, head_change=chg)
    else:
        L["household"].update(head="spouse" if mode == "family" and _head(p) == "spouse" else "person", head_change=None)

    # --- 주소 이력 --------------------------------------------------------
    base = [x for x in p.address_history[:-1] if x[0] < H] + [p.address_history[-1]]
    rows = []  # {"date", "addr", "addr_text", "reason", "status", "rel", "kind"}
    if hist_heavy:
        target = r.randint(20, 40)
        if not L["natur"]:  # 출생~성년 (부모 세대)
            start = per.birth + timedelta(days=r.randint(7, 30))
            k1 = r.randint(3, 7)
            span = (base[0][0] - timedelta(days=90) - start).days
            cands = list(range(300, max(301, span), 240))
            ds = [start] + [start + timedelta(days=o) for o in sorted(r.sample(cands, min(k1 - 1, len(cands))))]
            for j, d in enumerate(ds):
                rows.append({"date": d, "addr": _new_addr(r, rows[-1]["addr"] if rows else base[0][1]), "reason": "출생등록" if j == 0 and per.birth.year >= 1975 else "전입",
                             "kind": "child"})
        need = target - len(rows) - len(base)
        gaps = [(i, (base[i + 1][0] - base[i][0]).days) for i in range(len(base) - 1)]
        alloc = {i: 0 for i, _ in gaps}
        caps = {i: max(0, (g - 150) // 160) for i, g in gaps}
        for _ in range(max(0, need)):
            free = [i for i, _g in gaps if alloc[i] < caps[i]]
            if not free:
                break
            alloc[r.choices(free, [dict(gaps)[i] for i in free])[0]] += 1
        for i, (d, a) in enumerate(base):
            rows.append({"date": d, "addr": a, "reason": "전입", "kind": "profile", "idx": i})
            if i < len(base) - 1 and alloc[i]:
                g = dict(gaps)[i]
                cands = list(range(90, g - 90, 120))
                for o in sorted(r.sample(cands, min(alloc[i], len(cands)))):
                    rows.append({"date": d + timedelta(days=o), "addr": _new_addr(r, rows[-1]["addr"]), "reason": "전입",
                                 "kind": "extra"})
    else:
        for i, (d, a) in enumerate(base):
            rows.append({"date": d, "addr": a, "reason": "전입", "kind": "profile", "idx": i})

    # 세대주 및 관계
    ren = L["rename"]

    def my(d: date) -> str:
        return ren["old"] if ren and d < ren["permitted"] else per.name

    def parent_head(d: date) -> str:
        return p.father.name if _alive(dead.get("father"), d) else p.mother.name

    first_child = r.random() < 0.6
    hh = L["household"]
    for k, row in enumerate(rows):
        d = row["date"]
        last = k == len(rows) - 1
        if row["kind"] == "child" or (row["kind"] == "profile" and row["idx"] == 0 and first_child and not last
                                      and not L["natur"]):
            row["rel"] = f"{parent_head(d)}의 자"
        elif last and hh["mode"] == "parents":
            row["rel"] = f"{parent_head(d)}의 자"
        elif last and hh["head"] == "spouse":
            row["rel"] = f"{my(d)}의 본인" if hh.get("head_change") else f"{p.spouse.name}의 배우자"
        elif md and d >= md and _head(p) == "spouse" and hh["mode"] == "family":
            row["rel"] = f"{p.spouse.name}의 배우자"
        else:
            row["rel"] = f"{my(d)}의 본인"
        row["status"] = "거주자"
    # 세대주 변경 줄 (같은 주소)
    cur = rows[-1]
    if hh.get("head_change") and hh["head_change"] > cur["date"]:
        if hh["mode"] == "parents":
            rel = f"{p.mother.name}의 자"
        else:
            rel = f"{p.spouse.name}의 배우자"
        rows.append({"date": hh["head_change"], "addr": cur["addr"], "reason": "세대주변경", "status": "거주자",
                     "rel": rel, "kind": "head_change"})

    # 거주불명등록(말소)·재등록 / 국외이주 (같은 사람이 겪은 일이므로 프로필 단위로 정한다)
    def pick_gap(min_days: int, used: set) -> int | None:
        cand = [k for k in range(len(rows) - 1)
                if rows[k]["kind"] in ("profile", "extra") and rows[k + 1]["kind"] in ("profile", "extra")
                and (rows[k + 1]["date"] - rows[k]["date"]).days >= min_days and k not in used
                and rows[k]["date"] > _yrs(per.birth, 19)]
        return r.choice(cand) if cand else None

    used: set = set()
    events = []
    if special(r, "deregistration", 0.05):
        k = pick_gap(400, used)
        if k is not None:
            used.add(k)
            a = rows[k]["addr"]
            x = rows[k]["date"] + timedelta(days=r.randint(120, (rows[k + 1]["date"] - rows[k]["date"]).days - 120))
            if x < date(2010, 1, 1):  # 2009.10. 거주불명등록제 시행 전: 무단전출 말소
                events.append((k, {"date": x, "addr": None, "addr_text": "주민등록 말소", "reason": "무단전출말소",
                                   "status": "말소자", "rel": rows[k]["rel"], "kind": "event"}))
            else:
                admin = f"{a.region} {a.road} {r.randint(1, 300)} ({a.dong}주민센터, 행정상관리주소)"
                events.append((k, {"date": x, "addr": None, "addr_text": admin, "reason": "거주불명등록",
                                   "status": "거주불명자", "rel": rows[k]["rel"], "kind": "event"}))
            rows[k + 1]["reason"] = "재등록"
    if special(r, "emigration", 0.04):
        k = pick_gap(700, used)
        if k is not None:
            used.add(k)
            x = rows[k]["date"] + timedelta(days=r.randint(120, (rows[k + 1]["date"] - rows[k]["date"]).days - 365))
            to = r.choice(_EMIGRATE_TO)
            events.append((k, {"date": x, "addr": None, "addr_text": f"국외이주 ({to})", "reason": "국외이주신고",
                               "status": "말소자" if x < date(2015, 1, 22) else "재외국민", "rel": rows[k]["rel"],
                               "kind": "event"}))
            rows[k + 1]["reason"] = "재등록"
            L["emigrated"] = {"date": x, "to": to}
    for k, ev in sorted(events, key=lambda t: -t[0]):
        rows.insert(k + 1, ev)
    L["rows"] = rows
    L["current_reason"] = next(x["reason"] for x in rows if x["kind"] == "profile" and x["idx"] == len(base) - 1)
    return L


def _addr_text(row: dict, rng: random.Random) -> str:
    if row.get("addr") is None:
        return row["addr_text"]
    a = row["addr"]
    return a.road_full if row["date"].year >= 2014 or rng.random() < 0.5 else f"{a.jibun_full} {a.detail}".strip()


def _family_issuer(rng: random.Random, p: Profile) -> dict:
    """가족관계등록부 증명서 발급 정보 (방문 / 인터넷)."""
    time = f"{rng.randint(9, 17):02d}시 {rng.randint(0, 59):02d}분"
    if rng.random() < 0.4:  # 전자가족관계등록시스템(인터넷) 발급본은 전산운영책임관 명의
        return {"issuer": "법원행정처 전산정보중앙관리소 전산운영책임관",
                "issue_time": f"{rng.randint(0, 23):02d}시 {rng.randint(0, 59):02d}분",
                "applicant": p.person.name, "doc_check_no": issue_no(rng, 16)}
    a = p.person.address
    office = district_office(a) if rng.random() < 0.7 else " ".join(x for x in (a.sido, a.sigungu, a.dong + "장") if x)
    return {
        "issuer": office,
        "issue_time": time,
        "officer": K.make_name(rng, rng.choice("MF"))[0],
        "officer_phone": K.landline(rng, a.sido),
        "applicant": p.person.name,
    }


def _fam_common(rng: random.Random, p: Profile) -> dict:
    out = {"reg_base": _reg_base(p)}
    out.update(_family_issuer(rng, p))
    out["issue_date"] = D(p.issue_date, "kor")
    return out


def _resident_issuer(rng: random.Random, p: Profile) -> dict:
    """주민등록표 등·초본 발급 정보."""
    a = p.person.address
    internet = rng.random() < 0.5
    out = {
        "doc_no": issue_no(rng, 16) if internet else f"제 {rng.randint(1, 9999):04d} 호",
        "issue_date": D(p.issue_date, "kor"),
        "issuer": district_office(a) if internet or rng.random() < 0.3
        else " ".join(x for x in (a.sido, a.sigungu, a.dong + "장") if x),
        "applicant": p.person.name,
        "purpose": rng.choice(["금융기관 제출용", "금융기관제출", "대출신청", "은행 제출", "전세자금대출 신청"]),
    }
    if not internet:
        out["officer"] = K.make_name(rng, rng.choice("MF"))[0]
        out["officer_phone"] = K.landline(rng, a.sido)
    return out


# ---------------------------------------------------------------------------
# 주민등록표 등본 / 초본
# ---------------------------------------------------------------------------

def _sib_rel(head, sib) -> str:
    """세대주와 형제자매의 관계 표기."""
    if sib.birth < head.birth:
        if sib.gender == "M":
            return "형" if head.gender == "M" else "오빠"
        return "누나" if head.gender == "M" else "언니"
    return "동생"


@doc("resident_registration_copy", "주민등록표 등본", "family")
def resident_registration_copy(p: Profile, rng: random.Random) -> dict:
    """주민등록표 등본 (세대 전체). 부모·형제 동거, 세대주 변경, 동거인, 과거 주소 변동 포함 발급 등."""
    L = _life(p)
    hh = L["household"]
    moved_in, home = p.address_history[-1]
    masked = rng.random() < 0.5
    dfmt = "dash" if rng.random() < 0.85 else "dot"  # 정부24·주민센터 발급본은 2015-03-02 표기
    child_style = rng.random() < 0.8
    members = []
    cut = p.issue_date - timedelta(days=3)

    def add(per, rel: str, d: date, reason: str):
        members.append({
            "no": str(len(members) + 1), "relation": rel, "name": per.name, "name_hanja": per.hanja,
            "rrn": _rrn(per, masked), "moved_in": D(min(d, cut), dfmt), "reason": reason,
        })
        if per.hanja is None:
            del members[-1]["name_hanja"]

    def kid_rel(c) -> str:
        return "자" if child_style else ("아들" if c.gender == "M" else "딸")

    formed_reason = rng.choice(["전입세대구성", "전입세대구성", "세대분리"])
    if hh["mode"] == "parents":
        F = hh["formed"]
        head = p.father if hh["head"] == "father" else p.mother
        add(head, "본인", F, "전입")
        if hh["head"] == "father" and "mother" not in L["dead"]:
            add(p.mother, "배우자", F, "전입")
        for s in [x for x in L["siblings"] if x.birth < F]:
            add(s, kid_rel(s), F, "전입")
        add(p.person, kid_rel(p.person), moved_in, L["current_reason"])
        for s in [x for x in L["siblings"] if x.birth >= F]:
            add(s, kid_rel(s), s.birth + timedelta(days=rng.randint(3, 25)), "출생등록")
        if hh.get("head_change"):
            formed = ("세대주변경", hh["head_change"])
        else:
            formed = (formed_reason, F)
        head_since = F
    else:
        head = p.spouse if hh["head"] == "spouse" else p.person
        if hh["head"] == "spouse" and hh.get("head_change"):
            add(p.spouse, "본인", hh["spouse_joined"], rng.choice(["전입", "세대합가"]))
            add(p.person, "배우자", moved_in, L["current_reason"])
            formed = ("세대주변경", hh["head_change"])
            head_since = hh["spouse_joined"]
        else:
            head_since = moved_in
            add(head, "본인", moved_in, L["current_reason"] if head is p.person else "전입")
            if p.spouse is not None:
                other = p.spouse if head is p.person else p.person
                md = L["married"]
                if md > moved_in:  # 혼인 후 세대주 주소로 전입
                    joined = min(md + timedelta(days=rng.randint(0, 40)), p.issue_date - timedelta(days=10))
                    add(other, "배우자", joined, rng.choice(["전입", "전입", "세대합가"]))
                else:
                    add(other, "배우자", moved_in, "전입")
            formed = (rng.choice(["전입세대구성", "전입세대구성", "세대분리"] + (["세대합가"] if p.spouse else [])), moved_in)
        for c in sorted(p.children, key=lambda x: x.birth):
            if c.birth > moved_in:
                add(c, kid_rel(c), c.birth + timedelta(days=rng.randint(3, 25)), "출생등록")
            else:
                add(c, kid_rel(c), moved_in, "전입")
        # 부모 동거 (세대원이 많은 세대)
        late = [moved_in + timedelta(days=30), p.issue_date - timedelta(days=40)]
        for w in hh["co_parents"]:
            d = rand_date(rng, *late) if late[1] > late[0] else moved_in
            if w == "spouse_mother":
                sm = _new_person(rng, "F", rand_date(rng, _yrs(p.spouse.birth, -34), _yrs(p.spouse.birth, -22)))
                add(sm, "모", d, rng.choice(["전입", "세대합가"]))
            else:
                add(getattr(p, w), "부" if w == "father" else "모", d, rng.choice(["전입", "세대합가"]))
        if hh["mode"] == "siblings":
            for s in L["siblings"][:2]:
                add(s, _sib_rel(p.person, s), rand_date(rng, moved_in, max(moved_in, p.issue_date - timedelta(days=40))),
                    "전입")
    # 동거인 (친족이 아닌 세대원)
    if special(rng, "cohabitant", 0.06):
        lo = max(head_since, moved_in) + timedelta(days=10)
        hi = p.issue_date - timedelta(days=15)
        g = rng.choice("MF")
        b = rand_date(rng, date(1960, 1, 1), date(2003, 12, 31))
        add(_new_person(rng, g, b), "동거인", rand_date(rng, lo, hi) if hi > lo else hi, "전입")

    # 과거의 주소 변동 사항 포함 발급(선택)
    past = []
    many = heavy(rng, 0.3)
    if many or rng.random() < 0.35:
        if head is p.person:
            src = [x for x in L["rows"] if x["kind"] in ("profile", "extra") and x["date"] < moved_in]
            src = [(x["date"], x, x["reason"]) for x in src]
        else:  # 세대주(배우자·부모)의 이전 주소
            n = rng.randint(6, 18) if many else rng.randint(1, 3)
            d = head_since - timedelta(days=rng.randint(200, 900))
            src = []
            for _ in range(n):
                if d < _yrs(head.birth, 18):
                    break
                src.append((d, {"addr": _new_addr(rng), "date": d}, "전입"))
                d -= timedelta(days=rng.randint(180, 1400))
            src.reverse()
        if not many:
            src = src[-rng.randint(1, 3):]
        for i, (d, row, reason) in enumerate(src):
            past.append({"no": str(i + 1), "address": _addr_text(row, rng), "moved_in": D(d, dfmt), "reason": reason})
    out = {
        "household_head": {"name": head.name, "name_hanja": head.hanja},
        "household_formed": {"reason": formed[0], "date": D(formed[1], dfmt)},
        "past_addresses": past,
        "current_address": {"address": home.road_full, "moved_in": D(moved_in if head is p.person else head_since, dfmt),
                            "reason": L["current_reason"] if head is p.person else "전입"},
        "members": members,
    }
    out.update(_resident_issuer(rng, p))
    return out


@doc("resident_registration_abstract", "주민등록표 초본", "family")
def resident_registration_abstract(p: Profile, rng: random.Random) -> dict:
    """주민등록표 초본 (개인 인적사항 + 주소 변동 이력). 이사가 잦은 사람은 여러 쪽이 된다."""
    L = _life(p)
    per = p.person
    masked = rng.random() < 0.4
    dfmt = "dash" if rng.random() < 0.85 else "dot"
    src = L["rows"]
    scope = "전체 포함"
    if len(src) <= 6 and rng.random() < 0.3:
        scope = "최근 5년"
        cut = _yrs(p.issue_date, -5)
        keep = [x for x in src if x["date"] >= cut]
        src = keep or src[-1:]
    rows = []
    for i, x in enumerate(src):
        changed = x["date"] + timedelta(days=rng.choice([0, 0, rng.randint(1, 13)]))  # 변동일=신고일(14일 이내)
        rows.append({
            "no": str(i + 1),
            "address": _addr_text(x, rng),
            "moved_in": D(x["date"], dfmt),
            "changed": D(min(changed, p.issue_date - timedelta(days=1)), dfmt),
            "reason": x["reason"],
            "head_relation": x["rel"],
            "status": x["status"],
        })
    out = {
        "person": {"name": per.name, "name_hanja": per.hanja, "rrn": _rrn(per, masked)},
    }
    # 개인 인적사항 변경 내용 (개명, 성별정정에 따른 주민등록번호 정정)
    changes = []
    ren, gf = L["rename"], L["gender_fix"]
    if ren:
        old = f"{ren['old']}({ren['old_hanja']})" if ren["old_hanja"] else ren["old"]
        new = f"{per.name}({per.hanja})" if per.hanja else per.name
        changes.append((ren["reported"], f"성명 {old} → {new}", "개명"))
    if gf:
        changes.append((gf["reported"], f"주민등록번호 {_rrn(_P('', None, per.birth, gf['old_rrn'], 'M'), masked)} → "
                                         f"{_rrn(per, masked)}", "주민등록번호정정(성별정정)"))
    if changes:
        out["person_changes"] = [{"no": str(i + 1), "content": c, "changed": D(d, dfmt), "reason": rs}
                                 for i, (d, c, rs) in enumerate(sorted(changes))]
    out["history_scope"] = scope
    out["addresses"] = rows
    out.update(_resident_issuer(rng, p))
    return out


# ---------------------------------------------------------------------------
# 가족관계등록부 증명서 (일반 / 상세)
#   일반: 부모, 배우자, 생존한 현재 혼인 중의 자녀 / 기본: 출생·사망·국적상실 / 혼인: 현재 혼인
#   상세: 모든 자녀(전혼·사망 자녀), 친생부모 / 기본: 개명·국적취득·정정 등 / 혼인: 혼인·이혼 전체
# ---------------------------------------------------------------------------

def _detail(rng: random.Random) -> bool:
    return heavy(rng, 0.2) or special(rng, "detail_cert", 0.15)


def _foreign_parents(p: Profile, L: dict):
    """귀화자(중국 동포)의 부모는 중국 국적 외국인으로 기록된다."""
    if not L["natur"]:
        return p.father, p.mother
    f = _P(p.father.name, p.father.hanja, p.father.birth, None, "M", "중국")
    m = _P(p.mother.name, p.mother.hanja, p.mother.birth, None, "F", "중국")
    return f, m


@doc("family_relation_certificate", "가족관계증명서", "family")
def family_relation_certificate(p: Profile, rng: random.Random) -> dict:
    """가족관계증명서 (일반/상세). 사망한 부모, 전혼 자녀, 입양(친생부모) 등."""
    L = _life(p)
    detail = _detail(rng)
    full = rng.random() < 0.3  # 주민등록번호 뒷자리 모두 표시 신청
    me = _member(p, p.person, "person", "본인", masked=not full and rng.random() < 0.5)
    dead = L["dead"]
    fa, mo = _foreign_parents(p, L)
    adopted = L["adopted"] if detail else None
    fam = [_member(p, fa, "father", "양부" if adopted else "부", not full, status="사망" if "father" in dead else None),
           _member(p, mo, "mother", "양모" if adopted else "모", not full, status="사망" if "mother" in dead else None)]
    if adopted:
        bon = _bon_of(p, "person")
        fam.append(_member(p, adopted["father"], "bio", "친생부", not full, bon=bon))
        fam.append(_member(p, adopted["mother"], "bio", "친생모", not full,
                           bon=_bon(p, adopted["mother"], "biomother")))
    if p.spouse is not None:
        fam.append(_member(p, p.spouse, "spouse", "배우자", not full))
    kids = [(c, _bon_of(p, "child"), None) for c in p.children]
    if detail:
        ex = L["ex"]
        for c in L["ex_children"]:
            father_is_me = p.person.gender == "M"
            kb = _bon_of(p, "person") if father_is_me or (ex and ex["person"].nationality != "대한민국") \
                else _bon(p, ex["person"], "exhusband")
            kids.append((c, kb, None))
        if L["dead_child"]:
            kids.append((L["dead_child"][0], _bon_of(p, "child"), "사망"))
    for c, kb, st in sorted(kids, key=lambda x: x[0].birth):
        fam.append(_member(p, c, "child", "자녀", not full, bon=kb, status=st))
    out = {"cert_type": "상세" if detail else "일반", "self": me, "family": fam}
    out.update(_fam_common(rng, p))
    return out


@doc("basic_certificate", "기본증명서", "family")
def basic_certificate(p: Profile, rng: random.Random) -> dict:
    """기본증명서 (일반/상세). 상세에는 개명·국적취득·성별정정 기록이 나온다."""
    L = _life(p)
    per = p.person
    detail = _detail(rng)
    me = _member(p, per, "person", "본인", masked=rng.random() < 0.5)
    nat = L["natur"]
    if nat:
        birth = {"place": nat["birthplace"]}
    else:
        sido, sigungu, _z, dongs, _r = rng.choice(K.REGIONS) if rng.random() < 0.5 else \
            next(x for x in K.REGIONS if x[0] == p.address_history[0][1].sido)
        place = " ".join(x for x in (sido, sigungu) if x)
        if rng.random() < 0.4:
            place += f" {rng.choice(dongs)}"
        late = special(rng, "late_birth_report", 0.05)  # 출생신고가 늦은 경우 (과태료 대상)
        reported = per.birth + timedelta(days=rng.randint(40, 700) if late else rng.randint(3, 30))
        birth = {"place": place, "reported": _ymd(reported), "reporter": rng.choice(["부", "부", "모"])}
    out = {"cert_type": "상세" if detail else "일반", "self": me, "birth": birth}
    if detail and nat:
        out["naturalization"] = {"acquired": _ymd(nat["date"]), "reason": "귀화허가", "prev_nationality": nat["prev"],
                                 "notified": _ymd(nat["notified"]), "notifier": "법무부장관"}
    if detail and L["rename"]:
        ren = L["rename"]
        out["name_change"] = {"permitted": _ymd(ren["permitted"]), "court": ren["court"], "old_name": ren["old"],
                              "reported": _ymd(ren["reported"])}
    if detail and L["gender_fix"]:
        gf = L["gender_fix"]
        new, old = per.gender_ko, "여" if per.gender == "M" else "남"
        out["correction"] = {"permitted": _ymd(gf["permitted"]), "court": gf["court"],
                             "content": f"성별 {old} → {new}", "reported": _ymd(gf["reported"])}
    out.update(_fam_common(rng, p))
    return out


def _spouse_name(per) -> str:
    orig = getattr(per, "original", None)
    return f"{per.name}({orig})" if orig else per.name


@doc("marriage_relation_certificate", "혼인관계증명서", "family")
def marriage_relation_certificate(p: Profile, rng: random.Random) -> dict:
    """혼인관계증명서 (일반/상세). 일반은 현재 혼인만, 상세는 이혼한 혼인(외국인 배우자 포함)까지 표시."""
    L = _life(p)
    detail = _detail(rng)
    full = rng.random() < 0.3
    out = {"cert_type": "상세" if detail else "일반",
           "self": _member(p, p.person, "person", "본인", masked=not full and rng.random() < 0.5)}
    ex = L["ex"]
    if detail and ex:
        e = ex["person"]
        wed = {"kind": "혼인", "reported": _ymd(ex["married"]), "spouse_name": _spouse_name(e)}
        if e.nationality != "대한민국":
            wed.update(spouse_birth=_ymd(e.birth), spouse_nationality=e.nationality)
        else:
            wed["spouse_rrn"] = _rrn(e, not full)
        wed["office"] = ex["office"]
        div = {"kind": "이혼"}
        if ex["kind"] == "재판":
            jd = ex["divorced"] - timedelta(days=rng.randint(10, 40))
            div.update(judgment_date=_ymd(jd), court=ex["court"])
        div.update(reported=_ymd(ex["divorced"]), spouse_name=_spouse_name(e))
        if e.nationality != "대한민국":
            div["spouse_nationality"] = e.nationality
        else:
            div["spouse_rrn"] = _rrn(e, not full)
        div["office"] = ex["div_office"]
        out["past_events"] = [wed, div]
    if p.spouse is not None:
        out["spouse"] = _member(p, p.spouse, "spouse", "배우자", not full)
        md = L["married"]
        office_addr = p.address_history[-1][1] if rng.random() < 0.5 else p.person.address
        out["marriage"] = {
            "reported": _ymd(md),
            "spouse_name": p.spouse.name,
            "spouse_rrn": _rrn(p.spouse, not full),
            "office": office_addr.region,
        }
    out.update(_fam_common(rng, p))
    return out
