"""tuition_invoice: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/fx.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
import math
from docgen.docs.fx import _Out, _fm, _student_name, _study  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


def _num_date(d: date, cc: str) -> str:
    """미국 MM/DD/YYYY, 그 외 DD/MM/YYYY."""
    return f"{d:%m/%d/%Y}" if cc == "US" else f"{d:%d/%m/%Y}"


_COURSES = {  # 전공: (과목 코드, 과목명들)
    "Business Administration": ("BUS", ["Financial Accounting", "Managerial Economics", "Marketing Management", "Organizational Behavior",
                                        "Operations Management", "Corporate Finance", "Business Analytics", "Strategic Management"]),
    "Computer Science": ("CS", ["Data Structures", "Algorithms", "Operating Systems", "Computer Networks", "Machine Learning",
                                "Database Systems", "Software Engineering", "Theory of Computation"]),
    "Economics": ("ECON", ["Microeconomic Theory", "Macroeconomic Theory", "Econometrics I", "Mathematical Methods for Economists",
                           "International Trade", "Labor Economics", "Public Finance"]),
    "Psychology": ("PSYC", ["Introduction to Psychology", "Research Methods", "Cognitive Psychology", "Developmental Psychology",
                            "Social Psychology", "Statistics for Behavioral Sciences"]),
    "Mechanical Engineering": ("ME", ["Statics", "Thermodynamics I", "Fluid Mechanics", "Engineering Mathematics", "Materials Science",
                                      "Engineering Drawing and CAD"]),
    "Communication Design": ("DES", ["Typography I", "Visual Communication", "Drawing for Designers", "Digital Imaging",
                                     "Design History", "Color Theory"]),
    "Data Science": ("DS", ["Statistical Learning", "Data Engineering", "Probability and Inference", "Deep Learning",
                            "Data Visualization", "Optimization Methods"]),
    "Finance": ("FIN", ["Investments", "Derivatives", "Financial Econometrics", "Fixed Income Securities", "Corporate Valuation",
                        "Risk Management"]),
    "Public Policy": ("PPOL", ["Policy Analysis", "Microeconomics for Public Policy", "Quantitative Methods", "Public Management",
                               "Program Evaluation", "Politics of Policymaking"]),
    "Electrical and Computer Engineering": ("ECE", ["Digital Signal Processing", "VLSI Design", "Embedded Systems", "Communication Systems",
                                                    "Power Electronics", "Computer Architecture"]),
    "Education": ("EDUC", ["Foundations of Education", "Curriculum Design", "Educational Psychology", "Assessment and Evaluation",
                           "Educational Technology", "Research in Education"]),
    "Chemistry": ("CHEM", ["Advanced Organic Chemistry", "Physical Chemistry", "Spectroscopy", "Graduate Research Seminar",
                           "Chemical Kinetics", "Teaching Practicum"]),
}


_EXTRA_FEES = [("Student Union Fee", 80, 260), ("Recreation Center Fee", 90, 220), ("Transportation Fee (Transit Pass)", 60, 180),
               ("Library and Learning Resources Fee", 40, 150), ("Health Services Fee", 120, 320), ("Course Materials Fee", 50, 300),
               ("Graduate Student Association Fee", 20, 60), ("Orientation Fee", 75, 250), ("Laboratory Fee", 60, 240),
               ("Student ID Card Fee", 15, 40), ("Career Services Fee", 30, 90), ("Athletics Fee", 50, 200)]


@doc("tuition_invoice", "학비 청구서(Tuition Invoice)", "fx")
def tuition_invoice(p: Profile, rng: random.Random) -> dict:
    """해외 대학 학비 청구서 (Statement of Fees). 장학금은 입학허가서와 같은 프로필 단위 값."""
    s = _study(p)
    st, cur = s["student"], s["cur"]
    k = {"USD": 1, "GBP": 0.62, "CAD": 1.1, "AUD": 1.25}[cur]
    issue = s["letter_date"] + timedelta(days=rng.randint(10, 40))
    due = s["start"] - timedelta(days=rng.randint(7, 25))
    level_name = s["level"].replace("phd", "Doctoral").replace("master", "Graduate").replace("bachelor", "Undergraduate").title()
    many = heavy(rng, 0.25)
    items = []
    if many:  # 과목별 등록금(학점당) + 세부 수수료가 줄줄이 붙는 청구서
        code, titles = _COURSES.get(s["program"], ("GEN", ["Academic Writing", "Research Methods", "Statistics", "Seminar I", "Seminar II"]))
        n = min(len(titles), rng.randint(4, 6))
        credits = [rng.choice([3, 3, 3, 4]) for _ in range(n)]
        per_cr = s["tuition"] / sum(credits)
        base = 100 if s["level"] == "bachelor" else 500
        for t, c in zip(rng.sample(titles, n), credits):
            items.append((f"Tuition: {code} {base + rng.randint(0, 399)} {t} ({c} cr)", round(per_cr * c, 2)))
        diff = round(s["tuition"] - sum(a for _, a in items), 2)
        items[-1] = (items[-1][0], round(items[-1][1] + diff, 2))
    else:
        items.append(("Tuition - " + ("Full-time " if rng.random() < 0.5 else "") + level_name, s["tuition"]))
    items.append(("Student Activity Fee", K.round_to(rng.uniform(120, 450) * k, 1)))
    items.append(("Technology Fee", K.round_to(rng.uniform(150, 400) * k, 1)))
    if s["cc"] == "US":
        items.append(("Student Health Insurance Plan", K.round_to(rng.uniform(1400, 2900), 1)))
    else:
        items.append(("Overseas Student Health Cover" if s["cc"] == "AU" else "Health Insurance", K.round_to(rng.uniform(300, 900) * k, 1)))
    items.append(("International Student Service Fee", K.round_to(rng.uniform(100, 350) * k, 1)))
    if many:
        for nm, lo, hi in rng.sample(_EXTRA_FEES, rng.randint(6, 10)):
            items.append((nm, K.round_to(rng.uniform(lo, hi) * k, 1)))
    if s["housing"]:
        items.append(("On-Campus Housing" + rng.choice([" (Double Room)", " (Single Room)", ""]), K.round_to(rng.uniform(4200, 8800) * k, 10)))
        if rng.random() < 0.6:
            items.append(("Meal Plan", K.round_to(rng.uniform(1800, 3200) * k, 10)))
    plan = special(rng, "installment", 0.15)
    if plan:  # 분할납부(Payment Plan) 가입 수수료
        items.append(("Payment Plan Enrollment Fee", K.round_to(rng.choice([35, 50, 60, 75]) * k, 1)))
    credits_ = []
    if rng.random() < 0.4:
        credits_.append(("Enrollment Deposit Paid", -K.round_to(rng.choice([300, 500, 1000]) * k, 10), s["letter_date"] + timedelta(days=rng.randint(5, 20))))
    if s["scholarship"]:
        credits_.append((s["scholarship"]["name"], -s["scholarship"]["amount"], issue - timedelta(days=rng.randint(0, 3))))
    if special(rng, "payment_received", 0.15):  # 일부 먼저 송금한 금액
        part = K.round_to(sum(a for _, a in items) * rng.uniform(0.2, 0.5), 100)
        credits_.append((f"Payment Received - International Wire (Ref. {rng.randint(10**7, 10**8 - 1)})", -part,
                         issue + timedelta(days=rng.randint(1, 6))))
        issue = issue + timedelta(days=rng.randint(7, 12))
    total = round(sum(a for _, a in items) + sum(a for _, a, _ in credits_), 2)
    rows = [{"date": _num_date(issue - timedelta(days=rng.randint(0, 3)), s["cc"]), "description": d, "charge": _fm(a, cur)} for d, a in items]
    rows += [{"date": _num_date(min(dt, issue), s["cc"]), "description": d, "credit": _fm(-a, cur)} for d, a, dt in credits_]
    out = _Out({
        "university": {"name": s["uni"], "address": s["uni_addr"], "office": rng.choice(["Office of Student Accounts", "Bursar's Office", "Student Financial Services"])},
        "invoice_no": f"INV-{s['start'].year}{rng.randint(100000, 999999)}",
        "invoice_date": D(issue, "en_long"),
        "student": {"name": _student_name(st), "id": s["student_id"], "program": s["degree"] if "MBA" in s["degree"] else f"{s['degree']} in {s['program']}"},
        "term": s["term"],
        "items": rows,
        "summary": {"previous_balance": _fm(0, cur), "charges": _fm(sum(a for _, a in items), cur),
                    "credits": _fm(-sum(a for _, a, _ in credits_), cur) if credits_ else _fm(0, cur)},
        "total": f"{cur} {total:,.2f}",
        "due_date": D(due, "en_long"),
        "bank": {"beneficiary": s["uni"], "bank_name": s["bank"], "swift": s["swift"], "account": s["account"],
                 "routing_label": s["routing_label"], "routing": s["routing"], "reference": f"{s['student_id']} {_student_name(st)}"},
    })
    if plan:  # 분할납부 일정: 첫 회는 납부기한, 이후 매월
        n = rng.choice([3, 4, 4, 5])
        each = math.floor(total / n * 100) / 100
        amts = [each] * (n - 1) + [round(total - each * (n - 1), 2)]
        dates = [due] + [months_back(due, -i).replace(day=min(due.day, 28)) for i in range(1, n)]
        out["installments"] = [{"no": str(i + 1), "due_date": D(dt, "en_long"), "amount": _fm(a, cur)}
                               for i, (dt, a) in enumerate(zip(dates, amts))]
        out["amount_due_now"] = _fm(amts[0], cur)
    return out
