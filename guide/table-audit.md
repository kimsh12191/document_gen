# 표 점검 목록

<!-- 자동 생성 — python -m docgen.bench.table_audit --seeds 12 --out guide/table-audit.md -->

표(반복 묶음)의 정의와 질문은 [benchmark.md](benchmark.md#표의-정의). 이 목록은 사람이 보고 정할 것만 모읍니다 — 아무것도 고치지 않았습니다.
서식 545종 중 표가 있는 서식 214종, 표 묶음 328개 (seed 12개로 그려 봄).

| 점검 | 수 | 정할 것 | 고치는 곳 |
|---|---:|---|---|
| 행 수가 늘 같은 표 | 51 | 정해진 격자인가? 그러면 표가 아니라 kie | 서식 `questions.json` `{"table": {"<묶음>": {"ask": false}}}` |
| 오래된 순 표 (날짜 열) | 14 | 실서류도 오래된 순인가? 최신순이면 바꿈 | 그 서식 `generate.py` (행 순서) |
| 표 안 합계 열 | 9 | 합계는 표가 아니라 kie 칸 | 템플릿·`generate.py` 에서 합계를 행 밖 키로 |
| 번호를 이름에 붙인 반복 칸 | 326 | 반복 레코드면 표로 | 키를 `<묶음>.0.<열>` 꼴로 (템플릿·`fields.json`) |
| 겹친 목록 | 3 | 묻지 않음 (그대로 둬도 됨) | — |

## 행 수가 늘 같은 표

| 서식 | 묶음 | 행 | 열 |
|---|---|---:|---|
| `building_register` 집합건축물대장(전유부) | `exclusive` | 1 | kind(구분), floor(층별), structure(구조), usage(용도), area(면적(㎡)) |
| `card_statement` 신용카드 이용대금명세서 | `fee_per_100` | 5 | months(할부개월), fee(100원당수수료) |
| `hana_official_006` 자동이체 신청서 | `목록` | 2 | 예금주명, 이체일, 이체주기(이체주기(일☞주☞월☞년)), 이체금액 |
| `hana_official_011` 예금(신탁)잔액증명 의뢰서 | `계좌번호_목록` | 0 | value((통화코드:)) |
| `hana_official_052` \[필수\] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택전월세자금대출용) | `목록` | 0 | 공공정보등(■공공정보등) |
| `hana_official_053` \[필수\] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택구입자금대출용) | `목록` | 0 | 공공정보등(■공공정보등) |
| `hana_official_408` 본인확인서(FATCA CRS 개인,개인사업자용)(국문) | `tax.residence_list` | 2 | country(거주관할권*(1)), tin(납세자번호(TIN)) |
| `hf002` 은행거래신청서(영문) | `목록` | 0 | FixedFloating(FixedFloating(mth)) |
| `hf003` 은행거래신청서 | `deposit_list` | 3 | interest_account(통장발행), tax_free_limit(연원가식), product(상품명1), amount(가입금액1), period(계약기간1), transfer_amount(이체금액1) … |
| `hf003` 은행거래신청서 | `목록` | 0 | 갋 |
| `hf003` 은행거래신청서 | `redeposit_list` | 3 | product(\[신청상품\]1) |
| `hf011` 예금(신탁)잔액증명 의뢰서 | `계좌번호_목록` | 0 | value((통화코드:)) |
| `hf031` 국내원천소득 제한세율 적용신청서(외국법인용) | `목록` | 0 | 예, 아니오 |
| `hf032` 국내원천소득 제한세율 적용신청서(비거주자용) | `목록` | 0 | 예, 아니오 |
| `hf052` \[필수\] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택전월세자금대출용) | `목록` | 0 | 공공정보등(■공공정보등) |
| `hf053` \[필수\] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택구입자금대출용) | `목록` | 0 | 공공정보등(■공공정보등) |
| `hf102` 기업현황서(B2B전자결제서비스 업무, MP용) | `요약재무현황_목록` | 0 | 년 |
| `hf102` 기업현황서(B2B전자결제서비스 업무, MP용) | `주요경력_목록` | 0 | 기간, 근무처, 담당업무, 최종직위 |
| `hf151` 《기업》무역어음인수·할인신청서 | `목록` | 0 | 월, 일 |
| `hf154` 차입신청서(무역금융용) | `무역금융신청건포함명세_목록` | 0 | 당행, 타행 |
| `hf154` 차입신청서(무역금융용) | `운전자금_목록` | 0 | 당행, 타행 |
| `hf154` 차입신청서(무역금융용) | `시설자금_목록` | 0 | 당행, 타행 |
| `hf154` 차입신청서(무역금융용) | `지급보증_목록` | 0 | 타행 |
| `hf177` 퇴직연금 운용상품지정 신청서(DC) | `정기예금_목록` | 0 | 년 |
| `hf183` 퇴직연금 통지서비스 신청서(가입자용) | `목록` | 0 | 은행사용란 |
| `hf205` 외국환거래법시행령상 거주성확인서 | `국민_목록` | 0 | 아니오(아니오(NO)) |
| `hf205` 외국환거래법시행령상 거주성확인서 | `외국인_목록` | 0 | 아니오(아니오(NO)) |
| `hf206` 연간사업실적보고서(투자잔액 1,000만불 초과 기업) | `대부투자_목록` | 0 | 금기말 |
| `hf206` 연간사업실적보고서(투자잔액 1,000만불 초과 기업) | `지분율10미만_목록` | 0 | 금기말 |
| `hf216` 해외부동산 취득신고(수리)서 | `국내송금액_목록` | 0 | 미달러환산액 |
| `hf216` 해외부동산 취득신고(수리)서 | `현지조달액_목록` | 0 | 미달러환산액 |
| `hf217` 해외직접투자 내용변경 신고(보고)서 | `목록` | 2 | 변경후 |
| `hf223` 「외국환서식관리프로그램」전자무역업무이용(신규,변경,해지)신청서 | `신청인_목록` | 0 | 수발신인식별자, 상세수발신식별자, 전자문서인증키 |
| `hf236` 해외예금 및 신탁 잔액 보고서 | `목록` | 1 | 금액 |
| `hf294` 「외국환서식관리프로그램」선적서류 (일부)매입(추심) 의뢰서(2D용) | `TOISSUINGBANK_목록` | 0 | BENE, BANK, COMM, CUST, BL(B/L), AWB … |
| `hf297` 단기수출보험(수출채권유동화) 청약 확인서 | `주소_목록` | 0 | 대표자 |
| `hf318` 대북투자(변경)신고서 | `목록` | 0 | 대부투자, 총투자액 |
| `hf323` 북한지점 경비지급신고서 | `비독립채산지점_목록` | 0 | value((주소)(전화번호)(e-mail)) |
| `hf340` 기업 전자금융서비스 신청서(은행용) | `입금계좌지정신청신청안함_목록` | 0 | 해외IP차단 |
| `hf353` CMS Plus 이용신청서(지사) | `이체한도_목록` | 0 | value((영문+숫자혼합6~10자리)) |
| `hf356` CMS Plus 이용신청서 | `맞춤서비스_목록` | 0 | value((맞춤기능또는시스템연계내용)) |
| `hf356` CMS Plus 이용신청서 | `이체한도_목록` | 0 | value((영문+숫자혼합6~10자리)) |
| `hf368` 가상계좌서비스 이용계약서(외화) | `목록` | 0 | 예금주 |
| `hf378` 글로벌뱅킹서비스 이용,변경,해지 신청서 | `해외주소OverseasAddress_목록` | 0 | 직장Company |
| `hf380` 금융결제원CMS 이용계약서 | `목록` | 0 | 예금주명 |
| `hf408` 본인확인서(FATCA CRS 개인,개인사업자용)(국문) | `tax.residence_list` | 2 | country(거주관할권*(1)), tin(납세자번호(TIN)) |
| `hf421` \[필수\] 개인(신용)정보 수집·이용·제공·조회 동의서 \[비대면 계좌개설 안심차단 서비스\] | `목록` | 0 | 고유식별정보(■고유식별정보), 공공정보등(■공공정보등) |
| `hf422` \[필수\] 개인(신용)정보 수집·이용·조회 동의서\[비대면 계좌개설 안심차단 신청여부 조회용\] | `목록` | 0 | 고유식별정보(■고유식별정보) |
| `hf431` 전자금융거래 사고 피해 신고서(통합서류) | `목록` | 0 | 출입국사실증명원또는여권사본 |
| `land_register` 토지대장 | `grades` | 3 | date(등급수정년월일), grade(토지등급) |
| `privacy_consent` 개인(신용)정보 수집·이용·제공·조회 동의서 | `providers` | 3 | name(제공받는자), purpose(제공받는자의이용목적), items(제공하는항목), period(제공받는자의보유이용기간) |

## 오래된 순 표

날짜 열이 있는 3행 이상 표가 모든 seed 에서 오래된 순. 이력·내역 표는 실서류가 최신순인 경우가 많습니다 (예: 건강보험 자격득실확인서는 고침).

| 서식 | 묶음 | 행 | 열 |
|---|---|---|---|
| `articles_of_incorporation` 정관 | `revision_effective` | 1~7 | value(시행일) |
| `bank_statement` 거래내역확인서 | `rows` | 13~48 | datetime(거래일시), type(적요), memo(기재내용), out(찾으신금액), in(맡기신금액), balance(거래후잔액) |
| `bankbook_copy` 통장사본 | `txs` | 0~4 | date(거래일), memo(적요), in(맡기신금액), balance(잔액), out(찾으신금액) |
| `building_register` 집합건축물대장(전유부) | `owners` | 1~6 | name(성명(명칭)), rrn(주민(법인)등록번호), address(주소), share(소유권지분), change_date(변동일), change_cause(변동원인) |
| `card_statement` 신용카드 이용대금명세서 | `rows` | 11~108 | date(이용일자), merchant(이용하신가맹점), amount(이용금액), months(할부), seq(회차), principal(원금) … |
| `corporate_registry` 법인 등기사항전부증명서(현재 유효사항) | `branches` | 0~3 | no(지점번호), address(지점소재지), opened(설치일), opened_registered(등기일), closed(폐지일), closed_registered(등기일) |
| `health_insurance_payment` 건강보험료 납부확인서 | `rows` | 6~35 | month(년월), notice_health(고지보험료(건강보험)), notice_ltc(고지보험료(장기요양)), health(납부보험료(건강보험)), ltc(납부보험료(장기요양)), total(납부보험료(계)) … |
| `land_register` 토지대장 | `owners` | 2~7 | change_date(변동일자), change_cause(변동원인), address(주소), name(성명또는명칭), reg_no(등록번호), co_owners(공유자) |
| `land_register` 토지대장 | `land_prices` | 5~7 | base_date(개별공시지가기준일), price(개별공시지가) |
| `pension_enrollment_certificate` 국민연금 가입자 가입증명 | `rows` | 1~19 | kind(가입자종류), workplace(사업장명칭), start(자격취득일), end(자격상실일), wage(기준소득월액), note(비고) |
| `resident_registration_abstract` 주민등록표 초본 | `addresses` | 1~25 | no(번호), address(주소), moved_in(전입일), changed(변동일), head_relation(세대주및관계), status(등록상태) … |
| `resident_registration_copy` 주민등록표 등본 | `past_addresses` | 0~19 | no(번호), address(주소), moved_in(전입일/변동일), reason(변동사유) |
| `tuition_invoice` 학비 청구서(Tuition Invoice) | `installments` | 0~5 | no(InstallmentNo), due_date(InstallmentDueDate), amount(InstallmentAmount) |
| `vat_tax_base_certificate` 부가가치세 과세표준증명 | `items` | 4~9 | period(과세기간), kind(신고구분), filed(신고일), base_total(매출과세표준계), base_taxable(과세분), base_exempt(면세수입금액) … |

## 표 안 합계 열

| 서식 | 묶음 | 합계 열 |
|---|---|---|
| `hf082` 채권발행 등록 신청서 | `목록` | 세금계산서합계금액 |
| `hf094` 상생벤더구매론 승인명세 등록신청서 | `목록` | 세금계산서합계금액 |
| `hf099` 지급승인명세 등록 신청서 | `목록` | 세금계산서합계금액 |
| `hf153` 《기업》질권설정등록청구서 | `목록` | 총액 |
| `hf206` 연간사업실적보고서(투자잔액 1,000만불 초과 기업) | `목록` | 계 |
| `hf207` 연간사업실적보고서(투자잔액 300만불 초과 1,000만불 이하 기업) | `목록` | 계 |
| `hf252` 외국환 신고(확인)필증 | `휴대_목록` | 합계Sum |
| `hf252` 외국환 신고(확인)필증 | `목록` | 합계Sum |
| `local_tax_assessment` 지방세 세목별 과세증명서 | `items` | total |

## 번호를 이름에 붙인 반복 칸

`N` 자리에 번호가 붙은 키들 (예: `guarantorN.name` = guarantor1.name, guarantor2.name …).

