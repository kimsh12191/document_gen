"""하나은행 공개 서식 — 선언형 스펙 (20종).

scripts/build_form_specs.py 가 add_template/field_specs/ 에서 생성한다.
직접 고치지 말고 생성 스크립트의 라벨 표를 고칠 것.
서식 하나를 수제 템플릿으로 승격할 때는 여기서 해당 FORM 을 지운다.
"""
from ..formspec import FORM  # noqa: F401

FORM("hf381", "장외파생상품 일반투자자 (부)적정성 판단보고서", "finance", code="5-09-0527",
     title_note="하나은행 공개 서식 No.381 (파생상품)",
     sections=[("고객유형", [
        ("customer.name", "고객명", "text"),
        ("item", "고객유형", "text"),
        ("date", "생년월일 및 나이", "date"),
        ("item2", "미성년자/고령/초고령 구분", "text"),
        ("item3", "투자자정보 확인서 응답결과", "text"),
        ("item4", "고객등급", "text"),
        ("item5", "이유", "choice", ["상품위험등급대비고객등급미달"]),
        ("item6", "충족 여부", "text"),
        ("item7", "구분", "text"),
        ("item8", "상품예시", "text"),
        ("agent.name", "대리인", "text"),
        ("item9", "지점/부서명", "text"),
        ("item10", "담당자 (파생상품투자권유 자문인력)", "text")
     ])])

FORM("hf382", "장외파생상품 일반투자자 투자자정보 분석결과표", "finance", code="파생상품-0382",
     title_note="하나은행 공개 서식 No.382 (파생상품)",
     sections=[("고객유형", [
        ("customer.name", "고객명", "text"),
        ("item", "고객유형", "text"),
        ("date", "생년월일 및 나이", "date"),
        ("item2", "미성년자/고령/초고령 구분", "text"),
        ("item3", "투자자정보 확인서 응답결과", "text"),
        ("item4", "고객등급", "text"),
        ("agent.name", "대리인", "text"),
        ("item5", "지점/부서명", "text"),
        ("item6", "담당자 (파생상품투자권유 자문인력)", "text")
     ])])

FORM("hf383", "장외파생상품 투자성향에 적정하지 않은 거래확인서", "finance", code="파생상품-0383",
     title_note="하나은행 공개 서식 No.383 (파생상품)",
     sections=[("유의사항", [
        ("item", "구분", "text"),
        ("item2", "상품예시", "text"),
        ("customer.name", "고객명", "text"),
        ("agent.name", "대리인", "text"),
        ("item3", "지점/부서명", "text"),
        ("item4", "담당자 (파생상품투자권유 자문인력)", "text"),
        ("item5", "영업점장 (파생상품 영업관리자)", "text")
     ])])

FORM("hf384", "장외파생상품 일반투자자 투자자정보 확인서(법인 및 개인사업자 고객용)", "finance", code="5-09-0098",
     title_note="하나은행 공개 서식 No.384 (파생상품)",
     sections=[("거래목적", [
        ("date", "년 월 일(만 세)", "date"),
        ("item", "상장거래소명", "text"),
        ("no", "종목코드", "number"),
        ("item2", "자산 총계", "text"),
        ("item3", "부채 총계", "text"),
        ("item4", "종류", "text"),
        ("date2", "보유(예정)기간", "date"),
        ("item5", "소속부서", "text"),
        ("employer.position", "직급", "text"),
        ("customer.name", "성명", "text"),
        ("item6", "관련경력", "text"),
        ("item7", "관련자격", "text"),
        ("item8", "장외파생상품에 대한 지식 보유 정도", "text"),
        ("item9", "하 : 금융투자상품에 투자해 본 경험이 없음", "text"),
        ("item10", "거래경험 연수", "text"),
        ("customer.name", "고객명", "text"),
        ("agent.name", "대리인", "text"),
        ("item11", "지점/부서명", "text"),
        ("item12", "담당자 (파생상품투자권유 자문인력)", "text")
     ])])

FORM("hf385", "장외파생상품 일반투자자 투자자정보 확인서(개인 고객용)", "finance", code="5-09-0095",
     title_note="하나은행 공개 서식 No.385 (파생상품)",
     sections=[("고객유형 : 생년월일을 작성하여 주시기 바랍니다.", [
        ("item", "자산 총계", "text"),
        ("item2", "부채 총계", "text"),
        ("item3", "종류", "text"),
        ("date", "보유(예정)기간", "date"),
        ("item4", "장외파생상품에 대한 지식 보유 정도", "text"),
        ("item5", "거래경험 연수", "text"),
        ("customer.name", "고객명", "text"),
        ("item6", "지점/부서명", "text"),
        ("item7", "담당자 (파생상품투자권유 자문인력)", "text")
     ])])

FORM("hf386", "외환파생상품거래 헤지 수요 현황 및 거래 실행에 따른 확인서", "finance", code="5-09-0101",
     title_note="하나은행 공개 서식 No.386 (파생상품)",
     sections=[("기재사항", [
        ("item", "구 분 (해당 □란에 체크)", "text"),
        ("amount", "금 액", "amount"),
        ("item2", "수 입 (조달포함)", "text"),
        ("date", "택일", "choice", ["과거수출입실적기준"]),
        ("amount2", "헤지대상 금액 합계 (헤지비율 분모에 해당)", "amount"),
        ("amount3", "기 체결 외환파생상품 거래금액", "amount"),
        ("currency", "통화선도 (외환스왑, NDF 포함)", "currency"),
        ("currency2", "통화옵션", "currency"),
        ("currency3", "통화스왑", "currency"),
        ("item3", "환변동보험 및 기타( )", "text"),
        ("amount4", "기헤지거래 금액 합계(헤지비율 분자에 해당)", "amount")
     ])])

