# 서식 변형 — fx (외환·무역·유학)

무역 서류(상업송장·포장명세서·매매계약서·B/L·수입신고필증)의 변형은 **프로필 단위**로 `docgen/docs/fx.py` 의 `_shipment(p)` 에서 정한다.
변형용 난수는 따로 쓴다(seed `fxv:{p.seed}`). 그래서 기존 값의 난수 흐름은 그대로이고, 같은 고객의 서류끼리 품목·수량·컨테이너·분할선적·신용장·중계무역이 서로 맞는다.
유학 서류(입학허가서·학비 청구서)는 `_study(p)` 에서 seed `studyv:{p.seed}` 로 장학금·조건부 입학·입학 연기를 정한다(학비 청구서의 장학금 공제액 = 입학허가서 장학금).
heavy()/special() 을 쓰므로 `DOCGEN_HEAVY`, `DOCGEN_SPECIAL` 강제 설정이 그대로 먹는다.
영문 서류의 쪽 번호·계속 표시는 영문이다(`Page 1 of 3`, `Continued on next page` 등, `templates/fx/_fx.html.j2`). 둘째 쪽부터 맨 위에 서류명·번호 머리줄이 붙는다(.pg-repeat, 첫 쪽에서는 숨김).
템플릿 전용 표시 옵션(손으로 고친 줄, 부속 목록 여부 등)은 정답이 아니므로 `_Out.opt` 속성에 둔다(데이터 dict 의 키가 아니어서 정답·미표시 경고에 들어가지 않음).

## 프로필 단위 (`_shipment`, `_study`)

| 서류 | 경우 | 확률 | 새 키 | 설명 |
|---|---|---|---|---|
| 무역 공통 | heavy: 품목(라인아이템) 다수 | 0.25 | (items 길어짐) | 상품 2~6종의 색상·사이즈·로트·모델별 줄 20~60개. 물량은 컨테이너 2~9개(용적·중량 기준, 총액 상한 USD 3백만)에 맞춤. 송장·포장명세서·계약서 2~4쪽, 합계는 마지막 쪽 |
| 무역 공통 | 컨테이너 배정 | (heavy·다수 컨테이너일 때) | – | 줄이 충분하면 줄을 차례로 컨테이너에 배정(포장명세서 컨테이너별 소계 = B/L 부속 목록 수치), 아니면 합계를 나눔 |
| 무역 공통 | split_shipment 분할선적 | 0.12 | 송장·포장 `partial_shipment`, `contract_no` | 계약 물량을 2~3회로 나눠 선적, 이번 서류는 그중 한 회차("2ND LOT OF 3 LOTS"). 계약서 수량·금액은 전체(회차 수 배), 선적조항에 회차별 기한 |
| 무역 공통 | lc 신용장 결제 강제 | 0.12 (+원래 결제조건 중 L/C 2/7) | 송장 `lc.{no,date,bank}`, B/L·포장 `lc_no` | 송장 비고 "DRAWN UNDER … L/C NO.", B/L 수하인 TO ORDER OF 개설은행 + 화물란 L/C NO., 수입신고 결제방법 LS/LU |
| 무역 공통 | triangular 중계무역·제3국 결제 (수입만) | 0.1 | 송장 `manufacturer.{name,address}`, `beneficiary_bank.{name,swift,account}`, 계약서 `clauses.manufacturer` | 송장·포장명세서·계약서 판매자 = 홍콩/싱가포르 무역회사, B/L Shipper = 실제 제조사, 대금은 제3국 은행 계좌로. 수입신고 해외거래처 = 중계회사(HK/SG), 적출국 = 제조국 |
| 무역 공통 | 운임 후불 | (FOB/FCA 이면 항상) | `freight`, `freight_payable_at` | 기존: FREIGHT COLLECT, 도착지 지불 |
| 입학·학비 | scholarship 장학금 | 0.25 | 입학 `scholarship.{name,amount}`, 학비 items 공제 줄 | 학기당 금액. 학비 청구서 Payments/Credits 에 같은 금액 공제 |
| 입학 | conditional 조건부 입학 | 0.15 | `admission_type`, `conditions[]`, `condition_deadline` | 제목 "LETTER OF CONDITIONAL ADMISSION", 영어성적·졸업증명·선수과목·Pre-sessional 조건 상자 |
| 입학 | deferred 입학 연기 | 0.06 | `deferred_from` | 1년 전 학기에서 연기 승인 문장 |

## 서류 단위

