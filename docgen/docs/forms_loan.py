"""하나은행 공개 서식 — 선언형 스펙 (54종).

scripts/build_form_specs.py 가 add_template/field_specs/ 에서 생성한다.
직접 고치지 말고 생성 스크립트의 라벨 표를 고칠 것.
서식 하나를 수제 템플릿으로 승격할 때는 여기서 해당 FORM 을 지운다.
"""
from ..formspec import FORM  # noqa: F401

FORM("hf064", "대출정보 열람청구, 상환 및 말소접수 위임장(주택담보대출 대출이동서비스)", "bank_form", code="5-16-0401",
     title_note="하나은행 공개 서식 No.64 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.phone", "연락처", "text")
     ])])

FORM("hf066", "대출정보 열람청구 및 상환 위임장(대출이동서비스)", "bank_form", code="5-16-0365",
     title_note="하나은행 공개 서식 No.66 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text")
     ])])

FORM("hf068", "계약 체결 이행 등을 위한 필수 동의서(개인금융성 신용보험용)", "bank_form", code="5-06-0748",
     title_note="하나은행 공개 서식 No.68 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf069", "기업간결제 제신고(약정해지,변경) 신청서", "bank_form", code="5-06-0568",
     title_note="하나은행 공개 서식 No.69 (대출)",
     sections=[("신청기업 정보", [
        ("item", "연락처(선택)", "text"),
        ("item2", "주소(선택)", "text"),
        ("item3", "약정상품명", "text"),
        ("no", "약정번호", "number"),
        ("item4", "신청내용", "choice", ["결제성상품약정계좌변경", "결제성상품약정해지", "약정채권관계해제", "사업자번호변경", "세금계산서본지사정보등록/해제", "발주서취소"]),
        ("agent.name", "대리인성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.phone", "연락처", "text"),
        ("agent.relation", "본인과의 관계", "text"),
        ("item5", "위임인 : (인/서명)", "text")
     ])])

