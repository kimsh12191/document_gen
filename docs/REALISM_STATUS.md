# 서식 현실화 진행현황

`python scripts/realism_status.py build` 로 `docs/realism/*.md` 를 집계해 만든 파일입니다.

| 상태 | 건수 |
|---|---|
| 반영(검색근거) | 38 |
| 조사중 | 2 |
| 대기 | 30 |
| **합계** | **70 / 70** |

## 신원·신분

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 주민등록증 | `resident_id_card` | 주민등록법 시행령 제36조 앞면 표기사항(성명·사진·주민등록번호·주소·발행일·주민등록기관), 1999년 도입 현행 디자인, [행정안전부 주민등록증 안내](https://www.mois.go.kr/frt/sub/a06/b06/IDCard_2/screen.do), [나무위키 주민등록증](https://namu.wiki/w/%EC%A3%BC%EB%AF%BC%EB%93%B1%EB%A1%9D%EC%A6%9D) | 반영(검색근거) | 항목 구성은 기존과 일치 확인, 발행일을 실물 표기(2015. 3. 20.) 위주로 변경 |
| 운전면허증 | `driver_license` | 도로교통법 시행규칙 운전면허증 서식(2019 디자인), [모터그래프 운전면허 지역표기 숫자화](https://www.motorgraph.com/news/articleView.html?idxno=2989), [MS Purview 면허번호 형식](https://learn.microsoft.com/ko-kr/purview/sit-defn-south-korea-drivers-license-number), [갱신기간 생일 전후 6개월 변경](https://webzine.kacta.or.kr/news/articleView.html?idxno=24322) | 반영(검색근거) | 면허번호 끝 2자리를 체크숫자+발급회차로 변경, 경기북부(28) 코드·경찰청 관할 반영, 2026.1.1. 이후 발급분은 적성검사(갱신)기간을 생일 전후 6개월로 계산 |
| 여권 | `passport` | 여권법 시행규칙 / 차세대 전자여권(2021.12.21. 발급 개시) 정보면, ICAO 9303 TD3 MRZ, [외교부 차세대 전자여권 발급 개시](https://www.mofa.go.kr/www/brd/m_4080/view.do?seq=371764), [송파구 차세대 전자여권 안내](https://www.songpa.go.kr/www/contents.do?key=5472) | 반영(검색근거) | 차세대 여권 날짜를 월 한글/영문 병기(17 1월/JAN 2024)로 변경, 발행관청을 외교부/MINISTRY OF FOREIGN AFFAIRS로 병기, 구형(2021.12.20. 이전)은 영문 표기 유지 |
| 외국인등록증 | `alien_registration_card` | 출입국관리법 제33조(외국인등록증·영주증), 시행규칙 외국인등록증 서식, [출입국관리법 제33조 영주증(korea.kr)](https://m.korea.kr/briefing/actuallyView.do?newsId=148877182), [나무위키 외국인등록증](https://namu.wiki/w/%EC%99%B8%EA%B5%AD%EC%9D%B8%EB%93%B1%EB%A1%9D%EC%A6%9D) | 반영(검색근거) | 영주(F-5) 자격자는 영주증(PERMANENT RESIDENT CARD) 제목으로 표시, 체류자격 표기를 비전문취업(E-9) 형식 위주로 조정 |
| 인감증명서 | `seal_certificate` | 인감증명법 시행령 별지 제14호서식(방문)·제14호의2서식(전자발급), [별지 제14호서식 <개정 2016. 7. 5.>](https://www.law.go.kr/flDownload.do?flSeq=116810727), [별지 제14호의2서식 <신설 2024. 5. 7.>](https://www.law.go.kr/flDownload.do?flSeq=145805945) | 반영(검색근거) | 서식 표시줄 추가, 발급번호를 인감증명서 발급사실 확인용 번호(4-4-4)로 변경, 전자발급본(문서확인번호·일반용만) 추가, 본인/대리인 ○ 표시, 부동산 매수자 성명(법인명)·주민등록번호(법인등록번호)·주소(법인 소재지) 칸 상시 표시, 발급신청자 서명란 추가, 근거 없는 사용목적 항목 삭제, 증명문구·발급기관을 표 안으로 이동, 주민등록번호 전체 표시 |
| 본인서명사실확인서 | `signature_confirmation` | 본인서명사실 확인 등에 관한 법률 시행령 별지 제2호서식, [별지 제2호서식 <개정 2016. 7. 26.>](https://law.go.kr/flDownload.do?flSeq=68265497), [정부24 본인서명사실확인서 발급](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=13110000047) | 반영(검색근거) | 서식 표시줄·문서확인번호 추가, 용도를 부동산 관련 용도 및 자동차 매도용도(소유권 이전/제한물권 설정/그 밖의 용도) + 거래상대방(성명(법인명)·주민등록번호(법인등록번호)·주소) + 그 외의 용도 구조로 변경, 근저당권 설정 시 거래상대방=대출은행(법인), 위임받은 사람란 추가, 근거 없는 제출기관·세부용도 항목 삭제, 확인문구·발급기관을 표 안으로 이동 |

## 가족관계

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 주민등록표 등본 | `resident_registration_copy` | 주민등록법 시행규칙 별지 제18호서식(<개정 2019. 11. 19.>), [law.go.kr 별지1 주민등록등본](https://www.law.go.kr/flDownload.do?flSeq=135138117&bylClsCd=200203), [정부24 등·초본 발급](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=13100000015) | 반영(검색근거) | 서식 표시줄 추가, 증명문구·담당자·신청인·용도 및 목적·발급일·발급기관을 표 위 상단 블록으로 이동, 세대원표를 성명(한자)/주민등록번호 2단 행으로 변경, 과거 주소변동 행(선택) 추가, 날짜 2015-03-02 표기 위주, 정부24 진위확인 안내문 보완 |
| 주민등록표 초본 | `resident_registration_abstract` | 주민등록법 시행규칙 별지 제19호서식(<개정 2019. 11. 19.>), [정부24 등·초본 발급](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=13100000015), [나무위키 주민등록표초본](https://namu.wiki/w/%EC%A3%BC%EB%AF%BC%EB%93%B1%EB%A1%9D%ED%91%9C%EC%B4%88%EB%B3%B8) | 반영(검색근거) | 서식 표시줄, 상단 증명 블록(이 초본은 개인별 주민등록표의 원본내용과 틀림없음을 증명합니다·담당자·신청인·용도 및 목적·발급일·발급기관) 이동, 주소 변동 사항을 주소/전입일·변동일 + 세대주 및 관계/등록상태/변동사유 2단 행으로 변경, 변동일=신고일 규칙, 날짜 대시 표기 위주 |
| 가족관계증명서 | `family_relation_certificate` | 가족관계의 등록 등에 관한 법률 제15조제2항 일반증명서, 서식은 대법원 가족관계등록예규(규칙 아님), [대법원 전자가족관계등록시스템 안내(양천구청)](https://www.yangcheon.go.kr/site/yangcheon/01/10103020000002016081013.jsp), [등록사항별 증명서의 발급 등에 관한 사무처리지침](https://korea.legal/%EB%8C%80%EB%B2%95%EC%9B%90-%EC%98%88%EA%B7%9C/%EA%B0%80%EC%A1%B1%EA%B4%80%EA%B3%84%EB%93%B1%EB%A1%9D%EC%98%88%EA%B7%9C/%EB%93%B1%EB%A1%9D%EC%82%AC%ED%95%AD%EB%B3%84-%EC%A6%9D%EB%AA%85%EC%84%9C%EC%9D%98-%EB%B0%9C%EA%B8%89-%EB%93%B1%EC%97%90-%EA%B4%80%ED%95%9C-%EC%82%AC%EB%AC%B4%EC%B2%98%EB%A6%AC%EC%A7%80%EC%B9%A8/) | 반영(검색근거) | 근거 없는 [별지 제1호서식] 표시줄 삭제, 인터넷 발급 명의를 법원행정처 전산정보중앙관리소 전산운영책임관으로 수정(직인 포함), 인터넷 발급본에도 발급시각·신청인 표시 |
| 기본증명서 | `basic_certificate` | 가족관계등록법 제15조제2항 일반증명서(대법원 가족관계등록예규 양식), [등록사항별증명서 교부 안내(전자민원센터)](https://help.scourt.go.kr/nm/min_17/min_17_2/min_17_2_4/index.html), [기본증명서 종류](https://0muwon.com/entry/%EA%B8%B0%EB%B3%B8%EC%A6%9D%EB%AA%85%EC%84%9C-%EC%A2%85%EB%A5%98-%EC%9D%BC%EB%B0%98-%EC%83%81%EC%84%B8-%ED%8A%B9%EC%A0%95-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0) | 반영(검색근거) | 근거 없는 [별지 제1호서식] 표시줄 삭제, 인터넷 발급 명의(전산운영책임관)·발급시각·신청인 수정, 일반등록사항 출생 【출생장소】【신고일】【신고인】 구성 유지 |
| 혼인관계증명서 | `marriage_relation_certificate` | 가족관계등록법 제15조제2항 일반증명서(대법원 가족관계등록예규 양식), [전자가족관계등록시스템 발급 안내](https://www.yangcheon.go.kr/site/yangcheon/01/10103020000002016081013.jsp), [나무위키 가족관계등록부](https://namu.wiki/w/%EA%B0%80%EC%A1%B1%EA%B4%80%EA%B3%84%EB%93%B1%EB%A1%9D%EB%B6%80) | 반영(검색근거) | 근거 없는 서식 표시줄 삭제, 배우자를 본인표에서 분리해 혼인사항 아래 별도 표로 이동, 혼인 상세(【신고일】【배우자】【배우자의 주민등록번호】【처리관서】) 유지, 인터넷 발급 명의 수정 |

## 소득·재직

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 재직증명서 | `employment_certificate` | 근로기준법 제39조(사용증명서), 법정서식 없음·통용양식 ([예스폼](https://www.yesform.com/forms/vform_414817.php), [자비스](https://help.jobis.co/hc/ko/articles/12325781741721)) | 반영(검색근거) | 인적사항·재직사항·발급(용도/제출처) 세로 구분열 단일표로 변경, 담당업무·제출처 추가, 생년월일 변형, 직종 삭제, 문서번호 형식 다양화 |
| 경력증명서 | `career_certificate` | 근로기준법 제39조(사용증명서), 통용양식 ([비즈폼 표준 경력증명서](https://standard.bizforms.co.kr/form/form_view/form_795.asp), [예스폼](https://www.yesform.com/forms/vform_414818.php)) | 반영(검색근거) | 경력표 열 제목(근무기간·근무부서·직위·담당업무) 정리, 제출처 추가, 증명 문구를 통용 문구(위의 기재사항이 사실과 다름없음을 증명합니다)로 변경 |
| 급여명세서 | `pay_stub` | 근로기준법 제48조제2항·시행령 제27조의2, 고용노동부 임금명세서 예시 ([easylaw](https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=1694&ccfNo=2&cciNo=3&cnpClsNo=1), [고용노동부 임금명세서](https://www.moel.go.kr/wageCal.do)) | 반영(검색근거) | 고용노동부 예시 구조(지급일·성명·생년월일·사번·부서·직급, 매월/격월 또는 부정기 지급 구분, 지급액 계·공제액 계·실수령액, 근로일수·근로시간수·통상시급·가족수, 계산방법 표)로 재구성. 2026 요율·국민연금 상하한(2026.7~ 41만~659만원) 반영 |
| 근로계약서 | `employment_contract` | 고용노동부 표준근로계약서(기간의 정함이 없는 경우) ([고용노동부 표준근로계약서 7종](https://www.moel.go.kr/policy/policydata/view.do?bbs_seq=20190700008), [예스폼](https://www.yesform.com/forms/vbuse_4730.php)) | 반영(검색근거) | 제목 표기·조항 문구를 표준서식 원문대로(매주 _일(또는 매일단위)근무, 주휴일 매주 _요일 / 월(일, 시간)급 / 상여금·기타급여 있음( )·없음( ) / 지급방법 괄호체크) 정리, 연봉 표기 삭제, 수당 목록화, 서명란을 세로 배치로 변경, 근로자 주민번호 삭제(원서식에 없음) |
| 근로소득 원천징수영수증 | `withholding_receipt` | 소득세법 시행규칙 [별지 제24호서식(1)] 개정 2023.3.20(8쪽)·2025.3.21(9쪽)·2025.6.30·2026.3.20 ([법령 서식 2026.3.20](https://www.law.go.kr/LSW//flDownload.do?gubun=&flSeq=164446335&bylClsCd=110202), [국세법령 2025.6.30](https://taxlaw.nts.go.kr/downloadPDFFile.do?fleId=701000000001059462&fleSn=1)) | 반영(검색근거) | 제1쪽 구조로 재구성: 상단 거주구분·거주지국·내외국인·외국인단일세율·파견근로자·종교관련종사자·국적·세대주·연말정산 구분 체크, 징수의무자 ④주민등록번호·③-1·③-2 추가, Ⅰ ⑮-1~⑮-4 행 및 Ⅱ 비과세 및 감면소득 명세 행 추가, Ⅲ 실효세율 추가, 2쪽 정산명세 블록 삭제, 발급일 기준 서식 개정일 표기 |
| 소득금액증명원 | `income_certificate` | 국세청 소득금액증명(홈택스), 2022.9.22. 5종→1종 통합 서식 ([국세청 서식 개정 안내](https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2207&nttSn=1307651), [한국세정신문](https://taxtimes.co.kr/mobile/article.html?no=256087)) | 반영(검색근거) | 폐지된 근로소득자용/종합소득세 신고자용 구분 삭제, 통합서식 구조(납세자 인적사항·증명기간 / 종합소득세 신고 현황 / 연말정산 현황: 원천징수의무자·소득금액(과세대상급여액)·총결정세액)로 변경, 종소세 신고 이력은 20% 확률 표시 |
| 국민연금 가입자 가입증명 | `pension_enrollment_certificate` | 국민연금법 시행규칙 [별지 제11호서식] 국민연금가입자증명서 ([법령 서식](https://www.law.go.kr/LSW/flDownload.do?flSeq=94342797), [정부24 가입자 가입증명](https://www.gov.kr/portal/service/serviceInfo/B55201500022)) | 반영(검색근거) | 서식번호·제목(국민연금가입자증명서) 반영, □가입자의 인적사항(발급번호·발급일자·성명·주민등록번호) / □가입자의 종류 및 자격 취득일(최초 자격취득일, 가입자 종류·사업장 명칭·자격취득일·자격상실일) 구조로 변경, 주소·현 사업장 항목 삭제, 발급자를 국민연금공단 이사장으로 변경 |
| 건강보험 자격득실확인서 | `health_insurance_qualification` | 국민건강보험법 제11조(자격취득 등의 확인), 공단 발급 증명 ([정부24 자격득실 확인서](https://www.gov.kr/portal/service/serviceInfo/PTR000050333), [NHIS 발급 안내](https://www.nhis.or.kr/static/html/guide/sub2_010103.html)) | 반영(검색근거) | 근거 조문을 제96조의2에서 제11조로 정정, 가입자구분 값을 직장가입자·지역세대주·지역세대원·직장피부양자로 세분, 열 제목 표기(사업장 명칭) 정리 |
| 건강보험료 납부확인서 | `health_insurance_payment` | 국민건강보험공단 건강보험료 납부확인서 ([NHIS 보험료 납부확인서](https://www.nhis.or.kr/static/html/guide/sub2_010403.html), [발급 안내](https://www.watax.kr/social-insurance/health-insurance-payment-certificate-issuance)) | 반영(검색근거) | 월별 고지보험료·납부보험료를 건강보험/장기요양 구분 2단 헤더 표로 변경(고지 GT 추가), 성명 옆 주민등록번호/생년월일 변형, 가입자·사업장 정보를 한 표로 통합 |

## 세금·보험

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 납세증명서(국세완납증명) | `tax_payment_certificate` | 국세징수법 시행규칙 [별지 제94호서식], 국세청 민원사무처리규정 [별지 제21호서식](영문) 문구 대조 ([국세청 영문서식](https://www.law.go.kr/LSW//flDownload.do?flSeq=155626775), [정부24](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=12100000011)) | 반영(검색근거) | 서식번호 헤더(별지 제94호) 추가, 발급번호·제목·처리기간 한 줄 배치, 납세자 라벨 통일(상호(법인명)·성명(대표자)·주소(본점)), 사용목적 체크항목 [대금 수령/해외이주/기타], 폐지된 가산금 열 삭제 후 연장ㆍ유예 명세로 변경, 증명문구를 국세징수법 제108조·시행령 제95조 및 물적납세의무 문구로 교체 |
| 납세증명서(법인) | `tax_payment_certificate_corp` | 국세징수법 시행규칙 [별지 제94호서식], 국세청 민원사무처리규정 [별지 제21호서식](영문) 문구 대조 ([국세청 영문서식](https://www.law.go.kr/LSW//flDownload.do?flSeq=155626775), [정부24](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=12100000011)) | 반영(검색근거) | 개인용과 같은 별지 제94호서식 템플릿 공유, 법인등록번호를 주민등록번호(법인등록번호) 칸에 표시, 사용목적 체크항목·증명문구 동일 반영 |
| 지방세 납세증명서 | `local_tax_payment_certificate` | 지방세징수법 시행규칙 제2조·[별지 제1호서식] 지방세 납세증명(신청)서, 지방세징수법 제5조·시행령 제6조 ([정부24](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=13100000056), [창원시 민원편람](https://cwg.go.kr/www/selectMinwonWebView.do?deptCode=&key=55&minwonNo=234)) | 반영(검색근거) | 발급번호·제목·처리기간 한 줄 배치, 납세자에 상호·사업자등록번호 칸 추가(개인사업자면 값 표시), 라벨을 성명(법인명)·주소(영업소)·증명서 사용목적으로 정정, 2024년 폐지된 가산금 열 삭제, 증명문구를 징수유예등 또는 체납처분유예액 제외 문구로 정리 |
| 지방세 세목별 과세증명서 | `local_tax_assessment` | 지방세기본법 시행규칙 제33조·[별지 제49호서식] <개정 2024. 12. 31.> (국·영문 병기) ([법령 서식 파일](https://www.law.go.kr/flDownload.do?gubun=&flSeq=147966739&bylClsCd=110202), [정부24](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=13100000084)) | 반영(검색근거) | 서식번호를 별지 제5호에서 제49호로 정정, 제목·항목에 영문 병기(Issuance Number·Taxpayer·Tax Objects 등), 납세자 라벨을 주민(법인, 외국인)등록번호·주소(영업소)로 정정, 과세내역 열을 세목·부과연월·구분(정기분/1기분 등)·과세대상 순으로 재구성, 과세연도는 실제 내역 범위로 표시 |
| 부가가치세 과세표준증명 | `vat_tax_base_certificate` | 국세청 민원사무처리규정 [별지 제9호서식] 부가가치세과세표준증명(과ㆍ면세겸영사업자 포함) (2020. 11. 1. 개정) ([법령 서식 파일](https://www.law.go.kr/LSW//flDownload.do?flSeq=140436491), [정부24](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=12100000331)) | 반영(검색근거) | 서식 근거줄·부제(과ㆍ면세겸영사업자 포함) 추가, 납세자 항목을 성명(대표자)·주민(법인)등록번호·상호(법인명)·사업자등록번호·업태·종목 순으로 정리, 서식에 없는 과세유형·증명기간 삭제, 신고내용을 과세기간(시작~종료일)·신고구분·신고일·매출과세표준(계/과세분/면세수입금액)·납부할 세액(환급받을 세액)으로 재구성, 학원·농산물은 면세 매출이 대부분인 겸영사업자로 생성, 증명문구 위와 같이 증명합니다로 정정 |
| 종합소득세 과세표준확정신고 및 납부계산서 | `income_tax_return` | 소득세법 시행규칙 [별지 제40호서식(1)] (35쪽 중 제1쪽), 개정 2023.3.20·2024.3.22·2025.3.21·2026.3.20 ([2025년 서식](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=157666253&bylClsCd=110202), [국세청 주요서식](https://www.nts.go.kr/nts/na/ntt/selectNttList.do?mi=2240&bbsId=30683)) | 반영(검색근거) | 제목을 종합소득세ㆍ농어촌특별세 과세표준확정신고 및 납부계산서로 정정, 관리번호·거주구분·내ㆍ외국인·거주지국 칸 추가, ❶기본사항(①~⑩, 신고유형·기장의무·신고구분 코드 체크), ❷환급금 계좌신고(⑪⑫), ❸세액의 계산(⑲~㉟, 종합소득세/농어촌특별세 열) 구조로 재편, 1쪽에 없는 상호·사업장·소득별 금액·소득공제 명세와 지방소득세 열 삭제, 국세기본법 조문 포함 신고문구·세무대리인 확인란 추가, 개정일은 신고연도에 맞춰 표시 |

## 금융거래

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 통장사본 | `bankbook_copy` | 법정서식 없음, 통장 표지(첫 면) 사본 및 인터넷뱅킹 통장사본(통장표지) 출력 ([은행별 통장사본 출력](https://0muwon.com/entry/%EA%B5%AD%EB%AF%BC%EC%9D%80%ED%96%89-%EC%9A%B0%EB%A6%AC%EC%9D%80%ED%96%89-%EB%86%8D%ED%98%91-%ED%86%B5%EC%9E%A5-%EB%93%B1-%EC%9D%80%ED%96%89%EB%B3%84-%ED%86%B5%EC%9E%A5%ED%91%9C%EC%A7%80-%ED%86%B5%EC%9E%A5%EC%82%AC%EB%B3%B8-%EC%B6%9C%EB%A0%A5%EB%B0%A9%EB%B2%95), [하나은행 FAQ](https://kebhana.com/cont/customer/customer01/index,1,list,24.jsp)) | 반영(검색근거) | 인터넷 출력본을 증명서형(확인 문구·은행 직인)에서 통장 표지형(은행명·상품명·계좌번호·예금주 님·신규일·관리점, 출력일)으로 변경, 스캔본의 임의 문구(원본대조필) 삭제 |
| 거래내역확인서 | `bank_statement` | 법정서식 없음, 은행별 거래내역확인서·입출금거래내역서 통용 형식 ([거래내역확인서 출력](https://jab-guyver.co.kr/244), [국민은행 거래내역서](https://laystory.com/entry/%EA%B5%AD%EB%AF%BC%EC%9D%80%ED%96%89-%EC%9E%85%EC%B6%9C%EA%B8%88-%EA%B1%B0%EB%9E%98%EB%82%B4%EC%97%AD%EC%84%9C-%EB%B0%9C%EA%B8%89-%EB%B0%A9%EB%B2%95-%EC%A0%95%EB%A6%AC/)) | 반영(검색근거) | 열을 은행 통용 표기(거래일시·적요·기재내용·찾으신금액·맡기신금액·거래후잔액)로 변경: 거래구분은 적요(type), 상대방은 기재내용(memo)으로 분리하고 거래점 열 삭제, 적요 값(타행입금·자동이체·체크카드·CD출금·결산 등) 정리 |
| 잔액증명서 | `balance_certificate` |  | 조사중 |  |
| 부채증명서 | `debt_certificate` |  | 대기 |  |
| 신용카드 이용대금명세서 | `card_statement` |  | 대기 |  |

## 부동산

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 등기사항전부증명서(집합건물) | `real_estate_registry` | 인터넷등기소 등기사항전부증명서(집합건물) 출력 양식, 주요 등기사항 요약(참고용). [easylaw 구분건물 보존등기](https://www.easylaw.go.kr/CSP/CnpClsMainBtr.laf?popMenu=ov&csmSeq=566&ccfNo=2&cciNo=3&cnpClsNo=1), [요약본 PDF 예시](https://leadingplusfunding.com/file/prodProof/A000001669/20250106/20250106094656641MTczMi5wZGY.pdf) | 반영(검색근거) | 1동 표시에 도로명주소 변경(1번 소재지 실선 말소, 2번 도로명주소) 행 구성. 상단 [인터넷 발급] 위변조 안내문·열람용 효력 문구, 하단 발행번호·발급확인번호(XXXX-XXXX-0000)·발행일·쪽번호 및 바코드 자리 추가. 수수료·관할등기소·발행등기소 줄과 인증문 순서 정리. 약 18%는 주요 등기사항 요약(참고용) 페이지(소유지분현황·을구 요약·참고사항)로 생성. |
| 집합건축물대장(전유부) | `building_register` | 건축물대장의 기재 및 관리 등에 관한 규칙 [별지 제5호서식] <개정 2021. 7. 12.> 집합건축물대장(전유부, 갑), 297mm×210mm. [law.go.kr 서식](https://law.go.kr/flDownload.do?flSeq=106887043), [yesform](https://www.yesform.com/wdata/doc-1069707.php) | 반영(검색근거) | 서식번호를 별지 제4호→제5호(개정 2021.7.12.)로 정정, 쪽수 (3쪽 중 제1쪽)·장번호 추가. A4 가로(297×210) 배치로 변경하고 좌측 전유부분·공용부분, 우측 소유자현황·공동주택(아파트)가격 2단 구성. 소유자현황 성명/등록번호·변동일/변동원인 2단 표기, 하단 담당자·전화·용지규격 줄 정리. |
| 토지대장 | `land_register` | 공간정보의 구축 및 관리 등에 관한 법률 시행규칙 제68조, [별지 제63호서식] 토지대장. [moleg 입법예고](https://www.moleg.go.kr/lawinfo/makingInfo.mo?mid=a10104010000&lawSeq=78592&lawCd=0&lawType=TYPE5), [정부24 토지(임야)대장 발급](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=13100000026) | 반영(검색근거) | 서식번호(별지 제63호) 확인, 기존 구조 유지. 개별공시지가 표시 연수를 5~7년(정부24 기본 최근 7년)으로 확대, 소유권보존 변동원인 코드 통일, 토지표시·소유자 표에 빈 행을 넣어 실제 서식처럼 고정 틀 형태로 채움, 발급자 값에서 폐지된 민원24 제거. |
| 부동산 매매계약서 | `sales_contract` | 한국공인중개사협회 부동산(아파트) 매매계약서 양식(협회 서식 자료실). [kar.or.kr 부동산관련서식](http://www.kar.or.kr/pinfo/realtyformlist.asp), [easylaw 매매계약서 작성](https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=649&ccfNo=3&cciNo=2&cnpClsNo=1) | 반영(검색근거) | 협회 양식의 융자금·임대보증금 승계 행 추가, 맺음 문구를 간인·각 1통 보관 문장으로 교체하고 계약일을 별도 줄에 표기. 매도인·매수인별 대리인 행 추가, 개업공인중개사란을 공동중개 2단(사무소소재지·명칭·대표·등록번호·전화·소속공인중개사) 구성으로 변경(약 35% 공동중개). 원문 대조는 못 함. |
| 주택임대차표준계약서 | `lease_contract` | 법무부·국토교통부 주택임대차표준계약서(2023. 10. 6. 개정). [법무부 개정 표준계약서 안내](https://www.immigration.go.kr/bbs/moj/118/575868/artclView.do), [법무부 표준계약서 PDF](https://www.moj.go.kr/sites/moj/download/210818_01.pdf) | 반영(검색근거) | 2023 개정 반영: 계약의 종류에 계약갱신요구권 갱신계약 문구, 미납 국세·지방세·선순위 확정일자 칸에 없음/있음(확인·설명서 ⑨ 기재) 선택지, 관리비(정액/비정액 산정방식) 행 추가. 차임 행을 빈 양식으로 바꾸고 GT에서 제외. 제10조 장기수선충당금 반환 문구 보강, 특약에 표준 담보권 설정 제한·해제 문구와 개정 권고 특약(선순위·체납 미고지 시 위약금 없는 해제) 반영. 대리인 행·공동중개 2단 중개사란 추가, 한 장에 맞게 글자 크기 고정. |
| 전입세대확인서 | `move_in_household_list` | 주민등록법 시행규칙 [별지 제15호의2서식] <개정 2023. 12. 22.> 전입세대확인서 (신청서는 별지 제15호서식). [law.go.kr 서식](https://www.law.go.kr/flDownload.do?gubun=&flSeq=136503763&bylClsCd=110202), [신청서 서식](https://www.law.go.kr/flDownload.do?gubun=&flSeq=136503755&bylClsCd=110202) | 반영(검색근거) | 서식번호를 신청서 번호(제15호)에서 확인서 번호(제15호의2, 개정 2023.12.22.)로 정정. 상단 발급번호·발급일자 칸, 열람/교부 구분 추가. 2023 개정의 동거인 사항(순번·성명·전입일자·등록구분) 표 추가, 동거인 수를 대부분 0으로 현실화. 안내문 정리. |

## 개인사업자

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 사업자등록증 | `business_registration_certificate` | 부가가치세법 시행규칙 [별지 제7호서식(1)] 사업자등록증(개인) ([2014 서식 파일](https://www.law.go.kr/LSW/flDownload.do?flSeq=97706403), [찾기쉬운생활법령](https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=25&ccfNo=2&cciNo=1&cnpClsNo=1)) | 반영(검색근거) | 기존 항목 순서(상호·성명·생년월일·개업연월일·사업장소재지·사업의종류·발급사유·공동사업자·사업자단위과세·전자세금계산서 전용 전자우편주소)가 서식과 일치함을 확인, 항목명 균등배분(상 호 등) 적용, 날짜를 실물 표기(2020 년 01 월 05 일) 위주로 변경 |
| 사업자등록증(법인사업자) | `business_registration_certificate_corp` | 부가가치세법 시행규칙 [별지 제7호서식(2)] 사업자등록증(법인사업자) ([부가가치세법 시행규칙](https://law.go.kr/LSW/lsRvsDocListP.do?lsId=007289&chrClsCd=010202&lsRvsGubun=all), [삼일 별지서식](https://www.samili.com/tax/SeosikList2.asp?Code=54-13:3)) | 반영(검색근거) | 항목 순서(법인명(단체명)·대표자·개업연월일·법인등록번호·사업장소재지·본점소재지·사업의종류·발급사유·사업자단위과세·전자우편주소) 유지 확인, 항목명 균등배분, 날짜 실물 표기 적용 |
| 사업자등록증명 | `business_registration_proof` | 국세청 민원사무처리규정 [별지 제5호서식] 사업자등록증명 (영문 제6호) ([정부24](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=12100000016), [삼일 민원사무처리규정 서식](https://www.samili.com/tax/SeosikList.asp?Code=3618-13:1)) | 반영(검색근거) | 서식 근거줄(민원사무처리규정 제5호) 추가, 발급번호·제목·처리기간 한 줄 배치, 납세자/등록사항 묶음 표로 재배치, 라벨을 주민(법인)등록번호·성명(대표자) 등 민원증명 표기로 정리, 증명문구 위와 같이 증명합니다로 정정 |
| 표준재무제표증명 | `standard_financial_statement_proof` | 국세청 민원사무처리규정 [별지 제13호서식] 표준재무제표증명(국문) (2024. 4. 17. 개정) ([법령 서식 파일](https://www.law.go.kr/LSW//flDownload.do?flSeq=140436515), [정부24](https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=12100000326)) | 반영(검색근거) | 서식 근거줄·개정일 추가, 제목 아래 □개인 □법인 체크, 납세자 항목을 상호(법인명)·사업자등록번호·성명(대표자)·주민(법인)등록번호·업태·종목·사업장 순으로 정리, 사업연도·신고구분·첨부서류·신고일 추가(신고일은 종합소득세 신고서와 같은 날짜), 서식에 없는 귀속연도·사용목적·제출처 삭제, 증명문구를 붙임의 표준재무제표는 … 같음을 증명합니다로 교체, 재무제표는 붙임으로 배치 |

## 법인

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 법인 등기사항전부증명서(현재 유효사항) | `corporate_registry` |  | 대기 |  |
| 정관 | `articles_of_incorporation` |  | 대기 |  |
| 주주명부 | `shareholder_registry` |  | 대기 |  |
| 재무제표(재무상태표·손익계산서) | `financial_statements` |  | 대기 |  |
| 법인인감증명서 | `corporate_seal_certificate` |  | 대기 |  |
| 이사회의사록 | `board_minutes` |  | 대기 |  |
| 임시주주총회의사록 | `shareholders_meeting_minutes` |  | 대기 |  |
| 위임장 | `power_of_attorney` |  | 대기 |  |

## 외환·무역

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 상업송장(Commercial Invoice) | `commercial_invoice` |  | 조사중 |  |
| 무역 매매계약서(Sales Contract) | `trade_contract` |  | 대기 |  |
| 선하증권(B/L) | `bill_of_lading` |  | 대기 |  |
| 포장명세서(Packing List) | `packing_list` |  | 대기 |  |
| 수입신고필증 | `import_declaration` |  | 대기 |  |
| 입학허가서(Letter of Admission) | `admission_letter` |  | 대기 |  |
| 학비 청구서(Tuition Invoice) | `tuition_invoice` |  | 대기 |  |

## 은행 서식

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 대출거래신청서 | `loan_application` |  | 대기 |  |
| 기업여신 신청서 | `loan_application_corp` |  | 대기 |  |
| 여신거래약정서(가계용) | `credit_agreement` |  | 대기 |  |
| 여신거래약정서(기업용) | `credit_agreement_corp` |  | 대기 |  |
| 근저당권설정계약서 | `collateral_agreement` |  | 대기 |  |
| 보증약정서 | `guarantee_agreement` |  | 대기 |  |
| 자동이체 신청서 | `auto_transfer_application` |  | 대기 |  |
| 고객확인서(개인) | `customer_due_diligence` |  | 대기 |  |
| 고객확인서(법인·단체) | `corporate_customer_due_diligence` |  | 대기 |  |
| 개인(신용)정보 수집·이용·제공·조회 동의서 | `privacy_consent` |  | 대기 |  |
| 예금거래신청서 | `account_opening_application` |  | 대기 |  |
| 금융거래목적확인서 | `financial_transaction_purpose` |  | 대기 |  |
| 해외송금신청서 | `overseas_remittance_application` |  | 대기 |  |
| 해외금융계좌 납세자 확인서(개인) | `fatca_crs` |  | 대기 |  |
