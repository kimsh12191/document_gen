# bank_form 변형 목록 (여러 쪽 · 특수 상황 · 정정)

은행 서식 14종. 여러 쪽은 `heavy(rng, p)`, 특수 상황은 `special(rng, 이름, p)` (docgen/docs/_common.py).
고객 자체가 바뀌는 변형(외국인 고객, 주주 다수 재구성)은 시나리오 생성(`p.extra["scenario"]`)에서는 쓰지 않는다 (서류 간 일관성).
옛 은행(외환은행·KEB하나은행) 서식에도 같은 변형이 들어가며, 날짜·제도 플래그(`bk.*`)는 그대로 따른다.

공통
- 손글씨 값(이름·주소·전화·금액·계좌·생년월일 등)에 `f(..., fix=0.03~0.08)` 정정 효과. 정정 도장 글자는 `f.set_corr_name(...)` 로 작성자(신청인·채무자·설정자·보증인·대표이사·법정대리인) 이름.
- 체크 누락(`m.choice` 값 None)은 정답 null. 테스트가 모든 값 필드에 `data-field` 위치를 요구하므로 `lp.nochk` / `bf.nochk` 로 빈 위치 표시를 단다.
- 여러 쪽 약정서는 둘째 쪽부터 위에 은행명·서식번호 줄(`.pg-repeat` 의 `bf-cont`)이 반복된다. 조항 제목과 본문, 은행 사용란은 한 덩어리로 넘어간다.

