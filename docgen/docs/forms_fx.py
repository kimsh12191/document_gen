"""하나은행 공개 서식 — 선언형 스펙 (127종).

scripts/build_form_specs.py 가 add_template/field_specs/ 에서 생성한다.
직접 고치지 말고 생성 스크립트의 라벨 표를 고칠 것.
서식 하나를 수제 템플릿으로 승격할 때는 여기서 해당 FORM 을 지운다.
"""
from ..formspec import FORM  # noqa: F401

FORM("hf201", "거래외국환지정(변경)신청서(영문)", "fx", code="5-09-0450",
     title_note="하나은행 공개 서식 No.201 (외환)",
     sections=[("기재사항", [
        ("item", "(Identity verification)", "text"),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf202", "거래외국환지정(변경)신청서", "fx", code="3-09-1048",
     title_note="하나은행 공개 서식 No.202 (외환)",
     sections=[("기재사항", [
        ("item", "(실명확인)", "text"),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf203", "주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(영문)", "fx", code="5-09-0484",
     title_note="하나은행 공개 서식 No.203 (외환)",
     sections=[("기재사항", [
        ("item", "Foreign Investor", "choice", ["Foreigncompany"]),
        ("item2", "② Nationality", "text"),
        ("item3", "(Korean)", "text"),
        ("item4", "(English)", "text"),
        ("item5", "Others", "text"),
        ("item6", "⑫ Purpose of Investment", "text"),
        ("item7", "Cash Amount", "text"),
        ("fx_amount", "won(USD )", "fx_amount"),
        ("item8", "Capital Goods", "text"),
        ("item9", "Other", "text"),
        ("item10", "Par Value per Stock(B)", "text")
     ])])

FORM("hf204", "주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(국문)", "fx", code="5-09-0485",
     title_note="하나은행 공개 서식 No.204 (외환)",
     sections=[("기재사항", [
        ("item", "외국 투자가", "choice", ["외국법인", "국제경제협력기구"]),
        ("item2", "② 국적", "text"),
        ("no", "③ 주소 (영문) (전화번호 : )", "number"),
        ("item3", "(국문)", "text"),
        ("no2", "⑤ 사업자등록번호(본사)", "number"),
        ("item4", "(영문)", "text"),
        ("no3", "본사 (전화번호 : )", "number"),
        ("no4", "주공장(주사업장)소재지 (전화번호 : )", "number"),
        ("item5", "⑦ 하려는(하고 있는) 사업", "text"),
        ("item6", "기존 주 취득 시 원", "text"),
        ("item7", "취득(출연) 전 원", "text"),
        ("item8", "취득(출연) 후 원", "text"),
        ("item9", "⑫ 투자목적", "text"),
        ("fx_amount", "원(USD 상당)", "fx_amount"),
        ("amount", "⑮ 금번 외국인투자금액", "amount"),
        ("amount2", "취득총액 : 원(USD 상당)", "amount"),
        ("amount3", "1주(좌)당 액면가액(B)", "amount"),
        ("amount4", "1주(좌)당 취득가액(C)", "amount"),
        ("amount5", "액면총액(A×B)", "amount"),
        ("amount6", "취득총액(A×C)", "amount"),
        ("amount7", "액면총액 : 원", "amount"),
        ("item10", "⑱ 금번 투자에 따른 예상 근로자수", "text"),
        ("item11", "명", "text")
     ])])

FORM("hf205", "외국환거래법시행령상 거주성확인서", "fx", code="5-09-0545",
     title_note="하나은행 공개 서식 No.205 (외환)",
     sections=[("신청인의 인적사항", [
        ("item", "한글(KOREAN)", "text"),
        ("item2", "영문(ENGLISH)", "text"),
        ("customer.address", "주 소", "text"),
        ("customer.rrn", "주민등록번호", "number"),
        ("no", "여권번호", "number"),
        ("customer.nationality", "국적", "text"),
        ("item3", "항 목", "text"),
        ("item4", "㉮ 외국에서 영업활동에 종사하고 있습니까?", "text"),
        ("item5", "㉰ 국내에서 영업활동에 종사하고 있습니까?", "text"),
        ("item6", "㉱ 6개월 이상 국내에서 체재하고 있습니까?", "text")
     ])])

FORM("hf206", "연간사업실적보고서(투자잔액 1,000만불 초과 기업)", "fx", code="5-09-0201",
     title_note="하나은행 공개 서식 No.206 (외환)",
     sections=[("한국투자자(모기업) 개요", [
        ("item", "투자자명 담 당 자", "text"),
        ("item2", "계열명", "text"),
        ("item3", "소속부서: 직성명: 전화:", "text"),
        ("item4", "업종(중분류)1)", "text"),
        ("item5", "사후관리은행", "text"),
        ("item6", "투자자 법인성격", "choice", ["실제영업법인", "특수목적회사(SPC)"]),
        ("item7", "외국인투자기업2) 여부", "choice", ["아니오"]),
        ("item8", "법인명1)", "text"),
        ("company.ceo", "대표자", "text"),
        ("item9", "소재지(국가주성)2) , ,", "text"),
        ("item10", "투자업종3)", "text"),
        ("item11", "주요취급품목4)", "text"),
        ("date", "설립등기일", "date"),
        ("date2", "영업개시일", "date"),
        ("item12", "법인성격", "choice", ["실제영업법인", "특수목적회사(SPC)-최종투자목적국"]),
        ("item13", "설립형태", "choice", ["신설법인설립", "기존법인지분인수-지분인수비율"]),
        ("item14", "투자형태6)", "choice", ["단독투자", "공동투자", "합작투자(한국측투자비율"]),
        ("item15", "지배구조", "choice", ["비지주회사", "지주회사"]),
        ("company.name", "상호 또는 성명", "text"),
        ("item16", "순투자액8)(천미불)", "text"),
        ("item17", "전기말", "text"),
        ("item18", "금기말", "text"),
        ("amount", "합 계", "amount"),
        ("item19", "현지법인 자본현황", "text"),
        ("item20", "천미불", "text"),
        ("item21", "한국투자자 지분투자 내역", "text"),
        ("item22", "대여금 (단위 : 천미불)", "text"),
        ("item23", "주투자자 관계사1)", "text"),
        ("item24", "계(A)", "text"),
        ("item25", "채권인수2) (단위 : 천미불)", "text"),
        ("item26", "계(B)", "text"),
        ("amount2", "합계(A+B)", "amount"),
        ("amount3", "금액(천미불)", "amount"),
        ("item27", "지분투자", "text"),
        ("item28", "대부투자 (대여금 및 채권인수)", "text"),
        ("item29", "매출채권", "text"),
        ("item30", "배 당 금", "text"),
        ("item31", "한국투자자앞 지급액", "text"),
        ("item32", "차입처", "text"),
        ("item33", "보증자", "text"),
        ("date3", "차입기간", "date"),
        ("rate", "금리", "percent"),
        ("no", "코드1)", "number"),
        ("item34", "고정", "text"),
        ("count", "현지판매", "count"),
        ("item35", "대 한국 수출", "text"),
        ("item36", "제3국 수출", "text"),
        ("amount4", "금액", "amount"),
        ("item37", "비중", "text"),
        ("item38", "대 한국 수입", "text"),
        ("item39", "제3국 수입", "text"),
        ("item40", "자 산", "text"),
        ("item41", "부채와 자본", "text"),
        ("item42", "부채총계", "text"),
        ("item43", "자본총계", "text"),
        ("item44", "자산총계", "text"),
        ("item45", "부채 및 자본 총계", "text"),
        ("item46", "현지법인 운영상 애로사항", "choice", ["생산관련요인(노동생산성/부품·원자재조달)", "마케팅관련요인(홍보/판매)", "재무관련요인(현지금융조달/과실송금등)", "사회간접자본관련요인(도로/항만/전력/용수등)", "기타", "노동관련분야"]),
        ("item47", "대 정부 건의사항", "text"),
        ("item48", "현지업체와의 경쟁관계", "text"),
        ("item49", "향후 영업전망", "text"),
        ("item50", "국가명", "text")
     ])])

FORM("hf207", "연간사업실적보고서(투자잔액 300만불 초과 1,000만불 이하 기업)", "fx", code="5-09-0023",
     title_note="하나은행 공개 서식 No.207 (외환)",
     sections=[("한국투자자(모기업) 개요", [
        ("item", "투자자명 담 당 자", "text"),
        ("item2", "계열명", "text"),
        ("item3", "소속부서: 직성명: 전화:", "text"),
        ("item4", "업종(중분류)1)", "text"),
        ("item5", "사후관리은행", "text"),
        ("item6", "투자자 법인성격", "choice", ["실제영업법인", "특수목적회사(SPC)"]),
        ("item7", "외국인투자기업2) 여부", "choice", ["아니오"]),
        ("item8", "법인명1)", "text"),
        ("company.ceo", "대표자", "text"),
        ("item9", "소재지(국가주성)2) , ,", "text"),
        ("item10", "투자업종3)", "text"),
        ("item11", "주요취급품목4)", "text"),
        ("item12", "인원현황", "text"),
        ("date", "설립등기일", "date"),
        ("date2", "영업개시일", "date"),
        ("item13", "주주구성", "text"),
        ("amount", "합계", "amount"),
        ("item14", "법인성격", "text"),
        ("item15", "설립 형태", "choice", ["신설법인설립", "기존법인지분인수-지분인수비율"]),
        ("item16", "투자형태7)", "text"),
        ("item17", "지배구조", "text"),
        ("item18", "천미불", "text"),
        ("item19", "천미불(A×B)", "text"),
        ("item20", "천미불 (전기말: 천미불)", "text"),
        ("amount2", "금액(천미불)", "amount"),
        ("item21", "금기말", "text"),
        ("item22", "지분투자", "text"),
        ("item23", "대부투자 (대여금 및 채권인수)", "text"),
        ("item24", "배 당 금", "text"),
        ("item25", "한국투자자앞 지급액", "text"),
        ("item26", "차입처", "text"),
        ("item27", "보증자", "text"),
        ("date3", "차입기간", "date"),
        ("rate", "금리", "percent"),
        ("no", "코드1)", "number"),
        ("item28", "고정", "text"),
        ("count", "현지판매", "count"),
        ("item29", "대 한국 수출", "text"),
        ("item30", "제3국 수출", "text"),
        ("amount3", "금액", "amount"),
        ("item31", "비중", "text"),
        ("item32", "대 한국 수입", "text"),
        ("item33", "제3국 수입", "text"),
        ("item34", "자 산", "text"),
        ("item35", "부채와 자본", "text"),
        ("item36", "부채총계", "text"),
        ("item37", "자본총계", "text"),
        ("item38", "자산총계", "text"),
        ("item39", "부채 및 자본 총계", "text"),
        ("item40", "현지법인 운영상 애로사항", "choice", ["생산관련요인(노동생산성/부품·원자재조달)", "마케팅관련요인(홍보/판매)", "재무관련요인(현지금융조달/과실송금등)", "사회간접자본관련요인(도로/항만/전력/용수등)", "기타", "노동관련분야"]),
        ("item41", "대 정부 건의사항", "text"),
        ("item42", "현지업체와의 경쟁관계", "text"),
        ("item43", "향후 영업전망", "text"),
        ("item44", "국가명", "text")
     ])])

FORM("hf208", "지급확인서", "fx", code="5-09-0365",
     title_note="하나은행 공개 서식 No.208 (외환)",
     sections=[("납세증명서(관할 세무서장 발행)", [
        ("amount", "지 급 금 액", "amount"),
        ("foreign.name", "수 취 인", "text"),
        ("item", "수취인과의 관계", "text"),
        ("item2", "※ 송금사유와 목적을 구체적으로 기재하실 것", "text")
     ])])

FORM("hf209", "영수확인서", "fx", code="외환-0209",
     title_note="하나은행 공개 서식 No.209 (외환)",
     sections=[("기재사항", [
        ("amount", "영수금액", "amount"),
        ("amount2", "(USD상당금액 : )", "amount"),
        ("item", "송금인", "text"),
        ("item2", "송금인과관계", "text"),
        ("item3", "구분", "text"),
        ("item4", "증여", "text"),
        ("item5", "* 영수사유를 구체적으로 기재하실 것", "text")
     ])])

FORM("hf210", "대북투자 신고 및 투자실적 보고서", "fx", code="외환-0210",
     title_note="하나은행 공개 서식 No.210 (외환)",
     sections=[("대북투자사업 신고업체 투자현황 (단위 : 천미불)", [
        ("amount", "신고 금액", "amount"),
        ("amount2", "합계", "amount"),
        ("item", "투자내역", "text"),
        ("item2", "이익잉여금등 기타", "text"),
        ("item3", "변경내용", "text")
     ])])

FORM("hf211", "사업계획서", "fx", code="5-09-0191",
     title_note="하나은행 공개 서식 No.211 (외환)",
     sections=[("투자자 현황", [
        ("company.name", "상호 또는 성명", "text"),
        ("date", "설 립 년 월 일", "date"),
        ("customer.address", "소 재 지(주 소)", "text"),
        ("item", "투 자 자 규 모", "choice", ["대기업", "중소기업", "개인사업자", "개인", "기타(비영리단체등)"]),
        ("item2", "투자자 법인성격", "choice", ["실제영업법인", "특수목적회사(SPC)1)"]),
        ("item3", "외국인투자기업2) 여부", "choice", ["아니오"]),
        ("amount", "백만원", "amount"),
        ("item4", "업 종 (제 품)", "text"),
        ("item5", "담당자 및 연락처", "text"),
        ("company.name", "법 인 명", "text"),
        ("company.ceo", "대 표 자", "text"),
        ("item6", "법인형태", "choice", ["법인", "개인기업", "기타", "해외자원개발사업(", "법인설립", "법인미설립)"]),
        ("date2", "설립(예정)일", "choice", ["자본금미납입"]),
        ("item7", "총자본금", "text"),
        ("item8", "투자형태1)", "choice", ["단독투자", "공동투자", "합작투자(지분율"]),
        ("item9", "투자유형2)", "choice", ["M&A", "그린필드", "기존사업규모확장", "기업및금융구조조정"]),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자번호", "number"),
        ("company.ceo", "대표자명", "text"),
        ("company.corp_no", "법인등록번호", "number"),
        ("item10", "법인성격", "choice", ["실제영업법인", "특수목적회사(SPC)-최종투자목적국"]),
        ("item11", "설립형태", "choice", ["신설법인설립", "기존법인지분인수-지분인수비율"]),
        ("item12", "지배구조", "choice", ["비지주회사", "지주회사"]),
        ("item13", "투자목적 (택 일)", "choice", ["자원개발", "수출촉진", "보호무역타개", "저임활용", "선진기술도입", "현지시장진출"]),
        ("item14", "액면", "text"),
        ("amount2", "취득가액", "amount"),
        ("item15", "① 현금", "text"),
        ("item16", "② 현물", "text"),
        ("item17", "③ 주식", "text"),
        ("item18", "④ 이익잉여금", "text"),
        ("item19", "⑤ 기술투자", "text"),
        ("item20", "⑥ 기타( )", "text"),
        ("item21", "(①+②+③+④+⑤+⑥)", "text"),
        ("item22", "출자자명", "text"),
        ("item23", "출 자 전", "text"),
        ("item24", "금회출자", "text"),
        ("item25", "출 자 후", "text"),
        ("item26", "한국측(①)", "text"),
        ("item27", "현지측(②)", "text"),
        ("item28", "제3국(③)", "text"),
        ("amount3", "합 계(①+②+③)", "amount"),
        ("item29", "대 부 액", "text"),
        ("item30", "자금용도", "text"),
        ("rate", "이 율", "percent"),
        ("date3", "기 간", "date"),
        ("amount4", "원금상환방법", "amount"),
        ("amount5", "이자징수방법", "amount"),
        ("item31", "자기자금", "text"),
        ("item32", "차 입 금", "text")
     ])])

FORM("hf212", "해외직접투자 신고서(보고서)", "fx", code="5-09-0290",
     title_note="하나은행 공개 서식 No.212 (외환)",
     sections=[("합작인 경우 당해 사업에 관한 계약서", [
        ("item", "해 외 직 접 투 자 신 고 서(보고서)", "text"),
        ("company.name", "상 호", "text"),
        ("company.biz_no", "사 업 자 등 록 번 호", "number"),
        ("company.corp_no", "법 인 등 록 번 호", "number"),
        ("customer.rrn", "주 민 등 록 번 호", "number"),
        ("no", "전화번호：", "number"),
        ("company.biz_item", "업 종", "text"),
        ("item2", "투 자 국 명", "text"),
        ("company.address", "소 재 지", "text"),
        ("item3", "투 자 방 법", "text"),
        ("item4", "자 금 조 달", "text"),
        ("item5", "투 자 업 종", "text"),
        ("item6", "주 요 제 품", "text"),
        ("amount", "투 자 금 액", "amount"),
        ("amount2", "출 자 금 액", "amount"),
        ("rate", "투 자 비 율", "percent"),
        ("item7", "결 산 월", "text"),
        ("item8", "투 자 목 적", "text"),
        ("item9", "투 자 유 형", "text"),
        ("item10", "(자본금： )", "text"),
        ("no2", "신 고 번 호", "number"),
        ("amount3", "신 고 금 액", "amount"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf213", "사전 송금방식 수입대금 지급시", "fx", code="5-09-0519",
     title_note="하나은행 공개 서식 No.213 (외환)",
     sections=[("대금결제방식 및 대응수입예정일", [
        ("date", "대금 송금 후 물품 (선적서류)수령 예정일", "choice", ["1년이내"]),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf214", "자본거래 사후보고 확인서", "fx", code="5-09-0528",
     title_note="하나은행 공개 서식 No.214 (외환)",
     sections=[("신청인 정보", [
        ("customer.name", "신청인", "text"),
        ("no", "주민(사업자)번호", "number"),
        ("customer.phone", "연락처", "text"),
        ("customer.email", "이메일 주소", "text"),
        ("customer.address", "주소", "text")
     ])])

FORM("hf215", "상호계산계정 결산대차기잔액처분(변경)신고서", "fx", code="외환-0215",
     title_note="하나은행 공개 서식 No.215 (외환)",
     sections=[("기재사항", [
        ("amount", "금 액", "amount"),
        ("item", "송 금 처", "text"),
        ("item2", "송 금 방 법", "text"),
        ("item3", "송 금 은 행", "text"),
        ("no", "신고번호", "number"),
        ("date", "유효기간", "date")
     ])])

FORM("hf216", "해외부동산 취득신고(수리)서", "fx", code="5-09-0292",
     title_note="하나은행 공개 서식 No.216 (외환)",
     sections=[("내신고가 가능한 경우", [
        ("no", "주민(사업자)등록번호", "number"),
        ("no2", "(주소) (전화번호) (e-mail)", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("item", "(성명) (주소)", "text"),
        ("item2", "부 동 산 의 종 류", "choice", ["주택", "토지", "상가", "기타()"]),
        ("item3", "취 득 목 적", "choice", ["주거", "주거이외(투자등)", "임차(임차기간"]),
        ("company.address", "소 재 지", "text"),
        ("property.area", "면 적", "text"),
        ("amount", "취 득 가 액", "amount"),
        ("currency", "현지통화", "currency"),
        ("amount2", "총취득금액(A = B + C )", "amount"),
        ("amount3", "취득자금 국내송금액", "amount"),
        ("amount4", "모기지론(원리금상환송금예정금액)", "amount"),
        ("amount5", "모기지론(원리금상환현지조달금액)", "amount"),
        ("item4", "기 타 : ( )", "text"),
        ("foreign.name", "수 취 인 명", "text"),
        ("item5", "신고인과의 관계", "text"),
        ("no3", "신 고 ( 수 리 ) 번 호", "number"),
        ("amount6", "신 고 ( 수 리 ) 금 액", "amount"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf217", "해외직접투자 내용변경 신고(보고)서", "fx", code="5-09-0289",
     title_note="하나은행 공개 서식 No.217 (외환)",
     sections=[("변 경 사 항", [
        ("item", "2. 변 경 사 유 (요 약)", "text"),
        ("no", "신 고 번 호", "number"),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf218", "서약서(개인의 외국주택 취득)", "fx", code="5-09-0272",
     title_note="하나은행 공개 서식 No.218 (외환)",
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

FORM("hf219", "해외사무소 설치(변경)신고서", "fx", code="5-09-0271",
     title_note="하나은행 공개 서식 No.219 (외환)",
     sections=[("기재사항", [
        ("item", "해외사무소 설치(변경) 신고서", "text"),
        ("company.name", "상 호", "text"),
        ("company.ceo", "대 표 자", "text"),
        ("no", "사업자(주민)번호", "number"),
        ("company.corp_no", "법인등록번호", "number"),
        ("item2", "주소( 소재지)", "text"),
        ("no2", "(주소) (전화번호) (e-mail)", "number"),
        ("company.biz_item", "업 종", "text"),
        ("item3", "담 당 자", "text"),
        ("item4", "기 업 규 모", "text"),
        ("item5", "구 분", "text"),
        ("item6", "사 무 소 명", "text"),
        ("item7", "(국문) (영문)", "text"),
        ("company.address", "소 재 지", "text"),
        ("item8", "(국가명) (세부주소)", "text"),
        ("no3", "업 종 코 드", "number"),
        ("no4", "(표준산업분류코드 5자리)", "number"),
        ("item9", "주 재 원 수", "text"),
        ("item10", "본국파견 : 명, 현지채용 : 명", "text"),
        ("item11", "설 치 사 유", "text"),
        ("item12", "사 유", "text"),
        ("no5", "신 고 번 호", "number"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf220", "해외지점 설치(변경)신고서", "fx", code="5-09-0270",
     title_note="하나은행 공개 서식 No.220 (외환)",
     sections=[("기재사항", [
        ("item", "해외지점 설치(변경) 신고서", "text"),
        ("company.name", "상 호", "text"),
        ("company.ceo", "대 표 자", "text"),
        ("no", "사업자(주민)번호", "number"),
        ("company.corp_no", "법인등록번호", "number"),
        ("item2", "주소( 소재지)", "text"),
        ("no2", "(주소) (전화번호) (e-mail)", "number"),
        ("company.biz_item", "업 종", "text"),
        ("item3", "담 당 자", "text"),
        ("item4", "기 업 규 모", "text"),
        ("item5", "구 분", "text"),
        ("branch", "지 점 명", "text"),
        ("item6", "(국문) (영문)", "text"),
        ("company.address", "소 재 지", "text"),
        ("item7", "(국가명) (세부주소)", "text"),
        ("no3", "업 종 코 드", "number"),
        ("no4", "(표준산업분류코드 5자리)", "number"),
        ("item8", "주 재 원 수", "text"),
        ("item9", "본국파견 : 명, 현지채용 : 명", "text"),
        ("item10", "설 치 사 유", "text"),
        ("item11", "사 유", "text"),
        ("no5", "신 고 번 호", "number"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf221", "해외지사 설치·현황 보고서", "fx", code="5-09-0213",
     title_note="하나은행 공개 서식 No.221 (외환)",
     sections=[("해외지사 신고명세", [
        ("item", "변경내용", "text"),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf222", "해외 부동산 취득 보고서", "fx", code="5-09-0211",
     title_note="하나은행 공개 서식 No.222 (외환)",
     sections=[("부동산 취득 명의인 :", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf223", "「외국환서식관리프로그램」전자무역업무이용(신규,변경,해지)신청서", "fx", code="5-09-0054",
     title_note="하나은행 공개 서식 No.223 (외환)",
     sections=[("전자무역 기반사업자 가입승인서 사본 1 부", [
        ("item", "담 당", "text"),
        ("customer.name", "신 청 인", "text"),
        ("item2", "수발신인식별자", "text"),
        ("item3", "상세수발신식별자", "text"),
        ("item4", "전자문서인증키", "text"),
        ("item5", "하나은행", "text"),
        ("item6", "NET12", "text"),
        ("item7", "EDI", "choice", ["KTNet"]),
        ("item8", "계산서 발신업무", "choice", ["수출환어음매입", "신용장개설", "내국신용장개설", "수출입금통지", "타발송금입금통지", "계좌입금통지"]),
        ("item9", "e-Nego", "choice", ["uTradeHub"]),
        ("item10", "기반사업자: □ uTradeHub", "text"),
        ("item11", "자동승인", "choice", ["구매확인서승인", "내국신용장개설승인"]),
        ("item12", "예금과목", "text"),
        ("account", "계 좌 번 호", "number"),
        ("customer.name", "예 금 주", "text"),
        ("currency", "통화", "currency"),
        ("amount", "수수료결제계좌번호", "amount"),
        ("item13", "변 경 항 목", "text"),
        ("item14", "변 경 전", "text"),
        ("item15", "변 경 후", "text"),
        ("item16", "인감대조", "text"),
        ("item17", "지정사업자:", "text"),
        ("item18", "계산서 발급업무", "text"),
        ("item19", "e-L/C", "text"),
        ("item20", "지급지시 업무", "text"),
        ("item21", "상세수발신인식별자", "text"),
        ("item22", "약정항목: e-L/C 통지업무", "text")
     ])])

FORM("hf224", "Usance 송금 조건변경신청서", "fx", code="외환-0224",
     title_note="하나은행 공개 서식 No.224 (외환)",
     sections=[("기재사항", [
        ("item", "♣ 신청인 정보", "text"),
        ("customer.name", "성 명", "text"),
        ("no", "사업자번호 (I.D No.)", "number"),
        ("customer.address", "주소", "text"),
        ("no2", "Usance송금 번호", "number"),
        ("amount", "송금액", "amount"),
        ("foreign.name", "수취인명", "text"),
        ("no3", "수취인 주소 및 전화번호", "number"),
        ("no4", "수취인 계좌번호", "number"),
        ("item2", "수취은행 BIC", "text"),
        ("item3", "수취은행명", "text"),
        ("date", "만기(상환일)", "date")
     ])])

FORM("hf225", "Usance 송금 신청서", "fx", code="외환-0225",
     title_note="하나은행 공개 서식 No.225 (외환)",
     sections=[("기재사항", [
        ("item", "♣ 신청인 정보", "text"),
        ("item2", "성 명 (Applicant)", "text"),
        ("item3", "영문(English) :", "text"),
        ("item4", "한글(Korean) :", "text"),
        ("no", "사업자번호 (I.D No.)", "number"),
        ("no2", "송금인계좌번호(A/C)", "number"),
        ("item5", "주 소 (Address)", "text"),
        ("item6", "TEL No :", "text"),
        ("item7", "♣ 신청 정보", "text"),
        ("amount", "신청금액", "amount"),
        ("item8", "거래 방식 (선적 구분)", "choice", ["사전송금방식(선적전)", "사후송금방식(선적후)"]),
        ("item9", "수입 형태 *사전송금 방식만작성", "text"),
        ("date", "송금 희망일", "date"),
        ("item10", "인수은행", "text"),
        ("item11", "인수은행명 SWIFT Code :", "text"),
        ("date2", "만기(상환일)", "date"),
        ("item12", "♣ 선적 정보", "text"),
        ("no3", "계약서 번호", "number"),
        ("item13", "상품명세", "text"),
        ("item14", "가격조건", "text"),
        ("no4", "HS코드", "number"),
        ("item15", "원산지", "text"),
        ("item16", "수출국", "text"),
        ("item17", "(예정)선적항 (또는 공항)", "text"),
        ("item18", "선적국가", "text"),
        ("item19", "(예정)도착항 (또는 공항)", "text"),
        ("item20", "도착국가", "text"),
        ("item21", "♣ 송금 수취인 및 수취은행 정보", "text"),
        ("foreign.name", "수취인명", "text"),
        ("no5", "수취인 주소 및 전화번호", "number"),
        ("no6", "수취인 계좌번호", "number"),
        ("amount2", "송금수수료 부담자", "choice", ["SHA", "OUR"]),
        ("item22", "수취은행 BIC", "text"),
        ("item23", "수취은행명", "text"),
        ("item24", "담당자명", "text"),
        ("customer.phone", "전화번호", "number")
     ])])

FORM("hf226", "거주자의 외화자금 차입 및 상환 현황보고서", "fx", code="외환-0226",
     title_note="하나은행 공개 서식 No.226 (외환)",
     sections=[("기재사항", [
        ("item", "[차주정보]", "text"),
        ("item2", "[대주정보]", "text"),
        ("item3", "[차입내용]", "text"),
        ("fx_amount", "[해외외화 보유내역]", "fx_amount"),
        ("item4", "[차입조건]", "text"),
        ("item5", "[지급보증]", "text")
     ])])

FORM("hf227", "거주자의 해외 증권발행 및 상환 현황 보고서", "fx", code="외환-0227",
     title_note="하나은행 공개 서식 No.227 (외환)",
     sections=[("기재사항", [
        ("item", "[차주정보]", "text"),
        ("item2", "[대주정보]", "text"),
        ("item3", "[발행내용]", "text"),
        ("item4", "[발행비용]", "text"),
        ("fx_amount", "[해외외화 보유내역]", "fx_amount"),
        ("item5", "[발행조건]", "text"),
        ("item6", "[지급보증]", "text")
     ])])

FORM("hf228", "담보제공신고(보고)서", "fx", code="5-09-0274",
     title_note="하나은행 공개 서식 No.228 (외환)",
     sections=[("담보물 입증서류", [
        ("item", "담보제공 신고(보고)서", "text"),
        ("no", "(전화번호 : )", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("item2", "담 보 제 공 자", "text"),
        ("item3", "담 보 취 득 자", "text"),
        ("item4", "담 보 제 공 수 혜 자", "text"),
        ("property.kind", "담 보 물 종 류", "choice", ["예금", "부동산", "동산", "증권", "기타()"]),
        ("item5", "담 보 소 재 지", "text"),
        ("count", "수 량", "count"),
        ("amount", "담 보 가 액", "amount"),
        ("date", "담 보 제 공 기 간", "date"),
        ("item6", "담 보 제 공 용 도", "choice", ["해외교포등에대한여신과관련한원리금상환담보제공", "증권회사현지법인의현지차입에대한담보제공", "기타()"]),
        ("no2", "신 고 번 호", "number"),
        ("amount2", "신 고 금 액", "amount"),
        ("date2", "유 효 기 간", "date")
     ])])

FORM("hf229", "매매신고(보고)서", "fx", code="5-09-0276",
     title_note="하나은행 공개 서식 No.229 (외환)",
     sections=[("매매대상물 취득 증빙서류", [
        ("item", "( )매매신고(보고)서", "text"),
        ("no", "(전화번호)", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("no2", "(성명) (전화번호) (주소)", "number"),
        ("item2", "매 매 대 상 물 종 류", "text"),
        ("item3", "(미불화 상당액)", "text"),
        ("fx_rate", "(원 화 환 율)", "rate"),
        ("item4", "매 매 사 유", "text"),
        ("no3", "신 고 번 호", "number"),
        ("amount", "신 고 금 액", "amount"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf230", "보증계약신고(보고)서", "fx", code="5-09-0277",
     title_note="하나은행 공개 서식 No.230 (외환)",
     sections=[("보증계약서", [
        ("item", "보증계약신고(보고)서", "text"),
        ("no", "(전화번호 : )", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("item2", "보 증 채 권 자", "text"),
        ("item3", "보 증 채 무 자", "text"),
        ("item4", "보 증 수 혜 자", "text"),
        ("amount", "보 증 금 액", "amount"),
        ("date", "보 증 기 간", "date"),
        ("item5", "보 증 용 도", "choice", ["해외교포등에대한여신과관련한원리금상환보증", "거주자및거주자의현지법인등의현지금융에대한보증", "증권회사현지법인의현지차입에대한보증", "거주자의현지법인의해외리스에대한국내본사등의보증", "주채무계열소속30대계열기업체의장기차입에대한보증", "기타()"]),
        ("item6", "상 환 방 법", "text"),
        ("no2", "신 고 번 호", "number"),
        ("amount2", "신 고 금 액", "amount"),
        ("date2", "유 효 기 간", "date")
     ])])

FORM("hf231", "현지금융 차입·상환·보증등 한도 운영현황 보고서", "fx", code="외환-0231",
     title_note="하나은행 공개 서식 No.231 (외환)",
     sections=[("기재사항", [
        ("item", "대 주3) 대주지역", "text"),
        ("fx_amount", "차입구분4) 외화증권5)", "fx_amount"),
        ("item2", "대주지역", "text"),
        ("fx_amount2", "외화증권5)", "fx_amount"),
        ("amount", "계", "amount")
     ])])

FORM("hf232", "증권발행 신고(보고)서", "fx", code="5-09-0286",
     title_note="하나은행 공개 서식 No.232 (외환)",
     sections=[("기재사항", [
        ("item", "증권발행 신고(보고)서", "text"),
        ("no", "(전화번호)", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("item2", "상 호 기 타 명 칭", "text"),
        ("item3", "증 권 종 류", "text"),
        ("amount", "액면 금액 및 수량", "amount"),
        ("amount2", "발 행 금 액", "amount"),
        ("item4", "(공모, 사모)", "text"),
        ("item5", "계약 체결 시기 및 장소", "text"),
        ("item6", "발행 시기 및 장소", "text"),
        ("item7", "(상장시 : 증권거래소)", "text"),
        ("rate", "표 면 금 리", "percent"),
        ("item8", "발 행 가 격", "text"),
        ("date", "만 기", "date"),
        ("item9", "해 외 판 매 여 부", "text"),
        ("item10", "배당금지급시기 및 방 법", "text"),
        ("item11", "원리금상환방법", "text"),
        ("item12", "(All-in Cost : )", "text"),
        ("item13", "자 금 용 도", "text"),
        ("item14", "발 행 관 련 기 관", "text"),
        ("no2", "신 고 번 호", "number"),
        ("amount3", "신 고 금 액", "amount"),
        ("date2", "유 효 기 간", "date")
     ])])

FORM("hf233", "금전의 대차계약 신고(보고)서", "fx", code="5-09-0273",
     title_note="하나은행 공개 서식 No.233 (외환)",
     sections=[("기재사항", [
        ("item", "금전의 대차계약 신고(보고)서", "text"),
        ("no", "(전화번호 : )", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("item2", "차 주", "text"),
        ("item3", "대 주", "text"),
        ("amount", "통 화 및 금 액", "amount"),
        ("date", "차 입 일 / 대 출 일", "date"),
        ("item4", "(All-in Cost : )", "text"),
        ("date2", "대 차 기 간", "date"),
        ("item5", "사 용 용 도", "text"),
        ("item6", "상 환 방 법", "text"),
        ("no2", "신 고 번 호", "number"),
        ("amount2", "신 고 금 액", "amount"),
        ("date3", "유 효 기 간", "date")
     ])])

FORM("hf234", "외화송금의 내용변경 및 취소, 송금수표 분실신고 등 신청서", "fx", code="5-09-0064",
     title_note="하나은행 공개 서식 No.234 (외환)",
     sections=[("기재사항", [
        ("item", "송금방법", "choice", ["전신송금(T/T)", "송금수표(D/D)"]),
        ("date", "송금일자", "date"),
        ("no", "송금번호(수표번호)", "number"),
        ("foreign.name", "수취인", "text"),
        ("item2", "전신송금", "text"),
        ("item3", "송금수표", "text"),
        ("item4", "[전신송금 내용변경 기재란]", "text"),
        ("item5", "항목", "text"),
        ("bank", "거래은행", "text"),
        ("account", "계좌번호", "number"),
        ("customer.name", "성명", "text"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "전화번호", "number"),
        ("item6", "기타(사유 등)", "text"),
        ("date2", "생년월일 / 사업자번호", "date"),
        ("item7", "E-mail 주소", "text")
     ])])

FORM("hf235", "외국인투자기업등록(변경등록)신청서(국문)", "fx", code="5-09-0437",
     title_note="하나은행 공개 서식 No.235 (외환)",
     sections=[("출자목적물의 납입을 가장하여 외국인투자기업의 등록을", [
        ("item", "① 상호 또는 명칭(영문)", "text"),
        ("item2", "② 국적", "text"),
        ("item3", "[ ] 예 [ ] 아니오", "text"),
        ("item4", "SPC의 최종 지배모기업", "text"),
        ("item5", "상호 (국적: )", "text"),
        ("item6", "(국문)", "text"),
        ("no", "④ 사업자등록번호(본사)", "number"),
        ("item7", "(영문)", "text"),
        ("item8", "(*) SPC 여부 [ ] 예 [ ] 아니오", "text"),
        ("no2", "본사 (전화번호: ,FAX:", "number"),
        ("item9", "홈페이지", "text"),
        ("item10", "대표 E-mail", "text"),
        ("item11", "⑥ 신고(허가)된 사업명", "text"),
        ("item12", "⑦ 자본금(출연금)", "text"),
        ("amount", "취득총액: 원(*USD 상당)", "amount"),
        ("amount2", "액면총액:", "amount"),
        ("item13", "기존(변경등록) 명", "text"),
        ("item14", "등록 후 예상규모(신규 및 변경등록) 명", "text"),
        ("item15", "※ 변경내용", "text"),
        ("item16", "상호 또는 명칭(영문)", "text"),
        ("customer.nationality", "국적", "text"),
        ("item17", "종류", "text"),
        ("amount3", "1주(좌)당 액면가액(B)", "amount"),
        ("amount4", "1주(좌)당 양도 또는 감소가액(C)", "amount"),
        ("count", "수량(A)", "count"),
        ("amount5", "액면총액(A×B)", "amount"),
        ("amount6", "양도 또는 감소 총액(A×C)", "amount")
     ])])

FORM("hf236", "해외예금 및 신탁 잔액 보고서", "fx", code="5-09-0212",
     title_note="하나은행 공개 서식 No.236 (외환)",
     sections=[("기재사항", [
        ("item", "개설인명", "text"),
        ("customer.address", "주 소", "text"),
        ("no", "사업자(주민) 등록번호", "number"),
        ("item2", "직위 ‧ 성명", "text"),
        ("customer.phone", "전화번호", "number"),
        ("item3", "은행 부(점)", "text"),
        ("amount", "연중 입금액(B)", "amount"),
        ("amount2", "연중 출금액 (C)", "amount"),
        ("amount3", "금 액", "amount"),
        ("item4", "국내송금", "text"),
        ("item5", "국내회수", "text"),
        ("amount4", "수출대금", "amount"),
        ("amount5", "수입대금 지 급", "amount"),
        ("fx_amount", "외화증권 처 분", "fx_amount"),
        ("fx_amount2", "외화증권 취 득", "fx_amount"),
        ("item6", "예금 ‧ 신탁 처 분", "text"),
        ("item7", "예금 ‧ 신탁 예 치", "text")
     ])])

FORM("hf237", "해외예금 입금보고서", "fx", code="5-09-0363",
     title_note="하나은행 공개 서식 No.237 (외환)",
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

FORM("hf238", "해외직접투자사업 청산 및 대부채권 회수보고서", "fx", code="5-09-0215",
     title_note="하나은행 공개 서식 No.238 (외환)",
     sections=[("투자자 현황", [
        ("company.name", "상 호 또는 성 명", "text"),
        ("no", "사업자(주민)등록번호", "number"),
        ("customer.address", "소 재 지(주 소)", "text"),
        ("item", "현 지 법 인 명", "text"),
        ("item2", "법 인 형 태", "choice", ["법인", "개인기업", "기타", "해외자원개발사업"]),
        ("item3", "납 입 자 본 금", "text"),
        ("item4", "투 자 형 태주1)", "choice", ["단독투자", "공동투자", "합작투자(한국측투자비율"]),
        ("amount", "대부금액", "amount"),
        ("amount2", "기 회수금액", "amount"),
        ("amount3", "금회 회수금액", "amount"),
        ("amount4", "잔액", "amount"),
        ("amount5", "계", "amount")
     ])])

FORM("hf239", "해외 부동산 처분(변경)신고서", "fx", code="5-09-0210",
     title_note="하나은행 공개 서식 No.239 (외환)",
     sections=[("처분(변경)전 부동산 명의인 :", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf240", "외화증권(채권)취득보고서(법인 및 개인기업 설립보고서 포함)", "fx", code="5-09-0206",
     title_note="하나은행 공개 서식 No.240 (외환)",
     sections=[("투자자현황 (담당자명 : 전화번호 : )", [
        ("company.name", "상호 또는 성명", "text"),
        ("date", "설 립 년 월 일", "date"),
        ("customer.address", "소 재 지(주 소)", "text"),
        ("item", "투 자 자 규 모", "choice", ["대기업", "중소기업", "개인사업자", "개인"]),
        ("date", "신 고 일 자", "date"),
        ("no", "신 고 번 호", "number"),
        ("company.name", "법 인 명", "text"),
        ("item2", "법 인 형 태", "choice", ["법인", "개인기업", "기타", "해외자원개발사업"]),
        ("item3", "납 입 자 본 금", "text"),
        ("item4", "투 자 형 태주1)", "choice", ["단독투자", "공동투자", "합작투자(한국측투자비율"]),
        ("date2", "설 립 등 기 일", "date"),
        ("date3", "영업개시(예정)일", "date"),
        ("date4", "결 산 일", "date"),
        ("item5", "증권취득일 (자본금출자일)", "text"),
        ("item6", "증 권 종 류", "text"),
        ("amount", "액 면 가 액 합 계", "amount"),
        ("amount2", "취 득 가 액 합 계", "amount"),
        ("item7", "증 권 발 행 여 부", "choice", ["증권발행", "증권미발행"]),
        ("date5", "채 권 취 득 일", "date"),
        ("amount3", "대 부 원 금", "amount"),
        ("amount4", "이 자 율", "amount"),
        ("date6", "대 부 기 간", "date"),
        ("amount5", "원 금 회 수 방 법", "choice", ["만기일시회수", "분할회수(회)", "기타"])
     ])])

FORM("hf241", "대외지급보증 조건변경 신청서(SWIFT 방식)(2D)", "fx", code="5-09-0505",
     title_note="하나은행 공개 서식 No.241 (외환)",
     sections=[("보증서번호 :", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf242", "대외지급보증 발급 신청서(SWIFT 방식)(2D)", "fx", code="외환-0242",
     title_note="하나은행 공개 서식 No.242 (외환)",
     sections=[("Expiry Date(년/월/일) :", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf243", "외국환거래 UMS통지서비스 (변경)신청서", "fx", code="외환-0243",
     title_note="하나은행 공개 서식 No.243 (외환)",
     sections=[("기재사항", [
        ("customer.name", "고객명", "text"),
        ("date", "사업자등록번호 (생년월일)", "date"),
        ("no", "SMS 수신 전화번호", "number"),
        ("customer.address", "주 소", "text"),
        ("no2", "FAX 번호", "number"),
        ("item", "E-MAIL 주소", "text"),
        ("item2", "업 무", "text"),
        ("item3", "통지방법 (택일)", "text"),
        ("item4", "당발송금", "text"),
        ("item5", "타발송금 내도통지", "text"),
        ("item6", "타발송금 입금통지", "text"),
        ("fx_amount", "외화수표 추심", "fx_amount"),
        ("item7", "로칼 서류 접수", "text"),
        ("item8", "수입 선적서류접수 (□ 건별 / □ 고객별)", "text"),
        ("no3", "수출네고 특사번호 통지", "number"),
        ("item9", "수출입금통지 (매입/추심 포함)", "text"),
        ("item10", "수출인수통지 (매입/추심 포함)", "text")
     ])])

FORM("hf244", "자본재 등 도입물품명세 검토ㆍ확인신청서", "fx", code="외환-0244",
     title_note="하나은행 공개 서식 No.244 (외환)",
     sections=[("기재사항", [
        ("item", "③ 신고된 사업명", "text"),
        ("date", "④ 외국인투자 신고일 년 월 일", "date"),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf245", "장기차관 방식의 외국인투자신고서, 변경신고서(영문)", "fx", code="5-09-0483",
     title_note="하나은행 공개 서식 No.245 (외환)",
     sections=[("A copy of the loan contract", [
        ("customer.name", "Name", "text"),
        ("customer.address", "Address", "text"),
        ("item", "Amount of the Loan", "text"),
        ("fx_amount", "won (USD )", "fx_amount"),
        ("item2", "Average Loan Period", "text"),
        ("item3", "Rate of Interest", "text"),
        ("item4", "Other", "text"),
        ("item5", "Cash", "text"),
        ("item6", "Capital in kind", "text"),
        ("item7", "Purpose of Loan", "text"),
        ("item8", "Location of Investment", "text")
     ])])

FORM("hf246", "장기차관 방식의 외국인투자신고서, 변경신고서(국문)", "fx", code="5-09-0486",
     title_note="하나은행 공개 서식 No.246 (외환)",
     sections=[("차관계약서 사본 1부", [
        ("item", "상호 또는 명칭", "text"),
        ("no", "주소 (전화번호 : )", "number"),
        ("item2", "상호 또는 명칭(영문)", "text"),
        ("item3", "주소(영문)", "text"),
        ("amount", "차관금액", "amount"),
        ("fx_amount", "원 (USD 상당)", "fx_amount"),
        ("date", "[ ] 만기일시상환 [ ] 분할상환", "date"),
        ("date2", "평균차관 기간", "date"),
        ("amount2", "연 이자율", "amount"),
        ("item4", "현금", "text"),
        ("item5", "자본재", "text"),
        ("item6", "차관용도", "text"),
        ("item7", "금번 투자지역", "text")
     ])])

FORM("hf247", "외국인투자기업등록(변경등록)신청서(영문)", "fx", code="5-09-0438",
     title_note="하나은행 공개 서식 No.247 (외환)",
     sections=[("기재사항", [
        ("item", "① Name", "text"),
        ("item2", "② Nationality", "text"),
        ("no", "[ ] Yes [ ] No", "number"),
        ("item3", "UPS of SPC", "text"),
        ("item4", "Name (Nationality: )", "text"),
        ("item5", "(Korean)", "text"),
        ("item6", "(English)", "text"),
        ("no2", "(*) SPC [ ] Yes [ ] No", "number"),
        ("item7", "Homepage(website)", "text"),
        ("customer.email", "E-mail", "text"),
        ("item8", "Par Value of Stocks: won", "text"),
        ("customer.name", "Name", "text"),
        ("customer.nationality", "Nationality", "text"),
        ("item9", "Type", "text"),
        ("item10", "Par Value per Stock(B)", "text"),
        ("item11", "Quantity(A)", "text")
     ])])

FORM("hf248", "주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(영문)", "fx", code="5-09-0433",
     title_note="하나은행 공개 서식 No.248 (외환)",
     sections=[("기재사항", [
        ("customer.name", "Name", "text"),
        ("item", "Name (Phone Number : )", "text"),
        ("customer.nationality", "Nationality", "text")
     ])])

FORM("hf249", "주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(국문)", "fx", code="5-09-0431",
     title_note="하나은행 공개 서식 No.249 (외환)",
     sections=[("기재사항", [
        ("date", "① 신고(허가)일", "date"),
        ("item", "상호 또는 명칭", "text"),
        ("no", "주소 (전화번호: )", "number"),
        ("no2", "상호 또는 명칭 (전화번호: )", "number"),
        ("customer.nationality", "국적", "text"),
        ("amount", "취득총액: 원 (USD 상당)", "amount"),
        ("item2", "⑤ 하려는(하고 있는 사업)", "text"),
        ("item3", "⑦ 변경 후 내용", "text"),
        ("item4", "은 행 하나은행장 장 인", "text")
     ])])

FORM("hf252", "외국환 신고(확인)필증", "fx", code="외환-0252",
     title_note="하나은행 공개 서식 No.252 (외환)",
     sections=[("기재사항", [
        ("item", "반출입구분(Ex or Import)", "text"),
        ("date", "생년월일 Date of Birth", "date"),
        ("item2", "국 적 Nationality", "text"),
        ("no", "주민등록번호 : Passport No. :", "number"),
        ("amount", "합계(미화상당) Sum (US$ equiv)", "amount"),
        ("no2", "비 고(Note) (수표번호 등)", "number"),
        ("item3", "휴 대 (Carried)", "text"),
        ("item4", "송 금 (Remitted)", "text"),
        ("item5", "Official Use Only", "text")
     ])])

FORM("hf253", "( ) 변경신고(수리)서", "fx", code="외환-0253",
     title_note="하나은행 공개 서식 No.253 (외환)",
     sections=[("기 신고(수리)사항 :", [
        ("item", "3. 변경사유(요약)", "text"),
        ("no", "신 고(수 리) 번 호", "number"),
        ("amount", "신 고(수 리) 금 액", "amount"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf254", "금전의 대차계약 신고서", "fx", code="외환-0254",
     title_note="하나은행 공개 서식 No.254 (외환)",
     sections=[("금전대차 계약서", [
        ("item", "금 전 의 대 차 계 약 신 고 서", "text"),
        ("item2", "인", "text"),
        ("no", "(전화번호 : ) (E-mail : )", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("item3", "차 주", "choice", ["기관투자가", "일반법인", "개인", "기타())"]),
        ("item4", "대 주", "choice", ["기관투자가", "일반법인", "개인", "기타())"]),
        ("amount", "통 화 및 금 액", "choice", ["금액()", "외화(1미화1천만달러이하2미화1천만달러초과)", "원화(110억원이하210억원초과)"]),
        ("date", "차 입 / 대 출 일", "date"),
        ("rate", "적 용 금 리", "percent"),
        ("date2", "대 차 기 간", "date"),
        ("item5", "사 용 용 도", "text"),
        ("item6", "상 환 방 법", "text"),
        ("item7", "거 주 자 의 보 증 또 는 담 보 유 무", "choice", ["보증·담보없음", "보증제공", "담보제공"]),
        ("no2", "신 고 번 호", "number"),
        ("amount2", "신 고 금 액", "amount"),
        ("date", "신 고 일 자", "date"),
        ("date3", "유 효 기 간", "date"),
        ("item8", "기타 참고사항", "text")
     ])])

FORM("hf255", "자(손자)회사 사업계획서", "fx", code="외환-0255",
     title_note="하나은행 공개 서식 No.255 (외환)",
     sections=[("현지법인 현황", [
        ("item", "현 지 법 인 명", "text"),
        ("company.ceo", "대 표 자", "text"),
        ("customer.address", "소재지( 주소)", "text"),
        ("item2", "총 자 산", "text"),
        ("company.capital", "자 본 금", "text"),
        ("item3", "업 종 ( 제 품 )", "text"),
        ("date", "설 립 등 기 일", "date"),
        ("item4", "자(손자)회사명", "text"),
        ("date2", "설 립(예정)일", "date"),
        ("item5", "투 자 형 태", "choice", ["단독투자", "합작투자(지분율"]),
        ("item6", "법 인 성 격", "choice", ["실제영업법인", "특수목적회사(SPC)-최종투자목적국"]),
        ("item7", "설 립 형 태", "choice", ["신설법인설립", "기존법인지분인수-지분인수비율"]),
        ("item8", "액 면", "text"),
        ("amount", "취 득 가 액", "amount"),
        ("item9", "① 현 금", "text"),
        ("item10", "② 현 물", "text"),
        ("item11", "③ 주 식", "text"),
        ("item12", "⑤ 이익잉여금", "text"),
        ("item13", "⑤ 기 술 투 자", "text"),
        ("item14", "⑥ 기 타 ( )", "text"),
        ("item15", "출 자 자 명", "text"),
        ("item16", "출 자 전", "text"),
        ("item17", "금 회 출 자", "text"),
        ("item18", "출 자 후", "text"),
        ("item19", "한국측", "text"),
        ("item20", "소 계(①)", "text"),
        ("item21", "현지측(②)", "text"),
        ("item22", "제3국(③)", "text"),
        ("amount2", "합 계(①+②+③)", "amount"),
        ("item23", "자 금 운 용", "text"),
        ("item24", "자 금 조 달", "text"),
        ("item25", "토 지 건 물 기 계 설 비 운 영 자 금", "text"),
        ("item26", "차 입 금 자 본 금", "text")
     ])])

FORM("hf256", "외국환업무 등록 신청서", "fx", code="5-09-0376",
     title_note="하나은행 공개 서식 No.256 (외환)",
     sections=[("최근 대차대조표 및 손익계산서", [
        ("item", "외 국 환 업 무 등 록 신 청 서", "text"),
        ("item2", "① 상 호(본 점)", "text"),
        ("date", "② 설 립 연 월 일", "date"),
        ("date", "년 월 일", "date"),
        ("item3", "③ 대 표 자(본 점)", "text"),
        ("item4", "④ 국 적(대 표 자)", "text"),
        ("item5", "⑤ 본 점 소 재 지주)", "text"),
        ("item6", "⑥ 외 국 환 업 무 의 내 용", "text"),
        ("amount", "백만원", "amount"),
        ("item7", "납 입 자 본", "text"),
        ("item8", "개", "text"),
        ("item9", "국 내 : 개", "text"),
        ("item10", "해 외 : 개", "text"),
        ("item11", "위 험 관 리 전산시스템명", "text"),
        ("item12", "도 입 ( 개 발 ) 시 기", "text"),
        ("item13", "임 원 명", "text"),
        ("item14", "직 원 명", "text"),
        ("item15", "외국환전문요원 명", "text")
     ])])

FORM("hf258", "환전업무 등록신청서", "fx", code="외환-0258",
     title_note="하나은행 공개 서식 No.258 (외환)",
     sections=[("신분증 사본", [
        ("item", "환 전 업 무 등 록 신 청 서", "text"),
        ("item2", "① 상 호", "text"),
        ("date", "② 환전업시작일", "date"),
        ("date2", "( 년 월 일)", "date"),
        ("item3", "④ 주 소", "text"),
        ("item4", "등록구분", "choice", ["일반", "무인환전기기", "온라인"]),
        ("item5", "공동이용 행정정보", "text"),
        ("item6", "동의여부(√)", "text")
     ])])

FORM("hf259", "환전업무 등록내용 변경 신고서", "fx", code="외환-0259",
     title_note="하나은행 공개 서식 No.259 (외환)",
     sections=[("신분증 사본", [
        ("item", "① 상 호", "text"),
        ("date", "② 설 립 연 월 일", "date"),
        ("date", "년 월 일", "date"),
        ("item2", "③ 대 표 자", "text"),
        ("item3", "④ 주 소", "text"),
        ("item4", "신 고 내 용", "text"),
        ("item5", "⑤ 변 경 전", "text"),
        ("item6", "⑥ 변 경 후", "text"),
        ("item7", "⑦ 변 경 사 유", "text"),
        ("item8", "공동이용 행정정보", "text"),
        ("item9", "동의여부(√)", "text")
     ])])

FORM("hf260", "외국환업무 등록내용 변경 신고서", "fx", code="외환-0260",
     title_note="하나은행 공개 서식 No.260 (외환)",
     sections=[("기재사항", [
        ("item", "외국환업무등록내용변경신고서", "text"),
        ("item2", "① 상 호(본 점)", "text"),
        ("date", "년 월 일", "date"),
        ("item3", "③ 대 표 자(본점)", "text"),
        ("item4", "④ 국 적(대표자)", "text"),
        ("item5", "⑤ 본 점 소 재 지주)", "text"),
        ("amount", "백만원", "amount"),
        ("item6", "⑦ 위험관리시스템명", "text"),
        ("item7", "도입(개발)시기", "text"),
        ("item8", "직원 명", "text"),
        ("item9", "외국환전문요원 명", "text"),
        ("item10", "신 고 내 용", "text"),
        ("item11", "변 경 항 목", "text"),
        ("item12", "변 경 전", "text"),
        ("item13", "변 경 후", "text"),
        ("item14", "명 칭", "text"),
        ("company.address", "본 점 소 재 지", "text"),
        ("item15", "외 국 환 업 무 의 내 용", "text")
     ])])

FORM("hf261", "환전업무 폐지 신고서", "fx", code="외환-0261",
     title_note="하나은행 공개 서식 No.261 (외환)",
     sections=[("기재사항", [
        ("item", "환 전 업 무 폐 지 신 고 서", "text"),
        ("item2", "① 상 호", "text"),
        ("date", "년 월 일", "date"),
        ("item3", "③ 대 표 자", "text"),
        ("item4", "④ 주 소", "text"),
        ("item5", "⑤ 폐 지 사 유", "text")
     ])])

FORM("hf262", "상호계산신고서", "fx", code="5-09-0281",
     title_note="하나은행 공개 서식 No.262 (외환)",
     sections=[("기재사항", [
        ("item", "상 호 계 산 신 고 서", "text"),
        ("item2", "상호, 대표자 성명", "text"),
        ("no", "주소 및 전화번호", "number"),
        ("company.biz_item", "업 종", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item3", "상 호 및 대 표 자 ( 지 정 )", "text"),
        ("customer.address", "주 소", "text"),
        ("item4", "자본금(영업기금)", "text"),
        ("item5", "본 지 사 여 부", "text"),
        ("date", "③ 회 계 기 간", "date"),
        ("date2", "④ 지 사 설 치 유 효 기 간", "date"),
        ("item6", "⑤ 변 경 내 용", "text")
     ])])

FORM("hf263", "지급등의 방법(변경)신고(보고)서", "fx", code="외환-0263",
     title_note="하나은행 공개 서식 No.263 (외환)",
     sections=[("수출입계약서사본 1부", [
        ("item", "지급등의 방법(변경)신고/보고서", "text"),
        ("company.name", "상 호", "text"),
        ("company.ceo", "대 표 자 성 명", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("customer.address", "주 소", "text"),
        ("item2", "거 래 종 류", "choice", ["수출거래", "수입거래", "용역거래", "자본거래"]),
        ("item3", "상호 및 대표자 성명", "text"),
        ("no", "주 소, 전 화 번 호", "number"),
        ("item4", "결 제 방 법", "choice", ["신용장(L/C)", "추심(D/P,D/A)", "송금", "기타()"]),
        ("amount", "계약금액", "amount"),
        ("amount2", "신고금액", "amount"),
        ("date", "당초기간", "date"),
        ("item5", "변경", "text"),
        ("item6", "당초시기", "text"),
        ("amount3", "계정의 구분 및 대차기금액", "amount"),
        ("item7", "貸記", "text"),
        ("amount4", "잔액", "amount"),
        ("item8", "借記", "text"),
        ("item9", "구 분", "text"),
        ("item10", "결제시기", "text"),
        ("no2", "신고번호", "number"),
        ("date2", "유효기간", "date")
     ])])

FORM("hf264", "거주자간 해외직접투자 양수도 신고(보고)서", "fx", code="외환-0264",
     title_note="하나은행 공개 서식 No.264 (외환)",
     sections=[("양도인", [
        ("no", "사업자(주민등록)번호", "number"),
        ("customer.address", "소 재 지(주 소)", "text"),
        ("item", "투 자 자 규 모", "choice", ["대기업", "중소기업", "개인사업자", "개인"]),
        ("company.ceo", "대 표 자 명", "text"),
        ("company.corp_no", "법 인 등 록 번 호", "number"),
        ("item2", "(Tel.)", "text"),
        ("item3", "은행 지점", "text"),
        ("company.name", "법 인 명", "text"),
        ("date", "설 립 등 기 일", "date"),
        ("date", "신 고 일 자", "date"),
        ("no2", "신 고 번 호", "number"),
        ("item4", "투 자 내 역", "choice", ["투자금액", "투자비율"]),
        ("item5", "투자지분 양도내역", "choice", ["투자금액", "투자비율"]),
        ("date2", "양 수 도 일 자", "date"),
        ("amount", "양 수 도 가 액", "amount")
     ])])

FORM("hf265", "수탁기관 변경 신청서", "fx", code="5-09-0164",
     title_note="하나은행 공개 서식 No.265 (외환)",
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

FORM("hf266", "수출대금채권 매입의뢰서", "fx", code="5-09-0198",
     title_note="하나은행 공개 서식 No.266 (외환)",
     sections=[("기재사항", [
        ("no", "고객번호", "number"),
        ("no2", "매입번호", "number"),
        ("item", "소구 여부", "text"),
        ("amount", "통화 및 금액", "amount"),
        ("no3", "계약서번호", "number"),
        ("date", "입금만기일", "date"),
        ("account", "입금계좌번호", "number"),
        ("item2", "수 입 상", "text"),
        ("no4", "상업송장번호", "number"),
        ("item3", "상 품 명", "text"),
        ("no5", "수출신고번호", "number")
     ])])

FORM("hf267", "외국환거래용 인감(서명)신고서", "fx", code="3-09-0240",
     title_note="하나은행 공개 서식 No.267 (외환)",
     sections=[("기재사항", [
        ("item", "한 글(한문)", "text"),
        ("item2", "영 문", "text"),
        ("no", "무역업고유번호", "number"),
        ("customer.phone", "전화번호", "number"),
        ("item3", "한 글", "text"),
        ("company.ceo", "대표자", "text"),
        ("agent.name", "대리인", "text")
     ])])

FORM("hf268", "수입선적서류 도착통지 및 수입신용장 조건불일치에 관한 조회", "fx", code="5-09-0328",
     title_note="하나은행 공개 서식 No.268 (외환)",
     sections=[("기재사항", [
        ("item", "L/C NO(REF NO)", "text"),
        ("amount", "선적 서류 금액", "amount"),
        ("item2", "[은행 사용란] 통보 내역", "text"),
        ("no", "신용장 번호", "number")
     ])])

FORM("hf272", "REDEMPTION OF OUR LETTERS OF GUARANTEE", "fx", code="외환-0272",
     title_note="하나은행 공개 서식 No.272 (외환)",
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

FORM("hf273", "[서식관리프로그램] 수입신용장 취소 및 수입보증금 환급 신청서", "fx", code="외환-0273",
     title_note="하나은행 공개 서식 No.273 (외환)",
     sections=[("기재사항", [
        ("no", "번 호", "number"),
        ("amount", "금 액", "amount"),
        ("date", "유효기일", "date"),
        ("amount2", "취소신청금액", "amount"),
        ("amount3", "환급신청금액", "amount"),
        ("account", "입금계좌", "text")
     ])])

FORM("hf274", "「외국환서식관리프로그램」신용장 분실신고 및 재발행 신청서", "fx", code="5-09-0349",
     title_note="하나은행 공개 서식 No.274 (외환)",
     sections=[("기재사항", [
        ("no", "통 지 번 호", "number"),
        ("item", "발 행 은 행", "text"),
        ("no2", "L / C 번호", "number"),
        ("item2", "수 익 자", "text"),
        ("amount", "금 액", "amount"),
        ("item3", "개설의뢰인", "text"),
        ("date", "유 효 기 일", "date"),
        ("date2", "발 행 일", "date"),
        ("item4", "분실사유 :", "text"),
        ("item5", "첨부서류 : 분실신용장 사본", "text")
     ])])

FORM("hf275", "수입신용장 재개설 및 중계에 관한 약정서", "fx", code="외환-0275",
     title_note="하나은행 공개 서식 No.275 (외환)",
     sections=[("취급 신용장 내용(개별거래시에만 기재)", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf276", "확약서(단기수출보험(본지사금융))", "fx", code="외환-0276",
     title_note="하나은행 공개 서식 No.276 (외환)",
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

FORM("hf277", "포페이팅 의뢰서", "fx", code="외환-0277",
     title_note="하나은행 공개 서식 No.277 (외환)",
     sections=[("기재사항", [
        ("no", "고객번호", "number"),
        ("no2", "거래번호", "number"),
        ("item", "Forfaiting종류 (해당항목 선택)", "choice", ["인수후비소구조건매입", "소구조건매입후인수시비소구조건전환", "하이브리드포페이팅서비스", "Sight비소구조건매입"]),
        ("item2", "Forfaiting Amount", "text"),
        ("item3", "L/C NO.", "text"),
        ("item4", "L/C Issuing Bank", "text"),
        ("item5", "Applicant", "text"),
        ("item6", "Tenor", "text"),
        ("item7", "Expiry Date", "text"),
        ("item8", "Shipment Date", "text"),
        ("account", "입금 계좌번호", "number")
     ])])

FORM("hf278", "판매대금추심의뢰서 매입(취소) 등록 요청/확인서", "fx", code="외환-0278",
     title_note="하나은행 공개 서식 No.278 (외환)",
     sections=[("기재사항", [
        ("item", "내 국 신 용 장", "text"),
        ("currency", "통화코드", "currency"),
        ("item2", "FAX( ) -", "text")
     ])])

FORM("hf279", "추심의뢰서(Renego)", "fx", code="5-09-0333",
     title_note="하나은행 공개 서식 No.279 (외환)",
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

FORM("hf280", "추심 수출환어음 종결처리(유예) 요청서", "fx", code="5-09-0332",
     title_note="하나은행 공개 서식 No.280 (외환)",
     sections=[("기재사항", [
        ("item", "추심 수출환어음 내역", "text"),
        ("no", "거 래 번 호", "number"),
        ("amount", "추 심 금 액", "amount"),
        ("date", "추 심 의 뢰 일", "date"),
        ("no2", "신용장번호/계약서번호", "number"),
        ("date2", "개 설 일 자", "date"),
        ("date3", "유 효 기 일", "date")
     ])])

FORM("hf281", "「외국환서식관리프로그램」조건변경부 신용장양도(SKY T/S) 조건변경.취소 신청서", "fx", code="5-09-0324",
     title_note="하나은행 공개 서식 No.281 (외환)",
     sections=[("신청내역(원 신용장 번호 : )", [
        ("date", "유효기일", "date"),
        ("date2", "제시기일", "date"),
        ("date3", "선적기일", "date"),
        ("rate", "부보비율", "percent")
     ])])

FORM("hf282", "「외국환서식관리프로그램」조건변경부 신용장양도(SKY T/S) 신청서", "fx", code="5-09-0323",
     title_note="하나은행 공개 서식 No.282 (외환)",
     sections=[("신청내역(원 신용장 번호 : )", [
        ("date", "유효기일", "date"),
        ("date2", "제시기일", "date"),
        ("date3", "선적기일", "date"),
        ("rate", "부보비율", "percent")
     ])])

FORM("hf283", "인감증(외국환업무)", "fx", code="5-09-0329",
     title_note="하나은행 공개 서식 No.283 (외환)",
     sections=[("본증은 당행과의 외국환 거래에 있어서 인감(또는 서", [
        ("item", "한 글 (한문)", "text"),
        ("item2", "영문", "text"),
        ("item3", "검 인", "text")
     ])])

FORM("hf284", "인감증 분실신고 및 재발급 신청서(외국환업무)", "fx", code="외환-0284",
     title_note="하나은행 공개 서식 No.284 (외환)",
     sections=[("기재사항", [
        ("item", "각 영업점앞 통보", "text"),
        ("item2", "재 발 급", "text"),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item3", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf285", "인감증 발급신청서(외국환업무)", "fx", code="5-09-0330",
     title_note="하나은행 공개 서식 No.285 (외환)",
     sections=[("기재사항", [
        ("no", "인 감 증 번 호", "number"),
        ("date", "발 급 일 자", "date"),
        ("date2", "유 효 기 간", "date")
     ])])

FORM("hf286", "신용장 확인 신청 및 확약서", "fx", code="외환-0286",
     title_note="하나은행 공개 서식 No.286 (외환)",
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

FORM("hf287", "「외국환서식관리프로그램」신용장 양도 조건변경/취소 신청서 (Amendment / Cancellation)", "fx", code="5-09-0308",
     title_note="하나은행 공개 서식 No.287 (외환)",
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

FORM("hf288", "「외국환서식관리프로그램」신용장 양도 신청서(Application for Total/Partial transf", "fx", code="5-09-0309",
     title_note="하나은행 공개 서식 No.288 (외환)",
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

FORM("hf289", "수출환어음등의 재매입을 위한 약정서", "fx", code="5-09-0402",
     title_note="하나은행 공개 서식 No.289 (외환)",
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

FORM("hf290", "수출환어음 추심 후 매입전환 신청서", "fx", code="외환-0290",
     title_note="하나은행 공개 서식 No.290 (외환)",
     sections=[("기재사항", [
        ("no", "거래번호(추심번호)", "number"),
        ("date", "추심의뢰 일자", "date"),
        ("amount", "추심금액", "amount"),
        ("date2", "예정(확정)만기일", "date"),
        ("no2", "신용장 번호", "number"),
        ("item", "신용장 개설은행", "text"),
        ("item2", "신용장 개설의뢰인", "text")
     ])])

FORM("hf291", "「외국환서식관리프로그램」수출대금채권 양도에 따른 대금지급지시서 및 동의통지서", "fx", code="5-09-0307",
     title_note="하나은행 공개 서식 No.291 (외환)",
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

FORM("hf292", "수입통관도우미서비스 이용신청서", "fx", code="외환-0292",
     title_note="하나은행 공개 서식 No.292 (외환)",
     sections=[("신청인 관련 사항", [
        ("company.name", "업 체 명", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item", "( TEL / e-mail )", "text"),
        ("no", "신용장(또는 당발송금) 번호", "number"),
        ("date", "선 적 (예 정) 일", "date"),
        ("item2", "품 목", "text")
     ])])

FORM("hf293", "「외국환서식관리프로그램」선적서류 수령증 및 수입화물 대도(T/R)신청서", "fx", code="외환-0293",
     title_note="하나은행 공개 서식 No.293 (외환)",
     sections=[("기재사항", [
        ("item", "신용장", "text"),
        ("item2", "수령서류/통수", "text"),
        ("item3", "대도(T/R)", "text")
     ])])

FORM("hf294", "「외국환서식관리프로그램」선적서류 (일부)매입(추심) 의뢰서(2D용)", "fx", code="5-09-0295",
     title_note="하나은행 공개 서식 No.294 (외환)",
     sections=[("위와 같이 화환어음의 (일부)매입(추심)을 신청함에", [
        ("no", "고객번호", "number"),
        ("no2", "매입번호", "number"),
        ("amount", "일부 매입금액", "amount"),
        ("amount2", "일부 추심금액", "amount"),
        ("item", "AMOUNT", "text"),
        ("item2", "TENOR & MATURITY", "text"),
        ("item3", "COMMODITY", "text"),
        ("item4", "H.S. CODE", "text"),
        ("item5", "ACCOUNTEE (drawee)", "text"),
        ("item6", "BENEFICIARY (drawer)", "text"),
        ("item7", "PRICE TERM", "text"),
        ("no3", "수출신고번호", "number"),
        ("amount3", "FOB 금액", "amount"),
        ("item8", "수출 상대국", "text"),
        ("item9", "DOCUMENTS ATTACHED", "text"),
        ("item10", "DRAFT", "text"),
        ("item11", "INVOICE", "text"),
        ("item12", "BENE CERT", "text"),
        ("item13", "CUST", "text"),
        ("item14", "TO REIM. BANK", "text"),
        ("item15", "NAME : (BANK CODE :", "text"),
        ("item16", "명세", "text"),
        ("fx_amount", "외화계정 대체", "fx_amount"),
        ("item17", "원화계정 대체", "text"),
        ("item18", "A", "text"),
        ("item19", "B", "text"),
        ("amount4", "수입보증금", "amount")
     ])])

FORM("hf295", "보증서(수출환어음등 재매입용)", "fx", code="외환-0295",
     title_note="하나은행 공개 서식 No.295 (외환)",
     sections=[("기재사항", [
        ("no", "신용장 (계약서)번호", "number"),
        ("date", "발 행 일 자", "date"),
        ("amount", "신용장 (계약서)금액", "amount"),
        ("amount2", "매 입 금 액", "amount"),
        ("item", "발 행 은 행", "text")
     ])])

FORM("hf296", "매입제한 해제 신청서", "fx", code="5-09-0314",
     title_note="하나은행 공개 서식 No.296 (외환)",
     sections=[("기재사항", [
        ("no", "신용장통지번호", "number"),
        ("no2", "신 용 장 번 호", "number"),
        ("date", "발 행 일 자", "date"),
        ("amount", "신 용 장 금 액", "amount"),
        ("amount2", "해제신청금액", "amount"),
        ("item", "발 행 은 행", "text")
     ])])

FORM("hf297", "단기수출보험(수출채권유동화) 청약 확인서", "fx", code="5-09-0357",
     title_note="하나은행 공개 서식 No.297 (외환)",
     sections=[("보상한도 관련사항", [
        ("item", "청약 종류", "choice", ["신규", "갱신"]),
        ("amount", "한도 신청액", "amount"),
        ("item2", "일반구분1)", "choice", ["일반수출", "위탁가공무역"]),
        ("company.name", "상 호", "text"),
        ("company.ceo", "대표자", "text"),
        ("customer.address", "주 소", "text"),
        ("customer.phone", "전화번호", "number"),
        ("item3", "소재국", "text"),
        ("item4", "종 류", "choice", ["L/C", "CONFIRMEDL/C", "기타()"]),
        ("item5", "결제조건3)", "text"),
        ("item6", "수출상품명", "text"),
        ("item7", "신용장방식 ( ) 무신용장방식 ( )", "text"),
        ("item8", "이면계약 또는 대응구매계약 존재 여부", "choice", ["있음", "없음"]),
        ("item9", "최초 거래시점 : 년 월", "text"),
        ("item10", "총 거래실적 :", "text"),
        ("amount2", "수출금액", "amount"),
        ("item11", "신 용 장 방식", "text"),
        ("item12", "무신용장 방식", "text"),
        ("count", "건수 :", "count"),
        ("amount3", "금액 :", "amount"),
        ("item13", "CLAIM사유 및 결과 :", "text"),
        ("item14", "대행수입 여부", "text"),
        ("item15", "계약서상 수입자와의 관계", "text"),
        ("amount4", "계약서상 대금지급 책임인", "amount"),
        ("item16", "대행수입 사유", "text"),
        ("amount5", "이자보상 특약 가입여부", "choice", ["가입", "미가입"])
     ])])

FORM("hf299", "관리계좌확약서(수출대금)", "fx", code="외환-0299",
     title_note="하나은행 공개 서식 No.299 (외환)",
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

FORM("hf300", "LG 보증금 환급 신청 및 확약서", "fx", code="외환-0300",
     title_note="하나은행 공개 서식 No.300 (외환)",
     sections=[("기재사항", [
        ("no", "(무) 신용장 번호", "number"),
        ("date", "신용장 유효기일", "date"),
        ("item", "수출상 (Beneficiary)", "text"),
        ("amount", "L/G 금액", "amount"),
        ("date2", "L/G 발행일자", "date"),
        ("date3", "B/L 번호 및 선적 일자", "date"),
        ("amount2", "L/G 보증금 금액", "amount"),
        ("account", "입금 계좌 번호", "number")
     ])])

FORM("hf301", "Cable Nego 신청서", "fx", code="5-09-0316",
     title_note="하나은행 공개 서식 No.301 (외환)",
     sections=[("기재사항", [
        ("item", "신 용 장 내 역", "text"),
        ("no", "신용장 번호", "number"),
        ("item2", "개 설 은 행 (SWIFT CODE)", "text"),
        ("amount", "신청통화 및 금액", "amount"),
        ("date", "신용장 유효기일", "date")
     ])])

FORM("hf302", "「외국환서식관리프로그램」BILL OF EXCHANGE (환어음 고객용)", "fx", code="5-09-0047",
     title_note="하나은행 공개 서식 No.302 (외환)",
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

FORM("hf303", "수입실적 확인 및 증명 발급신청서(별지 제11호 서식)", "fx", code="5-09-0129",
     title_note="하나은행 공개 서식 No.303 (외환)",
     sections=[("기재사항", [
        ("item", "② 발급용도 :", "text"),
        ("no", "⑧ 증명발급번호 :", "number"),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf304", "수출실적 확인 및 증명 발급신청서(별지 제10호 서식)", "fx", code="5-09-0128",
     title_note="하나은행 공개 서식 No.304 (외환)",
     sections=[("기재사항", [
        ("item", "② 발급용도 :", "text"),
        ("no", "⑧ 증명발급번호 :", "number"),
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item2", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf305", "( )예금/신탁 거래신고서", "fx", code="외환-0305",
     title_note="하나은행 공개 서식 No.305 (외환)",
     sections=[("기타 신고기관의 장이 필요하다고 인정하는 서류 〈신", [
        ("item", "예금 [ ] [ ] 거래 신고서 신탁", "text"),
        ("no", "(전화번호)", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("no2", "(성명) (전화번호) (주소)", "number"),
        ("amount", "예치( 처분) 금 액", "amount"),
        ("amount2", "예치( 처분) 후잔액", "amount"),
        ("item2", "예 치 ( 처 분 ) 사 유", "text"),
        ("item3", "(성명) (주소)", "text"),
        ("item4", "송 금 은 행", "text"),
        ("no3", "신 고 번 호", "number"),
        ("amount3", "신 고 금 액", "amount"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf306", "증권대차계약 신고서", "fx", code="외환-0306",
     title_note="하나은행 공개 서식 No.306 (외환)",
     sections=[("증권대차 계약서", [
        ("item", "증 권 대 차 계 약 신 고 서", "text"),
        ("item2", "인", "text"),
        ("no", "(전화번호 : ) (E-mail : )", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("item3", "차 입 자", "text"),
        ("item4", "대 여 자", "text"),
        ("item5", "대차대상 증권종류", "text"),
        ("amount", "차 입 ( 한 도 ) 금 액", "amount"),
        ("count", "차 입 수 량", "count"),
        ("item6", "차 입 목 적", "choice", ["위험회피거래", "차익거래", "투기거래", "기타()"]),
        ("date", "차 입 기 간", "date"),
        ("no2", "신 고 번 호", "number"),
        ("amount2", "신 고 금 액", "amount"),
        ("date", "신 고 일 자", "date"),
        ("date2", "유 효 기 간", "date"),
        ("item7", "기타 참고사항", "text")
     ])])

FORM("hf307", "지급수단등의 수출입(변경)신고서", "fx", code="외환-0307",
     title_note="하나은행 공개 서식 No.307 (외환)",
     sections=[("거래당사자의 실체확인서류", [
        ("item", "지급수단등의 수출입(변경) 신고서", "text"),
        ("item2", "① 종 류", "text"),
        ("count", "② 수 량", "count"),
        ("amount", "③ 수 출 입 금 액", "amount"),
        ("item3", "④ 대 가 결 제 방 법", "text"),
        ("item4", "⑤상 호", "text"),
        ("item5", "⑥대 표 자", "text"),
        ("item6", "⑦소 재 지", "text"),
        ("item7", "⑧ 기 타(또는 변 경 내 용)", "text"),
        ("no", "신 고 번 호", "number"),
        ("amount2", "신 고 금 액", "amount"),
        ("date", "신 고 일 자", "date"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf308", "대북투자사업계획서", "fx", code="외환-0308",
     title_note="하나은행 공개 서식 No.308 (외환)",
     sections=[("투자자 현황", [
        ("company.name", "상호 또는 성명", "text"),
        ("date", "설 립 년 월 일", "date"),
        ("customer.address", "소재지(주 소)", "text"),
        ("item", "투 자 자 규 모", "choice", ["대기업", "중소기업", "개인사업자", "개인"]),
        ("company.biz_item", "업 종", "text"),
        ("item2", "담당자 및 연락처", "text"),
        ("company.name", "법 인 명", "text"),
        ("company.ceo", "대 표 자", "text"),
        ("item3", "법 인 형 태", "choice", ["법인", "개인기업", "기타"]),
        ("date2", "설 립(예정)일", "date"),
        ("item4", "총 자 본 금", "text"),
        ("item5", "투 자 형 태주)", "choice", ["단독투자", "공동투자", "합작투자(지분율;%)", "합영투자(지분율;%)"]),
        ("item6", "① 현 금", "text"),
        ("item7", "② 현 물", "text"),
        ("item8", "③ 주 식", "text"),
        ("item9", "⑤ 이익잉여금", "text"),
        ("item10", "⑤ 기 술 투 자", "text"),
        ("item11", "⑥ 기 타( )", "text"),
        ("item12", "자 기 자 금", "text"),
        ("item13", "차 입 금", "text"),
        ("item14", "출 자 자 명", "text"),
        ("item15", "출 자 전", "text"),
        ("item16", "금 회 출 자", "text"),
        ("item17", "출 자 후", "text"),
        ("item18", "한국측", "text"),
        ("item19", "소계(①)", "text"),
        ("item20", "현지측(②)", "text"),
        ("item21", "제3국(③)", "text"),
        ("amount", "합계(①+②+③)", "amount"),
        ("item22", "대 부 액", "text"),
        ("item23", "자 금 용 도", "text"),
        ("rate", "이 율", "percent"),
        ("date3", "년 월 일 ~ 년 월 일", "date"),
        ("item24", "자 금 운 용", "text"),
        ("item25", "자 금 조 달", "text"),
        ("item26", "토지 건물 기계설비 운영자금 . . .", "text"),
        ("item27", "차입금 자기자본", "text")
     ])])

FORM("hf309", "파생상품거래 신고서", "fx", code="외환-0309",
     title_note="하나은행 공개 서식 No.309 (외환)",
     sections=[("기타 한국은행총재가 필요하다고 인정하는 서류", [
        ("item", "파 생 상 품 거 래 신 고 서", "text"),
        ("item2", "인", "text"),
        ("no", "(전화번호 : ) (E-mail : )", "number"),
        ("customer.job", "업 종(직 업)", "text"),
        ("item3", "상호 및 대표자 성명", "text"),
        ("item4", "거 래 기 초 자 산", "choice", ["신용", "통화", "이자율", "주식", "상품", "기타()"]),
        ("item5", "거 래 종 류", "choice", ["선도거래", "선물거래", "스왑거래", "옵션거래", "신용파생상품거래(", "보장매입"]),
        ("amount", "계 약 ( 명 목 ) 금 액", "amount"),
        ("date", "만 기", "date"),
        ("item6", "세 부 내 용", "text"),
        ("no2", "신 고 번 호", "number"),
        ("amount2", "신 고 금 액", "amount"),
        ("date", "신 고 일 자", "date"),
        ("date2", "유 효 기 간", "date"),
        ("item7", "기 타 참 고 사 항", "text")
     ])])

FORM("hf310", "대북투자사업 청산 및 대부채권 회수보고서", "fx", code="외환-0310",
     title_note="하나은행 공개 서식 No.310 (외환)",
     sections=[("투자자 현황", [
        ("company.name", "상호 또는 성명", "text"),
        ("no", "사업자(주민)등록번호", "number"),
        ("no2", "(주소) (전화번호) (e-mail)", "number"),
        ("item", "현 지 법 인 명", "text"),
        ("item2", "주 소(소재지)", "text"),
        ("item3", "법 인 형 태", "choice", ["법인", "개인기업", "기타"]),
        ("item4", "납 입 자 본 금", "text"),
        ("item5", "투 자 형 태주)", "choice", ["단독투자", "공동투자", "합작투자(지분율;%)", "합영투자(지분율;%)"]),
        ("amount", "대 부 금 액", "amount"),
        ("amount2", "기 회수금액", "amount"),
        ("amount3", "금회 회수금액", "amount"),
        ("amount4", "잔 액", "amount"),
        ("amount5", "계", "amount")
     ])])

FORM("hf311", "상호계산계정 폐쇄 신고서", "fx", code="외환-0311",
     title_note="하나은행 공개 서식 No.311 (외환)",
     sections=[("기재사항", [
        ("item", "계 정 상 대 방", "text"),
        ("item2", "대 차 기 잔 고", "text"),
        ("item3", "폐 쇄 사 유", "text")
     ])])

FORM("hf312", "비거주자원화계정을 통한 송금(투자)보고서", "fx", code="5-09-0338",
     title_note="하나은행 공개 서식 No.312 (외환)",
     sections=[("투자자명 : (담당자명 : 전화번호 : )", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf313", "북한지사 설치·현황 보고서", "fx", code="외환-0313",
     title_note="하나은행 공개 서식 No.313 (외환)",
     sections=[("북한지사 신고(설치비, 영업기금 및 유지활동비 지급", [
        ("item", "송금내역", "text"),
        ("item2", "유지활동비", "text"),
        ("item3", "기타경비", "text"),
        ("item4", "변경내용", "text")
     ])])

FORM("hf314", "북한지사 설치(변경) 신고서", "fx", code="외환-0314",
     title_note="하나은행 공개 서식 No.314 (외환)",
     sections=[("기재사항", [
        ("item", "북한지사 설치(변경) 신고서", "text"),
        ("company.name", "상 호", "text"),
        ("company.biz_no", "사 업 자 등 록 번 호", "number"),
        ("company.ceo", "대 표 자", "text"),
        ("customer.rrn", "주 민 등 록 번 호", "number"),
        ("item2", "주 소 ( 소 재 지 )", "text"),
        ("no", "(주소) (전화번호) (e-mail)", "number"),
        ("item3", "신 고 구 분", "text"),
        ("item4", "지 사 구 분", "text"),
        ("item5", "지 사 명", "text"),
        ("company.address", "소 재 지", "text"),
        ("company.biz_item", "업 종", "text"),
        ("date", "회 계 기 간", "date"),
        ("item6", "주 재 원 수", "text"),
        ("item7", "남한파견 : 명, 현지채용 : 명", "text"),
        ("item8", "설 치 사 유", "text"),
        ("item9", "사유", "text"),
        ("no2", "신 고 번 호", "number"),
        ("date2", "유 효 기 간", "date")
     ])])

FORM("hf315", "증권(채권)취득 보고서", "fx", code="외환-0315",
     title_note="하나은행 공개 서식 No.315 (외환)",
     sections=[("투자자현황 (담당자명 : 전화번호 : )", [
        ("date", "설 립 년 월 일", "date"),
        ("no", "(주소) (전화번호) (e-mail)", "number"),
        ("item", "투 자 자 규 모", "choice", ["대기업", "중소기업", "개인사업자", "개인"]),
        ("date2", "신고수리일자", "date"),
        ("no2", "신고수리번호", "number"),
        ("company.name", "법 인 명", "text"),
        ("date3", "설 립 등 기 일", "date"),
        ("date4", "영업개시(예정)일", "date"),
        ("date5", "결 산 일", "date"),
        ("item2", "증권취득일(자본금출자일)", "text"),
        ("item3", "증 권 종 류", "text"),
        ("amount", "액 면 가 액 합 계", "amount"),
        ("amount2", "취득가액합계", "amount"),
        ("item4", "증 권 발 행 여 부", "choice", ["증권발행", "증권미발행"]),
        ("date6", "채 권 취 득 일", "date"),
        ("amount3", "대 부 원 금", "amount"),
        ("amount4", "이 자 율", "amount"),
        ("date7", "대 부 기 간", "date"),
        ("amount5", "원금회수방법", "choice", ["만기일시회수", "분할회수(총회,주기"])
     ])])

FORM("hf316", "북한지사 등의 영업활동 보고서", "fx", code="외환-0316",
     title_note="하나은행 공개 서식 No.316 (외환)",
     sections=[("지사 설치 신고인 현황 (담당자명 : 전화번호 : ", [
        ("company.name", "상호 또는 성명", "text"),
        ("no", "사업자(주민)등록번호", "number"),
        ("no2", "(주소) (전화번호) (e-mail)", "number"),
        ("item", "지 사 명", "text"),
        ("item2", "구 분", "choice", ["지점", "사무소"]),
        ("customer.address", "소 재 지(주 소)", "text"),
        ("date", "설 치 일", "date"),
        ("item3", "설 치 지 역", "text"),
        ("company.biz_item", "업 종", "text"),
        ("item4", "남한파견 : 명 현지채용 : 명", "text"),
        ("item5", "총 자 산", "text"),
        ("amount", "영업기금잔액", "amount"),
        ("company.revenue", "매 출 액", "text"),
        ("item6", "영 업 손 익 금", "text"),
        ("item7", "순이익(결손)금", "text"),
        ("item8", "자금차입현황", "text"),
        ("item9", "자금대여현황", "text"),
        ("item10", "영 업 기 금", "text"),
        ("item11", "설 치 비", "text"),
        ("item12", "유 지 활 동 비", "text")
     ])])

FORM("hf317", "증권발행 보고서", "fx", code="외환-0317",
     title_note="하나은행 공개 서식 No.317 (외환)",
     sections=[("발행조건 및 비용명세서", [
        ("item", "증 권 발 행 보 고 서", "text"),
        ("item2", "명 칭", "text"),
        ("item3", "(서명)", "text"),
        ("no", "(전화번호)", "number"),
        ("item4", "증 권 종 류", "text"),
        ("amount", "액면금액 및 수량", "amount"),
        ("amount2", "발 행 금 액", "amount"),
        ("item5", "계 약 체 결 시 및 장 소", "text"),
        ("item6", "발행시기 및 장소", "text"),
        ("item7", "(상장시 : 증권거래소)", "text"),
        ("rate", "표 면 금 리", "percent"),
        ("item8", "발 행 가 격", "text"),
        ("date", "만 기", "date"),
        ("item9", "해 외 판 매 여 부", "text"),
        ("item10", "배당금지급시기 및 방 법", "text"),
        ("item11", "원 리 금 상 환 방 법", "text"),
        ("item12", "(All-in Cost : )", "text"),
        ("item13", "자 금 용 도", "text"),
        ("item14", "발 행 관 련 기 관", "text")
     ])])

FORM("hf318", "대북투자(변경)신고서", "fx", code="5-09-0275",
     title_note="하나은행 공개 서식 No.318 (외환)",
     sections=[("기재사항", [
        ("item", "대북투자(변경)신고서", "text"),
        ("company.name", "상 호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.corp_no", "법인등록번호", "number"),
        ("customer.rrn", "주민등록번호", "number"),
        ("no", "(주소) (전화번호) (e-mail)", "number"),
        ("company.biz_item", "업 종", "text"),
        ("item2", "투 자 구 분", "choice", ["신규투자", "재투자(증액)", "감액", "폐지"]),
        ("item3", "투 자 방 식", "choice", ["증권취득", "대부채권취득", "기타"]),
        ("item4", "투 자 업 종", "text"),
        ("item5", "주 요 제 품", "text"),
        ("fx_amount", "(자본금 : USD )", "fx_amount"),
        ("no2", "신고수리번호", "number"),
        ("item6", "(U$)", "text"),
        ("date", "년 월 일", "date"),
        ("item7", "현금 (U$)", "text"),
        ("item8", "현물 (U$)", "text"),
        ("amount", "합계 (U$)", "amount")
     ])])

FORM("hf319", "증권취득 신고서", "fx", code="외환-0319",
     title_note="하나은행 공개 서식 No.319 (외환)",
     sections=[("증권취득 계약서", [
        ("item", "증 권 취 득 신 고 서", "text"),
        ("no", "(전화번호 : ) (E-mail : )", "number"),
        ("customer.job", "업 종(직 업)", "text"),
        ("item2", "증 권 취 득 자", "text"),
        ("item3", "증 권 취 득 상 대 방", "text"),
        ("item4", "증 권 취 득 방 법", "choice", ["보유증권대가교환방식(", "상장등록증권간교환/", "기타교환)", "현금매수방식", "기타()"]),
        ("item5", "증 권 종 류", "choice", ["직접기재()", "비거주자발행1년미만원화또는원화연계외화증권"]),
        ("amount", "액 면 가 액", "amount"),
        ("count", "수 량", "count"),
        ("item6", "취 득 단 가", "text"),
        ("amount2", "취 득 가 액", "amount"),
        ("item7", "취 득 사 유", "text"),
        ("no2", "신 고 번 호", "number"),
        ("amount3", "신 고 금 액", "amount"),
        ("date", "신 고 일 자", "date"),
        ("date", "유 효 기 간", "date"),
        ("item8", "기타 참고사항", "text")
     ])])

FORM("hf320", "재환전 신청서", "fx", code="5-09-0379",
     title_note="하나은행 공개 서식 No.320 (외환)",
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

FORM("hf321", "부동산취득신고(수리)서", "fx", code="외환-0321",
     title_note="하나은행 공개 서식 No.321 (외환)",
     sections=[("부동산감정서", [
        ("item", "부동산취득신고[수리]서", "text"),
        ("no", "(전화번호)", "number"),
        ("customer.job", "업 종( 직 업)", "text"),
        ("no2", "(성명) (전화번호) (주소)", "number"),
        ("item2", "부 동 산 의 종 류", "text"),
        ("company.address", "소 재 지", "text"),
        ("property.area", "면 적", "text"),
        ("item3", "(취득단가)", "text"),
        ("date", "취 득 기 간", "date"),
        ("item4", "취 득 사 유", "text"),
        ("no3", "신고(수리)번호", "number"),
        ("amount", "신고(수리)금액", "amount"),
        ("date2", "유 효 기 간", "date")
     ])])

FORM("hf322", "북한사무소 경비지급신고서", "fx", code="외환-0322",
     title_note="하나은행 공개 서식 No.322 (외환)",
     sections=[("기재사항", [
        ("item", "북한사무소 경비지급신고서", "text"),
        ("no", "주민(사업자)등록번호", "number"),
        ("no2", "(주소) (전화번호) (e-mail)", "number"),
        ("item2", "영 업 내 용", "text"),
        ("item3", "사 무 소 명", "text"),
        ("item4", "주소( 소재지)", "text"),
        ("company.biz_item", "업 종", "text"),
        ("item5", "(기 본 경 비)", "text"),
        ("item6", "(기 타 경 비)", "text"),
        ("item7", "남한파견 : 명, 현지채용 : 명", "text"),
        ("no3", "신 고 번 호", "number"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf323", "북한지점 경비지급신고서", "fx", code="외환-0323",
     title_note="하나은행 공개 서식 No.323 (외환)",
     sections=[("기재사항", [
        ("item", "북한지점 경비지급신고서", "text"),
        ("no", "주민(사업자)등록번호", "number"),
        ("no2", "(주소) (전화번호) (e-mail)", "number"),
        ("item2", "영 업 내 용", "text"),
        ("item3", "지 점 구 분", "choice", ["독립채산지점", "비독립채산지점"]),
        ("branch", "지 점 명", "text"),
        ("item4", "주 소(소재지)", "text"),
        ("company.biz_item", "업 종", "text"),
        ("item5", "영 업 기 금", "text"),
        ("item6", "비독립채산지점", "choice", ["설치비"]),
        ("item7", "( 기 본 경 비 )", "text"),
        ("item8", "남한파견 : 명, 현지채용 : 명", "text"),
        ("no3", "신 고 번 호", "number"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf324", "임대차계약신고서", "fx", code="외환-0324",
     title_note="하나은행 공개 서식 No.324 (외환)",
     sections=[("임대차물 증빙서류", [
        ("item", "임 대 차 계 약 신 고 서", "text"),
        ("no", "(전화번호)", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("no2", "(성명) (전화번호) (주소)", "number"),
        ("item2", "임 대 차 물 종 류", "text"),
        ("company.address", "소 재 지", "text"),
        ("count", "수 량", "count"),
        ("item3", "(임대차료)", "text"),
        ("date", "임 대 차 기 간", "date"),
        ("item4", "임 대 차 사 유", "text"),
        ("no3", "신 고 번 호", "number"),
        ("date", "신 고 일 자", "date")
     ])])

FORM("hf325", "증권취득신고서", "fx", code="외환-0325",
     title_note="하나은행 공개 서식 No.325 (외환)",
     sections=[("증권취득재원 증빙서류", [
        ("item", "증권 취득 신고서", "text"),
        ("no", "(전화번호)", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("no2", "(성명) (전화번호) (주소)", "number"),
        ("item2", "현금( ) 자본재( ) 기타( )", "text"),
        ("amount", "액 면 가 액", "amount"),
        ("count", "수 량", "count"),
        ("item3", "취 득 단 가", "text"),
        ("item4", "(미불화 상당액)", "text"),
        ("item5", "취 득 사 유", "text"),
        ("no3", "신 고 번 호", "number"),
        ("amount2", "신 고 금 액", "amount"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf326", "( )매매 신고서", "fx", code="외환-0326",
     title_note="하나은행 공개 서식 No.326 (외환)",
     sections=[("매매대상물 취득 증빙서류", [
        ("item", "( )매매 신고서", "text"),
        ("no", "(전화번호)", "number"),
        ("customer.job", "업 종 ( 직 업 )", "text"),
        ("no2", "(성명) (주소) (전화번호)", "number"),
        ("item2", "매 매 대 상 물 종 류", "text"),
        ("item3", "(미불화 상당액)", "text"),
        ("fx_rate", "(원 화 환 율)", "rate"),
        ("item4", "매 매 사 유", "text"),
        ("no3", "신 고 번 호", "number"),
        ("amount", "신 고 금 액", "amount"),
        ("date", "유 효 기 간", "date")
     ])])

FORM("hf327", "담보제공 신고서", "fx", code="외환-0327",
     title_note="하나은행 공개 서식 No.327 (외환)",
     sections=[("담보제공 계약서", [
        ("item", "담 보 제 공 신 고 서", "text"),
        ("item2", "인", "text"),
        ("no", "(전화번호 : ) (E-mail : )", "number"),
        ("customer.job", "업 종(직 업)", "text"),
        ("item3", "담 보 제 공 자", "choice", ["거주자/", "비거주자)"]),
        ("item4", "(□거주자/□비거주자)", "text"),
        ("item5", "담 보 취 득 자", "choice", ["거주자/", "비거주자)"]),
        ("item6", "담보제공 수혜자", "choice", ["거주자/", "비거주자)"]),
        ("property.kind", "담 보 물 종 류", "choice", ["부동산", "동산", "증권", "예금(현금)", "기타()"]),
        ("item7", "담 보 소 재 지", "text"),
        ("count", "수 량", "count"),
        ("amount", "담 보 가 액", "amount"),
        ("date", "담 보 제 공 기 간", "date"),
        ("item8", "담 보 제 공 용 도", "choice", ["비거주자간거래에대한담보제공", "기타()"]),
        ("no2", "신 고 번 호", "number"),
        ("amount2", "신 고 금 액", "amount"),
        ("date", "신 고 일 자", "date"),
        ("date2", "유 효 기 간", "date"),
        ("item9", "기타 참고사항", "text")
     ])])

FORM("hf328", "외국기업 국내지사 폐쇄신고서", "fx", code="외환-0328",
     title_note="하나은행 공개 서식 No.328 (외환)",
     sections=[("폐쇄사유에 관한 증빙서류", [
        ("item", "① 상 호", "text"),
        ("item2", "② 대 표 자", "text"),
        ("item3", "③ 소 재 지", "text"),
        ("item4", "④ 업 종", "text"),
        ("item5", "⑤ 폐 쇄 구 분", "choice", ["지점", "사무소"]),
        ("date", "폐 쇄 일 자", "date"),
        ("item6", "폐 쇄 사 유", "text"),
        ("no", "신 고 번 호", "number"),
        ("date", "신 고 일 자", "date")
     ])])

FORM("hf329", "외국기업 국내지사 설치신고서", "fx", code="외환-0329",
     title_note="하나은행 공개 서식 No.329 (외환)",
     sections=[("국내에서 영위하고자 하는 업무의 내용과 범위에 관한", [
        ("item", "① 상 호(본점)", "text"),
        ("date", "년 월 일", "date"),
        ("item2", "③ 대 표 자(본점)", "text"),
        ("item3", "④ 소 재 지(본점)", "text"),
        ("item4", "⑤ 사 업 내 용", "text"),
        ("item5", "⑥ 자 본 금", "text"),
        ("item6", "⑦ 상 호", "text"),
        ("item7", "⑧ 대 표 자", "text"),
        ("no", "주민등록번호 (또는 국적)", "number"),
        ("item8", "⑨ 소 재 지", "text"),
        ("item9", "⑩ 영 위 업 종", "text"),
        ("item10", "⑪ 설 치 구 분", "choice", ["지점", "사무소"]),
        ("no2", "신 고 번 호", "number"),
        ("date", "신 고 일 자", "date")
     ])])

FORM("hf330", "외국기업 국내지사 변경신고서", "fx", code="외환-0330",
     title_note="하나은행 공개 서식 No.330 (외환)",
     sections=[("변경사유서", [
        ("item", "① 상 호", "text"),
        ("item2", "② 대 표 자", "text"),
        ("item3", "③ 소 재 지", "text"),
        ("item4", "④ 업 종", "text"),
        ("item5", "변 경 내 용", "text"),
        ("item6", "⑤ 이미 신고된 사항", "text"),
        ("item7", "⑥ 변경하고자 하는 사항", "text"),
        ("item8", "변 경 사 유", "text"),
        ("no", "신 고 번 호", "number"),
        ("date", "신 고 일 자", "date")
     ])])

FORM("hf331", "해외지점의 영업활동 보고서", "fx", code="외환-0331",
     title_note="하나은행 공개 서식 No.331 (외환)",
     sections=[("지점설치 신고인 현황", [
        ("company.name", "상호 또는 성명", "text"),
        ("no", "사업자(주민)등록번호", "number"),
        ("customer.address", "주 소", "text"),
        ("branch", "지 점 명", "text"),
        ("date", "설 치 일", "date"),
        ("item", "설 치 국 가", "text"),
        ("company.biz_item", "업 종", "text"),
        ("item2", "본국파견 : 명 현지채용 : 명", "text"),
        ("item3", "총 자 산", "text"),
        ("amount", "영업기금잔액", "amount"),
        ("company.revenue", "매 출 액", "text"),
        ("item4", "영업손익금", "text"),
        ("item5", "순이익(결손)금", "text"),
        ("item6", "자금차입현황", "text"),
        ("item7", "자금대여현황", "text"),
        ("item8", "구 분", "text"),
        ("item9", "영 업 기 금", "text")
     ])])

FORM("hf332", "외국기업 국내 결산순이익금 송금신청서", "fx", code="외환-0332",
     title_note="하나은행 공개 서식 No.332 (외환)",
     sections=[("납세증명", [
        ("item", "외국기업국내지사 결산순이익금 송금신청서", "text"),
        ("item2", "① 상 호(본 점)", "text"),
        ("item3", "② 대 표 자(본 점)", "text"),
        ("item4", "③ 본 점 소 재 지", "text"),
        ("item5", "신 청 내 용", "text"),
        ("item6", "억원(U$ 상당)", "text"),
        ("date", "⑤ 송 금 예 정 일 자", "date"),
        ("amount", "⑥ 송 금 액 산 출 근 거", "amount"),
        ("date2", "년 월 일 ~ 년 월 일", "date")
     ])])

FORM("hf333", "송금(투자)보고서", "fx", code="외환-0333",
     title_note="하나은행 공개 서식 No.333 (외환)",
     sections=[("투자자명 : (담당자명 : 전화번호 : )", [
        ("company.name", "상호", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("company.ceo", "대표자", "text"),
        ("company.address", "소재지", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf334", "전자적무역결제금융등록(변경,해지)신청서", "fx", code="5-09-0114",
     title_note="하나은행 공개 서식 No.334 (외환)",
     sections=[("신청인(Importer) 등록", [
        ("item", "(한글)", "text"),
        ("item2", "(영문)", "text"),
        ("company.biz_no", "사업자번호", "number"),
        ("company.corp_no", "법인번호", "number"),
        ("company.ceo", "대표자성명", "text"),
        ("date", "대표자 생년월일", "date"),
        ("customer.phone", "전화번호", "number"),
        ("company.fax", "팩스번호", "number"),
        ("customer.name", "성명", "text"),
        ("item3", "(사무실) (H.P)", "text"),
        ("customer.email", "E-mail", "text"),
        ("item4", "원화(KRW)", "text"),
        ("fx_amount", "미화(USD)", "fx_amount"),
        ("item5", "위안화(CNY)", "text"),
        ("item6", "엔화(JPY)", "text"),
        ("no", "기업식별번호", "number"),
        ("item7", "(은행명)", "text"),
        ("item8", "Bic Code", "text"),
        ("no2", "(계좌번호)", "number"),
        ("item9", "주소(영문)", "text")
     ])])
