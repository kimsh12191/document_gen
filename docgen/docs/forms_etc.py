"""하나은행 공개 서식 — 선언형 스펙 (14종).

scripts/build_form_specs.py 가 add_template/field_specs/ 에서 생성한다.
직접 고치지 말고 생성 스크립트의 라벨 표를 고칠 것.
서식 하나를 수제 템플릿으로 승격할 때는 여기서 해당 FORM 을 지운다.
"""
from ..formspec import FORM  # noqa: F401

FORM("hf406", "하나카드 금융상품 판매대리 중개업자 증서", "bank_form", code="기타-0406",
     title_note="하나은행 공개 서식 No.406 (기타)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf420", "비대면 계좌개설 안심차단 서비스 신청서", "bank_form", code="5-08-0737",
     title_note="하나은행 공개 서식 No.420 (기타)",
     sections=[("기재사항", [
        ("item", "☐ 신청", "text"),
        ("item2", "☐ 해제", "text"),
        ("customer.name", "성명", "text"),
        ("customer.rrn", "주민등록번호", "number"),
        ("item3", "신청인과의 관계", "text"),
        ("customer.birth", "생년월일", "date")
     ])])

FORM("hf426", "이의제기 신청서", "bank_form", code="기타-0426",
     title_note="하나은행 공개 서식 No.426 (기타)",
     sections=[("사기이용계좌가 아니라는 사실을 증빙하는 자료 1부", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf427", "아이부자 선불전자지급수단 잔액 상속(지급) 및 서비스 해지 요청서(위임장 겸용)", "bank_form", code="5-99-0088",
     title_note="하나은행 공개 서식 No.427 (기타)",
     sections=[("피상속인 (사망 회원)", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("item", "자필기재 (인/서명)", "text"),
        ("account", "계좌번호", "number"),
        ("item2", "상속인", "choice", ["본인", "위임(별도위임장작성)"])
     ])])

FORM("hf430", "민원신청서", "bank_form", code="5-02-0001",
     title_note="하나은행 공개 서식 No.430 (기타)",
     sections=[("기재사항", [
        ("item", "*성 명", "text"),
        ("item2", "*법 인 명", "text"),
        ("no", "*사업자등록번호", "number"),
        ("item3", "*주 소", "text"),
        ("customer.email", "e-mail", "text"),
        ("item4", "*전 화", "text"),
        ("no2", "*휴대 전화번호", "number"),
        ("date", "*생년월일(주민등록기준)", "date"),
        ("item5", "*성 별", "text"),
        ("item6", "*신 청 취 지 (요구사항)", "text"),
        ("item7", "*신 청 사 유 (6하 원칙에 따라 기술)", "text")
     ])])

FORM("hf431", "전자금융거래 사고 피해 신고서(통합서류)", "bank_form", code="5-99-0002",
     title_note="하나은행 공개 서식 No.431 (기타)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("company.name", "법인명", "text"),
        ("customer.phone", "전화번호", "number"),
        ("customer.email", "e-mail", "text"),
        ("customer.address", "주소", "text"),
        ("item", "최초 사고발생 일시", "text"),
        ("date", "20 년 월 일( 요일) 시 분", "date"),
        ("item2", "최초 사고인지 일시", "text"),
        ("item3", "최초 계좌 지급정지 (거래제한) 일시", "text"),
        ("amount", "사고발생 총 피해금액", "amount"),
        ("item4", "금 원 ( ₩ )", "text"),
        ("item5", "사고발생 계좌내역 (본인명의 계좌)", "text"),
        ("item6", "출금은행", "text"),
        ("account", "출금계좌번호", "number"),
        ("item7", "입금은행 (상대은행)", "text"),
        ("item8", "입금(상대)계좌 예금주", "choice", ["본인", "타인(예금주명)"]),
        ("item9", "신분증 분실 신고 (해당기관 앞)", "choice", ["예(신고일", "아니오"]),
        ("item10", "휴대전화 분실 신고 (통신사 앞)", "choice", ["예(신고일", "아니오"]),
        ("item11", "명의도용 휴대전화 개설 신고 (통신사 앞)", "choice", ["예(신고일", "아니오"]),
        ("item12", "피해구제 환급 신청", "choice", ["신청예정", "신청후진행중", "피해구제종결(환급금수령또는완료통지)신청상태", "기타()신청은행은행(신청일", "미신고", "신고(고소,고발등)"]),
        ("item13", "신청상태", "text"),
        ("item14", "수사기관 수사 진행", "text"),
        ("item15", "진행상태", "text"),
        ("item16", "수사기관", "text"),
        ("item17", "행번", "text"),
        ("item18", "신분증 사본", "text"),
        ("item19", "본인서명사실확인서", "text"),
        ("item20", "출입국사실증명원 또는 여권 사본", "text"),
        ("item21", "신청취지 (요구사항)", "text")
     ])])

