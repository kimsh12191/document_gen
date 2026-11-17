"""admission_letter: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/fx.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.fx import _Out, _addr_en, _fm, _student_name, _study  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("admission_letter", "입학허가서(Letter of Admission)", "fx")
def admission_letter(p: Profile, rng: random.Random) -> dict:
    """해외 대학 입학허가서 (유학생 송금 증빙). 조건부 입학·장학금·입학 연기는 프로필 단위(_study)."""
    s = _study(p)
    st, cur = s["student"], s["cur"]
    out = _Out({
        "university": {"name": s["uni"], "address": s["uni_addr"], "office": rng.choice(["Office of Admissions", "Office of Graduate Admissions" if s["level"] != "bachelor" else "Office of Undergraduate Admissions"]),
                       "email": f"admissions@{s['domain']}"},
        "letter_date": D(s["letter_date"], "en_long"),
        "student": {"name": _student_name(st), "dob": D(st.birth, rng.choice(["en_long", "en"])), "id": s["student_id"],
                    "nationality": "Republic of Korea", "address": _addr_en(st.address)},
        "program": s["program"],
        "degree": s["degree"],
        "term": s["term"],
        "start_date": D(s["start"], "en_long"),
        "duration": f"{s['years']} year{'s' if s['years'] > 1 else ''} (full-time)",
        "deposit_deadline": D(s["letter_date"] + timedelta(days=rng.randint(21, 45)), "en_long"),
        "signer": s["director"],
        "signer_title": "Director of Admissions",
    })
    sem = "academic year" if s["cc"] == "UK" else "semester"
    if s["conditions"]:
        out["admission_type"] = "CONDITIONAL ADMISSION"
        out["conditions"] = list(s["conditions"]["items"])
        out["condition_deadline"] = D(s["conditions"]["deadline"], "en_long")
    if s["scholarship"]:
        out["scholarship"] = {"name": s["scholarship"]["name"], "amount": f"{_fm(s['scholarship']['amount'], cur)} per {sem}"}
    if s["deferred_from"]:
        out["deferred_from"] = s["deferred_from"]
    many = heavy(rng, 0.2)
    if many or special(rng, "cost_estimate", 0.25):
        # 유학생 재정증명용 예상 학비·생활비 (1년)
        k = {"USD": 1, "GBP": 0.62, "CAD": 1.1, "AUD": 1.25}[cur]
        tu = s["tuition"] * (1 if s["cc"] == "UK" else 2)
        living = K.round_to(rng.uniform(14000, 22000) * k, 100)
        ins = K.round_to(rng.uniform(1500, 3200) * k, 10)
        books = K.round_to(rng.uniform(800, 2000) * k, 10)
        out["cost"] = {"tuition": _fm(tu, cur), "living": _fm(living, cur), "insurance": _fm(ins, cur),
                       "books": _fm(books, cur), "total": _fm(tu + living + ins + books, cur)}
    if many:
        out.opt["next_steps"] = True
    return out
