"""가족관계·주민등록 서류 (주민등록표 등본/초본, 가족관계등록부 증명서)."""
from ..registry import doc
from ._common import *  # noqa: F401,F403

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


def _surname(per: Person) -> str:
    return per.name[:len(per.name) - 2]


def _bon(p: Profile, per: Person, role: str) -> str:
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


def _rrn(per: Person, masked: bool) -> str:
    return K.mask_rrn(per.rrn) if masked else per.rrn


def _ymd(d: date) -> str:
    return f"{d.year}년 {d.month:02d}월 {d.day:02d}일"


def _member(p: Profile, per: Person, who: str, label: str, masked: bool) -> dict:
    return {
        "relation": label,
        "name": per.name,
        "name_hanja": per.hanja,
        "birth": _ymd(per.birth),
        "rrn": _rrn(per, masked),
        "gender": per.gender_ko,
        "bon": _bon_of(p, who),
    }


def _family_issuer(rng: random.Random, p: Profile) -> dict:
    """가족관계등록부 증명서 발급 정보 (방문 / 인터넷)."""
    if rng.random() < 0.4:
        return {"issuer": "대법원 전자가족관계등록시스템", "doc_check_no": issue_no(rng, 16)}
    a = p.person.address
    office = district_office(a) if rng.random() < 0.7 else " ".join(x for x in (a.sido, a.sigungu, a.dong + "장") if x)
    return {
        "issuer": office,
        "issue_time": f"{rng.randint(9, 17):02d}시 {rng.randint(0, 59):02d}분",
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

@doc("resident_registration_copy", "주민등록표 등본", "family")
def resident_registration_copy(p: Profile, rng: random.Random) -> dict:
    """주민등록표 등본 (세대 전체)."""
    moved_in, home = p.address_history[-1]
    masked = rng.random() < 0.5
    head_key = _head(p)
    head = p.person if head_key == "person" else p.spouse
    dfmt = rng.choice(["dash", "dot"])
    members = []

    def add(per: Person, rel: str, d: date, reason: str):
        members.append({
            "no": str(len(members) + 1), "relation": rel, "name": per.name, "name_hanja": per.hanja,
            "rrn": _rrn(per, masked), "moved_in": D(d, dfmt), "reason": reason,
        })

    add(head, "본인", moved_in, "전입")
    if p.spouse is not None:
        other = p.spouse if head_key == "person" else p.person
        md = _marriage_date(p)
        if md > moved_in:  # 혼인 후 세대주 주소로 전입
            joined = min(md + timedelta(days=rng.randint(0, 40)), p.issue_date - timedelta(days=10))
            add(other, "배우자", joined, rng.choice(["전입", "전입", "세대합가"]))
        else:
            add(other, "배우자", moved_in, "전입")
    child_style = rng.random() < 0.8
    for c in sorted(p.children, key=lambda x: x.birth):
        rel = "자" if child_style else ("아들" if c.gender == "M" else "딸")
        if c.birth > moved_in:
            add(c, rel, c.birth + timedelta(days=rng.randint(3, 25)), "출생등록")
        else:
            add(c, rel, moved_in, "전입")
    out = {
        "household_head": {"name": head.name, "name_hanja": head.hanja},
        "household_formed": {"reason": rng.choice(["전입세대구성", "전입세대구성", "세대분리"] + (["세대합가"] if len(members) > 1 else [])),
                              "date": D(moved_in, dfmt)},
        "current_address": {"address": home.road_full, "moved_in": D(moved_in, dfmt), "reason": "전입"},
        "members": members,
    }
    out.update(_resident_issuer(rng, p))
    return out


@doc("resident_registration_abstract", "주민등록표 초본", "family")
def resident_registration_abstract(p: Profile, rng: random.Random) -> dict:
    """주민등록표 초본 (개인 인적사항 + 주소 변동 이력)."""
    per = p.person
    masked = rng.random() < 0.4
    dfmt = rng.choice(["dash", "dot"])
    head_key = _head(p)
    married = _marriage_date(p) if p.spouse else None
    hist = p.address_history
    rows = []
    for i, (d, a) in enumerate(hist):
        last = i == len(hist) - 1
        if i == 0 and rng.random() < 0.6:
            rel = f"{p.father.name}의 자"
        elif last and head_key == "spouse":
            rel = f"{p.spouse.name}의 배우자"
        elif married and d >= married and head_key == "spouse":
            rel = f"{p.spouse.name}의 배우자"
        else:
            rel = f"{per.name}의 본인"
        rows.append({
            "no": str(i + 1),
            "address": a.road_full if d.year >= 2014 or rng.random() < 0.5 else f"{a.jibun_full} {a.detail}".strip(),
            "moved_in": D(d, dfmt),
            "changed": D(d + timedelta(days=rng.randint(0, 12)), dfmt),
            "reason": "전입" if i else rng.choice(["전입", "최초 주소"]),
            "head_relation": rel,
            "status": "거주자",
        })
    out = {
        "person": {"name": per.name, "name_hanja": per.hanja, "rrn": _rrn(per, masked)},
        "history_scope": rng.choice(["전체 포함", "최근 5년"]) if len(rows) <= 3 else "전체 포함",
        "addresses": rows,
    }
    out.update(_resident_issuer(rng, p))
    return out


# ---------------------------------------------------------------------------
# 가족관계등록부 증명서
# ---------------------------------------------------------------------------

@doc("family_relation_certificate", "가족관계증명서", "family")
def family_relation_certificate(p: Profile, rng: random.Random) -> dict:
    """가족관계증명서(일반)."""
    full = rng.random() < 0.3  # 주민등록번호 뒷자리 모두 표시 신청
    me = _member(p, p.person, "person", "본인", masked=not full and rng.random() < 0.5)
    fam = [_member(p, p.father, "father", "부", not full), _member(p, p.mother, "mother", "모", not full)]
    if p.spouse is not None:
        fam.append(_member(p, p.spouse, "spouse", "배우자", not full))
    for c in sorted(p.children, key=lambda x: x.birth):
        fam.append(_member(p, c, "child", "자녀", not full))
    out = {"self": me, "family": fam}
    out.update(_fam_common(rng, p))
    return out


@doc("basic_certificate", "기본증명서", "family")
def basic_certificate(p: Profile, rng: random.Random) -> dict:
    """기본증명서(일반)."""
    per = p.person
    me = _member(p, per, "person", "본인", masked=rng.random() < 0.5)
    sido, sigungu, _z, dongs, _r = rng.choice(K.REGIONS) if rng.random() < 0.5 else \
        next(x for x in K.REGIONS if x[0] == p.address_history[0][1].sido)
    place = " ".join(x for x in (sido, sigungu) if x)
    if rng.random() < 0.4:
        place += f" {rng.choice(dongs)}"
    reported = per.birth + timedelta(days=rng.randint(3, 30))
    out = {
        "self": me,
        "birth": {"place": place, "reported": _ymd(reported), "reporter": rng.choice(["부", "부", "모"])},
    }
    out.update(_fam_common(rng, p))
    return out


@doc("marriage_relation_certificate", "혼인관계증명서", "family")
def marriage_relation_certificate(p: Profile, rng: random.Random) -> dict:
    """혼인관계증명서(일반). 미혼이면 본인만 표시된다."""
    full = rng.random() < 0.3
    out = {"self": _member(p, p.person, "person", "본인", masked=not full and rng.random() < 0.5)}
    if p.spouse is not None:
        out["spouse"] = _member(p, p.spouse, "spouse", "배우자", not full)
        md = _marriage_date(p)
        office_addr = p.address_history[-1][1] if rng.random() < 0.5 else p.person.address
        out["marriage"] = {
            "reported": _ymd(md),
            "spouse_name": p.spouse.name,
            "spouse_rrn": _rrn(p.spouse, not full),
            "office": office_addr.region,
        }
    out.update(_fam_common(rng, p))
    return out