| 서류 | 경우 | 확률 | 새 키 | 설명 |
|---|---|---|---|---|
| 상업송장 | 여러 쪽 | heavy 따라 | – | Marks 칸 rowspan 제거(줄 단위로 나뉨), 품목 많으면 MODEL 을 괄호로 한 줄에. 머리글 줄 반복 |
| 상업송장 | price_breakdown CIF 가격 구성 | 0.3 (CIF 만) | `price_breakdown.{fob,freight,insurance}` | 합계 위에 FOB VALUE / OCEAN FREIGHT / INSURANCE PREMIUM |
| 상업송장 | 비고 계약번호 | 0.35 (분할·중계면 항상) | `contract_no` | |
| 포장명세서 | by_container 컨테이너별 구분 | 0.6 (컨테이너 2개 이상, 줄 배정이 있을 때) | `containers[].{no,seal,packages,net_weight,gross_weight,measurement}` | "CONTAINER NO. / SEAL NO." 구분줄과 SUB-TOTAL 줄 |
| 매매계약서 | heavy: 일반거래조건 12~20조 | 0.3 | `gtc_terms.{qty_tolerance,late_penalty,inspection_days,claim_days,warranty,late_interest,governing_law}` (쓰인 조항만) | "GENERAL TERMS AND CONDITIONS" 별첨, 조항 번호 직접 표기(쪽이 나뉘어도 이어짐) |
| 매매계약서 | price_amend 단가 손 정정 | 0.12 | (`corrected`) | 한 줄 단가를 두 줄 긋고 손글씨로 바른 값 + 이니셜 정정 도장(매수 서명인 이니셜). 정답은 바른 값 |
| 매매계약서 | hand_filled 서명란 손글씨 | 0.3 | `buyer.sign_date`, (`corrected` fix 0.05~0.08) | 매수인 이름·직위·서명일 파란 손글씨, 정정 효과 |
| 매매계약서 | 서명 | sigspot | `sign.buyer`, `sign.seller` | 서명/빈칸(도장 없음). 서명일 `buyer.sign_date`, `seller.sign_date` 새로 표시 |
| B/L | heavy/다수 컨테이너: 부속 목록 | 컨테이너 4개 이상 또는 heavy 이며 2개 이상 | `containers[].{packages,gross_weight,measurement}` | 본문에 "AS PER ATTACHED SHEET", 다음 쪽 "ATTACHED SHEET"(컨테이너·씰·타입·포장수·중량·용적·합계) |
| B/L | 화물 요약 | – | `description` | 같은 상품 줄은 상품별 수량 합으로 묶음 |
| B/L | freight_charges 운임 명세 | 0.25 | `charges[].{name,quantity,rate,per,prepaid/collect}` | O/F, BAF, LSS, THC 요율표. Freight & Charges 칸 "AS PER BELOW" |
| B/L | surrender 서렌더 | 0.2 (기명식, 신용장 아님) | `surrender`, `surrender_date` | 화물란 위 빨간 이중 테두리 "SURRENDERED" 스탬프 + 일자 |
| B/L | sea_waybill 해상화물운송장 | 0.06 (기명식, 서렌더 아님) | `document_type`, `originals` = ZERO (0) | 제목 SEA WAYBILL, 하단 NON-NEGOTIABLE |
| 수입신고필증 | 란 구성 변경 | 항상 | `items[].specs[].{no,model,quantity,unit_price,amount}` (기존 `items[].model/quantity/unit_price/amount` 대체) | 란 = 세번부호(상품)별, 란 안에 규격 줄 01, 02 … 모든 란을 표시(전에는 3란만). 여러 쪽이면 머리줄(신고번호) 반복, 쪽 표기 "Page : 1/2" |
| 수입신고필증 | heavy | 프로필 heavy | – | 2~6란, 란마다 규격 줄 3~20개, 2~3쪽 |
| 수입신고필증 | duty_reduction 관세 감면 | 0.12 (FTA 아니고 관세율 > 0 인 란) | `items[].reduction.{rate,code,amount}` | (47)감면율, (49)감면분납부호/감면액, 세액은 감면 후, 부가세 과표도 감면 후 관세 기준 |
| 수입신고필증 | amended 수리 후 정정 | 0.1 | `amendment.{date,reason}` | 세관기재란에 정정승인일자·정정사유 |
| 입학허가서 | heavy: 예상 비용 + Next Steps | 0.2 | `cost.{tuition,living,insurance,books,total}` | 1년 예상 학비·생활비 표 + 입학 절차 9단계, 2쪽(아래 꼬리말은 쪽마다) |
| 입학허가서 | cost_estimate 예상 비용 표 | 0.25 | `cost.*` | 표만 |
| 학비 청구서 | heavy: 과목별 등록금·수수료 다수 | 0.25 | (items 길어짐) | 과목별(학점) 등록금 4~6줄 + 수수료 6~10줄 더, 2쪽. 결제 안내 상자는 통째로 넘어감 |
| 학비 청구서 | installment 분할납부 | 0.15 | `installments[].{no,due_date,amount}`, `amount_due_now` | Payment Plan Enrollment Fee 줄 + 3~5회 월별 납부 일정표 |
| 학비 청구서 | payment_received 일부 선납 | 0.15 | items 공제 줄 | "Payment Received - International Wire (Ref. …)" |

## 메모
- 수입신고필증 감면부호(Y4570 등)와 정정 표기 위치는 단순화한 추정이다. 실제 감면부호 체계는 관세청 부호표를 따른다.
- 일반거래조건 문구는 국내 무역계약 표준 조항을 요약한 것이다.
- 기존 학비 청구서의 무작위 장학금(0.3)은 프로필 단위 장학금으로 바꿨다.
- 중계무역 회사명·주소는 가상이다(실존 건물명 사용 안 함).
