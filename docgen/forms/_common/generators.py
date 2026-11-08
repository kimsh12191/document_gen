"""직접 만든 생성기 (코드). 여기에 함수를 더하면 studio 영역 편집기의 생성 방법 고르기 창에
"직접 만든 생성기 (코드)" 로 나오고, 칸의 생성 방법이 rule:<함수 이름> 이 된다. 설명: docgen/usergen.py

    @generator("화면에 보일 이름", note="짧은 설명")
    def 함수_이름(p, rng, item, row):   # p 고객 프로필, rng 난수(이것만), item 칸 정보(label·choices…), row 표 행 번호
        return "값"                      # None 이나 "" 면 빈 칸

코드 없이 되는 것은 먼저 그쪽으로: 보기 중 하나 · 틀(# 숫자, A 대문자, {가|나} 고르기) · 키 사전의 값 종류.
고친 뒤 확인: python -m docgen.formdir check <서식ID>, studio 생성 방법 고르기 창의 예시 값.
"""
from docgen.usergen import generator


@generator("카드번호 (가운데 가림)", note="1234-56**-****-7890 꼴")
def card_masked(p, rng, item, row):
    return f"{rng.randint(1000, 9999)}-{rng.randint(10, 99)}**-****-{rng.randint(1000, 9999)}"


@generator("거래 적요", note="입출금 내역의 적요 (이체·급여·카드대금 …), 고객 이름이 들어가기도")
def txn_memo(p, rng, item, row):
    pool = ["이체", "입금", "출금", "급여", "카드대금", "공과금", "자동이체", "ATM출금", "타행이체", "이자"]
    if rng.random() < 0.15:
        return p.person.name
    return rng.choice(pool)


@generator("주민등록번호 (뒷자리 가림)", note="900210-1****** 꼴, 고객 본인")
def rrn_masked(p, rng, item, row):
    return p.person.rrn[:8] + "******"
