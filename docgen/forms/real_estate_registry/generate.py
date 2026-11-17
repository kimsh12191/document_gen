"""real_estate_registry: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/real_estate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.real_estate import _Row, _area, _facts, _rd, _reg_no  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


def _unit_label(f: dict) -> str:
    """'래미안아파트 제101동 제12층 제1203호'"""
    s = f["bname"]
    if f["dong_no"]:
        s += f" 제{f['dong_no']}동"
    return f"{s} 제{f['floor']}층 제{f['ho']}호"


@doc("real_estate_registry", "등기사항전부증명서(집합건물)", "real_estate")
def real_estate_registry(p: Profile, rng: random.Random) -> dict:
    """등기사항전부증명서(말소사항 포함) - 집합건물. 표제부·갑구·을구.

    이력이 많은 물건(소유권 이전·근저당 설정/말소 반복)은 갑구·을구가 길어져 여러 쪽이 된다.
    말소된 사항은 빨간 실선으로 지우고, 말소 등기('3번근저당권설정등기말소')는 별도 순위번호로 적는다."""
    f = _facts(p)
    a, pr, hist = f["a"], f["pr"], f["hist"]
    view_dt = p.issue_date
    loc = f"{a.jibun_full} {f['bname']}" + (f" 제{f['dong_no']}동" if f["dong_no"] else "")
    loc += f"\n[도로명주소]\n{a.region} {a.road} {a.building_no}"
    nf = f["total_floors"]
    under = rng.random() < 0.7
    area1 = round(f["floor_area"] * rng.uniform(0.75, 0.95), 2)
    detail = (f"{pr.structure}\n(철근)콘크리트지붕 {nf}층 {f['usage_full']}\n"
              + (f"지하1층 {_area(round(f['floor_area'] * rng.uniform(0.6, 1.1), 2))}㎡\n" if under else "")
              + f"1층 {_area(area1)}㎡\n"
              + (f"2층 {_area(f['floor_area'])}㎡" if nf <= 2 else f"2층~{nf}층 각 {_area(f['floor_area'])}㎡"))
    loc_old = f"{a.jibun_full} {f['bname']}" + (f" 제{f['dong_no']}동" if f["dong_no"] else "")
    buildings = [_Row(display_no="1", receipt=_rd(f["preserve"]), location=loc_old if f["road_reg"] else loc,
                      detail=detail, cause=f["drawing_no"])]
    if f["road_reg"]:  # 도로명주소 직권 등기: 1번은 말소(실선), 2번에 도로명주소 추가
        buildings[0].struck = True
        buildings.append(_Row(display_no="2", location=loc, cause=f"도로명주소\n{_rd(f['road_reg'])} 등기"))
    land = {"display_no": "1", "location": f"1. {a.jibun_full}", "category": "대",
            "area": f"{_area(f['land_total'])}㎡", "cause": f"{_rd(f['preserve'])} 등기"}
    unit = {"display_no": "1", "receipt": _rd(f["preserve"]), "unit_no": f"제{f['floor']}층 제{f['ho']}호",
            "detail": f"{pr.structure}\n{_area(pr.exclusive_area)}㎡", "cause": f["drawing_no"]}
    land_right = {"display_no": "1", "kind": "1 소유권대지권", "ratio": f"{_area(f['land_total'])}분의 {_area(pr.land_area)}",
                  "cause": f"{_rd(f['land_right_date'])} 대지권\n{_rd(f['preserve'])} 등기"}
    t = view_dt
    hh, mm, ss = rng.randint(8, 18), rng.randint(0, 59), rng.randint(0, 59)
    out = {
        "unique_no": pr.unique_no,
        "property": f"{a.jibun_full} {_unit_label(f)}",
    }
    rows = len(hist["gapgu"]) * 3 + len(hist["eulgu"]) * 5
    pages = 1 + max(0, (rows - 30) // 70)  # 증명서 본문 쪽수 (요약 쪽 번호 표시용 어림)
    summary = rng.random() < 0.18  # 마지막 장: 주요 등기사항 요약 (참고용)
    if summary:
        out["summary"] = _registry_summary(hist)
        out["page_label"] = f"{pages + 1}/{pages + 1}"
    else:
        out.update({"registry_office": courthouse(a), "buildings": buildings, "land": land, "unit": unit, "land_right": land_right,
                    "gapgu": hist["gapgu"], "eulgu": hist["eulgu"]})
    if rng.random() < 0.5:
        out["view_datetime"] = f"{t.year}년{t.month:02d}월{t.day:02d}일 {hh:02d}시{mm:02d}분{ss:02d}초"
    else:
        out["issue_no"] = "".join(str(rng.randint(0, 9)) for _ in range(20))
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        out["confirm_no"] = "-".join("".join(rng.choice(letters) for _ in range(4)) for _ in range(2)) + f"-{rng.randint(0, 9999):04d}"
        out["issue_date_short"] = f"{t.year}/{t.month:02d}/{t.day:02d}"
        if not summary:
            out["issue_date"] = f"{t.year}년 {t.month}월 {t.day}일"
            out["fee"] = "1,000원"
    return out


def _registry_summary(hist: dict) -> dict:
    """주요 등기사항 요약(참고용): 말소되지 않은 사항만."""
    owners = []
    for s in sorted(hist["state"], key=lambda s: s["pi"]["name"]):
        pi = s["pi"]
        owners.append({"name": f"{pi['name']} ({'소유자' if s['share'] == '단독소유' else '공유자'})", "reg_no": _reg_no(pi),
                       "share": s["share"], "address": pi["addr"], "rank": s["rank"]})
    target = ", ".join(hist["cur_names"]) if len(hist["cur_names"]) < 3 else f"{hist['cur_names'][0]} 등"

    def main_text(e: dict) -> str:
        row = e["row"]
        if e["type"] == "mortgage":
            mx = f"금{won(e['cur_max'])}" if e.get("cur_max") else row["max_amount"]
            who = (e.get("cur_mortgagee") or row["mortgagee"]).split()[0]
            return f"채권최고액 {mx}  근저당권자 {who}"
        if e["type"] == "jeonse":
            return f"전세금 {row['deposit']}  전세권자 {e['who']}"
        if e["type"] == "lease":
            return f"임차보증금 {row['deposit']}  임차권자 {e['who']}"
        if "claim_amount" in row:
            return f"청구금액 {row['claim_amount']}  채권자 {row['creditor'].split()[0]}"
        if "right_holder" in row:
            return f"권리자 {row['right_holder']}"
        return f"채권자 {row.get('creditor', '').split()[0]}"

    def items(evs: list) -> list:
        return [{"rank": e["rank"], "purpose": e["row"]["purpose"], "receipt": e["row"]["receipt"].replace("\n", " "),
                 "main": main_text(e), "target_owner": target} for e in sorted(evs, key=lambda e: int(e["rank"]))]
    return {"owners": owners, "gapgu_rights": items(hist["open_gap"]), "rights": items(hist["open_eul"])}