FORM("hf387", "HANA FX TRADING SYSTEM 자동결제 이용신청서", "finance", code="5-09-0514",
     title_note="하나은행 공개 서식 No.387 (파생상품)",
     sections=[("기재사항", [
        ("no", "확인(인감, 서명, 계좌번호)", "number"),
        ("item", "원화계좌", "text"),
        ("fx_amount", "외화계좌", "fx_amount")
     ])])

FORM("hf388", "HANA FX TRADING SYSTEM 이용신청서", "finance", code="5-09-0476",
     title_note="하나은행 공개 서식 No.388 (파생상품)",
     sections=[("기재사항", [
        ("company.name", "회사명", "text"),
        ("company.ceo", "대표자", "text"),
        ("company.biz_no", "사업자 등록번호", "number"),
        ("no", "대표 전화번호", "number"),
        ("customer.address", "주소", "text"),
        ("item", "신청구분", "choice", ["신청", "변경", "해지"]),
        ("item2", "(영문+숫자 혼합6~10자리)", "text"),
        ("customer.name", "성명", "text"),
        ("item3", "부서/직위", "text"),
        ("customer.phone", "연락처", "text")
     ])])

FORM("hf389", "위임장(장외파생상품 일반투자자용)", "finance", code="5-09-0524",
     title_note="하나은행 공개 서식 No.389 (파생상품)",
     sections=[("대리인 정보", [
        ("item", "이름", "text"),
        ("agent.relation", "본인과의 관계", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.phone", "연락처", "text"),
        ("customer.address", "주소", "text"),
        ("item2", "고객명(위임인)", "text")
     ])])

FORM("hf390", "매매내역 등의 통지방법에 대한 고객확인서(장외파생상품)", "finance", code="파생상품-0390",
     title_note="하나은행 공개 서식 No.390 (파생상품)",
     sections=[("매매체결에 따른 해당 매매에 관한 거래확인서", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf391", "고령투자자확인서(장외파생상품용)", "finance", code="5-09-0465",
     title_note="하나은행 공개 서식 No.391 (파생상품)",
     sections=[("기재사항", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf392", "초고령투자자확인서(장외파생상품용)", "finance", code="5-09-0463",
     title_note="하나은행 공개 서식 No.392 (파생상품)",
     sections=[("기재사항", [
        ("date", "보유 및 이용기간", "date"),
        ("item", "거부 권리 및 불이익", "text"),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf393", "이자율스왑 연계 대출 분할상환 원금 및 이자율스왑 정산이자 출금서비스 특약", "finance", code="5-09-0511",
     title_note="하나은행 공개 서식 No.393 (파생상품)",
     sections=[("기재사항", [
        ("item", "대상여신", "text"),
        ("item2", "여신과목", "text"),
        ("date", "여신개시일", "date"),
        ("date2", "여신기간만료일", "date"),
        ("amount", "대상이자율스왑", "amount"),
        ("date3", "거래일", "date"),
        ("date4", "발효일", "date"),
        ("date5", "종료일", "date"),
        ("rate", "지급고정금리", "percent"),
        ("rate2", "수취변동금리", "percent")
     ])])

FORM("hf394", "적정성원칙 투자자확인서", "finance", code="5-09-0510",
     title_note="하나은행 공개 서식 No.394 (파생상품)",
     sections=[("기재사항", [
        ("item", "고객 등급", "text"),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf399", "파생상품거래 손실한도 초과 및 증거담보 요청 통지서", "finance", code="파생상품-0399",
     title_note="하나은행 공개 서식 No.399 (파생상품)",
     sections=[("기재사항", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf400", "파생상품거래 손실한도 감액통지서", "finance", code="파생상품-0400",
     title_note="하나은행 공개 서식 No.400 (파생상품)",
     sections=[("기재사항", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf401", "전문투자자 전환신청서", "finance", code="5-09-0104",
     title_note="하나은행 공개 서식 No.401 (파생상품)",
     sections=[("주권상장법인 :", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf402", "장외파생상품 거래 담당자 지정 통지서", "finance", code="5-09-0090",
     title_note="하나은행 공개 서식 No.402 (파생상품)",
     sections=[("기재사항", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf403", "일반투자자 전환신청서", "finance", code="5-09-0096",
     title_note="하나은행 공개 서식 No.403 (파생상품)",
     sections=[("고객유형: 다음에 해당하는 하나에 표시하여 주시기 ", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf405", "외환파생상품 거래 금액 확인서", "finance", code="5-09-0102",
     title_note="하나은행 공개 서식 No.405 (파생상품)",
     sections=[("외화매도(수출)", [
        ("currency", "통화선도(외환스왑, NDF포함)", "currency"),
        ("currency2", "통화옵션", "currency"),
        ("currency3", "통화스왑", "currency"),
        ("item", "환변동보험", "text"),
        ("amount", "합 계", "amount")
     ])])