| 서류 | 경우 | 확률 | 새 키 | 설명 |
|---|---|---|---|---|
| loan_application | heavy | 0.2 | (debts·assets 길어짐) | 다중채무: 부채현황 6~14건(카드론·현금서비스 등), 소유재산 추가. 표가 2단 배치에서 세로 배치로 바뀌고 2쪽 |
| loan_application | co_borrower | 0.12 | co_borrower.{name,rrn,relation,mobile,workplace}, sign/seal.co_borrower | 공동차주(배우자) 공동신청 + 서명란 |
| loan_application | agent | 0.1 | agent.{name,rrn,relation,phone,poa}, sign/seal.agent | 대리인 신청, 위임장 첨부 체크 |
| loan_application | sparse | 0.15 | (null) | 이메일·자택/직장전화·우편번호·직장주소·부서 미기재 |
| loan_application | no_check | 0.1 | (null) | 주택소유구분·주거형태·금리방식 중 체크 누락 |
| loan_application_corp | heavy | 0.25 | other_loans_total | 타 금융기관 여신 7~16건(저축은행·캐피탈·외화대출·L/C 등) + 합계 줄 (3건 이상이면 합계) |
| loan_application_corp | agent | 0.15 | agent.{name,position,phone,rrn}, sign/seal.agent | 직원 대리 신청 (법인인감 날인 위임장) |
| loan_application_corp | sparse | 0.15 | (null) | 팩스·영문명·종업원수·담당자 이메일 미기재 |
| loan_application_corp | no_check | 0.1 | (null) | 기업규모·자금구분·금리종류 중 체크 누락 |
| credit_agreement | heavy | 0.3 | special_terms[] | 제8조~제18조 약관 조항 + 제19조 특약사항 3~7개 → 2쪽 |
| credit_agreement | co_borrower | 0.1 | co_borrower.{name,rrn,address,phone}, sign/seal.co_borrower | 공동차주(배우자) 당사자란·서명란 |
| credit_agreement | handwriting_missing | 0.08 | handwritten = null | 자필기재란 비움 |
| credit_agreement | no_check | 0.08 | explained = null | 설명 확인 체크 누락 |
| credit_agreement_corp | heavy | 0.3 | special_terms[] | 제7조~제16조 + 제17조 특약(재무약정 등, 담보·보증 종류에 맞게) → 2쪽 |
| credit_agreement_corp | joint_guarantor | 0.15 | guarantors[].{name,rrn,address,relation}, seal.guarantor* | 실제경영자(+이사) 연대보증인 표 |
| credit_agreement_corp | no_check | 0.08 | explained = null | 설명 확인 체크 누락 |
| collateral_agreement | heavy | 0.25 | joint_collateral[].{kind,location,detail,unique_no}, special_terms[] | 공동담보 목록 5~12필지("이하 여백") + 제4~10조 + 특약 → 2쪽 |
| collateral_agreement | third_party | 0.1 | mortgagor_relation | 물상보증: 설정자 = 부(또는 배우자), 채무자 ≠ 설정자 |
| collateral_agreement | co_mortgagor | 0.15 | co_mortgagor.{name,rrn,address,share}, seal.co_mortgagor | 부부 공유 → 공동 설정자·인감 (third_party 와 배타) |
| collateral_agreement | handwriting_missing | 0.08 | (null) | 자필기재(피담보채무 범위 또는 확인) 하나 비움 |
| guarantee_agreement | heavy | 0.25 | special_terms[] | 제6~12조 + 제13조 특약 → 2쪽 |
| guarantee_agreement | multi_guarantor | 0.2 | co_guarantors[].{name,rrn,address,phone,relation}, seal.co_guarantor* | 연대보증인 2~3명 (당사자란·인감란) |
| guarantee_agreement | handwriting_missing | 0.1 | handwritten.* = null | 자필란 1~2칸 비움 |
| guarantee_agreement | no_check | 0.08 | explained = null | 설명 확인 체크 누락 |
| auto_transfer_application | heavy | 0.15 | extra_loans[].{loan_account,loan_product,target,transfer_day} | 추가 이체 대상 대출 4~9건 → 2쪽 |
| auto_transfer_application | other_holder | 0.15 | (debit.*, relation=가족) | 배우자 명의 타행 계좌에서 출금, 예금주 별도 서명 |
| auto_transfer_application | no_check | 0.08 | (null) | 관계·이체대상·제3자 제공 동의 중 체크 누락 |
| auto_transfer_application | sparse | 0.1 | applicant.address = null | 주소 미기재 |
| customer_due_diligence | heavy | 0.15 | edd.{annual_income,assets,fund_detail,purpose_detail,cash_tx,overseas_tx,accounts[]} | 고위험 고객 EDD 추가정보 + 타 금융회사 계좌 3~7건 → 2쪽 |
| customer_due_diligence | foreigner | 0.1 | (customer.* 외국인) | 외국인(외국인등록번호·국적·영문 서명), 확인증표 외국인등록증/여권 |
| customer_due_diligence | agent | 0.1 | agent.{name,rrn,relation}, sign/seal.agent | 대리인 정보란 기재 |
| customer_due_diligence | not_owner | 0.06 | owner.{name,birth,nationality} | 실제소유자 '아니오' + 실제소유자 기재 |
| customer_due_diligence | sparse / no_check | 0.12 / 0.08 | (null) | 이메일·영문명 미기재 / 거래빈도·예상금액·자금원천 체크 누락 |
| corporate_customer_due_diligence | heavy | 0.25 | shareholders[].{name,birth,shares,ratio,relation} | 투자 유치 법인: 주주 12~25명 별지 + 25% 기준 재판정(없으면 2단계 최대주주) → 2쪽 |
| corporate_customer_due_diligence | step3 | 0.1 | (owner_step=3단계) | 지분 확인 불가 → 대표자를 실제소유자로 |
| corporate_customer_due_diligence | agent | 0.15 | agent.{name,rrn,position} | 거래담당자(대리인)란 기재 |
| corporate_customer_due_diligence | sparse / no_check | 0.1 / 0.08 | (null) | 영문명·이메일 미기재 / 상장여부·자금원천·PEP 체크 누락 |
| privacy_consent | heavy | 0.25 | (providers 길어짐) | 제공받는 자 9~15곳(보증기관·국세청·건보공단·감정평가법인 등) → 2쪽 |
| privacy_consent | minor | 0.08 | legal_rep.{name,relation}, sign/seal.legal_rep | 미성년 본인 + 법정대리인 서명 |
| privacy_consent | marketing_unchecked | 0.12 | marketing.* = null, channels [] | 선택 동의란 미체크 |
| account_opening_application | heavy | 0.15 | extra_products[].{type,name,amount,term,account_no} | 같은 날 추가 신규 4~8계좌 |
| account_opening_application | minor | 0.1 | legal_rep.{name,rrn,relation,phone,documents}, sign/seal.legal_rep | 미성년 자녀 계좌를 부모가 개설 |
| account_opening_application | agent | 0.1 | agent.{name,rrn,relation,phone}, sign/seal.agent | 대리인 신규 '해당' (minor 와 배타) |
| account_opening_application | foreigner | 0.08 | customer.nationality | 외국인 고객 (minor·agent 와 배타) |
| account_opening_application | sparse | 0.12 | (null) | 이메일·영문명·우편번호 미기재 |
| financial_transaction_purpose | foreigner | 0.08 | customer.nationality | 외국인 근로자 급여계좌 |
| financial_transaction_purpose | no_evidence | 0.1 | evidence = null | 증빙 미제출 → 금융거래한도계좌 개설 |
| financial_transaction_purpose | no_check | 0.1 | questions.qN = null | 확인사항 체크 누락 |
| overseas_remittance_application | heavy | 0.2 | batch[].{beneficiary,country,bank,account_no,currency,amount,message}, batch_count | 거래처 여러 곳 일괄 송금 별지 6~11건 → 2쪽 (유학 송금 제외) |
| overseas_remittance_application | foreign_worker | 0.12 | (remitter·beneficiary 교체, 사유 국내보수송금) | 외국인 근로자 본국 가족 송금 (본국 은행·SWIFT·시기별 환율) |
| overseas_remittance_application | agent | 0.08 | agent.{name,rrn,relation,phone}, sign/seal.agent | 가족 대리 신청 (foreign_worker 와 배타) |
| overseas_remittance_application | sparse | 0.1 | (null) | 수취인 주소·관계 미기재 |
| fatca_crs | multi_residence | 0.4 (해외거주자일 때) | (residences 2~3건) | 거주관할권 둘 이상 |
| fatca_crs | foreigner | 0.08 | (holder.* 외국인) | 국내 거주 외국인 (미국인이면 FATCA) |
| fatca_crs | no_check | 0.08 | residence_category = null | 해당사항 없음 체크 누락 |
| fatca_crs | sparse | 0.1 | (null) | 연락처·출생국가 미기재 |

FATCA 서명란은 원래 고정 문구였는데 `m.sigspot("holder", ...)` 로 바꿔 sign/seal.holder 가 정답에 생겼다.
financial_transaction_purpose, fatca_crs 는 실제로 여러 쪽이 되는 경우가 드물어 heavy 를 넣지 않았다.
