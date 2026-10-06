"""하나은행 공개 서식 — 선언형 스펙 (23종).

scripts/build_form_specs.py 가 add_template/field_specs/ 에서 생성한다.
직접 고치지 말고 생성 스크립트의 라벨 표를 고칠 것.
서식 하나를 수제 템플릿으로 승격할 때는 여기서 해당 FORM 을 지운다.
"""
from ..formspec import FORM  # noqa: F401

FORM("hf164", "퇴직연금 퇴직급여 지급신청서(DC,기업형IRP)", "retirement", code="5-14-0037",
     title_note="하나은행 공개 서식 No.164 (퇴직연금)",
     sections=[("가입자정보", [
        ("company.name", "기업명", "text"),
        ("account", "퇴직연금 계좌번호", "number"),
        ("item", "제도구분", "choice", ["DC", "기업형IRP"]),
        ("customer.name", "성명", "text"),
        ("item2", "임원여부", "choice", ["근로자", "임원"]),
        ("employer.hire_date", "입사일자", "date"),
        ("item3", "* 마지막 근무일 기재", "text"),
        ("item4", "지급형태", "choice", ["개인형IRP(의무)"]),
        ("item5", "현물이전**", "choice", ["신청(보유상품‘해지없이’IRP로이전)"]),
        ("item6", "예외사유", "choice", ["만55세이후퇴직", "300만원이하퇴직금지급", "가입자사망", "한시적체류자격외국인의출국"]),
        ("item7", "잔여부담금***", "choice", ["없음"]),
        ("item8", "기업반환신청 *****", "choice", ["계속근로기간1년미만퇴직", "국민연금전환금", "임원퇴직급여한도금액"]),
        ("bank", "금융기관명", "text"),
        ("account", "계좌번호", "number"),
        ("item9", "근속 제외 · 가산월수", "choice", ["제외월수()", "가산월수()"]),
        ("item10", "가입자 단독청구", "choice", ["업체폐업", "기타(사용자지급거절등)"])
     ])])

FORM("hf165", "퇴직연금 계약이전신청서(DB)", "retirement", code="5-14-0022",
     title_note="하나은행 공개 서식 No.165 (퇴직연금)",
     sections=[("기업정보 20 년 월 일", [
        ("company.name", "기업명", "text"),
        ("account", "퇴직연금 계좌번호", "number"),
        ("item", "이전사유", "text"),
        ("item2", "이전방식", "text"),
        ("item3", "현물이전*", "choice", ["신청(보유상품‘해지없이’이전)"]),
        ("item4", "상품지정방식은 뒷장 기재", "text"),
        ("item5", "서명 또는 (인)", "text"),
        ("item6", "상품명", "text"),
        ("bank", "금융기관명", "text"),
        ("account", "계좌번호", "number"),
        ("customer.name", "예금주", "text")
     ])])

FORM("hf166", "퇴직연금 계약이전신청서(DC)", "retirement", code="5-14-0196",
     title_note="하나은행 공개 서식 No.166 (퇴직연금)",
     sections=[("기업정보 20 년 월 일", [
        ("company.name", "기업명", "text"),
        ("account", "퇴직연금 계좌번호", "number"),
        ("item", "예약지급일*", "text"),
        ("amount", "수수료 연동출금", "choice", ["동의(사전에약정된경우)", "미동의(기업별도입금)"]),
        ("item2", "이전사유", "text"),
        ("item3", "이전구분", "text"),
        ("item4", "현물이전**", "choice", ["신청(보유상품‘해지없이’이전)"]),
        ("item5", "금융기관", "text"),
        ("account", "계좌번호", "number"),
        ("customer.name", "예금주", "text"),
        ("item6", "서명 또는 (인)", "text")
     ])])

FORM("hf167", "퇴직연금 사전지정운용제도 신청서(디폴트옵션, 기업용)", "retirement", code="5-20-0027",
     title_note="하나은행 공개 서식 No.167 (퇴직연금)",
     sections=[("기본정보", [
        ("company.name", "기업명", "text"),
        ("company.biz_no", "사업자번호", "number"),
        ("item", "등록구분", "choice", ["신청", "변경"]),
        ("item2", "일괄선택", "text")
     ])])

