# 서식 현실화 — bank_account

| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |
|---|---|---|---|---|
| 고객확인서(개인) | `customer_due_diligence` | 특정금융정보법 제5조의2, 은행 고객거래확인서(개인·개인사업자용) 관행 ([신한 고객거래확인서](http://img.shinhan.com/nexhpe/download/ftpfile/data0/20121022182213_remotebusiness_06.pdf), [IBK저축은행 서식](https://www.ibksb.co.kr/download/1478183165)) | 반영(검색근거) | 제목을 고객거래확인서(개인·개인사업자용)로 변경, 구분(내국인/재외국민/외국인)·성별 추가, 직업 9종 및 급여소득자(직장명·부서/직위·업종·직장전화)/개인사업자(상호·사업자번호·업태/종목·개업일) 구분, 거래목적 8종·자금원천 9종 실제 선택지로 확장, 실제소유자 미해당 시 기재란, 하단 서식번호 줄 |
| 고객확인서(법인·단체) | `corporate_customer_due_diligence` | 특정금융정보법 시행령 제10조의5(실제소유자 3단계), 금융사 고객거래확인서(법인/단체) ([하나카드 KYC 서식](https://www.hanacard.co.kr/ATTACH/WWW/pdf/inhabit/kyc.pdf), [DB생명 서식](https://www.idblife.com/assets/Guide_owner_241212.pdf)) | 반영(검색근거) | 제목을 고객거래확인서(법인·단체용)로 변경, 법인구분을 대기업/중소기업/국가·지자체·공공단체/금융기관/비영리/외국법인 6종으로, 설립목적(비영리 필수)란 추가, 실제소유자 1~3단계 정의 문구를 시행령 문언에 맞춤, 실제소유자 지분율 내림차순 정렬, 하단 서식번호 줄 |
| 개인(신용)정보 수집·이용·제공·조회 동의서 | `privacy_consent` | 금융권 표준 개인(신용)정보 동의서(여신 금융거래 필수/선택) ([카카오뱅크 여신 필수동의](https://og.kakaobank.io/download/d0dbab62-97a5-4587-af47-7ce9762b94d8), [하나저축은행 여신 필수동의](https://www.hanasavings.com/html/loan/sunshine/Terms2_sunshine.html), [하나은행 5-06-0753](https://image.kebhana.com/cont/download/documents/provide/5006008760000_20181026.pdf)) | 반영(검색근거) | 표준서식 순서(목적→보유·이용기간→거부권리·불이익→항목)로 재배열, 항목을 개인식별·신용거래·신용능력·신용도판단·공공정보로 정리, 고유식별정보를 수집 표에 통합, 동의 문구를 '위 ...에 동의하십니까?' 형식으로, 제공표 열 제목을 '제공받는 자의 이용 목적/제공하는 항목/보유·이용 기간'으로, 신용조회회사→개인신용평가회사, 한국신용정보원 이용목적 문구, '필수 동의만으로 계약 체결 가능' 문구 추가, 상단 은행 귀중 |
| 예금거래신청서 | `account_opening_application` | 은행 자체 서식(공통 항목), 금융실명법 제3조 제3항 차명거래 금지 설명의무, 예금자보호법 시행령(2025.9.1. 1억원) ([금융위 보도자료](https://www.fsc.go.kr/no010101/84974), [easylaw 금융실명거래](https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=1771&ccfNo=2&cciNo=1&cnpClsNo=1)) | 반영(검색근거) | 차명거래 금지 설명 확인란(법정 문구+확인자 서명) 추가, 예금자보호 문구를 표준 안내문(1인당 원금+소정이자, 여타 보호상품 합산)으로 바꾸고 작성일 기준 한도(2025.9.1. 전 5천만원/이후 1억원)를 GT 필드로, 주택청약종합저축은 비보호 문구, 정기예금 이자지급방법 추가 |
| 금융거래목적확인서 | `financial_transaction_purpose` | 전기통신금융사기 피해 방지 및 피해금 환급에 관한 특별법(2024.8.28. 목적확인 의무화), 은행 금융거래목적확인서 ([KB 증빙서류 안내](https://kbthink.com/fraud/transaction-purpose-docs.html), [하나은행 안내문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2024/08/29/240827-0283_1.pdf), [한도계좌 100만원 상향](https://www.korea.kr/multi/visualNewsView.do?newsId=148928795)) | 반영(검색근거) | 거래목적 선택지를 급여계좌/사업자 거래/공과금 이체/모임 회비/아르바이트/기타로, 증빙서류를 목적별 실제 서류명 자유기재로 바꾸고 목적별 증빙서류 예시표(발급 3개월 이내) 추가, 법적 근거 안내문 교체, 글자 밀도 조정 |
| 해외송금신청서 | `overseas_remittance_application` |  | 조사중 |  |
| 해외금융계좌 납세자 확인서(개인) | `fatca_crs` |  | 대기 |  |

## 메모

