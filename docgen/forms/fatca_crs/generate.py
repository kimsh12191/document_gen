"""fatca_crs: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_account.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_account import _bank, _date, _staff  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.docs.bank_form_loan import _foreigner, _solo  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


_OTHER_RES = [("일본 (JAPAN)", "JAPAN"), ("중국 (CHINA)", "CHINA"), ("싱가포르 (SINGAPORE)", "SINGAPORE"),
              ("캐나다 (CANADA)", "CANADA"), ("호주 (AUSTRALIA)", "AUSTRALIA")]


@doc("fatca_crs", "해외금융계좌 납세자 확인서(개인)", "bank_form", category="internal")
def fatca_crs(p: Profile, rng: random.Random) -> dict:
    """FATCA/CRS 본인확인서(개인/개인사업자용) — 국제조세조정법·금융정보자동교환 이행규정에 따른 자기확인서."""
    per = p.person
    kind = rng.choices(["kr", "us", "other"], weights=[88, 6, 6])[0]
    res = []
    birth_place = "대한민국 (KOREA)"
    nationality = "대한민국 (KOREA)"
    if kind == "us":
        category = rng.choice(["미국 시민권자(이중국적자 포함)", "미국 영주권자", "미국 세법상 미국 거주자"])
        res.append({"country": "미국 (U.S.A.)",
                    "tin": f"{rng.randint(100, 665)}-{rng.randint(10, 99)}-{rng.randint(1000, 9999)}"})
        if category.startswith("미국 시민권자"):
            nationality = "대한민국, 미국"
            if rng.random() < 0.6:
                birth_place = "미국 (U.S.A.)"
    elif kind == "other":
        category = "미국 이외의 해외 거주자"
        country = rng.choice(_OTHER_RES)[0]
        reason = rng.choices(["A", "B", "C"], weights=[2, 6, 2])[0]
        r = {"country": country, "no_tin_reason": reason}
        if reason == "B":
            r["reason_detail"] = rng.choice(["단기 체류로 납세자번호 발급 대상 아님", "납세자번호 발급 신청 중"])
        res.append(r)
    else:
        category = "해당사항 없음"
    if kind != "kr" and special(rng, "multi_residence", 0.4):  # 거주관할권이 둘 이상
        for country, _ in rng.sample([x for x in _OTHER_RES if x[0] not in [r["country"] for r in res]], rng.randint(1, 2)):
            r = {"country": country}
            if rng.random() < 0.5:
                r["tin"] = "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([9, 10, 12])))
            else:
                r["no_tin_reason"] = rng.choice(["A", "C"])
            res.append(r)
    data = {
        "bank": _bank(p),
        "holder": {
            "name": per.name,
            "surname_en": per.surname_en,
            "given_en": per.given_en,
            "birth": D(per.birth, rng.choice(["dot", "dash"])),
            "birth_place": birth_place,
            "nationality": nationality,
            "mobile": per.mobile,
            "address": per.address.road_full,
        },
        "residence_category": category,
        "residences": res,
        "date": _date(p, rng),
        "signature": per.name,
        "bank_use": {"branch": p.bank_branch, **_staff(rng)},
    }
    h = data["holder"]
    if _solo(p) and special(rng, "foreigner", 0.08):  # 국내 거주 외국인 (CRS: 본국 세법상 거주자)
        fo = _foreigner(p, rng)
        h.update({"name": fo["name"], "surname_en": fo["surname_en"], "given_en": fo["given_en"],
                  "birth": D(fo["birth"], rng.choice(["dot", "dash"])), "mobile": fo["mobile"],
                  "birth_place": f"{fo['nationality']} ({fo['nationality_en']})",
                  "nationality": f"{fo['nationality']} ({fo['nationality_en']})"})
        data["signature"] = fo["name"]
        if fo["nationality_en"] == "UNITED STATES":
            data["residence_category"] = "미국 시민권자(이중국적자 포함)"
            data["residences"] = [{"country": "미국 (U.S.A.)",
                                   "tin": f"{rng.randint(100, 665)}-{rng.randint(10, 99)}-{rng.randint(1000, 9999)}"}]
        else:
            data["residence_category"] = rng.choice(["미국 이외의 해외 거주자", "해당사항 없음"])
            data["residences"] = [{"country": f"{fo['nationality']} ({fo['nationality_en']})",
                                   "tin": "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([9, 10, 12])))}] \
                if data["residence_category"] != "해당사항 없음" else []
    if special(rng, "no_check", 0.08):  # 해외 거주자 여부 체크 누락 (내국인)
        if data["residence_category"] == "해당사항 없음":
            data["residence_category"] = None
    if special(rng, "sparse", 0.1):  # 선택 기재란 공란
        h[rng.choice(["mobile", "birth_place"])] = None
    return data