FORM("hf072", "전자방식 외상매출채권 결제제도 이용신청서(외담대,동반성장론,e-안심팩토링대출용)", "bank_form", code="5-06-0733",
     title_note="하나은행 공개 서식 No.72 (대출)",
     sections=[("신청기업 정보", [
        ("item", "법인명 (또는 상호명)", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item2", "대표이사 (또는 대표자명)", "text"),
        ("date", "대표이사(대표자) 생년월일", "date"),
        ("company.biz_type", "업 태", "text"),
        ("company.biz_item", "업 종", "text"),
        ("item3", "주요취급품목", "text"),
        ("no", "(우편번호 : )", "number"),
        ("customer.phone", "전화번호", "number"),
        ("company.fax", "팩스번호", "number"),
        ("item4", "기업규모", "choice", ["대기업", "중견기업", "중기업", "소기업", "공공및기타"]),
        ("item5", "입점 Seller(판매기업)를 위한 채권발행", "text"),
        ("item6", "동반협력기업간 상생매출채권 발행 및 수취약정", "text"),
        ("item7", "*담당자명", "text"),
        ("company.department", "담당부서", "text"),
        ("no2", "*담당자전화번호", "number"),
        ("no3", "*담당자휴대전화번호", "choice", ["SKT", "KT", "LGU+"]),
        ("date2", "*담당자이메일", "date"),
        ("no4", "담당자 팩스번호", "number")
     ])])

FORM("hf078", "통화전환 옵션부 외화대출 원화대출 전환신청서", "bank_form", code="5-06-0147",
     title_note="하나은행 공개 서식 No.78 (대출)",
     sections=[("기재사항", [
        ("date", "원화대출전환 희망일", "date"),
        ("item", "신 청 사 유", "text"),
        ("item2", "대 출 과 목", "text"),
        ("amount", "대 출 금 액 (본건 전환후 외화대출잔액)", "amount"),
        ("date", "년 월 일", "date"),
        ("rate", "대 출 금 리", "percent")
     ])])

FORM("hf079", "정보교환 기업구매자금어음금 미결제통보확인서", "bank_form", code="5-06-0429",
     title_note="하나은행 공개 서식 No.79 (대출)",
     sections=[("기재사항", [
        ("item", "Fax ( ) -", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf080", "정보교환 기업구매자금어음 부도통보확인서", "bank_form", code="5-06-0428",
     title_note="하나은행 공개 서식 No.80 (대출)",
     sections=[("기재사항", [
        ("item", "Fax ( ) -", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf081", "정보교환 기업구매자금어음 인수거절통보확인서", "bank_form", code="5-06-0427",
     title_note="하나은행 공개 서식 No.81 (대출)",
     sections=[("기재사항", [
        ("item", "Fax ( ) -", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf082", "채권발행 등록 신청서", "bank_form", code="대출-0082",
     title_note="하나은행 공개 서식 No.82 (대출)",
     sections=[("기재사항", [
        ("item", "구매기업명", "text"),
        ("no", "구매기업 사업자등록번호", "number"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf083", "전자방식 외상매출채권 결제제도 이용신청서 (서울시농수산식품공사용)", "bank_form", code="5-06-0898",
     title_note="하나은행 공개 서식 No.83 (대출)",
     sections=[("신청기업 정보", [
        ("item", "법인명 (또는 상호명)", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item2", "대표이사 (또는 대표자명)", "text"),
        ("date", "대표이사(대표자)생년월일", "date"),
        ("company.biz_type", "업 태", "text"),
        ("company.biz_item", "업 종", "text"),
        ("item3", "주요취급품목", "text"),
        ("no", "(우편번호: )", "number"),
        ("customer.phone", "전화번호", "number"),
        ("company.fax", "팩스번호", "number"),
        ("item4", "기업규모", "choice", ["대기업", "중견기업", "중기업", "소기업", "공공및기타"]),
        ("item5", "*담당자명", "text"),
        ("company.department", "담당부서", "text"),
        ("no2", "*담당자 전화번호", "number"),
        ("no3", "*담당자 휴대전화번호", "choice", ["SKT", "KT", "LGU+"]),
        ("date2", "*담당자 이메일", "date"),
        ("no4", "담당자 팩스번호", "number")
     ])])

FORM("hf084", "외상매출채권 양도통지서(장래채권양도통지용)", "bank_form", code="5-06-0406",
     title_note="하나은행 공개 서식 No.84 (대출)",
     sections=[("양도채권의 표시", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf086", "미래채권담보대출 협력기업 일괄추천서", "bank_form", code="5-06-0404",
     title_note="하나은행 공개 서식 No.86 (대출)",
     sections=[("기재사항", [
        ("item", "총 계", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf087", "미래채권담보대출 추천서", "bank_form", code="5-06-0417",
     title_note="하나은행 공개 서식 No.87 (대출)",
     sections=[("추천대상 업체명", [
        ("date", "최초 거래일자", "date"),
        ("amount", "( )백만원", "amount"),
        ("date2", "평균결제기간(주2)", "date")
     ])])

FORM("hf088", "기업구매자금어음 추심취소 및 반환의뢰서", "bank_form", code="5-06-0293",
     title_note="하나은행 공개 서식 No.88 (대출)",
     sections=[("기재사항", [
        ("item", "기업구매자금어음 내용", "text"),
        ("item2", "세금계산서", "text"),
        ("amount", "공급가액", "amount"),
        ("item3", "건", "text")
     ])])

FORM("hf089", "외상매출채권 양도통지서(e-안심팩토링대출용)", "bank_form", code="5-06-0579",
     title_note="하나은행 공개 서식 No.89 (대출)",
     sections=[("양도채권의 표시", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf090", "납품대금 선입금(벤더입금) 신청서", "bank_form", code="5-06-0564",
     title_note="하나은행 공개 서식 No.90 (대출)",
     sections=[("기재사항", [
        ("item", "금 원(₩ )", "text"),
        ("item2", "판매기업입금일 (또는 결제일)", "text"),
        ("no", "( )은행, 계좌번호( )", "number"),
        ("item3", "벤더기업명", "text"),
        ("no2", "벤더기업사업자등록번호", "number"),
        ("amount", "벤더입금이자 부담주체", "choice", ["판매기업", "벤더기업"])
     ])])

FORM("hf091", "기업구매자금 결제제도 이용 신청서", "bank_form", code="대출-0091",
     title_note="하나은행 공개 서식 No.91 (대출)",
     sections=[("신청기업 정보", [
        ("item", "법인명 (또는 상호명)", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.corp_no", "법인등록번호", "number"),
        ("item2", "대표이사 (또는 대표자명)", "text"),
        ("date", "대표이사(대표자) 생년월일", "date"),
        ("company.biz_type", "업 태", "text"),
        ("company.biz_item", "종 목", "text"),
        ("item3", "주요취급품목", "text"),
        ("no", "(우편번호: )", "number"),
        ("customer.phone", "전화번호", "number"),
        ("company.fax", "팩스번호", "number"),
        ("item4", "신청기업 구분", "text"),
        ("item5", "\u0000 일반구매자금 결제제도", "text"),
        ("company.department", "담당 부서", "text"),
        ("item6", "담당자명", "text"),
        ("no2", "담당자 전화번호", "number"),
        ("no3", "담당자 휴대전화번호", "number"),
        ("no4", "담당자 팩스번호", "number"),
        ("date2", "담당자 이메일", "date")
     ])])

FORM("hf092", "외상매출채권양도통지서(개별채권양도통지용)", "bank_form", code="5-06-0546",
     title_note="하나은행 공개 서식 No.92 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf093", "미결제 전자채권대금 입금확인서", "bank_form", code="5-06-0641",
     title_note="하나은행 공개 서식 No.93 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf094", "상생벤더구매론 승인명세 등록신청서", "bank_form", code="대출-0094",
     title_note="하나은행 공개 서식 No.94 (대출)",
     sections=[("기재사항", [
        ("item", "1차 협력기업명", "text"),
        ("no", "1차 협력기업 사업자등록번호", "number"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf095", "벤더승인명세 등록 신청서", "bank_form", code="대출-0095",
     title_note="하나은행 공개 서식 No.95 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf096", "발주명세 등록신청서", "bank_form", code="대출-0096",
     title_note="하나은행 공개 서식 No.96 (대출)",
     sections=[("기재사항", [
        ("item", "중심기업명", "text"),
        ("no", "중심기업 사업자등록번호", "number"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf097", "미래채권 대출신청서(미래대,상생미래대용)", "bank_form", code="대출-0097",
     title_note="하나은행 공개 서식 No.97 (대출)",
     sections=[("기재사항", [
        ("item", "발주명세", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf098", "기업구매자금어음 지급제시 명세", "bank_form", code="5-06-0195",
     title_note="하나은행 공개 서식 No.98 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf099", "지급승인명세 등록 신청서", "bank_form", code="5-06-0565",
     title_note="하나은행 공개 서식 No.99 (대출)",
     sections=[("기재사항", [
        ("item", "중심기업명", "text"),
        ("no", "중심기업 사업자등록번호", "number"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf102", "기업현황서(B2B전자결제서비스 업무, MP용)", "bank_form", code="5-06-0653",
     title_note="하나은행 공개 서식 No.102 (대출)",
     sections=[("기업체 개황", [
        ("company.name", "기업체명", "text"),
        ("company.ceo", "대표자", "text"),
        ("item", "본 사", "text"),
        ("item2", "TEL", "text"),
        ("company.fax", "FAX", "text"),
        ("item3", "주사무소", "text"),
        ("item4", "사 업 장", "text"),
        ("item5", "업종 (표준산업분류기호)", "text"),
        ("item6", "설립년월", "text"),
        ("company.employees", "종업원 수", "text"),
        ("item7", "사업 모델 및 특성", "text"),
        ("item8", "모 델 명", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.corp_no", "법인등록번호", "number"),
        ("item9", "협회 및 단체가입", "text"),
        ("item10", "정부기관 및 금융기관우대", "text"),
        ("item11", "인허가등록", "text"),
        ("amount", "요약 재무 현황 (단위 : 백만원)", "amount"),
        ("item12", "20 년", "text"),
        ("item13", "총 자 산", "text"),
        ("company.capital", "자 본 금", "text"),
        ("item14", "자 기 자 본", "text"),
        ("company.revenue", "매 출 액", "text"),
        ("item15", "경 상 이 익", "text"),
        ("item16", "당기순이익", "text"),
        ("item17", "주거래은행", "text"),
        ("item18", "당좌거래은행", "text"),
        ("amount2", "합 계", "amount"),
        ("customer.name", "성 명", "text"),
        ("item19", "주요경력", "text"),
        ("amount3", "연간 판매금액", "amount"),
        ("amount4", "연간 구매금액", "amount")
     ])])

FORM("hf103", "B2B 전자결제서비스 업무 이용신청서(MP용)", "bank_form", code="5-06-0652",
     title_note="하나은행 공개 서식 No.103 (대출)",
     sections=[("신청기업정보", [
        ("item", "서비스 신청구분", "text"),
        ("item2", "\u0000 신규 \u0000 변경 \u0000 해지", "text"),
        ("item3", "보증기관 사용구분", "text"),
        ("item4", "\u0000 신용보증기금", "text"),
        ("item5", "\u0000 기술보증기금", "text"),
        ("item6", "\u0000 지역보증재단", "text"),
        ("item7", "기업명 (MP상호명)", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item8", "MP URL", "text"),
        ("item9", "신용보증", "text"),
        ("item10", "기술보증", "text"),
        ("company.biz_type", "업 태", "text"),
        ("company.biz_item", "업 종", "text"),
        ("item11", "지역보증", "text"),
        ("company.ceo", "대표자명", "text"),
        ("date", "대표자 생년월일", "date"),
        ("customer.phone", "전화번호", "number"),
        ("no", "FAX번호", "number"),
        ("customer.address", "주 소", "text"),
        ("item12", "인터넷뱅킹 가입구분", "text"),
        ("amount", "수 수 료 입금계좌", "amount"),
        ("account.holder", "예금주명", "text"),
        ("company.department", "담당부서", "text"),
        ("item13", "담당자명", "text"),
        ("customer.phone", "연락처", "text"),
        ("no2", "전화 번호: Fax번호 : 모바일번호 :", "number"),
        ("item14", "e-mail 주소", "text"),
        ("item15", "지급승인방식 구분", "text"),
        ("item16", "접수방식", "text"),
        ("item17", "지급승인방식", "text"),
        ("item18", "\u0000", "text")
     ])])

FORM("hf104", "기업구매자금어음 추심의뢰서", "bank_form", code="5-06-0196",
     title_note="하나은행 공개 서식 No.104 (대출)",
     sections=[("환어음 대금 추심의뢰 명세 (단위 : 원)", [
        ("item", "기업구매자금어음 (지급인) 내용", "text"),
        ("item2", "세금계산서", "text"),
        ("amount", "공급가액", "amount")
     ])])

FORM("hf105", "전자채권미결제 확인의뢰서 및 확인서", "bank_form", code="5-06-0259",
     title_note="하나은행 공개 서식 No.105 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf106", "기업구매자금어음(기업구매자금용)", "bank_form", code="5-06-0292",
     title_note="하나은행 공개 서식 No.106 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf107", "기업구매자금대출 연장신청서", "bank_form", code="5-06-0426",
     title_note="하나은행 공개 서식 No.107 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf108", "외상매출채권 대출신청서(외담대,e-안심팩토링대출 겸용)", "bank_form", code="5-06-0581",
     title_note="하나은행 공개 서식 No.108 (대출)",
     sections=[("기타 본인확인을 위하여 은행에서 요청하는 서류", [
        ("item", "외상매출채권명세", "text"),
        ("item2", "세금계산서 정보", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item3", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf109", "전자채권사고신고(취하)서", "bank_form", code="5-06-0261",
     title_note="하나은행 공개 서식 No.109 (대출)",
     sections=[("기재사항", [
        ("no", "전자채권번호", "number"),
        ("amount", "금 액", "amount"),
        ("date", "발 행 일", "date"),
        ("date2", "만 기 일", "date"),
        ("item", "판매기업 기업명", "text"),
        ("no2", "판매기업 사업자번호", "number"),
        ("item2", "담보금 입금유무", "text"),
        ("item3", "사고신고 구분", "choice", ["신고", "취하"]),
        ("item4", "사고신고(취하) 사 유", "text")
     ])])

FORM("hf110", "전자방식 외상매출채권 발행취소 신청서(외담대,e-안심팩토링용)", "bank_form", code="5-06-0550",
     title_note="하나은행 공개 서식 No.110 (대출)",
     sections=[("본인확인서류", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf111", "《개인》위임장(해외체제자 담보대출용)", "bank_form", code="대출-0111",
     title_note="하나은행 공개 서식 No.111 (대출)",
     sections=[("대출 거래관련 주요내용", [
        ("item", "(한글) (영문)", "text"),
        ("customer.birth", "생년월일", "date"),
        ("no", "영주권번호", "number"),
        ("customer.phone", "전화번호", "number"),
        ("no2", "여권번호", "number"),
        ("customer.address", "현주소", "text"),
        ("customer.name", "성명", "text"),
        ("customer.address", "주소", "text"),
        ("agent.relation", "본인과의 관계", "text")
     ])])

FORM("hf131", "전세자금대출 이용 확약서(서울보증보험증권 담보 전세자금대출용)", "bank_form", code="대출-0131",
     title_note="하나은행 공개 서식 No.131 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf132", "다주택처분확약서(서울보증보험)", "bank_form", code="5-06-0896",
     title_note="하나은행 공개 서식 No.132 (대출)",
     sections=[("2년 이내 1주택 초과분을 처분하지 못한 경우", [
        ("item", "본 인", "text"),
        ("no", "대출계좌번호", "number"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf135", "동의서(대출비용지급용)", "bank_form", code="5-06-0738",
     title_note="하나은행 공개 서식 No.135 (대출)",
     sections=[("출금계좌번호: 예금주: 금액: 원", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf137", "대출금 분할실행 신청서(에듀큐론용)", "bank_form", code="대출-0137",
     title_note="하나은행 공개 서식 No.137 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf138", "대출금 수령위임동의서", "bank_form", code="대출-0138",
     title_note="하나은행 공개 서식 No.138 (대출)",
     sections=[("기재사항", [
        ("item", "용도", "text"),
        ("customer.name", "예금주", "text"),
        ("item2", "차주와의 관계", "choice", ["부동산담보대출의경우매도인", "전세자금대출의경우임대인", "차주를대신하여당타행대출의상환을위임받은자", "공사대금수령업체", "상기외제3자(관계기재)"])
     ])])

FORM("hf139", "《기업》 지급보증거래 신청서(서면.전자 지급보증 겸용)", "bank_form", code="5-06-0703",
     title_note="하나은행 공개 서식 No.139 (대출)",
     sections=[("피보증 주채무의 불이행이 있는 때", [
        ("item", "৷ೇ৷‰ݮ‰৷ϱ֬ ਽֤֨", "text"),
        ("item2", "지급보증서 발급방식(택일)", "text"),
        ("item3", "서면 지급 보증서 전자 지급보증서", "text"),
        ("amount", "보증금액", "amount"),
        ("item4", "금 원", "text"),
        ("date", "보증기일", "date"),
        ("date2", "20 년 월 일", "date"),
        ("rate", "보증요율", "percent"),
        ("item5", "보증처 (지급보증 상대처)", "text"),
        ("date3", "보증기간중에기한이도래하는아래의특정채무를보증", "date"),
        ("item6", "피보증채무의 종류 :", "text"),
        ("item7", "인감 (서명) 대조", "text")
     ])])

FORM("hf140", "매출채권 잔액 확인서", "bank_form", code="5-06-0684",
     title_note="하나은행 공개 서식 No.140 (대출)",
     sections=[("본인은 판매기업", [
        ("item", "판매기업에 대한 정보", "text"),
        ("item2", "판매기업명", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item3", "판매기업 결제계좌", "text"),
        ("item4", "입금은행명", "text"),
        ("item5", "본인(구매기업)에 대한 정보", "text"),
        ("company.name", "회사명", "text"),
        ("company.ceo", "대표자", "text"),
        ("company.corp_no", "법인등록번호", "number"),
        ("company.department", "담당부서", "text"),
        ("customer.phone", "전화번호", "number"),
        ("amount", "합 계", "amount")
     ])])

FORM("hf141", "매출채권 잔액 확인서(사전확인용)", "bank_form", code="5-06-0685",
     title_note="하나은행 공개 서식 No.141 (대출)",
     sections=[("본인은 위의 판매기업", [
        ("item", "판매기업에 대한 정보", "text"),
        ("item2", "판매기업명", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item3", "판매기업 결제계좌", "text"),
        ("item4", "입금은행명", "text"),
        ("item5", "본인(구매기업)에 대한 정보", "text"),
        ("company.name", "회사명", "text"),
        ("company.ceo", "대표자", "text"),
        ("company.corp_no", "법인등록번호", "number"),
        ("company.department", "담당부서", "text"),
        ("customer.phone", "전화번호", "number"),
        ("amount", "합 계", "amount")
     ])])

FORM("hf142", "매출채권설정등기통지서", "bank_form", code="5-06-0686",
     title_note="하나은행 공개 서식 No.142 (대출)",
     sections=[("채무자가", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf144", "동산담보 제공 예정내역서(개별동산용)", "bank_form", code="대출-0144",
     title_note="하나은행 공개 서식 No.144 (대출)",
     sections=[("보관장소", [
        ("company.address", "소재지", "text"),
        ("item", "보관장소명(주)", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf145", "동산담보 제공 예정내역서(집합동산용)", "bank_form", code="5-06-0668",
     title_note="하나은행 공개 서식 No.145 (대출)",
     sections=[("보관장소", [
        ("company.address", "소재지", "text"),
        ("item", "보관장소명(주)", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf149", "《기업》금융거래확인서", "bank_form", code="대출-0149",
     title_note="하나은행 공개 서식 No.149 (대출)",
     sections=[("대출금 거래상황", [
        ("item", "당 초 차 입", "text"),
        ("item2", "금융회사 거래성실도 (우량업체, 적격업체등)", "text"),
        ("amount", "금 액", "amount"),
        ("item3", "종 류", "text"),
        ("date", "선정일자", "date"),
        ("date2", "유효기간", "date"),
        ("date3", "미결제 어음.수표 ( 년 월 일현재)", "date"),
        ("item4", "어 음", "text"),
        ("item5", "수 표", "text"),
        ("amount2", "연 체 금 액", "amount"),
        ("amount3", "이 자", "amount")
     ])])

FORM("hf150", "《기업》근저당권유용합의서", "bank_form", code="대출-0150",
     title_note="하나은행 공개 서식 No.150 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf151", "《기업》무역어음인수·할인신청서", "bank_form", code="대출-0151",
     title_note="하나은행 공개 서식 No.151 (대출)",
     sections=[("기재사항", [
        ("item", "금 원(￦ )", "text"),
        ("amount", "승 인 한 도(A)", "amount"),
        ("amount2", "여 신 잔 액(B)", "amount"),
        ("item2", "본 건 신 청 액(C)", "text"),
        ("amount3", "본건 취급 후 잔액(A+B+C)", "amount")
     ])])

FORM("hf152", "《기업》연대보증인(교체·면제)증서", "bank_form", code="대출-0152",
     title_note="하나은행 공개 서식 No.152 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf153", "《기업》질권설정등록청구서", "bank_form", code="대출-0153",
     title_note="하나은행 공개 서식 No.153 (대출)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf155", "채권양도통지서(외국법인용)(K-biz파트너론)", "bank_form", code="대출-0155",
     title_note="하나은행 공개 서식 No.155 (대출)",
     sections=[("양도채권의 표시(Assigned Claims)", [
        ("item", "4. 채무자(Obligor)", "text"),
        ("item2", "5. 특기사항(Special note)", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item3", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf157", "여신거래용 인감명판 등 신고서", "bank_form", code="5-09-0002",
     title_note="하나은행 공개 서식 No.157 (대출)",
     sections=[("위와같은신고등을지체함으로써발생하는손해는본인이전책임을", [
        ("company.name", "상 호", "text"),
        ("company.ceo", "대 표 자", "text"),
        ("customer.address", "주 소", "text"),
        ("item", "명 판", "text")
     ])])
