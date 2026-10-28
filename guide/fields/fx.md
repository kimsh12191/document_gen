# 외환·무역 — 서류별 항목

키 규칙과 타입은 [README.md](README.md)에 있습니다.


## 상업송장(Commercial Invoice) (`commercial_invoice`) — 키 37개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `shipper.name` | Shipper/Exporter | text | 100% | Mekong Garment JSC |
| `shipper.address` | ShipperAddress | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `invoice_no` | InvoiceNo | text | 100% | MGJ-2512-054 |
| `invoice_date` | InvoiceDate | date | 100% | 30 DEC 2025 |
| `consignee.name` | Consignee | text | 100% | UNION TRADING CO., LTD. |
| `consignee.address` | ConsigneeAddress | text | 100% | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361… |
| `notify` | NotifyParty | text | 100% | SAME AS ABOVE |
| `terms.delivery` | TermsofDelivery | text | 100% | FOB HO CHI MINH CITY (CAT LAI), VIETNAM … |
| `terms.payment` | TermsofPayment | text | 100% | T/T 60 DAYS AFTER B/L DATE |
| `origin` | CountryofOrigin | text | 100% | VIETNAM |
| `port_of_loading` | PortofLoading | text | 100% | HO CHI MINH CITY (CAT LAI), VIETNAM |
| `final_destination` | FinalDestination | text | 100% | BUSAN, KOREA |
| `carrier` | Carrier | text | 100% | CORAL VOYAGER V.126S |
| `sailing_date` | Sailingonorabout | date | 100% | 01 JAN 2026 |
| `marks` | MarksandNumbers | text | 100% | UNION BUSAN, KOREA C/NO. 1-488 MADE IN V… |
| `items[].description` | DescriptionofGoods | text | 100% | Men's Cotton Crew Neck T-Shirt |
| `items[].model` | Model | text | 100% | MT-277A |
| `items[].quantity` | Quantity/Unit | text | 100% | 18,100 PCS |
| `items[].unit_price` | Unit-price | amount | 100% | USD 3.70 |
| `items[].amount` | Amount | amount | 100% | USD 66,970.00 |
| `total_quantity` | TotalPackages | text | 100% | 488 CTNS |
| `total_amount` | TotalAmount | amount | 100% | USD 193,394.30 |
| `signed_by` | Signedby | text | 100% | Mekong Garment JSC |
| `signer` | Signer | text | 100% | Nguyen Van An |
| `contract_no` | ContractNo | text | 37% | HAN-SC-25529 |
| `lc.no` | L/CNo | text | 50% | M45972508NU76564 |
| `lc.date` | L/CDate | date | 50% | 09 JUL 2025 |
| `lc.bank` | L/CIssuingBank | text | 50% | INDUSTRIAL BANK OF KOREA |
| `manufacturer.name` | Manufacturer | text | 7% | Mekong Garment JSC |
| `manufacturer.address` | ManufacturerAddress | text | 7% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `beneficiary_bank.name` | BeneficiaryBank | text | 7% | BANK OF CHINA (HONG KONG) LIMITED |
| `beneficiary_bank.swift` | BeneficiaryBankSWIFT | text | 7% | BKCHHKHH |
| `beneficiary_bank.account` | BeneficiaryAccountNo | account_no | 7% | 799-657998-874 |
| `price_breakdown.fob` | FOBValue | amount | 3% | USD 142,545.17 |
| `price_breakdown.freight` | OceanFreight | amount | 3% | USD 7,240.21 |
| `price_breakdown.insurance` | InsurancePremium | amount | 3% | USD 115.42 |
| `partial_shipment` | PartialShipment | text | 7% | 1ST LOT OF 2 LOTS |