FORM("hf172", "퇴직연금 거래신청서(DC, 기업형IRP)", "retirement", code="5-14-0121",
     title_note="하나은행 공개 서식 No.172 (퇴직연금)",
     sections=[("가입정보", [
        ("company.name", "기업명", "text"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("item", "기업구분", "choice", ["법인", "개인사업자"]),
        ("item2", "제도구분", "choice", ["DC", "기업형IRP", "혼합형"]),
        ("item3", "근로자대표", "choice", ["노동조합", "근로자과반수"]),
        ("item4", "제도가입대상", "choice", ["입사즉시가입", "입사후1년경과가입"]),
        ("date", "퇴직연금 가입기간", "choice", ["제도가입이후근무분만", "제도가입이전근무분포함", "제도가입이전특정시점이후근무분포함(특정시점"]),
        ("item5", "부담금 납입 주기", "choice", ["월납", "분기납", "반기납", "연납"]),
        ("item6", "표준형DC 대상 여부", "choice", ["\u0007대상", "\u0007비대상"]),
        ("item7", "약관변경 통지방법", "choice", ["\u0007수령거절", "\u0007이메일", "\u0007알림톡(LMS)"]),
        ("amount", "장기할인수수료 대상 여부*", "choice", ["\u0007비대상", "\u0007대상(타사가일입자"]),
        ("amount2", "중소기업 수수료할인 대상 여부", "choice", ["\u0007비대상", "대상(중소기업확인서"]),
        ("item8", "기업반환계좌", "text"),
        ("no", "금융기관 : 계좌번호 : 예금주 :", "number"),
        ("date2", "신탁관리인(DC형만 기재)", "date"),
        ("item9", "이름", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.phone", "휴대폰번호", "number"),
        ("customer.email", "이메일주소", "text"),
        ("item10", "퇴직연금 거래인감", "text"),
        ("item11", "일괄선택", "choice", ["전체상품일괄선택"]),
        ("item12", "등록정보", "choice", ["일괄등록(가입자명부파일및부담금명부파일작성)", "개별등록(아래표작성)"]),
        ("date3", "이체개시일", "date"),
        ("date4", "이체종료일", "date")
     ])])

FORM("hf174", "퇴직연금 계약이전 동의서", "retirement", code="퇴직연금-0174",
     title_note="하나은행 공개 서식 No.174 (퇴직연금)",
     sections=[("기재사항", [
        ("company.name", "기업명", "text"),
        ("item", "제도 구분", "choice", ["DB", "DC"]),
        ("item2", "동의 주체", "choice", ["근로자과반수이상", "노동조합(근로자과반수로조직된노동조합이있는경우)"])
     ])])

FORM("hf175", "퇴직연금 AI 포트폴리오 설계(신규 리밸런싱)신청서", "retirement", code="퇴직연금-0175",
     title_note="하나은행 공개 서식 No.175 (퇴직연금)",
     sections=[("기본정보", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("item", "제도 구분", "choice", ["DC", "기업형IRP", "개인형IRP"]),
        ("item2", "하나연금닥터 AI 연금투자 솔루션", "text"),
        ("item3", "통지방법", "text"),
        ("item4", "신청여부", "choice", ["신청안함", "이메일", "알림톡(LMS)"]),
        ("item5", "상승 + (", "text")
     ])])

FORM("hf176", "퇴직연금 퇴직급여 지급신청서(DC,기업형IRP)", "retirement", code="5-14-0037",
     title_note="하나은행 공개 서식 No.176 (퇴직연금)",
     sections=[("가입자정보", [
        ("company.name", "기업명", "text"),
        ("account", "퇴직연금 계좌번호", "number"),
        ("item", "제도구분", "choice", ["DC", "기업형IRP"]),
        ("customer.name", "성명", "text"),
        ("item2", "임원여부", "choice", ["근로자", "임원"]),
        ("employer.hire_date", "입사일자", "date"),
        ("item3", "* 마지막 근무일 기재", "text"),
        ("item4", "지급형태", "choice", ["개인형IRP(의무)"]),
        ("item5", "현물이전**", "choice", ["신청(보유상품‘해지없이’IRP로이전)"]),
        ("item6", "예외사유", "choice", ["만55세이후퇴직", "300만원이하퇴직금지급", "가입자사망", "한시적체류자격외국인의출국"]),
        ("item7", "잔여부담금***", "choice", ["없음"]),
        ("item8", "기업반환신청 *****", "choice", ["계속근로기간1년미만퇴직", "국민연금전환금", "임원퇴직급여한도금액"]),
        ("bank", "금융기관명", "text"),
        ("account", "계좌번호", "number"),
        ("item9", "근속 제외 · 가산월수", "choice", ["제외월수()", "가산월수()"]),
        ("item10", "가입자 단독청구", "choice", ["업체폐업", "기타(사용자지급거절등)"])
     ])])

FORM("hf178", "퇴직연금 입금예정상품등록/변경 신청서", "retirement", code="5-14-0016",
     title_note="하나은행 공개 서식 No.178 (퇴직연금)",
     sections=[("기본정보", [
        ("item", "성명 (기업명)", "text"),
        ("customer.birth", "생년월일 (사업자등록번호)", "date"),
        ("item2", "제도 구분", "choice", ["DB", "DC", "기업형IRP", "개인형IRP"]),
        ("item3", "상품구분", "choice", ["일반상품", "AI포트폴리오"]),
        ("item4", "등록구분", "choice", ["기업부담금(퇴직금)", "개인부담금"]),
        ("item5", "상품명", "text"),
        ("item6", "상품명 전체 자필기재", "text"),
        ("item7", "일반금융소비자", "choice", ["미성년자", "피성년후견인", "피한정후견인", "만65세이상고령자"]),
        ("item8", "전문금융소비자", "choice", ["만19세이상~만65세미만성년자", "법인,조합등단체", "전문금융소비자이나상품설명을희망"]),
        ("item9", "약관 및 상품설명서", "choice", ["서면수령", "이메일", "알림톡(발송실패시LMS발송)"]),
        ("item10", "가입자(기업명)", "text"),
        ("agent.name", "대리인", "text")
     ])])

FORM("hf180", "DB 적립금 이전 요청서", "retirement", code="5-20-0021",
     title_note="하나은행 공개 서식 No.180 (퇴직연금)",
     sections=[("기재사항", [
        ("item", "이전받을 금융회사", "text"),
        ("item2", "자산관리기관명", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item3", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])

FORM("hf181", "이전 가입자 명부(DC,기업형 IRP용)", "retirement", code="5-20-0012",
     title_note="하나은행 공개 서식 No.181 (퇴직연금)",
     sections=[("현금", [
        ("item", "유 의 사 항", "text"),
        ("item2", "이전받을 금융회사", "text"),
        ("item3", "자산관리기관명", "text"),
        ("item4", "1 또는 2 기재하세요", "text")
     ])])

FORM("hf182", "이전신청(취소)서(DB,DC,기업형IRP 이전용)", "retirement", code="5-20-0011",
     title_note="하나은행 공개 서식 No.182 (퇴직연금)",
     sections=[("법인 인감증명서(직인란에 법인인감을 날인하는 경우에", [
        ("item", "신청내용", "choice", ["이전신청", "이전신청취소(", "에하나만√표시합니다.)"]),
        ("item2", "이전의사 확인*", "text"),
        ("company.name", "기업명", "text"),
        ("company.biz_no", "사업자 번호", "number"),
        ("item3", "담당자 성명", "text"),
        ("customer.phone", "전화번호", "number"),
        ("no", "금융회사명 : 관리번호 :", "number"),
        ("item4", "제도유형", "choice", ["DB", "DC", "기업형IRP"]),
        ("item5", "이전계약", "choice", ["운용관리계약+자산관리계약", "운용관리계약"]),
        ("item6", "이전유형", "choice", ["전부(계약)이전", "일부(적립금,가입자)이전"]),
        ("item7", "이전대상**", "choice", ["전액현금", "실물"]),
        ("item8", "원", "text"),
        ("item9", "금융회사명 :", "text")
     ])])

FORM("hf183", "퇴직연금 통지서비스 신청서(가입자용)", "retirement", code="5-14-0128",
     title_note="하나은행 공개 서식 No.183 (퇴직연금)",
     sections=[("기재사항", [
        ("item", "구분", "text"),
        ("item2", "고객기재란주1)", "text"),
        ("item3", "성명(업체명)", "text"),
        ("customer.birth", "생년월일", "date"),
        ("date", "년 월 일", "date"),
        ("company.biz_no", "사업자등록번호", "number"),
        ("customer.phone", "휴대전화", "text"),
        ("item4", "E-mail 주소", "text"),
        ("item5", "@", "text"),
        ("item6", "자택", "text"),
        ("item7", "자택전화", "text"),
        ("item8", "( ) -", "text"),
        ("item9", "직장전화", "text"),
        ("item10", "우편물수령처", "text"),
        ("item11", "전화연락처", "choice", ["자택", "직장", "휴대폰"]),
        ("item12", "통지구분", "text"),
        ("count", "목표수익률에 도달하면 펀드 자동환매", "choice", ["신청안함", "등록/변경", "해지"]),
        ("rate", "목표수익률", "percent"),
        ("item13", "신청여부", "choice", ["신청안함", "이메일", "알림톡(LMS)"])
     ])])

FORM("hf184", "퇴직연금 계약해지 신청서(개인형IRP)", "retirement", code="퇴직연금-0184",
     title_note="하나은행 공개 서식 No.184 (퇴직연금)",
     sections=[("기본정보", [
        ("customer.name", "성 명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("account", "퇴직연금 계좌번호", "number"),
        ("customer.phone", "연락처", "text"),
        ("item", "일반사유", "choice", ["일반중도해지"]),
        ("item2", "부득이한 사유", "choice", ["가입자의사망", "해외이주", "3개월이상요양", "개인회생및파산", "천재지변"]),
        ("bank", "금융기관명", "text"),
        ("amount", "기타 과세제외 금액으로 확인된 금액", "amount"),
        ("item3", "연금계좌의 운용소득", "text")
     ])])

FORM("hf185", "퇴직연금 DC 기업부담금 자동이체 신청서", "retirement", code="퇴직연금-0185",
     title_note="하나은행 공개 서식 No.185 (퇴직연금)",
     sections=[("기업정보", [
        ("company.name", "기업명", "text"),
        ("company.biz_no", "사업자 등록번호", "number"),
        ("item", "신청구분", "choice", ["신청", "변경", "해지"]),
        ("item2", "매월 일 (*1~5일 불가)", "text"),
        ("date", "년 월 일", "date"),
        ("item3", "※ 확정기여형퇴직연금(DC)계좌", "text"),
        ("item4", "총가입자수", "text"),
        ("amount", "총액", "amount")
     ])])

FORM("hf188", "퇴직연금 중도인출신청서(DC,기업형·개인형IRP)", "retirement", code="5-14-0021",
     title_note="하나은행 공개 서식 No.188 (퇴직연금)",
     sections=[("신청 정보", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.phone", "휴대전화", "text"),
        ("item", "제도", "choice", ["DC", "기업형IRP", "개인형IRP"]),
        ("no", "계좌번호 또는 회사명", "number"),
        ("item2", "DC, 기업형IRP의 가입자는 회사명 작성", "text"),
        ("employer.hire_date", "입사일", "date"),
        ("date", "중간정산일", "date"),
        ("amount", "신청금액", "choice", ["전부", "일부원"]),
        ("item3", "임원여부", "choice", ["근로자", "임원"]),
        ("item4", "가입자 부담금 여부", "choice", ["가입자부담금(적립금)없음", "가입자부담금(적립금)있음"]),
        ("item5", "추가 부담금 입금 여부", "choice", ["해당사항없음"]),
        ("item6", "신청시기", "text"),
        ("item7", "공통서류", "text"),
        ("count", "주택매매", "choice", ["부동산매매계약서(부동산중개인을통한거래)"]),
        ("item8", "주택 청약당첨", "choice", ["당첨자확인서류", "계약금납부일정확인서류"]),
        ("item9", "주택 신축", "choice", ["공사계약서", "건축설계서", "건축허가서또는착공신고필증"]),
        ("item10", "경매 취득", "choice", ["매각허가결정문(부동산의표시포함)", "대금지급기한통지서"]),
        ("item11", "오피스텔", "choice", ["건축물관리대장–건물용도"]),
        ("item12", "연장", "choice", ["잔금입금증(수기영수증제외)"]),
        ("item13", "잔금 지급 후", "choice", ["잔금입금증(수기영수증제외)", "전입후주민등록등본"]),
        ("amount2", "연간임금총액 확인서류", "choice", ["가입자의직전연도근로소득원천징수영수증또는급여명세서"]),
        ("item14", "필요서류", "text"),
        ("item15", "인적피해", "choice", ["사망/실종된경우", "입원치료의경우"])
     ])])

FORM("hf189", "퇴직연금 부담금 등록 신청서(DC,기업형IRP)", "retirement", code="퇴직연금-0189",
     title_note="하나은행 공개 서식 No.189 (퇴직연금)",
     sections=[("기업정보 20 년 월 일", [
        ("company.name", "기업명", "text"),
        ("account", "퇴직연금 계좌번호", "number"),
        ("item", "신청구분", "choice", ["등록", "취소"]),
        ("item2", "부담금등록 구분", "choice", ["일괄(파일)신청", "개별신청"]),
        ("item3", "부담금 종류", "choice", ["정기부담금", "잔여부담금(퇴직정산후부족액)", "경영성과급부담금", "계약이전부담금", "개인부담금", "지연이자"]),
        ("item4", "납부방법", "choice", ["별도계좌입금", "즉시연동납부", "예약연동납부[예약일"]),
        ("item5", "부담금", "text")
     ])])

FORM("hf191", "퇴직연금 계약해지 신청서(DB,DC)", "retirement", code="5-14-0040",
     title_note="하나은행 공개 서식 No.191 (퇴직연금)",
     sections=[("기업정보", [
        ("company.name", "기업명", "text"),
        ("account", "퇴직연금 계좌번호", "number"),
        ("item", "제도", "choice", ["DB", "DC"]),
        ("item2", "해지사유", "choice", ["제도폐지", "사업장파산/폐업", "사업장의인수합병", "법령변경"]),
        ("amount", "수수료 연동출금** (DC형만 해당)", "choice", ["연동출금동의(사전에약정된경우)", "연동출금미동의(기업별도입금)"]),
        ("item3", "서명 또는 (인)", "text"),
        ("customer.birth", "생년월일", "date"),
        ("employer.hire_date", "입사일자", "date"),
        ("date", "중간정산일자", "date"),
        ("item4", "지급형태", "text"),
        ("item5", "IRP 의무이전 예외사유", "text"),
        ("date2", "잔여부담금 (DC형만 기재)", "date"),
        ("item6", "입금 받는 계좌정보", "text"),
        ("item7", "기업반환 (기업반환계좌로 반환)", "text"),
        ("item8", "금융기관명 :", "text"),
        ("no", "계좌번호 :", "number")
     ])])

FORM("hf192", "퇴직연금 통지서비스 신청서(기업용)", "retirement", code="5-14-0127",
     title_note="하나은행 공개 서식 No.192 (퇴직연금)",
     sections=[("기재사항", [
        ("company.name", "기업명", "text"),
        ("item", "제도구분", "choice", ["DB", "DC", "기업형IRP"]),
        ("item2", "주담당자", "text"),
        ("item3", "부담당자", "text"),
        ("item4", "통지구분", "text"),
        ("count", "목표수익률에 도달하면 펀드 자동환매", "choice", ["신청안함", "등록/변경", "해지"]),
        ("account", "계좌번호", "number"),
        ("item5", "거 래 내 용", "text")
     ])])

FORM("hf193", "퇴직연금 계약해지 신청서(기업형IRP)", "retirement", code="5-14-0139",
     title_note="하나은행 공개 서식 No.193 (퇴직연금)",
     sections=[("기업정보", [
        ("company.name", "기업명", "text"),
        ("account", "퇴직연금 계좌번호", "number"),
        ("item", "해지사유", "choice", ["제도폐지", "사업장파산/폐업", "사업장의인수합병", "법령변경"]),
        ("amount", "수수료 연동출금**", "choice", ["연동출금동의(사전에약정된경우)", "연동출금미동의(기업별도입금)"]),
        ("item2", "IRP 의무이전 예외사유", "text"),
        ("item3", "입금 받는 계좌정보", "text"),
        ("item4", "기업반환 (기업반환계좌로 변환)", "text"),
        ("item5", "금융기관명 :", "text"),
        ("no", "계좌번호 :", "number")
     ])])

FORM("hf194", "퇴직연금 항목등록/변경 신청서", "retirement", code="5-14-0129",
     title_note="하나은행 공개 서식 No.194 (퇴직연금)",
     sections=[("기본정보", [
        ("item", "성명(업체명)", "text"),
        ("customer.birth", "생년월일(사업자번호)", "date"),
        ("item2", "제도구분", "choice", ["DB", "DC", "기업형IRP", "개인형IRP"]),
        ("item3", "구분", "choice", ["등록", "변경", "해제"]),
        ("item4", "공통사항", "choice", ["사업자번호변경", "기업반환계좌변경", "부담금납입주기변경", "기업담당자변경(추가항목필수기재)", "신탁관리인변경(추가항목필수기재)", "거래인감변경(거래인감통보서필수징구)"]),
        ("item5", "DB", "choice", ["대체상품매수동의"]),
        ("item6", "DC/기업형IRP", "choice", ["임금총액등록", "운용상품군(자동라인업)등록", "표준형DC등록", "비대면DC가입신청명부등록"]),
        ("item7", "개인형IRP", "choice", ["개인형IRP속성변경", "가입자격등록(인터넷)"]),
        ("item8", "변경 전", "text"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("item9", "신청구분", "choice", ["등록", "변경", "해제"]),
        ("item10", "담당자구분", "choice", ["주담당자", "부담당자", "보고서담당자"]),
        ("customer.phone", "휴대폰번호", "number"),
        ("customer.email", "이메일주소", "text"),
        ("item11", "기업담당자 성명", "text"),
        ("no", "기업담당자 휴대폰번호", "number"),
        ("date", "근로자 앞 문자 발송요청일", "date"),
        ("item12", "항목 설명", "text")
     ])])

FORM("hf195", "퇴직연금 가입자(등록·변경·삭제) 신청서(DB,DC,기업형IRP)", "retirement", code="5-14-0119",
     title_note="하나은행 공개 서식 No.195 (퇴직연금)",
     sections=[("기업정보", [
        ("company.name", "기업명", "text"),
        ("account", "퇴직연금 계좌번호", "number"),
        ("item", "퇴직연금 가입제도", "choice", ["DB", "DC", "기업형IRP"]),
        ("item2", "신청구분", "choice", ["등록"]),
        ("item3", "가입자등록 구분", "choice", ["일괄(파일)신청", "개별신청"]),
        ("item4", "가입자수", "text"),
        ("date", "가입자 명부 산정 기준일자", "date")
     ])])

FORM("hf196", "기업형IRP 가입대상 근로자 확인서", "retirement", code="퇴직연금-0196",
     title_note="하나은행 공개 서식 No.196 (퇴직연금)",
     sections=[("기업정보", [
        ("company.name", "기업명", "text"),
        ("company.biz_no", "사업자 번호", "number"),
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])
