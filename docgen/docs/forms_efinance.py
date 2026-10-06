"""하나은행 공개 서식 — 선언형 스펙 (31종).

scripts/build_form_specs.py 가 add_template/field_specs/ 에서 생성한다.
직접 고치지 말고 생성 스크립트의 라벨 표를 고칠 것.
서식 하나를 수제 템플릿으로 승격할 때는 여기서 해당 FORM 을 지운다.
"""
from ..formspec import FORM  # noqa: F401

FORM("hf342", "해외은행 계좌정보 수신서비스(SWIFT MT940) 이용신청서", "efinance", code="5-08-0488",
     title_note="하나은행 공개 서식 No.342 (전자금융)",
     sections=[("신청 종류 : □ 신규 □ 해지 □ 변경", [
        ("customer.name", "고객명", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("no", "이용자ID", "number"),
        ("item", "담당자(직위/성명)", "text"),
        ("customer.phone", "전화번호", "number"),
        ("item2", "e-Mail주소", "text"),
        ("company.address", "회사주소", "text"),
        ("item3", "(해외)통지은행 및 계좌 정보", "text"),
        ("item4", "통지은행명", "text"),
        ("item5", "Bank Code(BIC)", "text"),
        ("item6", "거래 인감", "text")
     ])])

FORM("hf344", "기업관계사 서비스 이용계약서(영문)", "efinance", code="5-08-0501",
     title_note="하나은행 공개 서식 No.344 (전자금융)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf346", "기업관계사 서비스 이용신청서", "efinance", code="5-08-0484",
     title_note="하나은행 공개 서식 No.346 (전자금융)",
     sections=[("기재사항", [
        ("item", "신청구분", "text"),
        ("item2", "서비스 종류", "choice", ["국내관계사", "국외관계사"]),
        ("company.corp_no", "법인등록번호", "number"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.name", "회사명", "text"),
        ("company.ceo", "대표자", "text"),
        ("customer.address", "주 소", "text"),
        ("customer.phone", "전화번호", "number"),
        ("item3", "Fax", "text"),
        ("item4", "조회 서비스 (위임범위)", "choice", ["전체", "부분", "예금(", "전체계좌,", "아래에서지정한계좌만조회),", "외환,"]),
        ("no", "관계사ID", "choice", ["실행자", "실행자"]),
        ("no2", "아이디(ID)", "choice", ["실행자", "OTP"]),
        ("amount", "대량한도", "amount"),
        ("item5", "1일 한글로 기재 원", "text"),
        ("no3", "계좌번호 (통장인감)", "number"),
        ("customer.name", "성 명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("agent.relation", "관계", "text")
     ])])

FORM("hf347", "기업관계사 서비스 이용계약서", "efinance", code="5-08-0498",
     title_note="하나은행 공개 서식 No.347 (전자금융)",
     sections=[("주계약사와 관계사간의 위임에 의하여 신청한 기타 위", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf348", "기업관계사 서비스 이용신청서(영문)", "efinance", code="5-08-0491",
     title_note="하나은행 공개 서식 No.348 (전자금융)",
     sections=[("기재사항", [
        ("item", "Application Type", "text"),
        ("item2", "Location of Affiliate", "choice", ["InKorea", "OutsideKorea"]),
        ("company.name", "Company Name", "text"),
        ("item3", "Representative", "text"),
        ("customer.address", "Address", "text"),
        ("item4", "Phone No.", "text"),
        ("item5", "Fax", "text"),
        ("no", "Affiliate’s ID", "choice", ["Executor", "Executor"]),
        ("no2", "ID", "choice", ["Executor", "OTP"]),
        ("item6", "Bulk Transfer Limit", "text"),
        ("item7", "KRW per day", "text"),
        ("customer.name", "Name", "text"),
        ("customer.birth", "Date of Birth", "text"),
        ("item8", "Relationship", "text"),
        ("item9", "Delegator", "text")
     ])])

FORM("hf349", "펌뱅킹 출금전용계좌이용 동의서", "efinance", code="5-08-0708",
     title_note="하나은행 공개 서식 No.349 (전자금융)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf350", "아이부자 걷기챌린지 서비스 동의서", "efinance", code="7-99-0062",
     title_note="하나은행 공개 서식 No.350 (전자금융)",
     sections=[("기재사항", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf352", "하나 sERP 상담신청서", "efinance", code="5-08-0576",
     title_note="하나은행 공개 서식 No.352 (전자금융)",
     sections=[("기재사항", [
        ("company.name", "기업명", "text"),
        ("company.ceo", "대표자명", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item", "담당자명", "text"),
        ("item2", "( - )", "text")
     ])])

FORM("hf353", "CMS Plus 이용신청서(지사)", "efinance", code="5-08-0479",
     title_note="하나은행 공개 서식 No.353 (전자금융)",
     sections=[("신청 구분 : □ 신규 □ 변경 □ 해지", [
        ("company.corp_no", "법인등록번호", "number"),
        ("company.biz_no", "사업자 등록 번호", "number"),
        ("item", "사업자명", "text"),
        ("company.ceo", "대표자", "text"),
        ("customer.address", "주소", "text"),
        ("item2", "대표 연락처 (선택 또는 전부 기재)", "text"),
        ("item3", "지사 출금계좌 지정", "text"),
        ("item4", "구 분", "text"),
        ("no", "아이디(ID)", "number"),
        ("customer.name", "성 명", "text"),
        ("item5", "개별 1회", "text"),
        ("date", "개별 1일", "date"),
        ("item6", "대량 1회", "text"),
        ("date2", "대량 1일", "date"),
        ("no2", "보안(OTP)카드 No", "number"),
        ("account", "출금 계좌", "text"),
        ("date3", "접수 일자", "date"),
        ("date4", "등록일자", "date"),
        ("customer.birth", "생년월일", "date"),
        ("agent.relation", "관 계", "text"),
        ("item7", "대표이사 (법인인감)", "text")
     ])])

FORM("hf354", "CMS Plus 이용계약서", "efinance", code="5-08-0500",
     title_note="하나은행 공개 서식 No.354 (전자금융)",
     sections=[("고객 시스템과 CMS System과의 각종 금융거래", [
        ("item", "Server", "text"),
        ("item2", "PC", "text"),
        ("item3", "모니터", "text"),
        ("item4", "설치장소", "text")
     ])])

FORM("hf355", "CMS Mega 이용계약서", "efinance", code="5-08-0499",
     title_note="하나은행 공개 서식 No.355 (전자금융)",
     sections=[("고객의 ERP시스템과 CMS서버와의 각종 금융거래데", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf356", "CMS Plus 이용신청서", "efinance", code="5-08-0478",
     title_note="하나은행 공개 서식 No.356 (전자금융)",
     sections=[("신청 구분 : □ 신규 □ 변경 □ 해지", [
        ("item", "회사명(대표자)", "text"),
        ("company.corp_no", "법인 등록번호", "number"),
        ("company.biz_no", "사업자 등록번호", "number"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "이용 Model", "choice", ["인터넷"]),
        ("item3", "(맞춤기능 또는 시스템 연계내용)", "text"),
        ("amount", "주2) 고객 시스템 연계수수료 등", "amount"),
        ("account", "계좌번호", "number"),
        ("item4", "거래인감(서명)", "text"),
        ("customer.name", "예금주", "text"),
        ("item5", "관리점", "text"),
        ("item6", "구분", "text"),
        ("no", "아이디(ID)", "number"),
        ("customer.name", "성 명", "text"),
        ("item7", "부서/직위", "text"),
        ("item8", "개별 1회", "text"),
        ("date", "개별 1일", "date"),
        ("item9", "대량 1회", "text"),
        ("date2", "대량 1일", "date"),
        ("no2", "보안(OTP)카드 No", "number"),
        ("item10", "총괄 관리자용", "text"),
        ("item11", "일반 이용자용", "text"),
        ("account", "출금 계좌", "text"),
        ("date3", "접수 일자", "date"),
        ("date4", "등록일자", "date"),
        ("customer.birth", "생년월일", "date"),
        ("agent.relation", "관 계", "text"),
        ("item12", "대표이사 (법인인감)", "text")
     ])])

FORM("hf357", "CMSiNet 지사정보 등록신청서", "efinance", code="5-08-0481",
     title_note="하나은행 공개 서식 No.357 (전자금융)",
     sections=[("기재사항", [
        ("company.biz_no", "사업자등록번호", "number"),
        ("item", "사업자명", "text"),
        ("item2", "사업자 대표", "text"),
        ("customer.address", "주 소", "text"),
        ("customer.phone", "전화번호", "number"),
        ("company.fax", "팩스번호", "number"),
        ("customer.email", "e-mail", "text")
     ])])

FORM("hf358", "CMS Global 이용신청서", "efinance", code="5-08-0391",
     title_note="하나은행 공개 서식 No.358 (전자금융)",
     sections=[("기재사항", [
        ("no", "사업자 등록번호 *", "number"),
        ("item", "회사명(대표자) *", "text"),
        ("item2", "주 소 *", "text"),
        ("item3", "e-mail주소 *", "text"),
        ("item4", "종류", "text"),
        ("item5", "口 초과 1개 국가당 KRW 50,000-", "text"),
        ("no2", "ID *", "number"),
        ("customer.name", "성 명", "text"),
        ("employer.position", "직 위", "text"),
        ("company.department", "부 서", "text"),
        ("customer.phone", "휴대폰", "text"),
        ("item6", "직통전화 *", "text")
     ])])

FORM("hf359", "하나 sERP 이용신청서", "efinance", code="5-08-0313",
     title_note="하나은행 공개 서식 No.359 (전자금융)",
     sections=[("기재사항", [
        ("item", "신 청 구 분", "choice", ["신고", "해지", "변경"]),
        ("no", "기업인터넷뱅킹 ID", "number"),
        ("company.name", "회 사 명", "text"),
        ("company.biz_no", "사 업 자 등 록 번 호", "number"),
        ("item2", "업 태 / 종 목", "text"),
        ("company.ceo", "대 표 자 명", "text"),
        ("item3", "( - )", "text"),
        ("item4", "담 당 자 명", "text"),
        ("company.department", "담 당 부 서", "text"),
        ("item5", "담 당 부 서 연 락 처", "text"),
        ("item6", "세금계산서 교부용e-Mail", "text"),
        ("item7", "출금계좌(하나은행)", "text"),
        ("customer.name", "예 금 주", "text"),
        ("item8", "본인 및 인감 확인", "text")
     ])])

FORM("hf362", "자동화기기 이용(신규,해지,변경)신청서", "efinance", code="전자금융-0362",
     title_note="하나은행 공개 서식 No.362 (전자금융)",
     sections=[("출금 또는 이체를 완료한 거래는 정정 또는 취소할 ", [
        ("customer.name", "성 명", "text"),
        ("customer.birth", "생 년 월 일", "date"),
        ("customer.phone", "전 화 번 호", "number")
     ])])

FORM("hf365", "Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(영문)", "efinance", code="전자금융-0365",
     title_note="하나은행 공개 서식 No.365 (전자금융)",
     sections=[("기재사항", [
        ("item", "(Korean) *", "text"),
        ("item2", "(English) *", "text"),
        ("item3", "Postal Code *", "text"),
        ("item4", "Address *", "text"),
        ("item5", "Phone No.*", "text"),
        ("item6", "Fax No.*", "text"),
        ("item7", "Signature/Seal *", "text")
     ])])

FORM("hf366", "Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(국문)", "efinance", code="전자금융-0366",
     title_note="하나은행 공개 서식 No.366 (전자금융)",
     sections=[("기재사항", [
        ("no", "법인등록번호 *", "number"),
        ("no2", "사업자 등록번호 *", "number"),
        ("item", "(국문) *", "text"),
        ("item2", "(영문) *", "text"),
        ("item3", "교육기관 대표자*", "text"),
        ("no3", "우편번호 *", "number"),
        ("item4", "주소 *", "text"),
        ("no4", "전화번호 *", "number"),
        ("no5", "팩스번호 *", "number"),
        ("item5", "관계 (부서/직위) *", "text"),
        ("item6", "서명/인감 *", "text"),
        ("item7", "교육기관 명: 주 소 :", "text"),
        ("item8", "교육기관 대표자 : (학교장)", "text")
     ])])

FORM("hf367", "Hana 1Q bank CMS iNet 서비스 이용 추가 계약서(iSBS)", "efinance", code="전자금융-0367",
     title_note="하나은행 공개 서식 No.367 (전자금융)",
     sections=[("고객이 본 계약의 내용을 이행하지 않는 경우", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf368", "가상계좌서비스 이용계약서(외화)", "efinance", code="전자금융-0368",
     title_note="하나은행 공개 서식 No.368 (전자금융)",
     sections=[("외화가상계좌의 사용용도(최대한 구체적으로 기재 요망", [
        ("item", "입금모계좌", "text"),
        ("fx_amount", "외화", "fx_amount"),
        ("amount", "수수료인출계좌", "amount"),
        ("item2", "원화", "text"),
        ("date", "정 산 일", "choice", ["입금당일정산", "입금후영업일에정산"]),
        ("item3", "정산방식", "choice", ["실시간입금", "일괄정산"]),
        ("item4", "예금주명 표기방식", "choice", ["예금주명만표기", "예금주명+부기명"]),
        ("item5", "가상계좌 재사용여부", "choice", ["재사용", "1회만사용"]),
        ("count", "가상계좌별 입금횟수 제한", "choice", ["제한없음", "매월회이하가능"])
     ])])

FORM("hf369", "가상계좌서비스 이용계약서(원화)", "efinance", code="전자금융-0369",
     title_note="하나은행 공개 서식 No.369 (전자금융)",
     sections=[("가상계좌의 사용용도(최대한 구체적으로 기재 요망)", [
        ("item", "입금 모계좌", "text"),
        ("amount", "수수료 인출계좌", "amount"),
        ("date", "정 산 일", "choice", ["입금당일정산", "입금후영업일에정산"]),
        ("item2", "정산방식", "choice", ["일괄정산", "실시간입금"]),
        ("item3", "예금주명 표기방식", "choice", ["예금주명만표기", "예금주명+부기명"]),
        ("item4", "가상계좌 재사용여부", "choice", ["재사용", "1회만사용"]),
        ("count", "가상계좌별 입금횟수 제한", "choice", ["제한없음", "매월회이하가능"])
     ])])

FORM("hf370", "펌뱅킹서비스 계약서(외화)", "efinance", code="5-08-0257",
     title_note="하나은행 공개 서식 No.370 (전자금융)",
     sections=[("“이용기관”이 요청하는 외화정기예금의 신규 개설 및", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf371", "펌뱅킹서비스 계약서(원화)", "efinance", code="전자금융-0371",
     title_note="하나은행 공개 서식 No.371 (전자금융)",
     sections=[("“이용기관”이 “납부자”로부터 출금동의를 받지 않고", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf372", "전산기기 임대차계약서(Hana 1Q bank CMS)", "efinance", code="전자금융-0372",
     title_note="하나은행 공개 서식 No.372 (전자금융)",
     sections=[("“장치”에 다른 기구를 설치할 경우 또는 “장치”를", [
        ("item", "Server", "text"),
        ("item2", "PC", "text"),
        ("item3", "모니터", "text"),
        ("item4", "설치장소", "text")
     ])])

FORM("hf374", "전자어음 이용(변경,해지) 신청서", "efinance", code="전자금융-0374",
     title_note="하나은행 공개 서식 No.374 (전자금융)",
     sections=[("고객정보", [
        ("item", "거래구분", "choice", ["신규가입", "변경해지(", "발행해지", "전체해지)"]),
        ("item2", "회원구분", "choice", ["발행인(수취,배서포함)", "수취/배서인", "보증인"]),
        ("item3", "법인명(성명)", "text"),
        ("company.ceo", "대표자", "text"),
        ("no", "사업자등록번호(법인)", "number"),
        ("company.biz_item", "업종", "text"),
        ("date", "생년월일(개인/개인사업자)", "date"),
        ("item4", "규모", "choice", ["대기업", "중소기업", "개인사업자", "개인"]),
        ("company.phone", "대표전화", "text"),
        ("company.department", "담당부서", "text"),
        ("company.phone", "회사전화", "text"),
        ("customer.phone", "휴대폰", "text"),
        ("company.fax", "FAX", "text"),
        ("item5", "E-Mail", "text"),
        ("item6", "발행(당좌)지정계좌", "text"),
        ("item7", "거래인감", "text"),
        ("item8", "수취(요구불)지정계좌", "text"),
        ("item9", "변경 항목", "text"),
        ("item10", "[변경전]", "text")
     ])])

FORM("hf375", "자금관리서비스 이용계약서", "efinance", code="전자금융-0375",
     title_note="하나은행 공개 서식 No.375 (전자금융)",
     sections=[("자금집금서비스", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf376", "위임장(해외체류자 전자금융용)", "efinance", code="5-08-0487",
     title_note="하나은행 공개 서식 No.376 (전자금융)",
     sections=[("인감란에는 출금계좌통장의 인감을 날인하여 주십시요.", [
        ("customer.name", "성 명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주 소", "text"),
        ("agent.relation", "본인과의관계", "text")
     ])])

FORM("hf377", "해외영업점 계좌개설 신청서", "efinance", code="전자금융-0377",
     title_note="하나은행 공개 서식 No.377 (전자금융)",
     sections=[("기재사항", [
        ("item", "한글 Korean", "text"),
        ("date", "생년월일 Date of Birth", "date"),
        ("item2", "국 적 Nationality", "text"),
        ("no", "여권번호 Passport No.", "number"),
        ("item3", "여권유효기일 Date of Expiry", "text"),
        ("item4", "영문 English", "text"),
        ("item5", "선택Selective", "choice", ["TelephoneNo.", "MobilephoneNo."]),
        ("currency", "개설통화 Currency", "currency"),
        ("item6", "접수 은행/지점명 Bank/Branch", "text"),
        ("item7", "고객명(Name)", "text"),
        ("no2", "계좌번호(A/C No.)", "number")
     ])])

FORM("hf378", "글로벌뱅킹서비스 이용,변경,해지 신청서", "efinance", code="5-08-0480",
     title_note="하나은행 공개 서식 No.378 (전자금융)",
     sections=[("목적", [
        ("item", "성 명 Name", "text"),
        ("item2", "한글 Korean", "text"),
        ("date", "생년월일 Date of Birth", "date"),
        ("no", "여권번호 Passport No.", "number"),
        ("item3", "영문 English", "text"),
        ("item4", "해외주소 Overseas Address", "text"),
        ("no2", "서비스이용 계좌번호 A/C No.", "number"),
        ("item5", "개설은행/지점명 Bank/Branch", "text"),
        ("item6", "서명/인감 Signature", "text")
     ])])

FORM("hf379", "주류구매전용카드 가맹점가입신청서", "efinance", code="전자금융-0379",
     title_note="하나은행 공개 서식 No.379 (전자금융)",
     sections=[("대표자 신분증 사본 1부.", [
        ("company.name", "상호", "text"),
        ("customer.name", "성명", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item", "☐ ☐ ☐ - ☐ ☐ ☐", "text"),
        ("account", "계좌번호", "number"),
        ("customer.name", "예금주", "text"),
        ("company.established", "개업일", "date"),
        ("company.biz_item", "업종", "text"),
        ("item2", "취급품목", "text"),
        ("company.capital", "자본금", "text"),
        ("company.employees", "종업원수", "text"),
        ("item3", "소속", "text")
     ])])

FORM("hf380", "금융결제원CMS 이용계약서", "efinance", code="5-08-0210",
     title_note="하나은행 공개 서식 No.380 (전자금융)",
     sections=[("기재사항", [
        ("item", "출금이체", "text"),
        ("item2", "입금이체", "text"),
        ("item3", "구 분", "text"),
        ("item4", "입금(출금)대행비용", "text"),
        ("item5", "이체건당", "text"),
        ("item6", "120원", "text"),
        ("item7", "260원", "text"),
        ("item8", "100원", "text"),
        ("no", "계약지점코드", "number"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item9", "－", "text")
     ])])
