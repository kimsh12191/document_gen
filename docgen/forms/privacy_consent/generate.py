"""privacy_consent: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_account.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_account import _bank, _date, _staff_name  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.docs.bank_form_loan import _minor  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


_GUARANTORS = ["신용보증기금", "기술보증기금", "한국주택금융공사", "서울보증보험", "지역신용보증재단"]


_MARKETING_CHANNELS = ["전화", "문자메시지", "이메일", "우편", "앱 푸시"]


@doc("privacy_consent", "개인(신용)정보 수집·이용·제공·조회 동의서", "bank_form", category="internal")
def privacy_consent(p: Profile, rng: random.Random) -> dict:
    """여신 금융거래용 개인(신용)정보 동의서 (필수/선택 동의)."""
    guar = rng.sample(_GUARANTORS, rng.randint(2, 4))
    providers = [
        {"name": "신용정보집중기관(한국신용정보원)",
         "purpose": "본인의 신용을 판단하기 위한 자료로 활용하거나 공공기관에서 정책자료로 활용",
         "items": "개인식별정보, 신용거래정보, 신용도판단정보, 신용능력정보, 공공정보",
         "period": "관련 법령 및 규약에서 정한 기간"},
        {"name": rng.choice(["개인신용평가회사(NICE평가정보, 코리아크레딧뷰로)",
                             "NICE평가정보㈜, 코리아크레딧뷰로㈜"]),
         "purpose": "개인신용평가, 본인 실명 및 신용도 확인", "items": "개인식별정보, 신용거래정보, 신용도판단정보",
         "period": "제공 목적 달성 시까지"},
        {"name": ", ".join(guar), "purpose": "보증심사 및 보증서 발급·관리",
         "items": "개인식별정보, 신용거래정보, 신용능력정보", "period": "보증거래 종료일로부터 5년"},
    ]
    m_collect = rng.choice(["동의함", "동의하지 않음"])
    m_provide = rng.choice(["동의함", "동의하지 않음"]) if m_collect == "동의함" else "동의하지 않음"
    channels = sorted(rng.sample(_MARKETING_CHANNELS, rng.randint(1, 4)), key=_MARKETING_CHANNELS.index) \
        if m_collect == "동의함" else []
    if heavy(rng, 0.25):  # 제공받는 자가 많은 동의서 (보증기관·보험사·공공기관 등) → 여러 쪽
        providers += rng.sample(_EXTRA_PROVIDERS, rng.randint(6, len(_EXTRA_PROVIDERS)))
    data = {
        "bank": _bank(p),
        "consent": {
            "collect": "동의함",
            "unique_id": "동의함",
            "provide": "동의함",
            "provide_unique_id": "동의함",
            "inquiry": "동의함",
        },
        "providers": providers,
        "marketing": {"collect": m_collect, "provide": m_provide, "channels": channels},
        "applicant": {"name": p.person.name, "birth": D(p.person.birth, rng.choice(["dot", "kor"]))},
        "date": _date(p, rng),
        "bank_use": {"clerk": _staff_name(rng)},
    }
    if special(rng, "minor", 0.08):  # 미성년자 본인 + 법정대리인(부모) 동의
        kid = _minor(p, rng)
        data["applicant"] = {"name": kid.name, "birth": D(kid.birth, rng.choice(["dot", "kor"]))}
        data["legal_rep"] = {"name": p.person.name, "relation": "부" if p.person.gender == "M" else "모"}
    if special(rng, "marketing_unchecked", 0.12):  # 선택 동의란을 비워 둠 (체크 누락)
        data["marketing"] = {"collect": None, "provide": None, "channels": []}
    return data


_EXTRA_PROVIDERS = [
    {"name": "서울보증보험㈜", "purpose": "보증보험 가입 심사 및 보험금 지급", "items": "개인식별정보, 신용거래정보, 신용능력정보",
     "period": "보험계약 종료일로부터 5년"},
    {"name": "한국주택금융공사", "purpose": "주택금융 보증 심사 및 사후관리", "items": "개인식별정보, 신용거래정보, 주택 보유 정보",
     "period": "보증 종료일로부터 5년"},
    {"name": "주택도시보증공사", "purpose": "전세보증금반환보증 심사 및 관리", "items": "개인식별정보, 임대차 계약 정보",
     "period": "보증 종료일로부터 5년"},
    {"name": "국세청", "purpose": "소득금액증명 등 소득 확인", "items": "성명, 주민등록번호, 소득 자료", "period": "조회 목적 달성 시까지"},
    {"name": "국민건강보험공단", "purpose": "건강보험 자격 및 보험료 납부내역 확인", "items": "성명, 주민등록번호, 직장 및 보험료 정보",
     "period": "조회 목적 달성 시까지"},
    {"name": "국민연금공단", "purpose": "연금보험료 납부내역 확인", "items": "성명, 주민등록번호, 가입 이력", "period": "조회 목적 달성 시까지"},
    {"name": "행정안전부", "purpose": "주민등록 진위 및 전입세대 확인", "items": "성명, 주민등록번호, 주소", "period": "조회 목적 달성 시까지"},
    {"name": "금융결제원", "purpose": "자동이체·CMS 등록 및 어음정보 확인", "items": "성명, 계좌번호, 거래정보", "period": "거래 종료일로부터 5년"},
    {"name": "한국신용정보원 (채무재조정 정보)", "purpose": "신용회복 지원 및 채무조정 여부 확인", "items": "신용도판단정보",
     "period": "관련 법령에서 정한 기간"},
    {"name": "법무법인·법무사 (등기 위임)", "purpose": "근저당권 설정·말소 등기 업무", "items": "성명, 주민등록번호, 주소, 담보물 정보",
     "period": "등기 완료 시까지"},
    {"name": "감정평가법인", "purpose": "담보물 감정평가", "items": "성명, 연락처, 담보물 정보", "period": "평가 완료 후 1년"},
    {"name": "채권추심회사 (위탁 시)", "purpose": "연체채권 회수 업무 위탁", "items": "개인식별정보, 연락처, 신용거래정보",
     "period": "위탁계약 종료 시까지"},
]
