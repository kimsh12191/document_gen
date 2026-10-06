"""하나은행 공개 서식 — 선언형 스펙 (30종).

scripts/build_form_specs.py 가 add_template/field_specs/ 에서 생성한다.
직접 고치지 말고 생성 스크립트의 라벨 표를 고칠 것.
서식 하나를 수제 템플릿으로 승격할 때는 여기서 해당 FORM 을 지운다.
"""
from ..formspec import FORM  # noqa: F401

FORM("hf004", "보호예수품 반환 의뢰서", "bank_form", code="5-08-0776",
     title_note="하나은행 공개 서식 No.4 (예금)",
     sections=[("신청사항(반환)", [
        ("item", "예수방법", "choice", ["봉함예수", "개봉예수"]),
        ("count", "예수수량", "count"),
        ("item2", "자 필 기 재", "text"),
        ("customer.birth", "생년월일 (사업자등록번호)", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text")
     ])])

FORM("hf005", "보호예수 의뢰서", "bank_form", code="5-08-0026",
     title_note="하나은행 공개 서식 No.5 (예금)",
     sections=[("신청사항", [
        ("item", "감사통할책임자", "text"),
        ("item2", "예수종류", "choice", ["봉함예수", "개봉예수"]),
        ("count", "예수수량", "count"),
        ("date", "만기일자", "choice", ["6개월(년월일)", "예적금만기일(년월일)"]),
        ("item3", "자 필 기 재", "text"),
        ("item4", "보호예수증서 약관 수령확인", "text"),
        ("item5", "수령 방법", "choice", ["영업점"]),
        ("customer.birth", "생년월일 (사업자등록번호)", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text")
     ])])

FORM("hf007", "질권실행 의뢰서(수신_제3자 질권용)", "bank_form", code="5-08-0765",
     title_note="하나은행 공개 서식 No.7 (예금)",
     sections=[("기재사항", [
        ("customer.birth", "생년월일 (사업자등록번호)", "date"),
        ("customer.phone", "연락처", "text"),
        ("customer.address", "주소", "text")
     ])])

FORM("hf008", "질권해지 통지서(수신_제3자 질권용)", "bank_form", code="5-08-0099",
     title_note="하나은행 공개 서식 No.8 (예금)",
     sections=[("기재사항", [
        ("customer.birth", "생년월일 (사업자등록번호)", "date"),
        ("customer.phone", "연락처", "text"),
        ("customer.address", "주소", "text")
     ])])

FORM("hf009", "질권설정 승낙의뢰서(수신_제3자 질권용)", "bank_form", code="5-08-0075",
     title_note="하나은행 공개 서식 No.9 (예금)",
     sections=[("질권설정 예금현황", [
        ("customer.birth", "생년월일 (사업자등록번호)", "date"),
        ("customer.phone", "연락처", "text"),
        ("customer.address", "주소", "text")
     ])])

FORM("hf010", "주식(사채)납입금 수납대행의뢰서(보관증명서 발급의뢰서 겸용)", "bank_form", code="5-08-0045",
     title_note="하나은행 공개 서식 No.10 (예금)",
     sections=[("신청 사항", [
        ("item", "주식납입금수납", "choice", ["설립", "신주발행"]),
        ("item2", "증명서 종류", "choice", ["보관증명서"]),
        ("item3", "사채납입금수납", "choice", ["사채발행(사채종류"]),
        ("date", "년 월 일부터 년 월 일까지", "date"),
        ("date", "년 월 일", "date"),
        ("item4", "하나은행 (부)지점", "text"),
        ("company.name", "회 사 명", "text"),
        ("item5", "위탁회사 주소", "text")
     ])])

FORM("hf016", "종합금융상품 ON-LINE 거래 약정서", "bank_form", code="5-08-0702",
     title_note="하나은행 공개 서식 No.16 (예금)",
     sections=[("(출금)", [
        ("customer.name", "예 금 주", "text"),
        ("date", "사업자등록번호 (생년월일)", "date"),
        ("item", "통장인감", "text"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "전화번호", "number"),
        ("account", "계좌번호", "number"),
        ("item2", "참고사항 (신청내용 등)", "text")
     ])])

FORM("hf017", "종합금융상품 ON-LINE_거래 (이체)신청서", "bank_form", code="예금-0017",
     title_note="하나은행 공개 서식 No.17 (예금)",
     sections=[("기재사항", [
        ("item", "성명 (회사명)", "text"),
        ("customer.phone", "전 화 번 호", "number"),
        ("no", "Fax 번호", "number"),
        ("item2", "예금종류", "choice", ["발행어음", "CMA"]),
        ("account", "계좌번호", "number"),
        ("amount", "입금 금액", "amount"),
        ("amount2", "인출금액", "amount"),
        ("date", "기간(만기일)", "date"),
        ("item3", "이체 방법", "choice", ["지준", "전금", "계좌"]),
        ("rate", "이율", "percent"),
        ("item4", "입금 방법", "choice", ["지준", "전금", "계좌"]),
        ("amount3", "지준 입금액", "amount"),
        ("amount4", "전금 입금액", "amount"),
        ("amount5", "계좌 입금액", "amount"),
        ("item5", "인출방법", "choice", ["부리식", "할인식"]),
        ("item6", "※참고사항", "text")
     ])])

FORM("hf018", "본인계좌 일괄지급정지 조회신청서", "bank_form", code="예금-0018",
     title_note="하나은행 공개 서식 No.18 (예금)",
     sections=[("신청사항", [
        ("item", "자 필 기 재", "text"),
        ("item2", "신청내용", "choice", ["금융기관별조회(", "전체금융기관", "전체은행", "하나", "신한", "국민"]),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf019", "본인계좌 일괄지급정지(해제)신청서", "bank_form", code="예금-0019",
     title_note="하나은행 공개 서식 No.19 (예금)",
     sections=[("고객확인사항", [
        ("item", "이름", "text"),
        ("customer.rrn", "주민등록번호", "number"),
        ("customer.phone", "연락처", "text")
     ])])

FORM("hf020", "노무비닷컴계좌 개설 및 지급이체서비스 이용 신청서", "bank_form", code="5-08-0553",
     title_note="하나은행 공개 서식 No.20 (예금)",
     sections=[("신청기업정보", [
        ("company.name", "기업명", "text"),
        ("company.biz_no", "사업자번호", "number"),
        ("customer.address", "주 소", "text"),
        ("company.department", "부 서", "text"),
        ("customer.name", "성 명", "text"),
        ("item", "TEL", "text"),
        ("company.fax", "FAX", "text"),
        ("item2", "법인", "choice", ["공통", "대표자신청시", "대리인신청시", "법인인감및통장도장"])
     ])])

FORM("hf021", "일괄처리(지급)요청서", "bank_form", code="5-08-0591",
     title_note="하나은행 공개 서식 No.21 (예금)",
     sections=[("타행환 입금시 신청금액은 건별 최고 5억원 입니다.", [
        ("amount", "합계", "amount"),
        ("amount2", "수수료", "amount"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount3", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf023", "하도급협력대금통장(상생결제 노무비) 지급이체서비스 이용신청서", "bank_form", code="5-08-0552",
     title_note="하나은행 공개 서식 No.23 (예금)",
     sections=[("신청기관정보", [
        ("company.name", "업 체 명", "text"),
        ("company.biz_no", "사업자번호", "number"),
        ("customer.zipcode", "우편번호", "number"),
        ("company.department", "부서", "text"),
        ("customer.name", "성 명", "text"),
        ("item", "TEL", "text"),
        ("company.fax", "F A X", "text"),
        ("item2", "법인", "choice", ["공통", "대표자신청시", "대리인신청시"])
     ])])

FORM("hf029", "사용인감계(금융계좌개설용)", "bank_form", code="5-08-0056",
     title_note="하나은행 공개 서식 No.29 (예금)",
     sections=[("기재사항", [
        ("item", "사 용 인 감", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("item2", "연락처(선택항목)", "text"),
        ("agent.relation", "본인과의 관계", "text"),
        ("item3", "주소(선택항목)", "text")
     ])])

FORM("hf030", "국내원천소득 제한세율 적용신청서(외국법인용-영문)", "bank_form", code="예금-0030",
     title_note="하나은행 공개 서식 No.30 (예금)",
     sections=[("Determination of Beneficial ", [
        ("item", "Filing No.", "text"),
        ("item2", "Filing Date", "text"),
        ("item3", "1. Applicant Information", "text"),
        ("item4", "② Name of Corporation", "text"),
        ("item5", "⑥ Address", "text"),
        ("item6", "③ Name of Representative", "text"),
        ("item7", "⑦ Country of Residence", "text"),
        ("item8", "⑧ Country Code", "text"),
        ("item9", "⑤ Date of Incorporation", "text"),
        ("item10", "⑨ Telephone Number", "text"),
        ("item11", "⑬ Address or Location", "text")
     ])])

FORM("hf031", "국내원천소득 제한세율 적용신청서(외국법인용)", "bank_form", code="3-08-1298",
     title_note="하나은행 공개 서식 No.31 (예금)",
     sections=[("신청인의 인적사항", [
        ("item", "② 법인명", "text"),
        ("item2", "⑥ 주소", "text"),
        ("item3", "③ 대표자 성명", "text"),
        ("item4", "⑦ 거주지국", "text"),
        ("no", "④ 납세자번호", "number"),
        ("no2", "⑧ 국가코드", "number"),
        ("date", "⑤ 설립년월일", "date"),
        ("no3", "⑨ 전화번호", "number"),
        ("item5", "⑭ 거주지국의 세법상 납세의무가 있습니까?", "text"),
        ("item6", "⑮ 지급받는 국내원천소득의 실질귀속자입니까?", "text"),
        ("item7", "⑪ 성명 또는 법인명", "text"),
        ("no4", "⑫ 사업자(주민)등록번호", "number"),
        ("item8", "⑬ 주소 또는 소재지", "text")
     ])])

FORM("hf032", "국내원천소득 제한세율 적용신청서(비거주자용)", "bank_form", code="3-08-1297",
     title_note="하나은행 공개 서식 No.32 (예금)",
     sections=[("신청인의 인적사항", [
        ("item", "(거주지국 주소) (국내 거소)", "text"),
        ("no", "③ 납세자번호", "number"),
        ("date", "④ 생년월일", "date"),
        ("item2", "⑤ 거주지국", "text"),
        ("no2", "⑥ 거주지국코드", "number"),
        ("item3", "(거주지 전화) (국내 전화)", "text"),
        ("item4", "㉮ 국내에 주소를 두고 있습니까?", "text"),
        ("item5", "㉳ 대한민국의 공무원입니까?", "text"),
        ("item6", "⑪ 성명 또는 법인명", "text"),
        ("no3", "⑫ 사업자(주민)등록번호", "number"),
        ("item7", "⑬ 주소 또는 소재지", "text")
     ])])

FORM("hf033", "국내원천소득 제한세율 적용신청서(비거주자용-영문)", "bank_form", code="5-08-0177",
     title_note="하나은행 공개 서식 No.33 (예금)",
     sections=[("Applicant Information", [
        ("item", "Filing No.", "text"),
        ("item2", "Filing Date", "text"),
        ("item3", "④ Date of Birth", "text"),
        ("item4", "⑤ Country of Residence", "text"),
        ("item5", "⑥ Country Code", "text"),
        ("item6", "⑬ Address or Location", "text")
     ])])

FORM("hf034", "확인서(잔액통보생략용)", "bank_form", code="5-08-0067",
     title_note="하나은행 공개 서식 No.34 (예금)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf035", "수표·어음용지 폐기신고서", "bank_form", code="5-08-0030",
     title_note="하나은행 공개 서식 No.35 (예금)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf036", "예금(신탁) 이관 의뢰서", "bank_form", code="예금-0036",
     title_note="하나은행 공개 서식 No.36 (예금)",
     sections=[("기재사항", [
        ("item", "이 관 점", "text"),
        ("item2", "수 관 점", "text"),
        ("item3", "예금(신탁)종류", "text"),
        ("account", "계 좌 번 호", "number"),
        ("item4", "예금주(위탁자)", "text"),
        ("amount", "예금(신탁)잔액", "amount"),
        ("item5", "현 취 급 점 명", "text")
     ])])

FORM("hf037", "위탁유가증권 반환청구서", "bank_form", code="5-08-0042",
     title_note="하나은행 공개 서식 No.37 (예금)",
     sections=[("기재사항", [
        ("no", "유가증권수탁 통장번호", "number"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf038", "수표(어음)발행사실 확인의뢰서", "bank_form", code="5-08-0029",
     title_note="하나은행 공개 서식 No.38 (예금)",
     sections=[("기재사항", [
        ("item", "은행사용란", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf039", "유가증권 수탁약정서", "bank_form", code="예금-0039",
     title_note="하나은행 공개 서식 No.39 (예금)",
     sections=[("기재사항", [
        ("item", "신청인 성명(예금주)", "text"),
        ("item2", "거래인감 (또는 서명)", "text"),
        ("no", "추심대전 입금계좌번호", "number"),
        ("customer.birth", "생년월일 (사업자등록번호)", "date"),
        ("item3", "주소 (선택 또는 전부기재)", "choice", ["자택", "직장"]),
        ("item4", "연락처 (선택 또는 전부기재)", "choice", ["자택", "직장", "휴대폰", "이메일"]),
        ("item5", "보관어음 월별 잔고현황 통지여부", "text")
     ])])

FORM("hf041", "사고신고 담보금 지급정지가처분담보금 처리를 위한 약정서", "bank_form", code="예금-0041",
     title_note="하나은행 공개 서식 No.41 (예금)",
     sections=[("고객이 당해어음을 회수하여 제시하는 경우", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf042", "사채원리금 지급대행 계약서", "bank_form", code="예금-0042",
     title_note="하나은행 공개 서식 No.42 (예금)",
     sections=[("사채의 명칭 :", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf043", "세금우대종합저축(비과세저축) 제변경신고서(비과세공용)", "bank_form", code="예금-0043",
     title_note="하나은행 공개 서식 No.43 (예금)",
     sections=[("기재사항", [
        ("item", "예금/신탁 종류", "text"),
        ("account", "계 좌 번 호", "number"),
        ("customer.name", "성 명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("item2", "주 소 (선택항목)", "text"),
        ("item3", "신청구분", "choice", ["한도설정", "한도증액", "한도감액", "장애인등록", "장애인해제", "상속인등록"]),
        ("item4", "변 경 내 용", "text"),
        ("item5", "변 경 전", "text"),
        ("item6", "변 경 후", "text"),
        ("amount", "한 도 설 정", "amount"),
        ("amount2", "한 도 증 액", "amount"),
        ("amount3", "한 도 감 액", "amount"),
        ("item7", "상속인 등록", "text")
     ])])

FORM("hf044", "예금(신탁) 양도승낙 의뢰서 및 양도승낙서", "bank_form", code="예금-0044",
     title_note="하나은행 공개 서식 No.44 (예금)",
     sections=[("기재사항", [
        ("item", "예금주(양도인) (위탁자겸 수익자)", "text"),
        ("item2", "예금(신탁)종별", "text"),
        ("amount", "금 액", "amount"),
        ("account", "계 좌 번 호", "number"),
        ("date", "만 기 일", "date")
     ])])

FORM("hf045", "야간금고입금의뢰서", "bank_form", code="예금-0045",
     title_note="하나은행 공개 서식 No.45 (예금)",
     sections=[("수표류는 뒷면 명세란에 내역을 기재하여 주십시오.", [
        ("no", "입금가방 번호", "number"),
        ("item", "담 당", "text"),
        ("amount", "입 금 총 액", "amount"),
        ("item2", "金 원整", "text"),
        ("item3", "현 금", "text"),
        ("item4", "수 표 류", "text"),
        ("item5", "당 점 권", "text"),
        ("item6", "원", "text"),
        ("item7", "소 계(A)", "text"),
        ("item8", "소 계(B)", "text"),
        ("item9", "총 계(A+B) 원", "text"),
        ("item10", "총 계(A+B)", "text"),
        ("amount2", "금 액", "amount"),
        ("amount3", "합 계", "amount")
     ])])

FORM("hf046", "목돈을 불리는 통장 거래신청서", "bank_form", code="예금-0046",
     title_note="하나은행 공개 서식 No.46 (예금)",
     sections=[("기재사항", [
        ("item", "확 인", "text"),
        ("customer.name", "성명", "text"),
        ("customer.rrn", "주민등록번호", "number"),
        ("item2", "자택", "text"),
        ("employer.name", "근무처", "text"),
        ("no", "모계좌(이체지정계좌) 계좌번호", "number"),
        ("date", "일자", "date"),
        ("item3", "변경인감", "text")
     ])])