| 서식 | 키 |
|---|---|
| `gov_business_registration` 사업자등록증 | `official.annex_biz_noN`, `official.annex_issueN`, `official.issueN`, `official.openedN` |
| `gov_income` 소득금액증명 | `official.issueN` |
| `hana_corporate_agreement` 여신거래약정서(기업용) | `terms.endN`, `terms.startN`, `terms.writtenN` |
| `hana_official_001` 상속예금 명의변경(지급) 의뢰서 및 손해담보 확약서(상속예금 지급 위임장 겸용) | `signerN.name` |
| `hana_official_006` 자동이체 신청서 | `accountN`, `dateN`, `은행N`, `입금인자내용N`, `지급인자내용N` |
| `hana_official_011` 예금(신탁)잔액증명 의뢰서 | `accountN`, `발급부수N` |
| `hana_official_015` 통합제신고서 | `signerN.name` |
| `hana_official_024` 금융거래정보제공(요구·동의)서 | `customer.birthN`, `customer.phoneN`, `signerN.name` |
| `hana_official_028` 위임장 | `customer.addressN` |
| `hana_official_047` 대출상담 및 신청서(한국주택금융공사채권유동화목적 보금자리론용) | `customer.addressN`, `customer.nameN`, `customer.phoneN`, `customer.rrnN`, `dateN`, `employer.nameN`, `signerN.name`, `근무기간N` … |
| `hana_official_048` 가계형소호 여신차입신청서 | `company.addressN`, `dateN`, `signerN.name` |
| `hana_official_049` 《개인》대출신청서(가계용) | `customer.nameN`, `dateN`, `signerN.name` |
| `hana_official_051` 대출계약 철회신청서 | `dateN`, `signerN.name` |
| `hana_official_052` \[필수\] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택전월세자금대출용) | `signerN.name` |
| `hana_official_053` \[필수\] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택구입자금대출용) | `signerN.name` |
| `hana_official_054` 주택도시기금 대출 신청서(가계용) | `customer.addressN`, `customer.nameN`, `customer.phoneN`, `월세보증금N`, `월임대료N`, `전세보증금N` |
| `hana_official_055` 주택도시기금 대출상담 및 신청서(내집마련 디딤돌 대출용) | `customer.addressN`, `customer.phoneN`, `방수N`, `배우자N`, `본인N` |
| `hana_official_058` 융자상담 및 차입신청서(기업용) | `company.addressN`, `customer.emailN`, `customer.phoneN` |
| `hana_official_059` 개인(신용)정보 조회 동의서 | `signerN.name`, `이용목적N`, `일반개인정보N` |
| `hana_official_060` \[필수\] 개인(신용)정보 수집이용 동의서(대출성상품 적합성적정성 판단용) | `signerN.name` |
| `hana_official_061` 적합성, 적정성 고객정보 확인서(개인 및 개인사업자용) | `signerN.name` |
| `hana_official_062` 적합성, 적정성 고객정보 확인서(법인용) | `signerN.name` |
| `hana_official_065` 국토교통부 주택소유확인 시스템 등 이용 관련 \[필수\] 개인(신용)정보 수집·이용·제공 동의서 | `signerN.name`, `일반개인정보N` |
| `hana_official_118` \[필수\] 개인(신용)정보 수집·이용·제공_동의서\[가계여신_금융거래\] | `signerN.name`, `공공정보등N` |
| `hana_official_128` 필수 개인(신용)정보 수집, 이용 및 제공 동의서(소호여신) | `signerN.name`, `공공정보등N` |
| `hana_official_129` 필수 개인(신용)정보 수집, 이용 및 제공 동의서(법인여신) | `signerN.name`, `공공정보등N` |
| `hana_official_138` 대출금 수령위임동의서 | `signerN.name` |
| `hana_official_139` 《기업》 지급보증거래 신청서(서면.전자 지급보증 겸용) | `dateN`, `signerN.name`, `피보증채무의종류N` |
| `hana_official_149` 《기업》금융거래확인서 | `signerN.name`, `연체발생일N` |
| `hana_official_157` 여신거래용 인감명판 등 신고서 | `signerN.name` |
| `hana_official_199` 외화송금신청서 | `dateN`, `signerN.name`, `신청인과의관계N`, `은행명N`, `은행코드N` |
| `hana_official_408` 본인확인서(FATCA CRS 개인,개인사업자용)(국문) | `dateN`, `signerN.name` |
| `hana_official_413` 고객확인서(법인,고유번호나 납세번호가 있는 임의 단체용) | `FAXN`, `customer.addressN`, `대표자N`, `전화N` |
| `hana_official_414` \[필수\] 개인(신용)정보 수집·이용·제공 동의서 \[공공마이데이터 주민등록 등·초본 조회용\] | `signerN.name`, `일반개인정보N` |
| `hana_official_416` \[필수\] 개인(신용)정보 수집·이용·제공 동의서 \[공공마이데이터 사업자정보 조회용\] | `signerN.name`, `고유식별정보N`, `일반개인정보N` |
| `hana_official_419` \[필수\] 개인(신용)정보 수집 · 이용 동의서 (비여신 금융거래) | `signerN.name` |
| `hana_official_420` 비대면 계좌개설 안심차단 서비스 신청서 | `signerN.name` |
| `hana_official_428` 본인확인서(FATCA CRS 법인,임의단체용)(국문) | `company.nameN`, `customer.birthN`, `customer.nameN`, `거주관할권주소N`, `성N`, `지분율N` |
| `hana_personal_agreement` 대출거래약정서(가계용) | `terms.endN`, `terms.startN`, `terms.writtenN` |
| `hf001` 상속예금 명의변경(지급) 의뢰서 및 손해담보 확약서(상속예금 지급 위임장 겸용) | `signerN.name` |
| `hf002` 은행거래신청서(영문) | `AccountItemN`, `AnnualN`, `ApplicantN`, `BankbookN`, `CategoryN`, `DateofOpeningN`, `EmployeeNumberN`, `HomeN` … |
| `hf003` 은행거래신청서 | `accountN`, `agent.nameN`, `bank.auto_transfer_accountN`, `bank.contract_amountN`, `bank.deposit_amountN`, `bank.first_trade_dateN`, `bank.kindN`, `bank.open_dateN` … |
| `hf006` 자동이체 신청서 | `accountN`, `dateN`, `은행N`, `입금인자내용N`, `지급인자내용N` |
| `hf009` 질권설정 승낙의뢰서(수신_제3자 질권용) | `customer.addressN`, `customer.birthN`, `customer.phoneN`, `signerN.name` |
| `hf010` 주식(사채)납입금 수납대행의뢰서(보관증명서 발급의뢰서 겸용) | `dateN` |
| `hf011` 예금(신탁)잔액증명 의뢰서 | `accountN`, `발급부수N` |
| `hf015` 통합제신고서 | `signerN.name` |
| `hf016` 종합금융상품 ON-LINE 거래 약정서 | `accountN`, `customer.nameN`, `signerN.name` |
| `hf017` 종합금융상품 ON-LINE_거래 (이체)신청서 | `accountN` |
| `hf018` 본인계좌 일괄지급정지 조회신청서 | `customer.nameN`, `dateN` |
| `hf020` 노무비닷컴계좌 개설 및 지급이체서비스 이용 신청서 | `customer.nameN` |
| `hf023` 하도급협력대금통장(상생결제 노무비) 지급이체서비스 이용신청서 | `customer.nameN` |
| `hf024` 금융거래정보제공(요구·동의)서 | `customer.birthN`, `customer.phoneN`, `signerN.name` |
| `hf025` 대여금고(신규·변경·해지)신청서 | `agent.addressN`, `agent.birthN`, `agent.phoneN`, `agent.relationN`, `signerN.name` |
| `hf026` \[필수\]개인(신용)정보 제3자 제공동의서(하나미소드림적금가입자용) | `signerN.name` |
| `hf028` 위임장 | `customer.addressN` |
| `hf030` 국내원천소득 제한세율 적용신청서(외국법인용-영문) | `customer.addressN` |
| `hf031` 국내원천소득 제한세율 적용신청서(외국법인용) | `거주지국의세법상납세의무가있습니까N`, `지급받는국내원천소득의실질귀속자입니까N` |
| `hf032` 국내원천소득 제한세율 적용신청서(비거주자용) | `signerN.name`, `가국내에주소를두고있습니까N`, `나국내에계속하여183일이상거주하고있습니까N`, `바대한민국의공무원입니까N` |
| `hf036` 예금(신탁) 이관 의뢰서 | `dateN`, `signerN.name` |
| `hf037` 위탁유가증권 반환청구서 | `dateN`, `signerN.name` |
| `hf042` 사채원리금 지급대행 계약서 | `dateN`, `signerN.name` |
| `hf043` 세금우대종합저축(비과세저축) 제변경신고서(비과세공용) | `customer.addressN`, `customer.birthN`, `signerN.name` |
| `hf044` 예금(신탁) 양도승낙 의뢰서 및 양도승낙서 | `accountN`, `customer.birthN`, `customer.nameN`, `dateN`, `deposit.amountN`, `deposit.due_dateN`, `deposit.productN`, `related.birthN` … |
| `hf045` 야간금고입금의뢰서 | `개N`, `매N`, `소계N`, `약속어음N`, `원N`, `천원권N` |
| `hf046` 목돈을 불리는 통장 거래신청서 | `dateN` |
| `hf047` 대출상담 및 신청서(한국주택금융공사채권유동화목적 보금자리론용) | `customer.addressN`, `customer.nameN`, `customer.phoneN`, `customer.rrnN`, `dateN`, `employer.nameN`, `signerN.name`, `근무기간N` … |
| `hf048` 가계형소호 여신차입신청서 | `company.addressN`, `dateN`, `signerN.name` |
| `hf049` 《개인》대출신청서(가계용) | `customer.nameN`, `dateN`, `signerN.name` |
| `hf050` \[필수\]개인(신용)정보 제3자 제공 동의서(토지분양대금 대출 약정_대구도시개발공사) | `signerN.name` |
| `hf051` 대출계약 철회신청서 | `dateN`, `signerN.name` |
| `hf052` \[필수\] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택전월세자금대출용) | `signerN.name` |
| `hf053` \[필수\] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택구입자금대출용) | `signerN.name` |
| `hf054` 주택도시기금 대출 신청서(가계용) | `customer.addressN`, `customer.nameN`, `customer.phoneN`, `월세보증금N`, `월임대료N`, `전세보증금N` |
| `hf055` 주택도시기금 대출상담 및 신청서(내집마련 디딤돌 대출용) | `customer.addressN`, `customer.phoneN`, `방수N`, `배우자N`, `본인N` |
| `hf056` \[필수\] 개인(신용)정보 제3자 제공 동의서(하나더넥스트 내집연금용_역모기지) | `dateN` |
| `hf058` 융자상담 및 차입신청서(기업용) | `company.addressN`, `customer.emailN`, `customer.phoneN` |
| `hf059` 개인(신용)정보 조회 동의서 | `signerN.name`, `이용목적N`, `일반개인정보N` |
| `hf060` \[필수\] 개인(신용)정보 수집이용 동의서(대출성상품 적합성적정성 판단용) | `signerN.name` |
| `hf061` 적합성, 적정성 고객정보 확인서(개인 및 개인사업자용) | `signerN.name` |
| `hf062` 적합성, 적정성 고객정보 확인서(법인용) | `signerN.name` |
| `hf065` 국토교통부 주택소유확인 시스템 등 이용 관련 \[필수\] 개인(신용)정보 수집·이용·제공 동의서 | `signerN.name`, `일반개인정보N` |
| `hf068` 계약 체결 이행 등을 위한 필수 동의서(개인금융성 신용보험용) | `signerN.name`, `공공정보등N` |
| `hf069` 기업간결제 제신고(약정해지,변경) 신청서 | `customer.phoneN` |
| `hf074` \[필수\] 개인(신용)정보 제3자 제공 동의서(햇살론17) | `signerN.name` |
| `hf077` \[필수\]개인(신용)정보 제3자 제공 동의서(토지분양대금대출약정_대전광역시,대전도시공사) | `signerN.name` |
| `hf078` 통화전환 옵션부 외화대출 원화대출 전환신청서 | `dateN`, `주N` |
| `hf079` 정보교환 기업구매자금어음금 미결제통보확인서 | `FaxN` |
| `hf080` 정보교환 기업구매자금어음 부도통보확인서 | `FaxN` |
| `hf081` 정보교환 기업구매자금어음 인수거절통보확인서 | `FaxN` |
| `hf082` 채권발행 등록 신청서 | `signerN.name` |
| `hf084` 외상매출채권 양도통지서(장래채권양도통지용) | `customer.addressN`, `dateN`, `signerN.name` |
| `hf087` 미래채권담보대출 추천서 | `signerN.name` |
| `hf089` 외상매출채권 양도통지서(e-안심팩토링대출용) | `customer.addressN`, `dateN` |
| `hf090` 납품대금 선입금(벤더입금) 신청서 | `signerN.name` |
| `hf094` 상생벤더구매론 승인명세 등록신청서 | `signerN.name` |
| `hf095` 벤더승인명세 등록 신청서 | `signerN.name` |
| `hf096` 발주명세 등록신청서 | `signerN.name` |
| `hf099` 지급승인명세 등록 신청서 | `signerN.name` |
| `hf102` 기업현황서(B2B전자결제서비스 업무, MP용) | `FAXN`, `TELN`, `company.nameN`, `signerN.name` |
| `hf103` B2B 전자결제서비스 업무 이용신청서(MP용) | `customer.addressN` |
| `hf104` 기업구매자금어음 추심의뢰서 | `dateN`, `signerN.name` |
| `hf105` 전자채권미결제 확인의뢰서 및 확인서 | `dateN` |
| `hf110` 전자방식 외상매출채권 발행취소 신청서(외담대,e-안심팩토링용) | `company.nameN`, `dateN`, `signerN.name` |
| `hf111` 《개인》위임장(해외체제자 담보대출용) | `customer.nameN` |
| `hf112` \[필수\]개인(신용)정보 제공동의서(서민맞춤대출용) | `signerN.name` |
| `hf113` 개인(신용)정보 수집.이용 및 제공 동의서\[필수적 동의\](적격대출용) | `dateN`, `signerN.name`, `공공정보등N`, `공사및하나은행N`, `신용등급및평점정보N`, `일반개인정보N`, `재산채무소득의총액납세실적N` |
| `hf114` 개인(신용)정보 수집.이용 제공 동의서(주택보유수 확인등) | `signerN.name`, `일반개인정보N` |
| `hf115` \[필수\] 개인(신용)정보 수집이용, 제공 동의서(핀크생활비대출용) | `signerN.name` |
| `hf116` \[필수\] 개인(신용)정보 수집이용, 제공 동의서(공무원대출) | `signerN.name`, `신용거래정보N` |
| `hf117` \[필수\] 개인(신용)정보 수집이용, 제공 동의서(군인생활안정자금) | `signerN.name`, `신용거래정보N` |
| `hf118` \[필수\] 개인(신용)정보 수집·이용·제공_동의서\[가계여신_금융거래\] | `signerN.name`, `공공정보등N` |
| `hf119` 필수 개인(신용)정보_수집·이용·제공_동의서\[하나_사잇돌_중금리대출용\] | `signerN.name`, `신용거래정보N` |
| `hf120` 필수 개인(신용)정보수집·이용및제공동의서(하나원클릭모기지,원클릭전세론,e금리고정형적격) | `dateN`, `signerN.name`, `공공정보등N`, `성명생년월일주소전화번호N` |
| `hf121` \[필수\] 개인(신용)정보 제3차 제공 동의서(우량주택전세론,군간부전세자금대출) | `signerN.name` |
| `hf122` \[필수\] 개인(신용)정보 수집·이용 및 제공 동의서(전세자금대출 권리보험가입용) | `signerN.name`, `개인대출현황대출한도금액N`, `신용거래정보N` |
| `hf123` \[필수\] 개인(신용)정보 수집·이용 동의서 \[전세자금대출-주택금융보증서용\] | `signerN.name` |
| `hf124` \[필수\] 개인(신용)정보 처리 동의서(전세자금대출 권리보험가입용) | `신용거래정보N` |
| `hf125` \[필수\] 개인(신용)정보 수집·이용 및 제공동의서\[군간부전세자금대출기본),군간부월세자금대출\] | `signerN.name`, `신용거래정보N` |
| `hf126` \[필수\] 상품별 개인(신용)정보 수집·이용·제공 동의서\[목돈안드는 행복전세,목돈 안다는 드림전세(집주인담보대출)용\] | `signerN.name`, `개인식별정보외에고객이제공한정보N`, `성명N`, `일반개인정보N` |
| `hf127` 상품별 필수 개인(신용)정보 제공동의서(하나V-Plus대출) | `signerN.name` |
| `hf128` 필수 개인(신용)정보 수집, 이용 및 제공 동의서(소호여신) | `signerN.name`, `공공정보등N` |
| `hf129` 필수 개인(신용)정보 수집, 이용 및 제공 동의서(법인여신) | `signerN.name`, `공공정보등N` |
| `hf134` 개인(신용)정보 수집.이용 동의서(매도인,무상거주인등 제3자용)(적격대출용) | `signerN.name` |
| `hf135` 동의서(대출비용지급용) | `dateN` |
| `hf136` 《기업》차입신청서(한도내 개별/분할실행용) | `dateN` |
| `hf137` 대출금 분할실행 신청서(에듀큐론용) | `분할실행신청액N` |
| `hf138` 대출금 수령위임동의서 | `signerN.name` |
| `hf139` 《기업》 지급보증거래 신청서(서면.전자 지급보증 겸용) | `dateN`, `signerN.name`, `피보증채무의종류N` |
| `hf140` 매출채권 잔액 확인서 | `company.biz_noN` |
| `hf141` 매출채권 잔액 확인서(사전확인용) | `company.biz_noN` |
| `hf142` 매출채권설정등기통지서 | `dateN`, `절취선N` |
| `hf149` 《기업》금융거래확인서 | `signerN.name`, `연체발생일N` |
| `hf150` 《기업》근저당권유용합의서 | `customer.addressN`, `customer.birthN`, `dateN`, `signerN.name` |
| `hf151` 《기업》무역어음인수·할인신청서 | `년N` |
| `hf153` 《기업》질권설정등록청구서 | `dateN` |
| `hf154` 차입신청서(무역금융용) | `계N` |
| `hf157` 여신거래용 인감명판 등 신고서 | `signerN.name` |
| `hf158` 위임장(하나골드신탁 만기 연장 접수용) | `customer.phoneN`, `dateN`, `signerN.name` |
| `hf159` \[필수\] 개인(신용)정보 수집·이용 동의서(일임형ISA) | `agent.nameN` |
| `hf160` 계약대상자확인서(일임형ISA용) | `agent.nameN`, `dateN`, `가입대상N` |
| `hf161` 위임장 (특정금전신탁용) | `signerN.name` |
| `hf162` ISA계약만기연장 확인서 | `ISA계좌번호N`, `customer.nameN`, `둥록점명N`, `상담직원명N`, `연장전계약만기일N`, `연장후계약만기일N` |
| `hf163` 위임장(일임형 개인종합자산관리계좌(ISA)용) | `customer.addressN`, `customer.birthN`, `customer.phoneN` |
| `hf164` 퇴직연금 퇴직급여 지급신청서(DC,기업형IRP) | `accountN`, `signerN.name`, `금융기관명N` |
| `hf165` 퇴직연금 계약이전신청서(DB) | `foreign.accountN`, `foreign.nameN`, `signerN.name`, `금융기관명N` |
| `hf166` 퇴직연금 계약이전신청서(DC) | `signerN.name` |
| `hf168` 퇴직연금 사전지정운용방법 지정 신청서(디폴트옵션 지정) | `handwrittenN`, `signerN.name` |
| `hf169` 퇴직연금 가입자 거래신청서(DC/기업형IRP) | `handwrittenN`, `signerN.name` |
| `hf170` 퇴직연금 계약이전 신청서(기업형IRP) | `accountN`, `signerN.name` |
| `hf171` 퇴직연금 거래신청서(개인형IRP) | `handwrittenN`, `signerN.name` |
| `hf172` 퇴직연금 거래신청서(DC, 기업형IRP) | `accountN`, `customer.birthN`, `customer.nameN`, `dateN` |
| `hf173` 투자자확인서(퇴직연금용) | `dateN`, `signerN.name` |
| `hf174` 퇴직연금 계약이전 동의서 | `signerN.name` |
| `hf176` 퇴직연금 퇴직급여 지급신청서(DC,기업형IRP) | `accountN`, `signerN.name`, `금융기관명N` |
| `hf177` 퇴직연금 운용상품지정 신청서(DC) | `상품명N` |
| `hf178` 퇴직연금 입금예정상품등록/변경 신청서 | `handwrittenN`, `signerN.name` |
| `hf179` 퇴직연금 퇴직급여 지급신청서(DB) | `accountN`, `signerN.name`, `금융기관명N` |
| `hf182` 이전신청(취소)서(DB,DC,기업형IRP 이전용) | `customer.phoneN`, `signerN.name`, `금융회사명N` |
| `hf184` 퇴직연금 계약해지 신청서(개인형IRP) | `accountN` |
| `hf185` 퇴직연금 DC 기업부담금 자동이체 신청서 | `accountN`, `dateN` |
| `hf186` 퇴직연금_거래신청서(DB) | `customer.birthN`, `customer.nameN`, `dateN`, `비대상N`, `사원번호이메일N`, `성명N`, `입사일중간정산일자N`, `주민등록번호N` … |
| `hf188` 퇴직연금 중도인출신청서(DC,기업형·개인형IRP) | `customer.nameN`, `dateN`, `valueN` |
| `hf191` 퇴직연금 계약해지 신청서(DB,DC) | `accountN`, `signerN.name`, `금융기관명N` |
| `hf193` 퇴직연금 계약해지 신청서(기업형IRP) | `accountN`, `signerN.name` |
| `hf194` 퇴직연금 항목등록/변경 신청서 | `customer.birthN`, `customer.nameN` |
| `hf195` 퇴직연금 가입자(등록·변경·삭제) 신청서(DB,DC,기업형IRP) | `customer.nameN`, `customer.rrnN`, `사원번호N` |
| `hf197` 위임장(집합투자증권 및 연금저축계좌 투자용) | `customer.addressN`, `customer.birthN`, `customer.phoneN` |
| `hf198` 공모부동산집합투자증권 과세특례신청서 | `signerN.name` |
| `hf199` 외화송금신청서 | `dateN`, `signerN.name`, `신청인과의관계N`, `은행명N`, `은행코드N` |
| `hf201` 거래외국환지정(변경)신청서(영문) | `PhoneNoN` |
| `hf202` 거래외국환지정(변경)신청서 | `customer.emailN`, `signerN.name`, `소N` |
| `hf203` 주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(영문) | `AcquisitionPricewonN`, `CapitalN`, `DateofCompletionN`, `DateofReceiptN`, `DelegatedN`, `HeadquarterN`, `MainfactoryN`, `NotificationNoN` … |
| `hf204` 주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(국문) | `customer.addressN`, `customer.nationalityN`, `dateN`, `signerN.name`, `valueN`, `금번투자에따른예상근로자수N`, `금번투자지역N`, `기존주취득시N` … |
| `hf205` 외국환거래법시행령상 거주성확인서 | `예N`, `항목N` |
| `hf206` 연간사업실적보고서(투자잔액 1,000만불 초과 기업) | `계N`, `금액N`, `기타N`, `비중N`, `소재지N`, `주요취급품목N`, `주투자자관계사N`, `지분율10이상투자자N` … |
| `hf207` 연간사업실적보고서(투자잔액 300만불 초과 1,000만불 이하 기업) | `금액N`, `비중N`, `소재지N`, `주요취급품목N`, `투자업종N` |
| `hf208` 지급확인서 | `signerN.name` |
| `hf210` 대북투자 신고 및 투자실적 보고서 | `dateN`, `구분주N`, `비고N`, `비율N`, `업종N`, `투자방법N`, `투자지역N`, `합작투자자N` |
| `hf211` 사업계획서 | `company.ceoN`, `company.nameN`, `한국측N` |
| `hf215` 상호계산계정 결산대차기잔액처분(변경)신고서 | `dateN` |
| `hf216` 해외부동산 취득신고(수리)서 | `dateN`, `signerN.name`, `모기지론N`, `미달러환산액N`, `수취인명N`, `총취득금액N` |
| `hf217` 해외직접투자 내용변경 신고(보고)서 | `signerN.name` |
| `hf218` 서약서(개인의 외국주택 취득) | `signerN.name` |
| `hf219` 해외사무소 설치(변경)신고서 | `dateN`, `signerN.name` |
| `hf220` 해외지점 설치(변경)신고서 | `dateN`, `signerN.name` |
| `hf221` 해외지사 설치·현황 보고서 | `dateN`, `구분N` |
| `hf222` 해외 부동산 취득 보고서 | `가성명또는법인명N`, `나주민등록번호N`, `다주소또는소재지N` |
| `hf223` 「외국환서식관리프로그램」전자무역업무이용(신규,변경,해지)신청서 | `NETN`, `dateN`, `signerN.name`, `계산서N`, `기재사항N`, `상세수발신인식별자N`, `수수료결제계좌번호N`, `전자문서인증키N` |
| `hf224` Usance 송금 조건변경신청서 | `signerN.name`, `수취인주소및전화번호N` |
| `hf225` Usance 송금 신청서 | `dateN`, `signerN.name`, `수취인주소및전화번호N` |
| `hf228` 담보제공신고(보고)서 | `dateN`, `signerN.name` |
| `hf229` 매매신고(보고)서 | `dateN` |
| `hf230` 보증계약신고(보고)서 | `dateN`, `signerN.name` |
| `hf232` 증권발행 신고(보고)서 | `dateN`, `signerN.name` |
| `hf233` 금전의 대차계약 신고(보고)서 | `dateN`, `signerN.name` |
| `hf235` 외국인투자기업등록(변경등록)신청서(국문) | `customer.nationalityN`, `valueN`, `상호또는명칭N`, `액면총액N`, `투자기업N` |
| `hf236` 해외예금 및 신탁 잔액 보고서 | `국가명N`, `예금기관명N`, `해외입금수출대금외화증권처분예금신탁처분기타계N`, `해외처분수입대금지급외화증권취득예금신탁예치기타계N` |
| `hf237` 해외예금 입금보고서 | `국가명N`, `예금종류N`, `입금액N`, `입금재원N` |
| `hf238` 해외직접투자사업 청산 및 대부채권 회수보고서 | `company.addressN` |
| `hf239` 해외 부동산 처분(변경)신고서 | `가성명또는법인명N`, `나주민등록번호N`, `다주소또는소재지N` |
| `hf240` 외화증권(채권)취득보고서(법인 및 개인기업 설립보고서 포함) | `company.addressN` |
| `hf242` 대외지급보증 발급 신청서(SWIFT 방식)(2D) | `BeneficiaryN` |
| `hf244` 자본재 등 도입물품명세 검토ㆍ확인신청서 | `HSK분류번호N`, `company.biz_noN`, `customer.nationalityN`, `dateN`, `signerN.name`, `규격N`, `금액N`, `상호또는명칭N` … |
| `hf245` 장기차관 방식의 외국인투자신고서, 변경신고서(영문) | `AverageLoanPeriodN`, `CapitalinkindN`, `CashN`, `ChangeinInformationN`, `DateofReceiptN`, `InformationAfterChangeN`, `LocationofInvestmentN`, `NotificationNoN` … |
| `hf246` 장기차관 방식의 외국인투자신고서, 변경신고서(국문) | `customer.addressN`, `customer.nationalityN`, `dateN`, `signerN.name`, `금번투자지역N`, `기타N`, `변경신고의경우변경내용N`, `변경후내용N` … |
| `hf247` 외국인투자기업등록(변경등록)신청서(영문) | `customer.nameN`, `customer.nationalityN`, `valueN` |
| `hf248` 주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(영문) | `AcquisitionPriceWonN`, `ChangeinN`, `DateofCompletionN`, `DateofReceiptN`, `InformationN`, `NotificationNoN`, `ReceiptNumberN`, `changedN` … |
| `hf249` 주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(국문) | `customer.addressN`, `customer.nationalityN`, `dateN`, `signerN.name`, `변경내용N`, `변경사항N`, `변경후내용N`, `상호또는명칭N` … |
| `hf251` \[필수\] 개인(신용)정보 수집 이용 동의서(외투용)_국문 | `signerN.name` |
| `hf252` 외국환 신고(확인)필증 | `customer.nameN` |
| `hf253` ( ) 변경신고(수리)서 | `signerN.name` |
| `hf254` 금전의 대차계약 신고서 | `dateN` |
| `hf255` 자(손자)회사 사업계획서 | `company.addressN`, `company.biz_itemN`, `company.ceoN`, `자본금N` |
| `hf262` 상호계산신고서 | `company.biz_itemN` |
| `hf263` 지급등의 방법(변경)신고(보고)서 | `변경N`, `신고금액N` |
| `hf264` 거주자간 해외직접투자 양수도 신고(보고)서 | `company.addressN`, `company.biz_noN`, `dateN`, `signerN.name`, `상호또는성명N`, `신고번호N` |
| `hf265` 수탁기관 변경 신청서 | `customer.addressN`, `dateN`, `상호또는명칭N` |
| `hf267` 외국환거래용 인감(서명)신고서 | `영문N`, `한글N` |
| `hf268` 수입선적서류 도착통지 및 수입신용장 조건불일치에 관한 조회 | `dateN`, `선적서류금액N` |
| `hf272` REDEMPTION OF OUR LETTERS OF GUARANTEE | `GentlemenN`, `LGAmountN`, `NumberofBLN`, `NumberofCreditN`, `NumberofLGN`, `VesselNameN` |
| `hf275` 수입신용장 재개설 및 중계에 관한 약정서 | `customer.addressN`, `signerN.name`, `은행명N` |
| `hf278` 판매대금추심의뢰서 매입(취소) 등록 요청/확인서 | `FAXN`, `signerN.name` |
| `hf280` 추심 수출환어음 종결처리(유예) 요청서 | `customer.phoneN`, `dateN`, `signerN.name`, `개설일자N`, `거래번호N`, `신용장번호계약서번호N`, `유효기일N`, `추심금액N` … |
| `hf285` 인감증 발급신청서(외국환업무) | `signerN.name` |
| `hf291` 「외국환서식관리프로그램」수출대금채권 양도에 따른 대금지급지시서 및 동의통지서 | `TitleN`, `customer.nameN`, `dateN`, `employer.positionN`, `signerN.name` |
| `hf292` 수입통관도우미서비스 이용신청서 | `dateN` |
| `hf297` 단기수출보험(수출채권유동화) 청약 확인서 | `company.ceoN`, `company.nameN`, `customer.addressN`, `소재국N` |
| `hf302` 「외국환서식관리프로그램」BILL OF EXCHANGE (환어음 고객용) | `ATN`, `DATEDN`, `FORN`, `TON` |
| `hf305` ( )예금/신탁 거래신고서 | `signerN.name` |
| `hf306` 증권대차계약 신고서 | `dateN` |
| `hf307` 지급수단등의 수출입(변경)신고서 | `company.ceoN`, `company.nameN`, `dateN` |
| `hf308` 대북투자사업계획서 | `자기자금N`, `차입금N` |
| `hf309` 파생상품거래 신고서 | `company.biz_itemN`, `dateN` |
| `hf310` 대북투자사업 청산 및 대부채권 회수보고서 | `계N` |
| `hf311` 상호계산계정 폐쇄 신고서 | `dateN` |
| `hf313` 북한지사 설치·현황 보고서 | `dateN`, `구분N` |
| `hf314` 북한지사 설치(변경) 신고서 | `dateN`, `signerN.name` |
| `hf317` 증권발행 보고서 | `signerN.name` |
| `hf318` 대북투자(변경)신고서 | `dateN`, `signerN.name` |
| `hf319` 증권취득 신고서 | `dateN` |
| `hf321` 부동산취득신고(수리)서 | `dateN` |
| `hf322` 북한사무소 경비지급신고서 | `dateN`, `signerN.name`, `valueN` |
| `hf323` 북한지점 경비지급신고서 | `dateN`, `signerN.name`, `valueN` |
| `hf324` 임대차계약신고서 | `dateN` |
| `hf325` 증권취득신고서 | `dateN` |
| `hf326` ( )매매 신고서 | `dateN`, `signerN.name` |
| `hf327` 담보제공 신고서 | `dateN` |
| `hf328` 외국기업 국내지사 폐쇄신고서 | `dateN` |
| `hf329` 외국기업 국내지사 설치신고서 | `company.addressN`, `company.ceoN`, `company.nameN`, `dateN` |
| `hf330` 외국기업 국내지사 변경신고서 | `dateN` |
| `hf331` 해외지점의 영업활동 보고서 | `customer.addressN` |
| `hf334` 전자적무역결제금융등록(변경,해지)신청서 | `customer.emailN`, `customer.nameN`, `customer.phoneN`, `valueN`, `팩스번호N` |
| `hf335` 하나 입출금 거래내역 문자통지서비스 신청서 | `문자통지대상휴대폰번호N` |
| `hf336` 개인 전자금융 서비스 신청서(영문) | `ApplicantN`, `CategoryN`, `DelegatorN`, `DesignateChangeN`, `HomePhoneN`, `KRWN`, `OTPManufacturerN`, `OtherRequestsN` … |
| `hf337` 개인 전자금융 서비스 신청서 | `3시간지연4시간지연N`, `OTP제조업체N`, `agent.nameN`, `customer.addressN`, `customer.birthN`, `customer.emailN`, `customer.home_phoneN`, `customer.nameN` … |
| `hf338` 기업 전자금융서비스 신청서(은행용)(영문) | `DailyKRWN`, `DesignationofBeneficiaryAccountN`, `OTPN`, `OnetimeKRWN`, `RequestCancelN`, `WithdrawalAccountN`, `customer.addressN` |
| `hf340` 기업 전자금융서비스 신청서(은행용) | `OTPN`, `accountN`, `agent.nameN`, `signerN.name`, `입금계좌지정N` |
| `hf341` 기업 전자금융서비스 신청확인서(고객용) | `전국대표번호N`, `해외이용시N` |
| `hf343` 금융거래정보 이용제공 동의서(기업관계사서비스용)(영문) | `HanaBankN` |
| `hf344` 기업관계사 서비스 이용계약서(영문) | `CEON`, `company.nameN`, `customer.addressN`, `dateN` |
| `hf346` 기업관계사 서비스 이용신청서 | `company.biz_noN`, `company.ceoN`, `company.corp_noN`, `customer.addressN`, `employer.nameN` |
| `hf347` 기업관계사 서비스 이용계약서 | `customer.addressN`, `employer.nameN`, `signerN.name` |
| `hf348` 기업관계사 서비스 이용신청서(영문) | `BusinessRegistrationNoN`, `CorporateRegistrationNoN`, `RepresentativeN`, `company.nameN`, `customer.addressN` |
| `hf350` 아이부자 걷기챌린지 서비스 동의서 | `signerN.name` |
| `hf354` CMS Plus 이용계약서 | `customer.addressN` |
| `hf355` CMS Mega 이용계약서 | `customer.addressN` |
| `hf356` CMS Plus 이용신청서 | `customer.nameN`, `customer.phoneN` |
| `hf357` CMSiNet 지사정보 등록신청서 | `customer.addressN` |
| `hf358` CMS Global 이용신청서 | `customer.addressN`, `customer.nameN`, `email주소N`, `口KRWN`, `口초과1개국가당KRWN` |
| `hf359` 하나 sERP 이용신청서 | `customer.nameN` |
| `hf362` 자동화기기 이용(신규,해지,변경)신청서 | `customer.birthN`, `customer.nameN`, `customer.phoneN`, `dateN`, `signerN.name`, `이용계좌번호N` |
| `hf363` 개인(신용)정보 수집이용 동의서\[은행공동인증서비스(BankSign)\] | `signerN.name` |
| `hf364` 개인(신용)정보 제3자 제공 동의서\[은행공동인증서비스(BankSign)\] | `signerN.name` |
| `hf365` Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(영문) | `PostalCodeN`, `SignatureSealN`, `customer.addressN`, `valueN` |
| `hf366` Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(국문) | `agent.addressN`, `company.corp_noN`, `customer.addressN`, `customer.zipcodeN`, `valueN` |
| `hf367` Hana 1Q bank CMS iNet 서비스 이용 추가 계약서(iSBS) | `customer.addressN`, `signerN.name` |
| `hf372` 전산기기 임대차계약서(Hana 1Q bank CMS) | `customer.addressN` |
| `hf374` 전자어음 이용(변경,해지) 신청서 | `signerN.name`, `valueN` |
| `hf376` 위임장(해외체류자 전자금융용) | `signerN.name` |
| `hf377` 해외영업점 계좌개설 신청서 | `signerN.name`, `성명NameN` |
| `hf378` 글로벌뱅킹서비스 이용,변경,해지 신청서 | `InquiryN`, `signerN.name`, `성명NameN`, `조회N` |
| `hf379` 주류구매전용카드 가맹점가입신청서 | `customer.nameN`, `dateN`, `employer.nameN`, `signerN.name` |
| `hf380` 금융결제원CMS 이용계약서 | `signerN.name`, `원N` |
| `hf381` 장외파생상품 일반투자자 (부)적정성 판단보고서 | `customer.nameN`, `dateN`, `거래목적위험회피목적여부N` |
| `hf382` 장외파생상품 일반투자자 투자자정보 분석결과표 | `customer.nameN`, `dateN` |
| `hf383` 장외파생상품 투자성향에 적정하지 않은 거래확인서 | `customer.nameN`, `dateN` |
| `hf384` 장외파생상품 일반투자자 투자자정보 확인서(법인 및 개인사업자 고객용) | `customer.nameN`, `dateN`, `employer.departmentN`, `employer.positionN`, `관련경력N`, `관련자격N`, `상장거래소명N`, `하금융투자상품에투자해본경험이없음N` |
| `hf385` 장외파생상품 일반투자자 투자자정보 확인서(개인 고객용) | `dateN` |
| `hf389` 위임장(장외파생상품 일반투자자용) | `customer.nameN` |
| `hf399` 파생상품거래 손실한도 초과 및 증거담보 요청 통지서 | `customer.addressN` |
| `hf400` 파생상품거래 손실한도 감액통지서 | `signerN.name` |
| `hf405` 외환파생상품 거래 금액 확인서 | `위험헤지비율N`, `통화선도N`, `통화스왑N`, `통화옵션N`, `환변동보험N` |
| `hf407` 본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(영문) | `FundN`, `InvestmentN`, `OfficeN`, `RetirementN` |
| `hf408` 본인확인서(FATCA CRS 개인,개인사업자용)(국문) | `dateN`, `signerN.name` |
| `hf409` 본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(국문) | `가한국에서설립된펀드일것N`, `구분N`, `다음의요건을모두충족하는금융기관N`, `다음의요건을모두충족해야함N`, `별정우체국법에의한별정우체국연금관리단N` |
| `hf410` 본인확인서(FATCA CRS 법인,임의단체용)(영문) | `GivenNameN`, `JurisdictionofResidenceN`, `NameofEntityN`, `OverseaaddressN`, `SareRatioN`, `SurnameN`, `TaxpayerIdentificationNON`, `customer.birthN` |
| `hf411` \[필수\]본인 행정정보 제공 요구서(공공마이데이터 수신 묶음정보用 - 주민등록표 등·초본 조회) | `customer.birthN`, `customer.nameN`, `customer.phoneN` |
| `hf412` \[필수\]본인 행정정보 제공 요구서(공공마이데이터 수신 묶음정보用 - 사업자등록증명 조회) | `customer.birthN`, `customer.nameN`, `customer.phoneN` |
| `hf413` 고객확인서(법인,고유번호나 납세번호가 있는 임의 단체용) | `FAXN`, `customer.addressN`, `대표자N`, `전화N` |
| `hf414` \[필수\] 개인(신용)정보 수집·이용·제공 동의서 \[공공마이데이터 주민등록 등·초본 조회용\] | `signerN.name`, `일반개인정보N` |
| `hf415` \[필수\] 개인(신용)정보 제3자 제공 동의서 \[공공마이데이터 주민등록 등·초본 조회용\] | `signerN.name` |
| `hf416` \[필수\] 개인(신용)정보 수집·이용·제공 동의서 \[공공마이데이터 사업자정보 조회용\] | `signerN.name`, `고유식별정보N`, `일반개인정보N` |
| `hf417` \[필수\] 개인(신용)정보 제3자 제공 동의서 \[공공마이데이터 사업자정보 조회용\] | `signerN.name` |
| `hf418` \[필수\] 개인(신용)정보 수집·이용 동의서 \[비대면 스크래핑 서비스\] | `signerN.name` |
| `hf419` \[필수\] 개인(신용)정보 수집 · 이용 동의서 (비여신 금융거래) | `signerN.name` |
| `hf420` 비대면 계좌개설 안심차단 서비스 신청서 | `signerN.name` |
| `hf421` \[필수\] 개인(신용)정보 수집·이용·제공·조회 동의서 \[비대면 계좌개설 안심차단 서비스\] | `signerN.name`, `거부권리및불이익N` |
| `hf422` \[필수\] 개인(신용)정보 수집·이용·조회 동의서\[비대면 계좌개설 안심차단 신청여부 조회용\] | `signerN.name` |
| `hf423` \[선택\] 개인(신용)정보 수집ㆍ이용 및 제공동의서 (상품서비스 안내 등) | `signerN.name` |
| `hf424` \[필수\] 개인(신용)정보 제3자제공 동의서 \[하나카드 발급_미성년자용\] | `signerN.name` |
| `hf425` \[필수\] 개인(신용)정보 제3자제공 동의서 \[하나카드 발급_법정대리인용\] | `signerN.name` |
| `hf426` 이의제기 신청서 | `customer.phoneN` |
| `hf427` 아이부자 선불전자지급수단 잔액 상속(지급) 및 서비스 해지 요청서(위임장 겸용) | `customer.birthN`, `customer.phoneN` |
| `hf428` 본인확인서(FATCA CRS 법인,임의단체용)(국문) | `company.nameN`, `customer.birthN`, `customer.nameN`, `거주관할권주소N`, `성N`, `지분율N` |
| `hf429` 본인확인서(FATCA CRS 개인,개인사업자용)(영문) | `GivenNameN`, `SurnameN`, `customer.birthN` |
| `hf430` 민원신청서 | `agent.emailN`, `customer.emailN`, `dateN`, `signerN.name`, `기타N`, `본인확인N`, `신용거래정보N` |
| `hf431` 전자금융거래 사고 피해 신고서(통합서류) | `accountN`, `company.nameN`, `customer.nameN`, `customer.phoneN`, `dateN`, `signerN.name`, `신용거래정보N`, `입금은행N` … |
| `hf432` \[필수\] 개인(신용)정보 제3자 제공 동의서 (하나원큐 공모주 정보제공 제휴서비스용) | `signerN.name` |
| `hf434` 세종특별자치시 지역개발채권 매입 신청서 | `customer.addressN`, `customer.phoneN`, `customer.rrnN`, `dateN`, `signerN.name` |
| `hf435` 대전광역시 지역개발채권 매입 신청서 | `customer.addressN`, `customer.phoneN`, `customer.rrnN`, `dateN`, `signerN.name` |
| `hf437` 고객정보 활용 동의서(매출채권보험_모집대행업무용) | `customer.phoneN`, `signerN.name`, `필수사항N` |
| `hf438` 매출채권보험 상담 신청서(신청기업용) | `company.biz_noN`, `company.corp_noN`, `company.nameN`, `customer.phoneN`, `signerN.name`, `년N`, `월N`, `일N` |
| `hf440` 금융사고예방을 위한 문자통지(SMS) 서비스 신청서 | `customer.phoneN` |
| `hf441` 법원보관금 납부서(은행제출용) | `accountN`, `customer.nameN`, `customer.phoneN`, `customer.rrnN`, `dateN`, `납부금액N`, `납부자성명N`, `납부자주소N` … |
| `passport` 여권 | `mrz.lineN` |