FORM("hf433", "추심지급 신청서", "bank_form", code="5-08-0205",
     title_note="하나은행 공개 서식 No.433 (기타)",
     sections=[("기재사항", [
        ("item", "접수점", "text"),
        ("item2", "※ 예시 : 서울중앙지방법원등", "text"),
        ("item3", "채권자", "text"),
        ("item4", "연락처(필수)", "text"),
        ("customer.email", "E-mail", "text"),
        ("amount", "최소 추심 요청 금액", "choice", ["1만원", "기타(수수료제외후원이상일때)"]),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("agent.relation", "본인과의 관계", "text")
     ])])

FORM("hf434", "세종특별자치시 지역개발채권 매입 신청서", "bank_form", code="5-08-0344",
     title_note="하나은행 공개 서식 No.434 (기타)",
     sections=[("위의 지역개발채권 매도금액(즉시매도시)을 정히 영수", [
        ("item", "성명 / 법인명", "text"),
        ("customer.rrn", "주민등록번호 (사업자등록번호)", "number"),
        ("customer.address", "주 소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "대리인( 성명)", "text"),
        ("customer.rrn", "주민등록번호", "number"),
        ("item3", "징 구 기 관", "text")
     ])])

FORM("hf435", "대전광역시 지역개발채권 매입 신청서", "bank_form", code="5-08-0230",
     title_note="하나은행 공개 서식 No.435 (기타)",
     sections=[("위의 지역개발채권 매도금액(즉시매도시)을 정히 영수", [
        ("item", "성명 / 법인명", "text"),
        ("customer.rrn", "주민등록번호 (사업자등록번호)", "number"),
        ("customer.address", "주 소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "대리인( 성명)", "text"),
        ("customer.rrn", "주민등록번호", "number"),
        ("item3", "징 구 기 관", "text")
     ])])

FORM("hf436", "주주명부(법인 비대면 실명확인 서비스 용)", "bank_form", code="기타-0436",
     title_note="하나은행 공개 서식 No.436 (기타)",
     sections=[("기재사항", [
        ("amount", "합 계", "amount"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount2", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf438", "매출채권보험 상담 신청서(신청기업용)", "bank_form", code="5-99-0040",
     title_note="하나은행 공개 서식 No.438 (기타)",
     sections=[("기업체 개요", [
        ("company.name", "기업체명", "text"),
        ("company.ceo", "대표자", "text"),
        ("company.established", "설립일", "date"),
        ("company.corp_no", "법인등록번호", "number"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("customer.phone", "전화번호", "number"),
        ("item", "사업장주소", "text"),
        ("customer.email", "E-mail", "text"),
        ("item2", "당기매출액 (최근 1년 매출액)", "text"),
        ("no", "업종/업종분류코드", "number"),
        ("item3", "품목", "text"),
        ("item4", "( ) 신용보험센터", "text"),
        ("item5", "신청기업 담당자", "text"),
        ("employer.position", "직위", "text"),
        ("customer.phone", "연락처", "text")
     ])])

FORM("hf439", "상조회사 선수금 예치확인서", "bank_form", code="5-99-0020",
     title_note="하나은행 공개 서식 No.439 (기타)",
     sections=[("상조회사 정보", [
        ("item", "상조회사명", "text"),
        ("company.biz_no", "사업자번호", "number"),
        ("customer.address", "주 소", "text")
     ])])

FORM("hf440", "금융사고예방을 위한 문자통지(SMS) 서비스 신청서", "bank_form", code="5-08-0320",
     title_note="하나은행 공개 서식 No.440 (기타)",
     sections=[("고객별 문자통지 운영 방법", [
        ("item", "여 부(해당 항목에 “V” 표기)", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf441", "법원보관금 납부서(은행제출용)", "bank_form", code="5-08-0258",
     title_note="하나은행 공개 서식 No.441 (기타)",
     sections=[("법원보관금은 해당법원의 법원보관금취급점에서 납부하실", [
        ("item", "법 원 명", "text"),
        ("no", "사건번호", "number"),
        ("amount", "납부금액", "amount"),
        ("item2", "보관금종류", "text"),
        ("item3", "납부자 성명", "text"),
        ("customer.rrn", "주민등록번호 (사업자등록번호)", "number"),
        ("item4", "납부자 주소", "text"),
        ("customer.phone", "전화번호", "number"),
        ("amount2", "잔액환급 계좌번호", "amount"),
        ("item5", "은행", "text"),
        ("customer.name", "예금주", "text"),
        ("account", "계좌번호", "number")
     ])])
