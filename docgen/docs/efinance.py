"""전자금융 서식 (인터넷·모바일뱅킹, 문자통지, 전자어음).

하나은행 공개 서식에서 뽑은 기재란 명세를 따랐다
(add_template/field_specs/전자금융/{335,337,340,373}.json).

제도 기준
  전자금융거래법 — 접근매체(보안카드·OTP·인증서) 등록, 이체한도 신고
  전자어음의 발행 및 유통에 관한 법률 — 전자어음 등록·교부
"""
from ..banks import since
from ..registry import doc
from ._common import *  # noqa: F401,F403

SERVICES_PERSONAL = ["인터넷뱅킹", "모바일뱅킹", "폰뱅킹", "텔레뱅킹", "오픈뱅킹"]
SERVICES_CORP = ["인터넷뱅킹(기업)", "펌뱅킹", "CMS", "전자어음", "외환업무", "급여이체", "자금관리(CMS Plus)"]
MEDIA = ["보안카드", "OTP(카드형)", "OTP(토큰형)", "공동인증서", "금융인증서", "모바일 OTP"]


def _staff(rng: random.Random) -> dict:
    return {"clerk": K.make_name(rng, rng.choice("MF"))[0],
            "manager": K.make_name(rng, rng.choice("MF"))[0]}


def _date(p: Profile, rng: random.Random) -> str:
    return D(p.issue_date, rng.choice(["kor", "kor", "kor_short", "dot"]))


def _media(p: Profile, rng: random.Random, n: int = 1) -> list[str]:
    pool = [x for x in MEDIA if x != "모바일 OTP" or since(p.issue_date, "mobile_otp")]
    return rng.sample(pool, k=min(n, len(pool)))


def _limits(rng: random.Random, corporate: bool) -> dict:
    """이체한도 — 전자금융거래 이용자별 신고 한도 (1회 / 1일)."""
    if corporate:
        once = rng.choice([100_000_000, 300_000_000, 500_000_000, 1_000_000_000])
        daily = once * rng.choice([2, 3, 5])
    else:
        once = rng.choice([10_000_000, 20_000_000, 50_000_000, 100_000_000])
        daily = once * rng.choice([1, 2, 5])
    return {"once": K.won(once), "daily": K.won(daily)}


# ---------------------------------------------------------------------------
# 개인 전자금융 서비스 신청서
# ---------------------------------------------------------------------------


@doc("efinance_application_personal", "개인 전자금융 서비스 신청서", "efinance", category="internal")
def efinance_application_personal(p: Profile, rng: random.Random) -> dict:
    """개인 고객의 인터넷·모바일뱅킹 가입과 접근매체·이체한도를 신고하는 서식."""
    per = p.person
    kind = rng.choices(["신규", "변경", "해지", "재발급"], weights=[58, 20, 10, 12])[0]
    services = rng.sample(SERVICES_PERSONAL, k=rng.randint(1, 3))
    if "인터넷뱅킹" not in services and rng.random() < 0.6:
        services.insert(0, "인터넷뱅킹")
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "kind": kind,
        "customer": {
            "name": per.name,
            "birth": D(per.birth, "dot"),
            "phone": per.mobile,
            "email": per.email,
            "address": per.address.road_short,
        },
        "user_id": f"{per.given_en.lower()}{rng.randint(100, 9999)}",
        "services": services,
        "account": p.accounts[0].number,
        "media": _media(p, rng, rng.randint(1, 2)),
        "media_no": f"{rng.randint(10, 99)}-{rng.randint(100000, 999999)}",
        "limits": _limits(rng, False),
        "sms_notice": rng.choices(["신청", "신청하지 않음"], weights=[76, 24])[0],
        "overseas_ip": rng.choices(["차단", "허용"], weights=[82, 18])[0],
        "delay_transfer": rng.choices(["신청", "신청하지 않음"], weights=[42, 58])[0],
        "date": _date(p, rng),
        "signature": per.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 기업 전자금융서비스 신청서 (은행용)
# ---------------------------------------------------------------------------


