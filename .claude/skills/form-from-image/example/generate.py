"""예금(신탁) 잔액증명 의뢰서: 칸끼리 관계 맞추기 (layout.json 의 키)."""
from datetime import date, timedelta

from docgen.formkit import date_like, get, put, rows, to_date


def _birth(rng, like):
    """다른 사람 생년월일: 20~70세 (rule:date 는 최근 날짜를 낸다)."""
    return date_like(date(rng.randint(1955, 2004), rng.randint(1, 12), rng.randint(1, 28)), like)


def adjust(d, p, rng):
    """d: 칸 목록으로 채운 값 · p: 고객 프로필 · rng: 이 문서의 난수."""
    # 받는 지점: 원본이 "○○ 지점(부) 앞" 이라 값 끝의 "지점" 을 뺀다
    branch = get(d, "bank.branch")
    if branch:
        put(d, "bank.branch", branch.removesuffix("지점"))
    # 날짜 표기를 한 서류 안에서 하나로 (예금주 생년월일 표기에 맞춤)
    like = get(d, "customer.birth") or "1980.01.01"
    base = to_date(get(d, "base_date")) or date(2025, 1, 1)
    put(d, "base_date", date_like(base, like))
    # 정기발급 유효기간: 시작 ≤ 끝, 최대 3년 (원본 "※ 최대 3년이하로 설정 가능")
    start = base + timedelta(days=rng.randint(0, 30))
    end = start + timedelta(days=rng.choice([182, 365, 730, 1095]) - 1)
    put(d, "valid.from", date_like(start, like))
    put(d, "valid.to", date_like(end, like))
    for key in ("window_agent.birth", "agent.birth"):
        if get(d, key):
            put(d, key, _birth(rng, like))
    # 전체계좌면 계좌번호를 적지 않는다 (원본 "※ 전체계좌 선택시 계좌번호 작성 불요")
    if get(d, "target_scope") == "전체계좌":
        for r in rows(d, "accounts"):
            r["number"] = None
    # 보기 하나짜리 체크(계좌마스킹)는 반쯤 비운다
    if rng.random() < 0.5:
        put(d, "masking", None)
    return d