## 무역 매매계약서(Sales Contract) (`trade_contract`) — 키 42개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `seller.name` | Seller | text | 100% | Mekong Garment JSC |
| `seller.address` | SellerAddress | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `buyer.name` | Buyer | text | 100% | UNION TRADING CO., LTD. |
| `buyer.address` | BuyerAddress | text | 100% | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361… |
| `contract_no` | ContractNo | text | 100% | MGJ-SC-25461 |
| `contract_date` | Date | date | 100% | November 10, 2025 |
| `items[].description` | Commodity&Description | text | 100% | Men's Cotton Crew Neck T-Shirt |
| `items[].model` | Model | text | 100% | MT-277A |
| `items[].quantity` | Quantity | text | 100% | 18,100 PCS |
| `items[].unit_price` | UnitPrice | amount | 100% | USD 3.70 |
| `items[].amount` | Amount | amount | 100% | USD 66,970.00 |
| `total_amount` | TotalAmount | amount | 100% | USD 193,394.30 |
| `total_words` | TotalAmountinWords | text | 100% | SAY US DOLLARS ONE HUNDRED NINETY THREE … |
| `clauses.price_terms` | PriceTerms | text | 100% | FOB HO CHI MINH CITY (CAT LAI), VIETNAM … |
| `clauses.origin` | Origin | text | 100% | Vietnam |
| `clauses.packing` | Packing | text | 100% | Export standard packing in cartons, suit… |
| `clauses.shipping_mark` | ShippingMark | text | 100% | UNION BUSAN, KOREA C/NO. 1-UP MADE IN VI… |
| `clauses.shipment` | Shipment | text | 100% | Not later than January 09, 2026. Partial… |
| `clauses.port_of_shipment` | PortofShipment | text | 100% | HO CHI MINH CITY (CAT LAI), VIETNAM |
| `clauses.destination` | Destination | text | 100% | BUSAN, KOREA |
| `clauses.payment` | Payment | text | 100% | By telegraphic transfer within 60 days a… |
| `clauses.inspection` | Inspection | text | 100% | Inspection by an independent surveyor (S… |
| `clauses.arbitration` | Arbitration | text | 100% | Any dispute shall be settled by arbitrat… |
| `seal.buyer` | BuyerSignature | seal | 100% |  |
| `sign.buyer` | BuyerSignature | signature | 100% | Akira Tanaka |
| `buyer.signer` | BuyerSignatory | text | 100% | Park Chanyeon |
| `buyer.title` | BuyerTitle | text | 100% | Representative Director |
| `buyer.sign_date` | BuyerSigningDate | date | 100% | 13 NOV 2025 |
| `seal.seller` | SellerSignature | seal | 100% |  |
| `sign.seller` | SellerSignature | signature | 100% | Nguyen Van An |
| `seller.signer` | SellerSignatory | text | 100% | Nguyen Van An |
| `seller.title` | SellerTitle | text | 100% | Export Manager |
| `seller.sign_date` | SellerSigningDate | date | 100% | 10 NOV 2025 |
| `clauses.insurance` | Insurance | text | 27% | To be covered by the Seller for 110% of … |
| `gtc_terms.late_penalty` | LateShipmentPenalty | percent | 30% | 1% |
| `gtc_terms.inspection_days` | InspectionPeriod(days) | number | 30% | 21 |
| `gtc_terms.warranty` | WarrantyPeriod | text | 37% | eighteen (18) months |
| `gtc_terms.late_interest` | LatePaymentInterest | percent | 37% | 6% |
| `gtc_terms.governing_law` | GoverningLaw | text | 30% | the State of New York, U.S.A. |
| `gtc_terms.qty_tolerance` | QuantityTolerance | percent | 33% | 3% |
| `gtc_terms.claim_days` | ClaimPeriod(days) | number | 27% | 90 |
| `clauses.manufacturer` | Manufacturer | text | 7% | Mekong Garment JSC, 45 Le Loi St, Distri… |

## 선하증권(B/L) (`bill_of_lading`) — 키 46개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `shipper.name` | Shipper | text | 100% | Mekong Garment JSC |
| `shipper.address` | ShipperAddress | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `booking_no` | BookingNo | text | 100% | BKG3185811 |
| `bl_no` | B/LNo | text | 100% | OCLN15701972 |
| `carrier` | Carrier | text | 100% | OCEANLINK CONTAINER LINES |
| `forwarder` | ForwardingAgent | text | 100% | Daon Logistics Co., Ltd. |
| `consignee.name` | Consignee | text | 100% | UNION TRADING CO., LTD. |
| `consignee.address` | ConsigneeAddress | text | 37% | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361… |
| `notify.name` | NotifyParty | text | 100% | SAME AS CONSIGNEE |
| `pre_carriage` | Pre-carriageby | text | 100% | TRUCK |
| `place_of_receipt` | PlaceofReceipt | text | 100% | HO CHI MINH CITY (CAT LAI) CY |
| `origin` | PointandCountryofOrigin | text | 100% | VIETNAM |
| `vessel_voyage` | OceanVessel/VoyNo | text | 100% | CORAL VOYAGER 126S |
| `port_of_loading` | PortofLoading | text | 100% | HO CHI MINH CITY (CAT LAI), VIETNAM |
| `port_of_discharge` | PortofDischarge | text | 100% | BUSAN, KOREA |
| `place_of_delivery` | PlaceofDelivery | text | 100% | BUSAN CY |
| `containers[].no` | ContainerNo | text | 100% | OCLU1212140 |
| `containers[].type` | ContainerType | text | 100% | 40'HC |
| `containers[].seal` | SealNo | text | 100% | H388222 |
| `marks` | MarksandNumbers | text | 100% | UNION BUSAN, KOREA C/NO. 1-488 MADE IN V… |
| `container_count` | No.ofContainers | text | 100% | 1 X 40'HC |
| `packages` | No.ofPackages | text | 100% | 488 CTNS |
| `description` | DescriptionofGoods | text | 100% | Men's Cotton Crew Neck T-Shirt  18,100 P… |
| `freight` | Freight | text | 100% | FREIGHT COLLECT |
| `gross_weight` | GrossWeight | text | 100% | 9,381.96 KGS |
| `measurement` | Measurement | text | 100% | 49.050 CBM |
| `total_words` | TotalNumberinWords | text | 100% | SAY: ONE (1) CONTAINER ONLY |
| `freight_payable_at` | FreightPayableat | text | 100% | BUSAN |
| `issue_place` | PlaceofIssue | text | 100% | HO CHI MINH CITY (CAT LAI) |
| `issue_date` | DateofIssue | date | 100% | 01 JAN 2026 |
| `originals` | NumberofOriginalB/L | text | 100% | THREE (3) |
| `on_board_date` | OnBoardDate | date | 100% | 01 JAN 2026 |
| `document_type` | DocumentType | text | 3% | SEA WAYBILL |
| `surrender` | Surrender | text | 7% | SURRENDERED |
| `surrender_date` | SurrenderDate | date | 7% | 18 AUG 2025 |
| `containers[].packages` | ContainerPackages | text | 30% | 1,571 PKGS |
| `containers[].gross_weight` | ContainerGrossWeight | number | 30% | 41,420.40 |
| `containers[].measurement` | ContainerMeasurement | number | 30% | 44.735 |
| `notify.address` | NotifyPartyAddress | text | 63% | 13F, DN SQUARE, 499 HWAUN-RO, SEO-GU, GW… |
| `lc_no` | L/CNo | text | 50% | M45972508NU76564 |
| `charges[].name` | Charge | text | 27% | OCEAN FREIGHT |
| `charges[].quantity` | RevenueTons | number | 27% | 2.00 |
| `charges[].rate` | Rate | number | 27% | 3,300.00 |
| `charges[].per` | Per | text | 27% | CNTR |
| `charges[].collect` | Collect | amount | 10% | USD 6,600.00 |
| `charges[].prepaid` | Prepaid | amount | 27% | USD 280.00 |

## 포장명세서(Packing List) (`packing_list`) — 키 36개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `shipper.name` | Shipper/Exporter | text | 100% | Mekong Garment JSC |
| `shipper.address` | ShipperAddress | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `invoice_no` | InvoiceNo | text | 100% | MGJ-2512-054 |
| `invoice_date` | InvoiceDate | date | 100% | 30 DEC 2025 |
| `consignee.name` | Consignee | text | 100% | UNION TRADING CO., LTD. |
| `consignee.address` | ConsigneeAddress | text | 100% | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361… |
| `contract_no` | ContractNo | text | 53% | MGJ-SC-25461 |
| `notify` | NotifyParty | text | 100% | SAME AS CONSIGNEE |
| `port_of_loading` | PortofLoading | text | 100% | HO CHI MINH CITY (CAT LAI), VIETNAM |
| `final_destination` | FinalDestination | text | 100% | BUSAN, KOREA |
| `carrier` | Carrier | text | 100% | CORAL VOYAGER V.126S |
| `sailing_date` | Sailingonorabout | date | 100% | January 01, 2026 |
| `marks` | MarksandNumbers | text | 100% | UNION BUSAN, KOREA C/NO. 1-488 MADE IN V… |
| `items[].ctn_no` | C/TNo | text | 100% | 1-181 |
| `items[].description` | DescriptionofGoods | text | 100% | Men's Cotton Crew Neck T-Shirt |
| `items[].packages` | Packages | text | 100% | 181 CTNS |
| `items[].quantity` | Quantity | text | 100% | 18,100 PCS |
| `items[].net_weight` | NetWeight | number | 100% | 3,258.00 |
| `items[].gross_weight` | GrossWeight | number | 100% | 3,518.64 |
| `items[].measurement` | Measurement | number | 100% | 16.290 |
| `total.packages` | TotalPackages | text | 100% | 488 CTNS |
| `total.net_weight` | TotalNetWeight | text | 100% | 8,687.00 KGS |
| `total.gross_weight` | TotalGrossWeight | text | 100% | 9,381.96 KGS |
| `total.measurement` | TotalMeasurement | text | 100% | 49.050 CBM |
| `signed_by` | Signedby | text | 100% | Mekong Garment JSC |
| `signer` | Signer | text | 100% | Nguyen Van An |
| `containers[].no` | ContainerNo | text | 20% | TPMU9280511 |
| `containers[].seal` | SealNo | text | 20% | SL436094 |
| `containers[].packages` | ContainerPackages | text | 20% | 409 PKGS |
| `containers[].net_weight` | ContainerNetWeight | number | 20% | 15,244.00 |
| `containers[].gross_weight` | ContainerGrossWeight | number | 20% | 15,653.52 |
| `containers[].measurement` | ContainerMeasurement | number | 20% | 51.260 |
| `lc_no` | L/CNo | text | 50% | M45972508NU76564 |
| `manufacturer.name` | Manufacturer | text | 7% | Mekong Garment JSC |
| `manufacturer.address` | ManufacturerAddress | text | 7% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `partial_shipment` | PartialShipment | text | 7% | 1ST LOT OF 2 LOTS |

## 수입신고필증 (`import_declaration`) — 키 67개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `decl_no` | 신고번호 | text | 100% | 20097-26-7868647U |
| `decl_date` | 신고일 | date | 100% | 2026/01/10 |
| `customs` | 세관.과 | text | 100% | 030-17 |
| `arrival_date` | 입항일 | date | 100% | 2026/01/09 |
| `bl_no` | B/L번호 | text | 100% | OCLN15701972 |
| `cargo_no` | 화물관리번호 | text | 100% | 26OCLN610441I-2996-002 |
| `warehouse_date` | 반입일 | date | 100% | 2026/01/10 |
| `collection_type` | 징수형태 | number | 100% | 11 |
| `declarant` | 신고인 | text | 100% | 대한관세법인 정채유 |
| `importer.name` | 수입자 | text | 100% | (주)유니온무역 |
| `importer.code` | 수입자통관고유부호 | text | 100% | 유니온무8255080 |
| `taxpayer.code` | 납세의무자통관고유부호 | text | 100% | 유니온무8255080 |
| `taxpayer.address` | 납세의무자주소 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `taxpayer.name` | 납세의무자상호 | text | 100% | (주)유니온무역 |
| `taxpayer.ceo` | 납세의무자성명 | text | 100% | 박찬연 |
| `taxpayer.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `forwarder` | 운송주선인 | text | 100% | DAON LOGISTICS CO., LTD. |
| `supplier` | 해외거래처 | text | 100% | MEKONG GARMENT JSC (VN) |
| `clearance_plan` | 통관계획 | text | 100% | D 보세구역장치후 |
| `origin_cert` | 원산지증명서유무 | text | 100% | Y |
| `total_weight` | 총중량 | text | 100% | 9,382 KG |
| `total_packages` | 총포장갯수 | text | 100% | 488 CT |
| `arrival_port` | 국내도착항 | text | 100% | KRPUS 부산항 |
| `transport` | 운송형태 | text | 100% | 10 FCL |
| `export_country` | 적출국 | text | 100% | VN VIETNAM |
| `vessel` | 선기명 | text | 100% | CORAL VOYAGER |
| `master_bl` | MASTERB/L번호 | text | 100% | OCLN15701972 |
| `carrier_code` | 운수기관부호 | text | 100% | OCLN |
| `inspection_place` | 검사(반입)장소 | text | 100% | 03055276-55499004 부산신항국제터미널 |
| `items[].line_no` | 란번호 | number | 100% | 001 |
| `line_total` | 총란수 | amount | 100% | 003 |
| `items[].std_name` | 품명 | text | 100% | T-SHIRTS, KNITTED, OF COTTON |
| `items[].trade_name` | 거래품명 | text | 100% | MEN'S COTTON CREW NECK T-SHIRT |
| `items[].specs[].no` | 규격번호 | number | 100% | 01 |
| `items[].specs[].model` | 모델·규격 | text | 100% | MT-277A |
| `items[].specs[].quantity` | 수량 | text | 100% | 18,100 PCS |
| `items[].specs[].unit_price` | 단가 | amount | 100% | 3.70 |
| `items[].specs[].amount` | 금액 | amount | 100% | 66,970.00 |
| `items[].hs_code` | 세번부호 | text | 100% | 6109.10-0000 |
| `items[].net_weight` | 순중량 | text | 100% | 3,258.0 KG |
| `items[].taxable_usd` | 과세가격(USD) | amount | 100% | $67,865 |
| `items[].taxable_krw` | 과세가격(원화) | amount | 100% | ₩98,445,056 |
| `items[].origin` | 원산지 | text | 100% | VN-B-Y |
| `items[].duty_type` | 세종 | text | 100% | 관 |
| `items[].duty_rate` | 관세율 | text | 100% | 0.00(FVN1) |
| `items[].duty_amount` | 관세액 | amount | 100% | 0 |
| `items[].vat_rate` | 부가세율 | text | 100% | 10.00(A) |
| `items[].vat_amount` | 부가세액 | amount | 100% | 9,844,500 |
| `payment` | 결제금액 | text | 100% | FOB-USD-193,394.30-TT |
| `exchange_rate` | 환율 | number | 100% | 1,450.60 |
| `total_taxable` | 총과세가격 | amount | 100% | ₩284,287,194 |
| `freight` | 운임 | amount | 100% | ₩3,553,041 |
| `vat_base` | 부가가치세과표 | amount | 100% | ₩284,287,194 |
| `insurance` | 보험료 | amount | 100% | ₩196,382 |
| `tax.duty` | 관세 | amount | 100% | 0 |
| `customs_office` | 세관 | text | 100% | 부산세관 |
| `officer` | 담당자 | text | 100% | 이도경 |
| `receipt_datetime` | 접수일시 | datetime | 100% | 2026/01/10 12:33 |
| `accept_date` | 수리일자 | date | 100% | 2026/01/11 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 세관장인 |
| `tax.vat` | 부가세 | amount | 100% | 28,428,700 |
| `tax.total` | 총세액합계 | amount | 100% | 28,428,700 |
| `amendment.date` | 정정승인일자 | date | 10% | 2026/04/03 |
| `amendment.reason` | 정정사유 | text | 10% | (42)원산지표시 정정 |
| `items[].reduction.rate` | 감면율 | number | 3% | 50.00 |
| `items[].reduction.code` | 감면분납부호 | text | 3% | Y8010 |
| `items[].reduction.amount` | 감면액 | amount | 3% | 12,607,110 |

## 입학허가서(Letter of Admission) (`admission_letter`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `university.name` | University | text | 100% | Westlake State University |
| `university.office` | Office | text | 100% | Office of Graduate Admissions |
| `university.address` | UniversityAddress | text | 100% | 1800 Lakeview Dr, Seattle, WA 98105, USA |
| `university.email` | Email | text | 100% | admissions@westlakestate.edu |
| `letter_date` | Date | date | 100% | December 05, 2025 |
| `student.name` | StudentName | text | 100% | Chanyeon Park |
| `student.address` | StudentAddress | text | 100% | Apt. 110-501, 524 Bangbae-ro, Seocho-gu,… |
| `admission_type` | AdmissionType | text | 13% | CONDITIONAL ADMISSION |
| `term` | TermofEntry | text | 100% | Fall 2026 |
| `student.birth` | DateofBirth | date | 100% | 10 FEB 1990 |
| `student.nationality` | Citizenship | text | 100% | Republic of Korea |
| `student.id` | StudentID | text | 100% | M94946101 |
| `program` | Program | text | 100% | Education |
| `degree` | Degree | text | 100% | Master of Education (M.Ed.) |
| `start_date` | ClassesBegin | date | 100% | August 25, 2026 |
| `duration` | Duration | text | 100% | 2 years (full-time) |
| `condition_deadline` | ConditionDeadline | date | 13% | July 20, 2026 |
| `conditions[]` | Condition | text | 13% | Submission of an official TOEFL iBT scor… |
| `deposit_deadline` | DepositDeadline | date | 100% | December 31, 2025 |
| `signer` | Signedby | text | 100% | Emily R. Watson |
| `signer_title` | Title | text | 100% | Director of Admissions |
| `cost.tuition` | EstimatedTuition | number | 43% | $56,000.00 |
| `cost.living` | EstimatedLivingExpenses | number | 43% | $22,000.00 |
| `cost.insurance` | EstimatedHealthInsurance | number | 43% | $3,120.00 |
| `cost.books` | EstimatedBooksandSupplies | number | 43% | $1,620.00 |
| `cost.total` | TotalEstimatedCost | amount | 43% | $82,740.00 |
| `scholarship.name` | Scholarship | text | 23% | International Student Award |
| `scholarship.amount` | ScholarshipAmount | text | 23% | $8,860.00 per semester |
| `deferred_from` | DeferredFrom | text | 7% | Spring 2025 |

## 학비 청구서(Tuition Invoice) (`tuition_invoice`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `university.name` | University | text | 100% | Westlake State University |
| `university.office` | Office | text | 100% | Student Financial Services |
| `university.address` | UniversityAddress | text | 100% | 1800 Lakeview Dr, Seattle, WA 98105, USA |
| `student.name` | StudentName | text | 100% | Chanyeon Park |
| `student.id` | StudentID | text | 100% | M94946101 |
| `student.program` | Program | text | 100% | Master of Education (M.Ed.) in Education |
| `invoice_no` | InvoiceNo | text | 100% | INV-2026368927 |
| `invoice_date` | InvoiceDate | date | 100% | December 31, 2025 |
| `term` | Term | text | 100% | Fall 2026 |
| `items[].date` | Date | date | 100% | 12/30/2025 |
| `items[].description` | Description | text | 100% | Tuition - Full-time Graduate |
| `items[].charge` | Charges | amount | 100% | $17,430.00 |
| `items[].credit` | Payments/Credits | amount | 50% | $1,000.00 |
| `summary.previous_balance` | PreviousBalance | amount | 100% | $0.00 |
| `summary.charges` | NewCharges | amount | 100% | $21,032.00 |
| `summary.credits` | Payments/Credits | amount | 100% | $10,400.00 |
| `total` | TotalAmountDue | amount | 100% | USD 10,632.00 |
| `due_date` | DueDate | date | 100% | August 03, 2026 |
| `bank.beneficiary` | Beneficiary | text | 100% | Westlake State University |
| `bank.bank_name` | BankName | text | 100% | Bank of America, N.A. |
| `bank.swift` | SWIFT | text | 100% | BOFAUS3N |
| `bank.account` | AccountNumber | account_no | 100% | 212604946606 |
| `bank.routing_label` | RoutingLabel | text | 100% | ABA Routing No. |
| `bank.routing` | RoutingNumber | number | 100% | 036941220 |
| `bank.reference` | PaymentReference | text | 100% | M94946101 Chanyeon Park |
| `amount_due_now` | AmountDueNow | amount | 3% | £2,247.25 |
| `installments[].no` | InstallmentNo | number | 3% | 1 |
| `installments[].due_date` | InstallmentDueDate | date | 3% | January 01, 2026 |
| `installments[].amount` | InstallmentAmount | amount | 3% | £2,247.25 |