@doc("efinance_application_corp", "기업 전자금융서비스 신청서", "efinance", category="internal")
def efinance_application_corp(p: Profile, rng: random.Random) -> dict:
    """법인 고객의 기업 인터넷뱅킹·펌뱅킹 등 전자금융서비스 이용을 신청하는 서식."""
    c = p.corporation
    manager = p.directors[0]
    services = rng.sample(SERVICES_CORP, k=rng.randint(2, 4))
    users = [{
        "name": manager.name,
        "birth": D(manager.birth, "dot"),
        "role": "이체 담당자",
        "user_id": f"{c.name_en.split()[0][:4].lower()}{rng.randint(10, 99)}",
        "media": _media(p, rng, 1)[0],
    }]
    if rng.random() < 0.7:
        approver = p.directors[1] if len(p.directors) > 1 else p.person
        users.append({
            "name": approver.name,
            "birth": D(approver.birth, "dot"),
            "role": "승인 책임자",
            "user_id": f"{c.name_en.split()[0][:4].lower()}{rng.randint(10, 99)}",
            "media": _media(p, rng, 1)[0],
        })
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "kind": rng.choices(["신규", "변경", "해지"], weights=[62, 28, 10])[0],
        "company": {
            "name": c.name,
            "biz_no": c.biz_no,
            "corp_no": c.corp_no,
            "ceo": c.ceo.name,
            "phone": c.phone,
            "email": c.email,
            "address": c.address.road_short,
        },
        "services": services,
        "account": p.accounts[0].number,
        "users": users,
        "approval": rng.choices(["단독 승인", "복수 승인(2인)", "복수 승인(3인)"], weights=[38, 48, 14])[0],
        "limits": _limits(rng, True),
        "fee_account": p.accounts[0].number,
        "contract_no": f"EB{rng.randint(1000000, 9999999)}",
        "date": _date(p, rng),
        "signature": c.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 입출금 거래내역 문자통지서비스 신청서
# ---------------------------------------------------------------------------


@doc("sms_notice_application", "입출금 거래내역 문자통지서비스 신청서", "efinance", category="internal")
def sms_notice_application(p: Profile, rng: random.Random) -> dict:
    """계좌 입출금 내역을 문자(SMS)·알림톡으로 통지받는 서비스를 신청하는 서식."""
    per = p.person
    ways = ["SMS(문자)", "알림톡"] if since(p.issue_date, "kakao_notice") else ["SMS(문자)"]
    accounts = [{"number": a.number, "kind": rng.choice(["입출금예금", "저축예금", "급여통장"])}
                for a in p.accounts[:rng.randint(1, min(2, len(p.accounts)))]]
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "kind": rng.choices(["신규", "변경", "해지"], weights=[66, 22, 12])[0],
        "customer": {"name": per.name, "birth": D(per.birth, "dot"),
                     "phone": per.mobile, "address": per.address.road_short},
        "accounts": accounts,
        "way": rng.choice(ways),
        "target": rng.choices(["입금·출금 모두", "출금만", "입금만"], weights=[62, 30, 8])[0],
        "threshold": K.won(rng.choice([10_000, 50_000, 100_000, 500_000, 1_000_000])),
        "fee": K.won(rng.choice([0, 300, 500, 900])),
        "fee_account": p.accounts[0].number,
        "notify_phone": per.mobile,
        "date": _date(p, rng),
        "signature": per.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 전자어음 교부 신청서
# ---------------------------------------------------------------------------


@doc("electronic_note_issue", "전자어음 교부 신청서", "efinance", category="internal")
def electronic_note_issue(p: Profile, rng: random.Random) -> dict:
    """전자어음의 발행 한도를 배정받고 전자어음관리기관에 등록하는 교부 신청서."""
    c = p.corporation
    limit = K.round_to(c.revenue * rng.uniform(0.05, 0.25), 10_000_000)
    limit = max(50_000_000, min(limit, 10_000_000_000))
    count = rng.choice([10, 20, 30, 50, 100])
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "kind": rng.choices(["신규 교부", "한도 증액", "재교부"], weights=[58, 28, 14])[0],
        "company": {
            "name": c.name,
            "biz_no": c.biz_no,
            "corp_no": c.corp_no,
            "ceo": c.ceo.name,
            "phone": c.phone,
            "address": c.address.road_short,
            "established": D(c.established, "dot"),
        },
        "credit_grade": rng.choice(["BBB+", "BBB", "BBB-", "BB+", "BB", "A-"]),
        "limit": K.won(limit),
        "count": f"{count}매",
        "term": rng.choice(["발행일로부터 3개월", "발행일로부터 6개월", "발행일로부터 1년"]),
        "account": p.accounts[0].number,
        "manager": {"name": p.directors[0].name, "phone": p.directors[0].mobile,
                    "department": "재무팀"},
        "registry": "금융결제원 전자어음관리기관",
        "date": _date(p, rng),
        "signature": c.name,
        "staff": _staff(rng),
    }