## 겹친 목록

| 서식 | 키 |
|---|---|
| `corporate_registry` 법인 등기사항전부증명서(현재 유효사항) | `purpose_history.*.purposes.*` |
| `hf003` 은행거래신청서 | `deposit_list_list.*.*.transfer_day` |
| `import_declaration` 수입신고필증 | `items.*.specs.*.amount`, `items.*.specs.*.model`, `items.*.specs.*.no`, `items.*.specs.*.quantity`, `items.*.specs.*.unit_price` |

## 모든 표

| 서식 | 묶음 | 행 (최소~최대) | 나옴 | 순서 | 제목 | 열 |
|---|---|---|---|---|---|---|
| `account_opening_application` | `extra_products` | 0~8 | 3/12 | - | - | type(예금종류), name(상품명), amount(신규금액), term(계약기간), account_no(계좌번호) |
| `admission_letter` | `conditions` | 0~3 | 3/12 | - | - | value(Condition) |
| `articles_of_incorporation` | `revision_history` | 2~8 | 12/12 | - | - | value(제정·개정일) |
| `articles_of_incorporation` | `purposes` | 5~8 | 12/12 | - | - | value(목적) |
| `articles_of_incorporation` | `revision_effective` | 1~7 | 12/12 | asc | - | value(시행일) |
| `auto_transfer_application` | `extra_loans` | 0~8 | 1/12 | - | - | loan_account(납부자번호), loan_product(대출상품), target(이체대상), transfer_day(출금일) |
| `balance_certificate` | `rows` | 1~11 | 12/12 | - | - | kind(과목), account_no(계좌번호), balance(예금잔액), uncleared(미결제타점권), pledge(질권), restriction(지급정지·압류·가압류) … |
| `balance_certificate` | `remarks` | 0~1 | 2/12 | - | - | value(비고) |
| `bank_statement` | `rows` | 13~48 | 12/12 | asc | - | datetime(거래일시), type(적요), memo(기재내용), out(찾으신금액), in(맡기신금액), balance(거래후잔액) |
| `bankbook_copy` | `txs` | 0~4 | 4/12 | asc | - | date(거래일), memo(적요), in(맡기신금액), balance(잔액), out(찾으신금액) |
| `bill_of_lading` | `containers` | 1~6 | 12/12 | - | - | no(ContainerNo), type(ContainerType), seal(SealNo), packages(ContainerPackages), gross_weight(ContainerGrossWeight), measurement(ContainerMeasurement) |
| `bill_of_lading` | `charges` | 0~4 | 5/12 | - | - | name(Charge), quantity(RevenueTons), rate(Rate), per(Per), prepaid(Prepaid), collect(Collect) |
| `board_minutes` | `agendas` | 1~6 | 12/12 | - | - | no(의안번호), title(의안), body(결의내용), detail(세부내용) |
| `board_minutes` | `signers` | 3~5 | 12/12 | - | - | title(자격), name(성명), remote(비고) |
| `building_register` | `exclusive` | 1~1 | 12/12 | - | - | kind(구분), floor(층별), structure(구조), usage(용도), area(면적(㎡)) |
| `building_register` | `common` | 1~14 | 12/12 | - | - | kind(구분), floor(층별), structure(구조), usage(용도), area(면적(㎡)) |
| `building_register` | `owners` | 1~6 | 12/12 | asc | - | name(성명(명칭)), rrn(주민(법인)등록번호), address(주소), share(소유권지분), change_date(변동일), change_cause(변동원인) |
| `building_register` | `house_prices` | 3~8 | 12/12 | desc | - | base_date(기준일), price(공동주택(아파트)가격) |
| `business_registration_certificate` | `sub_kinds` | 0~1 | 1/12 | - | - | biz_type(업태), biz_item(종목) |
| `business_registration_certificate_corp` | `sub_kinds` | 0~1 | 2/12 | - | - | biz_type(업태), biz_item(종목) |
| `business_registration_proof` | `kinds` | 1~2 | 12/12 | - | - | biz_type(업태), biz_item(종목), code(업종코드), main(구분) |
| `card_statement` | `rows` | 11~108 | 12/12 | asc | - | date(이용일자), merchant(이용하신가맹점), amount(이용금액), months(할부), seq(회차), principal(원금) … |
| `card_statement` | `fee_per_100` | 5~5 | 12/12 | - | - | months(할부개월), fee(100원당수수료) |
| `career_certificate` | `careers` | 1~6 | 12/12 | - | - | period(근무기간), department(근무부서), position(직위), duty(담당업무) |
| `collateral_agreement` | `joint_collateral` | 0~11 | 5/12 | - | - | kind(종류), location(소재지번), detail(지목면적), unique_no(고유번호) |
| `collateral_agreement` | `special_terms` | 0~5 | 5/12 | - | - | value(특약사항) |
| `commercial_invoice` | `items` | 2~51 | 12/12 | - | - | description(DescriptionofGoods), model(Model), quantity(Quantity/Unit), unit_price(Unit-price), amount(Amount) |
| `corporate_customer_due_diligence` | `owners` | 1~3 | 12/12 | mixed | - | name(성명), birth(생년월일), nationality(국적), ratio(지분율), relation(법인과의관계) |
| `corporate_customer_due_diligence` | `shareholders` | 0~22 | 3/12 | mixed | - | name(주주명), birth(생년월일), shares(소유주식수), ratio(지분율), relation(법인과의관계) |
| `corporate_registry` | `office_history` | 0~1 | 2/12 | - | - | address(본점) |
| `corporate_registry` | `capital_history` | 0~3 | 6/12 | - | - | issued_shares(발행주식의총수), common_shares(보통주식), capital(자본금의액), changed(변경연월일), registered(등기연월일) |
| `corporate_registry` | `purposes` | 5~8 | 12/12 | - | - | value(목적) |
| `corporate_registry` | `officers` | 5~17 | 12/12 | mixed | - | position(직위), name(성명), rrn(주민등록번호), appointed(취임일), appointment_type(취임구분), registered(등기일) … |
| `corporate_registry` | `branches` | 0~3 | 4/12 | asc | - | no(지점번호), address(지점소재지), opened(설치일), opened_registered(등기일), closed(폐지일), closed_registered(등기일) |
| `credit_agreement` | `special_terms` | 0~7 | 6/12 | - | - | value(특약사항) |
| `credit_agreement_corp` | `special_terms` | 0~6 | 4/12 | - | - | value(특약사항) |
| `credit_agreement_corp` | `guarantors` | 0~1 | 1/12 | - | - | name(연대보증인), rrn(실명번호), address(주소), relation(채무자와의관계) |
| `customer_due_diligence` | `edd.accounts` | 0~7 | 2/12 | - | - | bank(금융회사), kind(계좌종류), purpose(주된용도) |
| `debt_certificate` | `loans` | 1~11 | 12/12 | mixed | - | subject(대출과목), account_no(계좌번호), loan_date(대출일), maturity(만기일), amount(대출금액), balance(대출잔액) … |
| `employment_contract` | `allowances` | 1~2 | 12/12 | - | - | name(기타급여(제수당등)), amount(기타급여(제수당등)) |
| `employment_contract` | `special_terms` | 0~9 | 5/12 | - | - | value(특약사항) |
| `family_relation_certificate` | `family` | 2~5 | 12/12 | mixed | - | relation(구분), name(성명), name_hanja(성명(한자)), birth(출생연월일), rrn(주민등록번호), gender(성별) … |
| `fatca_crs` | `residences` | 0~2 | 1/12 | - | - | country(거주관할권), tin(납세자번호), no_tin_reason(납세자번호미기재사유) |
| `financial_statements` | `assets` | 18~23 | 12/12 | - | - | account(과목), current(당기), prior(전기) |
| `financial_statements` | `liabilities` | 8~10 | 12/12 | - | - | account(과목), current(당기), prior(전기) |
| `financial_statements` | `equity` | 5~6 | 12/12 | - | - | account(과목), current(당기), prior(전기) |
| `financial_statements` | `income_statement` | 13~28 | 12/12 | - | - | account(과목), current(당기), prior(전기) |
| `financial_statements` | `appropriation` | 0~5 | 1/12 | - | - | account(과목), current(당기), prior(전기) |
| `guarantee_agreement` | `co_guarantors` | 0~1 | 2/12 | - | - | name(보증인), rrn(실명번호), address(보증인주소), phone(연락처), relation(채무자와의관계) |
| `guarantee_agreement` | `special_terms` | 0~4 | 3/12 | - | - | value(특약사항) |
| `hana_official_001` | `목록` | 1~10 | 12/12 | mixed | - | 상품명, 계좌번호, 금액, 성명, 생년월일, 연락처 … |
| `hana_official_006` | `목록` | 2~2 | 12/12 | - | - | 예금주명, 이체일, 이체주기(이체주기(일☞주☞월☞년)), 이체금액 |
| `hana_official_006` | `관리비지로공과금기타_목록` | 1~3 | 12/12 | mixed | - | 수납기관(수납기관(아파트,상가)), 납부자번호(납부자번호(동,호수,수용가번호,등)), 지로번호기관코드(지로번호/기관코드), 납부희망일 |
| `hana_official_011` | `계좌번호_목록` | 0~0 | 0/12 | - | - | value((통화코드:)) |
| `hana_official_052` | `목록` | 0~0 | 0/12 | - | - | 공공정보등(■공공정보등) |
| `hana_official_053` | `목록` | 0~0 | 0/12 | - | - | 공공정보등(■공공정보등) |
| `hana_official_054` | `목록` | 1~2 | 12/12 | - | - | 임차보증금, 소액보증금, 금액, 자금용도, 담보종류 |
| `hana_official_055` | `목록` | 1~2 | 12/12 | - | - | 차입기관명, 금액, 자금용도, 담보종류 |
| `hana_official_058` | `부채현황_목록` | 1~4 | 12/12 | - | - | 금융기관명, 금액, 담보, 자금용도 |
| `hana_official_149` | `목록` | 1~12 | 12/12 | mixed | - | 종별, 용도, 이율, 일자, 금액, 잔액 … |
| `hana_official_157` | `목록` | 1~5 | 12/12 | - | - | 변경후 |
| `hana_official_408` | `tax.residence_list` | 2~2 | 12/12 | - | - | country(거주관할권*(1)), tin(납세자번호(TIN)) |
| `hana_official_413` | `목록` | 1~3 | 12/12 | - | - | 사업장(사업장(국내)), 영문명, 생년월일, 국적, 한글명, 지분율 … |
| `hana_official_428` | `목록` | 1~3 | 12/12 | - | - | 실질지배자(실질지배자(1)), 거주관할권(거주관할권(국가)), 납세자번호(납세자번호(TIN)) |
| `health_insurance_payment` | `rows` | 6~35 | 12/12 | asc | - | month(년월), notice_health(고지보험료(건강보험)), notice_ltc(고지보험료(장기요양)), health(납부보험료(건강보험)), ltc(납부보험료(장기요양)), total(납부보험료(계)) … |
| `health_insurance_qualification` | `rows` | 2~25 | 12/12 | desc | - | kind(가입자구분), workplace(사업장명칭), start(자격취득일), end(자격상실일) |
| `hf001` | `목록` | 1~10 | 12/12 | mixed | - | 상품명, 계좌번호, 금액, 성명, 생년월일, 연락처 … |
| `hf002` | `목록` | 0~0 | 0/12 | - | - | FixedFloating(FixedFloating(mth)) |
| `hf003` | `deposit_list` | 3~3 | 12/12 | mixed | - | interest_account(통장발행), tax_free_limit(연원가식), product(상품명1), amount(가입금액1), period(계약기간1), transfer_amount(이체금액1) … |
| `hf003` | `목록` | 0~0 | 0/12 | - | - | 갋 |
| `hf003` | `redeposit_list` | 3~3 | 12/12 | - | - | product(\[신청상품\]1) |
| `hf006` | `목록` | 1~2 | 12/12 | - | - | 예금주명, 이체일, 이체주기(이체주기(일☞주☞월☞년)), 이체금액 |
| `hf006` | `관리비지로공과금기타_목록` | 1~3 | 12/12 | mixed | - | 수납기관(수납기관(아파트,상가)), 납부자번호(납부자번호(동,호수,수용가번호,등)), 지로번호기관코드(지로번호/기관코드), 납부희망일 |
| `hf007` | `목록` | 1~3 | 12/12 | mixed | - | 예금종류, 예금주(예금주(위탁자/수탁자)), 계좌번호, 예금액, 만기일주1, 질권설정금액 … |
| `hf008` | `목록` | 1~3 | 12/12 | mixed | - | 예금종류, 예금주(예금주(위탁자/수탁자)), 계좌번호, 예금액, 만기일, 질권설정금액 … |
| `hf009` | `목록` | 1~3 | 12/12 | mixed | - | 예금종류, 예금주(예금주(위탁자/수탁자)), 계좌번호, 금액주1, 만기일주2, 질권설정금액 … |
| `hf011` | `계좌번호_목록` | 0~0 | 0/12 | - | - | value((통화코드:)) |
| `hf016` | `목록` | 1~5 | 12/12 | - | - | 은행지점 |
| `hf017` | `목록` | 1~3 | 12/12 | - | - | 계좌번호, 은행명, 금액 |
| `hf019` | `목록` | 1~6 | 12/12 | - | - | 개설기관명, 계좌번호 |
| `hf021` | `목록` | 2~10 | 12/12 | - | - | 거래금액(거래금액(원)), 지급적요, 입금은행, 입금계좌번호, 수취인명, 입금적요 |
| `hf031` | `목록` | 0~0 | 0/12 | - | - | 예, 아니오 |
| `hf032` | `목록` | 0~0 | 0/12 | - | - | 예, 아니오 |
| `hf033` | `목록` | 1~7 | 12/12 | - | - | Yes, No |
| `hf034` | `목록` | 1~8 | 12/12 | - | - | 예금종별, 계좌번호 |
| `hf037` | `목록` | 1~9 | 12/12 | mixed | - | 위탁일자, 수탁번호, 종류, 증서어음번호(증서【어음】번호), 지급지, 발행인 … |
| `hf038` | `목록` | 1~17 | 12/12 | mixed | - | 수표어음, 번호, 발행일, 지급일, 금액, 수취인 … |
| `hf042` | `목록` | 1~2 | 12/12 | - | - | 예금주, 계좌번호 |
| `hf043` | `목록` | 1~5 | 12/12 | - | - | 변경후 |
| `hf045` | `목록` | 1~34 | 12/12 | mixed | - | 수표종류, 지급은행, 수표번호, 발행일자, 지급일자, 발행인 … |
| `hf046` | `목록` | 1~16 | 12/12 | mixed | - | 일자, 내용 |
| `hf052` | `목록` | 0~0 | 0/12 | - | - | 공공정보등(■공공정보등) |
| `hf053` | `목록` | 0~0 | 0/12 | - | - | 공공정보등(■공공정보등) |
| `hf054` | `목록` | 1~2 | 12/12 | - | - | 임차보증금, 소액보증금, 금액, 자금용도, 담보종류 |
| `hf055` | `목록` | 1~2 | 12/12 | - | - | 차입기관명, 금액, 자금용도, 담보종류 |
| `hf058` | `부채현황_목록` | 1~4 | 12/12 | - | - | 금융기관명, 금액, 담보, 자금용도 |
| `hf072` | `목록` | 1~2 | 12/12 | - | - | 비고 |
| `hf082` | `목록` | 1~18 | 12/12 | mixed | - | 중심업체코드, 판매기업사업자번호, 판매기업명, 채권발행일자채권만기일자, 채권금액, 세금계산서승인번호 … |
| `hf083` | `목록` | 1~2 | 12/12 | - | - | 비고 |
| `hf085` | `목록` | 1~3 | 12/12 | - | - | 상품명, 중심업체코드, 한도승인번호, 정보제공내용 |
| `hf086` | `목록` | 1~3 | 12/12 | mixed | - | 업체명, 대표자, 법인번호, 사업자번호, 최초거래일자, 납품실적(납품실적*) … |
| `hf088` | `목록` | 1~10 | 12/12 | mixed | - | 사업자번호, 사업자명, 추심금액, 추심의뢰일, 지급은행, 대표품명 … |
| `hf090` | `목록` | 1~3 | 12/12 | mixed | - | 선입금신청금액, 채권번호, 채권금액, 발행일, 결제일, 중심업체코드 … |
| `hf092` | `목록` | 1~37 | 12/12 | mixed | - | 외상매출채권번호, 채권양도인사업자번호, 채권양도인, 채권양도금액, 채권발행일, 채권지급일 … |
| `hf093` | `목록` | 1~14 | 12/12 | mixed | - | 전자채권번호, 구매기업명(구매기업명(사업자번호)), 발행일, 만기일(만기일(미결제일)), 입금액, 입금일 … |
| `hf094` | `목록` | 1~20 | 12/12 | mixed | - | 원청채권종류, 원청채권번호, 원청구매기업명, 사업자등록번호, 원청채권금액, 원청채권발행일 … |
| `hf095` | `목록` | 1~5 | 12/12 | mixed | - | 하위벤더기업명, 사업자등록번호, 벤더승인금액, 세금계산서발행일, 세금계산서발행금액, 세금계산서승인번호 … |
| `hf096` | `목록` | 1~3 | 12/12 | mixed | - | 차협력기업명, 사업자등록번호, 발주번호, 발주금액, 납품기한, 대금지급일 … |
| `hf097` | `목록` | 1~3 | 12/12 | mixed | - | 대출실행일, 대출신청금액, 의뢰일, 발주번호, 발주금액, 납품기한 … |
| `hf098` | `목록` | 1~11 | 12/12 | mixed | - | 결제원어음번호, 어음금액, 인수거절여부, 인수거절사유, 대출일, 대출신청금액 … |
| `hf099` | `목록` | 1~15 | 12/12 | mixed | - | 판매기업사업자번호, 판매기업명, 구매기업결제일자, 판매기업입금일자, 승인금액, 선입금가능일자 … |
| `hf100` | `목록` | 1~5 | 12/12 | mixed | - | 채권번호, 구매기업명, 대표자, 공급물품명, 세금계산서발행일, 전자채권금액 … |
| `hf102` | `사업모델및특성_목록` | 1~3 | 12/12 | - | - | 모델명, 내용, 특성 |
| `hf102` | `요약재무현황_목록` | 0~0 | 0/12 | - | - | 년 |
| `hf102` | `목록` | 1~6 | 12/12 | mixed | - | 주주명, 소유주식수, 지분율, 대주주와의관계, 회사와의관계, 성명 … |
| `hf102` | `주요경력_목록` | 0~0 | 0/12 | - | - | 기간, 근무처, 담당업무, 최종직위 |
| `hf104` | `목록` | 1~6 | 12/12 | mixed | - | 사업자번호, 사업자명, 어음금액, 발행일, 대표품명, 공급가액 … |
| `hf105` | `목록` | 1~2 | 12/12 | - | - | 전자채권번호, 발행기업명(발행기업명(사업자등록번호)), 금액, 발행일, 만기일, 미결제사유 |
| `hf107` | `목록` | 1~14 | 12/12 | mixed | - | 계좌번호, 추심의뢰인, 대출금액, 대출취급일, 당초만기일, 기한연장일 … |
| `hf108` | `목록` | 1~10 | 12/12 | mixed | - | 대출실행일, 대출신청금액, 의뢰일, 의뢰번호, 매출금액, 지급기일 … |
| `hf110` | `목록` | 1~5 | 12/12 | mixed | - | 채권번호, 판매기업명, 판매기업사업자번호, 발행일, 만기일, 채권금액 … |
| `hf140` | `목록` | 1~6 | 12/12 | mixed | - | 일련번호, 매출채권금액, 발생일, 지급기일, 다른권리존재여부, 특기사항 |
| `hf141` | `목록` | 1~3 | 12/12 | mixed | - | 일련번호, 매출채권금액, 발생일(발생(예정)일), 지급기일, 매출채권확정여부, 다른권리존재여부 |
| `hf142` | `목록` | 1~3 | 12/12 | mixed | - | 일련번호, 발생일, 만기일, 채권금액, 비고 |
| `hf144` | `목록` | 1~5 | 12/12 | - | - | 제품명, 식별번호(식별번호(주)), 모델명, 제조사, 제조년월, 비고 |
| `hf145` | `목록` | 1~4 | 12/12 | - | - | 동산의명칭, 규격, 수량(수량(주1)), 수량단위, 단가(단가(주2)), 제조사 … |
| `hf149` | `목록` | 1~12 | 12/12 | mixed | - | 종별, 용도, 이율, 일자, 금액, 잔액 … |
| `hf151` | `목록` | 0~0 | 0/12 | - | - | 월, 일 |
| `hf152` | `목록` | 1~3 | 12/12 | mixed | - | 약정일자, 거래약정서류명(거래약정서류명(또는어음채무내용)), 채무한도액, 보증종류 |
| `hf153` | `목록` | 1~5 | 12/12 | - | - | 종류, 기호, 번호, 액면금액, 매수, 총액 |
| `hf154` | `related_list` | 1~2 | 12/12 | - | - | name(성명), age(연령), job(직업및직위), relation(차주와의관계), monthly_income(월평균수입), net_assets(실자산) … |
| `hf154` | `loan.basis_list` | 1~5 | 12/12 | - | - | line(수량) |
| `hf154` | `bank.opinion_list` | 1~3 | 12/12 | - | - | line(수량) |
| `hf154` | `무역금융신청건포함명세_목록` | 0~0 | 0/12 | - | - | 당행, 타행 |
| `hf154` | `운전자금_목록` | 0~0 | 0/12 | - | - | 당행, 타행 |
| `hf154` | `시설자금_목록` | 0~0 | 0/12 | - | - | 당행, 타행 |
| `hf154` | `지급보증_목록` | 0~0 | 0/12 | - | - | 타행 |
| `hf154` | `deposit_list` | 1~2 | 12/12 | - | - | savings_pledged(담보제공액), time_pledged(담보제공액), savings_note(비고), time_note(비고) |
| `hf157` | `목록` | 1~5 | 12/12 | - | - | 변경후 |
| `hf165` | `목록` | 1~4 | 12/12 | mixed | - | 가입자명(가입자명*), 생년월일(생년월일(주민번호)), 제도전환전출일자(제도전환/전출일자), 서명또는(서명또는(인)), 지급요청금액, 매도순위 … |
| `hf165` | `매도상품_목록` | 1~5 | 12/12 | mixed | - | 상품명, 상품계좌번호, 만기일 |
| `hf165` | `이전받는금융기관_목록` | 1~4 | 12/12 | mixed | - | 상품계좌번호, 만기일 |
| `hf166` | `목록` | 1~3 | 12/12 | mixed | - | 가입자성명, 서명또는(서명또는(인)), 생년월일(생년월일(주민번호)), 제도전환전출일자(제도전환/전출일자), 현물이전유의사항확인 |
| `hf169` | `기업부담금_목록` | 1~5 | 12/12 | - | - | 상품명, 매수비율(매수비율(%)) |
| `hf169` | `개인부담금_목록` | 1~5 | 12/12 | - | - | 상품명, 매수비율(매수비율(%)) |
| `hf169` | `목록` | 1~2 | 12/12 | - | - | 상품명, 매수비율(매수비율(%)) |
| `hf171` | `기업부담금_목록` | 1~5 | 12/12 | - | - | 상품명, 매수비율(매수비율(%)) |
| `hf171` | `개인부담금_목록` | 1~5 | 12/12 | - | - | 상품명, 매수비율(매수비율(%)) |
| `hf174` | `목록` | 1~40 | 12/12 | mixed | - | 성명, 생년월일, 인서명(인/서명) |
| `hf177` | `수익증권_목록` | 1~9 | 12/12 | - | - | 경남은행정기예금 |
| `hf177` | `정기예금_목록` | 0~0 | 0/12 | - | - | 년 |
| `hf177` | `저축은행정기예금_목록` | 1~2 | 12/12 | - | - | JT저축은행정기예금, 년 |
| `hf178` | `기업부담금_목록` | 1~5 | 12/12 | - | - | 상품명, 매수비율(매수비율(%)) |
| `hf178` | `개인부담금_목록` | 1~5 | 12/12 | - | - | 상품명, 매수비율(매수비율(%)) |
| `hf178` | `목록` | 1~2 | 12/12 | - | - | 상품명, 매수비율(매수비율(%)) |
| `hf179` | `목록` | 1~3 | 12/12 | - | - | 매도순위, 상품명, 계좌번호, 매도금액(매도금액(원/좌)) |
| `hf180` | `목록` | 1~12 | 12/12 | - | - | 이전하는금융회사(이전하는금융회사(운용관리기관명)), 운용관리기관명, 자산관리기관명, 적립금이전액(적립금이전액*), 실물이전여부 |
| `hf181` | `목록` | 1~15 | 12/12 | - | - | 이전하는금융회사(이전하는금융회사(운용관리기관명)), 운용관리기관명자산관리기관명, 성명, 주민번호, 연락처, 실물이전여부1현금2실물(실물이전여부1.현금2.실물) … |
| `hf183` | `목록` | 0~0 | 0/12 | - | - | 은행사용란 |
| `hf185` | `목록` | 1~10 | 12/12 | mixed | - | 가입자명, 생년월일, 이체금액, 원 |
| `hf188` | `sell_list` | 1~3 | 12/12 | - | - | order(매도순위), product(상품명), account(계좌번호), amount(매도금액(원/좌)) |
| `hf189` | `목록` | 1~10 | 12/12 | mixed | - | 성명, 생년월일주1, 기업부담금, 개인부담금 |
| `hf191` | `목록` | 1~2 | 12/12 | - | - | 성명, 서명또는(서명또는(인)), 생년월일, 입사일자, 잔여부담금(잔여부담금(DC형만기재)), 중간정산일자 … |
| `hf192` | `목록` | 1~2 | 12/12 | - | - | 휴대폰번호, 이메일주소 |
| `hf205` | `국민_목록` | 0~0 | 0/12 | - | - | 아니오(아니오(NO)) |
| `hf205` | `외국인_목록` | 0~0 | 0/12 | - | - | 아니오(아니오(NO)) |
| `hf206` | `주주현황7_목록` | 1~7 | 12/12 | - | - | 국가, 상호또는성명, 금기말, 전기말, 계열여부 |
| `hf206` | `대부투자_목록` | 0~0 | 0/12 | - | - | 금기말 |
| `hf206` | `지분율10미만_목록` | 0~0 | 0/12 | - | - | 금기말 |
| `hf206` | `목록` | 2~4 | 12/12 | - | - | 금기말, 전기말, 이자, 차입처, 코드1, 차입금액 … |
| `hf207` | `주주구성_목록` | 1~3 | 12/12 | - | - | 상호또는성명, 국가, 지분율(지분율(%)), 순투자액5(순투자액(천미불)5)) |
| `hf207` | `목록` | 1~4 | 12/12 | - | - | 금기말, 전기말, 차입처, 코드1, 차입금액, 보증자 … |
| `hf210` | `목록` | 1~2 | 12/12 | - | - | 투자자, 현지법인명, 현금, 신고일자, 신고금액 |
| `hf211` | `취득증권_목록` | 1~2 | 12/12 | - | - | 증권종류, 주수, 주당가액 |
| `hf211` | `한국측_목록` | 1~15 | 12/12 | - | - | 금액, 비율(비율(%)) |
| `hf211` | `목록` | 1~8 | 12/12 | - | - | 금액, 비율(비율(%)) |
| `hf216` | `국내송금액_목록` | 0~0 | 0/12 | - | - | 미달러환산액 |
| `hf216` | `현지조달액_목록` | 0~0 | 0/12 | - | - | 미달러환산액 |
| `hf217` | `목록` | 2~2 | 12/12 | - | - | 변경후 |
| `hf221` | `목록` | 1~3 | 12/12 | - | - | 신고자, 사업자번호(사업자(주민)번호), 지사명, 설치국가 |
| `hf223` | `변경신청_목록` | 1~2 | 12/12 | - | - | 변경항목, 변경전, 변경후 |
| `hf223` | `지급지시업무관련출금계좌_목록` | 1~3 | 12/12 | - | - | 예금과목, 계좌번호, 예금주, 통화 |
| `hf223` | `신청인_목록` | 0~0 | 0/12 | - | - | 수발신인식별자, 상세수발신식별자, 전자문서인증키 |
| `hf226` | `목록` | 1~3 | 12/12 | mixed | - | 차주명, 사업자등록번호, 담당자성명, 담당자전화번호, 대주명, 대주소재국 … |
| `hf227` | `목록` | 1~3 | 12/12 | mixed | - | 발행자명, 사업자등록번호, 담당자성명, 담당자전화번호, 대주명, 대주소재국 … |
| `hf231` | `목록` | 1~4 | 12/12 | mixed | - | 보고업체명1(보고업체명1)(본사명)), 사업자번호법인번호(사업자번호/법인번호), 차주2, 대주3대주지역(대주3)대주지역), 차입구분4외화증권5(차입구분4)외화증권5), 차입잔액6 … |
| `hf234` | `수취인_목록` | 1~5 | 12/12 | - | - | 변경후 |
| `hf236` | `목록` | 1~1 | 12/12 | - | - | 금액 |
| `hf238` | `목록` | 1~4 | 12/12 | mixed | - | 원금, 구분회수일자, 회수재산의종류, 금액, 비고 |
| `hf238` | `회수금액_목록` | 1~2 | 12/12 | - | - | 원금 |
| `hf252` | `휴대_목록` | 1~2 | 12/12 | - | - | 통화종류CodeofCurrency, 형태Form, 통화별금액AmountineachCurrency, 합계Sum(합계(미화상당)Sum(US$equiv)), 반출입용도Use, 비고(비고(Note)(수표번호등)) |
| `hf252` | `목록` | 1~2 | 12/12 | - | - | 형태Form, 통화별금액AmountineachCurrency, 합계Sum(합계(미화상당)Sum(US$equiv)), 반출입용도Use, 비고(비고(Note)(수표번호등)), 일자Date … |
| `hf255` | `한국측_목록` | 1~3 | 12/12 | - | - | 출자자명, 금액, 비율(비율(%)) |
| `hf255` | `목록` | 1~8 | 12/12 | - | - | 금액, 비율(비율(%)) |
| `hf260` | `목록` | 1~3 | 12/12 | - | - | 변경후 |
| `hf278` | `목록` | 1~5 | 12/12 | - | - | 번호, 종류, 통화코드, 매입금액(매입(추심)금액), 판매대금추심의뢰서번호, 매입점포코드(매입(추심)점포코드) |
| `hf279` | `목록` | 1~4 | 12/12 | - | - | OurRefNo(OurRef.No.), Amount, 사유(사유(하자내용등)), Discrepancies |
| `hf281` | `목록` | 1~3 | 12/12 | - | - | 변경후 |
| `hf282` | `목록` | 1~4 | 12/12 | - | - | 조건변경부신용장내용 |
| `hf293` | `목록` | 1~10 | 12/12 | - | - | 신용장번호, 통화, 금액, 선하증권, 항공화물운송장, 상업송장보험서류 … |
| `hf294` | `TOISSUINGBANK_목록` | 0~0 | 0/12 | - | - | BENE, BANK, COMM, CUST, BL(B/L), AWB … |
| `hf297` | `주소_목록` | 0~0 | 0/12 | - | - | 대표자 |
| `hf297` | `최근1년간거래실적_목록` | 1~2 | 12/12 | - | - | 결제금액, 만기경과미결제액 |
| `hf308` | `한국측_목록` | 1~2 | 12/12 | - | - | 출자자명, 금액, 비율(비율(%)) |
| `hf308` | `목록` | 1~8 | 12/12 | - | - | 금액, 비율(비율(%)) |
| `hf310` | `목록` | 1~3 | 12/12 | mixed | - | 원금, 구분회수일자, 회수재산의종류, 금액, 비고 |
| `hf310` | `회수금액_목록` | 1~2 | 12/12 | - | - | 원금 |
| `hf313` | `목록` | 1~3 | 12/12 | - | - | 신고자, 지사명, 설치지역, 신고금액, 북한지사명 |
| `hf318` | `목록` | 0~0 | 0/12 | - | - | 대부투자, 총투자액 |
| `hf323` | `비독립채산지점_목록` | 0~0 | 0/12 | - | - | value((주소)(전화번호)(e-mail)) |
| `hf334` | `목록` | 1~4 | 12/12 | - | - | 거래인감, 비고 |
| `hf335` | `목록` | 1~2 | 12/12 | - | - | 문자통지신청계좌2, 문자통지신청계좌3 |
| `hf336` | `목록` | 1~2 | 12/12 | - | - | BankName, AccountNo(AccountNo.), SpeedDialNumberforPhoneBanking |
| `hf337` | `목록` | 1~2 | 12/12 | - | - | 은행명, 계좌번호, 폰뱅킹단축번호, 통장인감서명(통장인감/서명) |
| `hf338` | `목록` | 1~3 | 12/12 | - | - | OverseasIPBlockingService, OfficeName, BusinessRegistrationNo(BusinessRegistrationNo.), CorporateRegistrationNo(CorporateRegistrationNo.) |
| `hf338` | `WithdrawalAccount_목록` | 1~2 | 12/12 | - | - | UserID |
| `hf340` | `입금계좌지정신청신청안함_목록` | 0~0 | 0/12 | - | - | 해외IP차단 |
| `hf340` | `기업뱅킹본지사서비스신청해지_목록` | 1~2 | 12/12 | - | - | 지사명, 사업자번호, 법인등록번호 |
| `hf340` | `출금계좌_목록` | 1~2 | 12/12 | - | - | 대량이체한도iNetCMS에한함(대량이체한도iNet*CMS에한함) |
| `hf342` | `통지계좌_목록` | 1~4 | 12/12 | - | - | 통화, 계좌번호, 예금주 |
| `hf346` | `목록` | 1~2 | 12/12 | - | - | 실행자ID(실행자ID*), 통화, 계좌번호, 인감서명(인감/서명) |
| `hf348` | `목록` | 1~2 | 12/12 | - | - | ExecutorID(ExecutorID*), Currency, AccountNo(AccountNo.), RegisteredSealSign(RegisteredSeal/Sign) |
| `hf353` | `주소_목록` | 1~2 | 12/12 | - | - | 대표자, 생년월일, 대표이사 |
| `hf353` | `목록` | 1~8 | 12/12 | - | - | 통화, 계좌번호, 예금주명, 인감서명(인감/서명), 실행자아이디(실행자아이디(ID)), 개설점 … |
| `hf353` | `이체한도_목록` | 0~0 | 0/12 | - | - | value((영문+숫자혼합6~10자리)) |
| `hf354` | `목록` | 1~2 | 12/12 | - | - | 명세, 수량, 키보드마우스포함(키보드,마우스포함) |
| `hf354` | `HW_목록` | 1~3 | 12/12 | - | - | 수량 |
| `hf356` | `주소_목록` | 1~2 | 12/12 | - | - | 사업자등록번호, 생년월일, 대표이사 |
| `hf356` | `맞춤서비스_목록` | 0~0 | 0/12 | - | - | value((맞춤기능또는시스템연계내용)) |
| `hf356` | `목록` | 1~12 | 12/12 | - | - | value((영문+숫자혼합6~10자리)), 일련번호(일련번호(은행영업점직원이기입)), 실행자아이디(실행자아이디(ID)), 계좌번호, 통장인감, 개설점 … |
| `hf356` | `이체한도_목록` | 0~0 | 0/12 | - | - | value((영문+숫자혼합6~10자리)) |
| `hf357` | `목록` | 2~5 | 12/12 | - | - | 실행자ID, 통화, 계좌번호, 예금주명, 인감서명(인감/서명), 개설점 |
| `hf358` | `이용수수료1_목록` | 1~2 | 12/12 | - | - | 조회집금서비스2신청국가(조회+집금서비스2)신청국가) |
| `hf363` | `목록` | 1~2 | 12/12 | - | - | 수집이용목적(수집·이용목적), 고유식별정보, 개인정보(개인(신용)정보), 일반개인정보 |
| `hf364` | `목록` | 1~2 | 12/12 | - | - | 제공받는자, 이용목적 |
| `hf365` | `목록` | 1~6 | 12/12 | - | - | Currency, AccountNo(AccountNo.(AccountType)), AccountHolderName, SealSignature(Seal/Signature) |
| `hf366` | `목록` | 1~6 | 12/12 | - | - | 통화, 계좌번호(계좌번호(계좌종류)), 예금주명, 인감서명(인감/서명) |
| `hf368` | `목록` | 0~0 | 0/12 | - | - | 예금주 |
| `hf369` | `목록` | 1~2 | 12/12 | - | - | 계좌번호, 예금주 |
| `hf372` | `목록` | 1~2 | 12/12 | - | - | 명세, 수량, 키보드마우스포함(키보드,마우스포함) |
| `hf372` | `HW_목록` | 1~3 | 12/12 | - | - | 수량 |
| `hf377` | `국내주소DomesticAddress_목록` | 1~4 | 12/12 | mixed | - | 여권유효기일DateofExpiry |
| `hf377` | `해외주소OverseasAddress_목록` | 1~4 | 12/12 | mixed | - | 여권유효기일DateofExpiry |
| `hf378` | `해외주소OverseasAddress_목록` | 0~0 | 0/12 | - | - | 직장Company |
| `hf378` | `자택House_목록` | 1~2 | 12/12 | - | - | 여권번호PassportNo(여권번호PassportNo.) |
| `hf378` | `직장Company_목록` | 1~2 | 12/12 | - | - | 여권번호PassportNo(여권번호PassportNo.) |
| `hf380` | `목록` | 0~0 | 0/12 | - | - | 예금주명 |
| `hf386` | `택일_목록` | 1~2 | 12/12 | - | - | 수출(수출(투자포함)), 수입(수입(조달포함)), 비고 |
| `hf386` | `목록` | 1~3 | 12/12 | - | - | 수입(수입(조달포함)), 비고 |
| `hf386` | `기체결외환파생상품거래금액_목록` | 1~3 | 12/12 | - | - | 수입(수입(조달포함)), 비고 |
| `hf387` | `원화계좌_목록` | 1~3 | 12/12 | - | - | 통화, 계좌번호, 통장용인감(통장용인감(서명)) |
| `hf387` | `외화계좌_목록` | 1~5 | 12/12 | - | - | 통화, 계좌번호, 통장용인감(통장용인감(서명)) |
| `hf390` | `목록` | 1~7 | 12/12 | - | - | 담당자명, 부서및직급, 전화번호 |
| `hf402` | `목록` | 1~8 | 12/12 | mixed | - | 성명, 소속부서및직급, 생년월일, 인감(인감(서명)), 권한의제한, 전화번호팩스번호(전화번호&팩스번호) … |
| `hf408` | `tax.residence_list` | 2~2 | 12/12 | - | - | country(거주관할권*(1)), tin(납세자번호(TIN)) |
| `hf413` | `목록` | 1~7 | 12/12 | mixed | - | 사업장(사업장(국내)), 영문명, 생년월일, 국적, 한글명, 지분율 … |
| `hf421` | `목록` | 0~0 | 0/12 | - | - | 고유식별정보(■고유식별정보), 공공정보등(■공공정보등) |
| `hf422` | `목록` | 0~0 | 0/12 | - | - | 고유식별정보(■고유식별정보) |
| `hf427` | `목록` | 1~9 | 12/12 | mixed | - | 성명, 생년월일, 연락처 |
| `hf428` | `목록` | 1~3 | 12/12 | - | - | 실질지배자(실질지배자(1)), 거주관할권(거주관할권(국가)), 납세자번호(납세자번호(TIN)) |
| `hf429` | `목록` | 1~2 | 12/12 | - | - | value((CapitalLetter)*), FATCA, CRS, PhoneNo(PhoneNo.) |
| `hf430` | `목록` | 1~16 | 12/12 | - | - | 기타 |
| `hf431` | `목록` | 0~0 | 0/12 | - | - | 출입국사실증명원또는여권사본 |
| `hf436` | `목록` | 1~3 | 12/12 | mixed | - | 주주명, 생년월일(생년월일(YYYY-MM-DD)), 주식의종류(주식의종류(보통주등)), 지분율(지분율(%)), 주식수(주식수(주)), 주당액면가액(주당액면가액(원)) … |
| `hf439` | `목록` | 1~3 | 12/12 | - | - | 예금과목, 계좌번호, 금액 |
| `import_declaration` | `items` | 2~6 | 12/12 | - | - | line_no(란번호), std_name(품명), trade_name(거래품명), hs_code(세번부호), net_weight(순중량), taxable_usd(과세가격(USD)) … |
| `income_certificate` | `filing_rows` | 0~6 | 6/12 | - | - | year(귀속연도), income_type(소득구분), revenue(수입금액), income(소득금액) |
| `income_certificate` | `rows` | 1~4 | 12/12 | - | - | year(귀속연도), income_type(소득구분), payer(법인명(상호)), payer_biz_no(사업자등록번호), amount(소득금액(과세대상급여액)), tax(총결정세액) |
| `income_tax_return` | `incomes` | 0~4 | 8/12 | - | - | type(소득구분), payer(소득의지급자), revenue(총수입금액), expense(필요경비), amount(소득금액), withheld(원천징수세액) |
| `income_tax_return` | `dependents` | 0~4 | 8/12 | - | - | relation(관계), name(성명), rrn(주민등록번호), basic(기본공제), extra(추가공제) |
| `income_tax_return` | `deduction_items` | 0~4 | 8/12 | - | - | item(소득공제항목), amount(금액) |
| `income_tax_return` | `credit_items` | 0~3 | 8/12 | - | - | item(세액공제항목), amount(금액) |
| `income_tax_return` | `prepaid_items` | 0~2 | 8/12 | - | - | item(기납부세액항목), amount(금액) |
| `land_register` | `land` | 1~7 | 12/12 | - | - | category(지목), area(면적), reason(사유) |
| `land_register` | `owners` | 2~7 | 12/12 | asc | - | change_date(변동일자), change_cause(변동원인), address(주소), name(성명또는명칭), reg_no(등록번호), co_owners(공유자) |
| `land_register` | `grades` | 3~3 | 12/12 | - | - | date(등급수정년월일), grade(토지등급) |
| `land_register` | `land_prices` | 5~7 | 12/12 | asc | - | base_date(개별공시지가기준일), price(개별공시지가) |
| `lease_contract` | `specials` | 3~13 | 12/12 | - | - | value(특약사항) |
| `lease_contract` | `brokers` | 1~2 | 12/12 | - | - | office_address(사무소소재지), office_name(사무소명칭), representative(대표), reg_no(등록번호), phone(전화), assistant(소속공인중개사) |
| `loan_application` | `debts` | 0~2 | 8/12 | - | - | lender(금융기관), kind(대출종류), balance(잔액), maturity(만기일), refinance(상환여부) |
| `loan_application` | `assets` | 0~2 | 9/12 | - | - | kind(종류), location(소재지), value(평가금액) |
| `loan_application_corp` | `other_loans` | 0~11 | 11/12 | - | - | lender(금융기관), kind(여신종류), balance(잔액), collateral(담보) |
| `local_tax_assessment` | `items` | 4~41 | 12/12 | - | - | tax_item(세목), levied(부과연월), kind(구분), object(과세대상), base(과세표준), tax(세액) … |
| `local_tax_payment_certificate` | `deferrals` | 0~1 | 1/12 | - | - | tax_year(과세연도), tax_item(세목), due(납부기한), amount(세액), period(유예기간) |
| `move_in_household_list` | `households` | 1~6 | 12/12 | mixed | - | no(순번), head_name(세대주성명), move_in_date(전입일자), reg_type(등록구분), first_name(최초전입자성명), first_date(최초전입일자) … |
| `move_in_household_list` | `cohabitants` | 0~1 | 3/12 | - | - | no(순번), name(동거인성명), move_in_date(전입일자), reg_type(등록구분) |
| `overseas_remittance_application` | `batch` | 0~8 | 1/12 | - | - | beneficiary(수취인), message(송금메시지), country(국가), bank(수취은행), account_no(계좌번호), currency(통화) … |
| `packing_list` | `items` | 2~51 | 12/12 | - | - | ctn_no(C/TNo), description(DescriptionofGoods), packages(Packages), quantity(Quantity), net_weight(NetWeight), gross_weight(GrossWeight) … |
| `packing_list` | `containers` | 0~6 | 2/12 | - | - | no(ContainerNo), seal(SealNo), packages(ContainerPackages), net_weight(ContainerNetWeight), gross_weight(ContainerGrossWeight), measurement(ContainerMeasurement) |
| `pay_stub` | `payments` | 3~13 | 12/12 | - | - | name(임금항목), amount(지급금액) |
| `pay_stub` | `deductions` | 6~12 | 12/12 | - | - | name(공제항목), amount(공제금액) |
| `pay_stub` | `payments_irregular` | 0~2 | 8/12 | - | - | name(임금항목), amount(지급금액) |
| `pay_stub` | `calc_methods` | 6~20 | 12/12 | - | - | item(구분), method(산출식또는산출방법), amount(금액(원)) |
| `pension_enrollment_certificate` | `rows` | 1~19 | 12/12 | asc | - | kind(가입자종류), workplace(사업장명칭), start(자격취득일), end(자격상실일), wage(기준소득월액), note(비고) |
| `power_of_attorney` | `tasks` | 1~3 | 12/12 | - | - | value(위임내용) |
| `privacy_consent` | `providers` | 3~3 | 12/12 | - | - | name(제공받는자), purpose(제공받는자의이용목적), items(제공하는항목), period(제공받는자의보유이용기간) |
| `real_estate_registry` | `buildings` | 0~2 | 10/12 | - | - | display_no(표시번호), receipt(접수), location(소재지번,건물명칭및번호), detail(건물내역), cause(등기원인및기타사항) |
| `real_estate_registry` | `gapgu` | 0~7 | 10/12 | - | - | rank(순위번호), purpose(등기목적), receipt(접수), holder.role(권리자구분), holder.name(소유자), holder.reg_no(등록번호) … |
| `real_estate_registry` | `eulgu` | 0~6 | 9/12 | - | - | rank(순위번호), purpose(등기목적), receipt(접수), cause(등기원인), max_amount(채권최고액), debtor(채무자) … |
| `real_estate_registry` | `summary.owners` | 0~2 | 2/12 | - | - | name(등기명의인), reg_no((주민)등록번호), share(최종지분), address(주소), rank(순위번호) |
| `real_estate_registry` | `summary.rights` | 0~1 | 2/12 | - | - | rank(순위번호), purpose(등기목적), receipt(접수정보), main(주요등기사항), target_owner(대상소유자) |
| `real_estate_registry` | `summary.gapgu_rights` | 0~1 | 1/12 | - | - | rank(순위번호), purpose(등기목적), receipt(접수정보), main(주요등기사항), target_owner(대상소유자) |
| `resident_registration_abstract` | `addresses` | 1~25 | 12/12 | asc | - | no(번호), address(주소), moved_in(전입일), changed(변동일), head_relation(세대주및관계), status(등록상태) … |
| `resident_registration_copy` | `past_addresses` | 0~19 | 8/12 | asc | - | no(번호), address(주소), moved_in(전입일/변동일), reason(변동사유) |
| `resident_registration_copy` | `members` | 1~5 | 12/12 | mixed | - | no(번호), relation(세대주관계), name(성명), name_hanja(한자), moved_in(전입일/변동일), reason(변동사유) … |
| `sales_contract` | `specials` | 3~13 | 12/12 | - | - | value(특약사항) |
| `sales_contract` | `brokers` | 1~2 | 12/12 | - | - | office_address(사무소소재지), office_name(사무소명칭), representative(대표), reg_no(등록번호), phone(전화), assistant(소속공인중개사) |
| `shareholder_registry` | `shareholders` | 3~34 | 12/12 | mixed | - | no(번호), name(주주명), id_no(주민등록번호(사업자번호)), address(주소), share_type(주식종류), shares(소유주식수) … |
| `shareholders_meeting_minutes` | `attendees` | 0~28 | 7/12 | - | - | name(주주명), shares(소유주식수), method(출석구분), proxy(대리인) |
| `shareholders_meeting_minutes` | `agendas` | 1~5 | 12/12 | - | - | no(의안번호), title(의안), body(결의내용), detail(세부내용) |
| `shareholders_meeting_minutes` | `signers` | 2~4 | 12/12 | - | - | title(자격), name(성명) |
| `standard_financial_statement_proof` | `bs_accounts.quick` | 0~6 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `bs_accounts.inventory` | 0~2 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `bs_accounts.investment` | 0~3 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `bs_accounts.tangible` | 0~8 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `bs_accounts.intangible` | 0~2 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `bs_accounts.other_noncurrent` | 0~2 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `bs_accounts.current_liab` | 0~7 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `bs_accounts.noncurrent_liab` | 0~3 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `pl_accounts.revenue` | 0~2 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `pl_accounts.cogs` | 0~3 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `pl_accounts.sga` | 0~15 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `pl_accounts.non_op_income` | 0~2 | 4/12 | - | - | account(계정과목), amount(금액) |
| `standard_financial_statement_proof` | `pl_accounts.non_op_expense` | 0~2 | 4/12 | - | - | account(계정과목), amount(금액) |
| `trade_contract` | `items` | 2~51 | 12/12 | - | - | description(Commodity&Description), model(Model), quantity(Quantity), unit_price(UnitPrice), amount(Amount) |
| `tuition_invoice` | `items` | 5~21 | 12/12 | mixed | - | date(Date), description(Description), charge(Charges), credit(Payments/Credits) |
| `tuition_invoice` | `installments` | 0~5 | 4/12 | asc | - | no(InstallmentNo), due_date(InstallmentDueDate), amount(InstallmentAmount) |
| `vat_tax_base_certificate` | `items` | 4~9 | 12/12 | asc | - | period(과세기간), kind(신고구분), filed(신고일), base_total(매출과세표준계), base_taxable(과세분), base_exempt(면세수입금액) … |
