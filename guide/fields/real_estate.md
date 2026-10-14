# 부동산 — 서류별 항목

키 규칙과 타입은 [README.md](README.md)에 있습니다.


## 등기사항전부증명서(집합건물) (`real_estate_registry`) — 키 84개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `property` | 부동산의표시 | text | 100% | 경기도 수원시 영통구 원천동 87 한신휴플러스에듀포레 제115동 제21층… |
| `unique_no` | 고유번호 | text | 100% | 1792-2013-094176 |
| `buildings[].display_no` | 표시번호 | number | 80% | 1 |
| `buildings[].receipt` | 접수 | date | 80% | 1994년11월4일 |
| `buildings[].location` | 소재지번,건물명칭및번호 | text | 80% | 경기도 수원시 영통구 원천동 87 한신휴플러스에듀포레 제115동 |
| `buildings[].detail` | 건물내역 | text | 80% | 철근콘크리트구조 (철근)콘크리트지붕 21층 공동주택(아파트) 지하1층 1… |
| `buildings[].cause` | 등기원인및기타사항 | text | 80% | 도면편철장 제8책 제698장 |
| `land.display_no` | 표시번호 | number | 80% | 1 |
| `land.location` | 소재지번 | text | 80% | 1. 경기도 수원시 영통구 원천동 87 |
| `land.category` | 지목 | text | 80% | 대 |
| `land.area` | 면적 | text | 80% | 31,054.7㎡ |
| `land.cause` | 등기원인및기타사항 | text | 80% | 1994년11월4일 등기 |
| `unit.display_no` | 표시번호 | number | 80% | 1 |
| `unit.receipt` | 접수 | date | 80% | 1994년11월4일 |
| `unit.unit_no` | 건물번호 | text | 80% | 제21층 제2104호 |
| `unit.detail` | 건물내역 | text | 80% | 철근콘크리트구조 101.84㎡ |
| `unit.cause` | 등기원인및기타사항 | text | 80% | 도면편철장 제8책 제698장 |
| `land_right.display_no` | 표시번호 | number | 80% | 1 |
| `land_right.kind` | 대지권종류 | text | 80% | 1 소유권대지권 |
| `land_right.ratio` | 대지권비율 | text | 80% | 31,054.7분의 54.47 |
| `land_right.cause` | 등기원인및기타사항 | text | 80% | 1994년10월19일 대지권 1994년11월4일 등기 |
| `gapgu[].rank` | 순위번호 | number | 80% | 1 |
| `gapgu[].purpose` | 등기목적 | text | 80% | 소유권보존 |
| `gapgu[].receipt` | 접수 | text | 80% | 1994년11월4일 제30434호 |
| `gapgu[].holder.role` | 권리자구분 | text | 80% | 소유자 |
| `gapgu[].holder.name` | 소유자 | text | 80% | 주식회사쌍용건설 |
| `gapgu[].holder.reg_no` | 등록번호 | text | 80% | 171512-4430096 |
| `gapgu[].holder.address` | 주소 | text | 80% | 경기도 수원시 영통구 시청로 108 |
| `gapgu[].cause` | 등기원인 | text | 80% | 2020년1월13일 매매 |
| `gapgu[].holder.note` | 거래가액 | text | 63% | 거래가액 금410,000,000원 |
| `eulgu[].rank` | 순위번호 | number | 70% | 1 |
| `eulgu[].purpose` | 등기목적 | text | 70% | 근저당권설정 |
| `eulgu[].receipt` | 접수 | text | 70% | 2020년2월18일 제40565호 |
| `eulgu[].cause` | 등기원인 | text | 70% | 2020년2월18일 설정계약 |
| `eulgu[].max_amount` | 채권최고액 | amount | 67% | 금318,000,000원 |
| `eulgu[].debtor` | 채무자 | text | 67% | 박기우 |
| `eulgu[].debtor_address` | 채무자주소 | text | 67% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `eulgu[].mortgagee` | 근저당권자 | text | 67% | 주식회사우리은행 171511-7786133 |
| `eulgu[].mortgagee_address` | 근저당권자주소 | text | 67% | 서울특별시 중구 소공로 51 (송도지점) |
| `registry_office` | 관할등기소 | text | 80% | 수원지방법원 등기과 |
| `view_datetime` | 열람일시 | datetime | 47% | 2026년01월31일 15시31분14초 |
| `gapgu[].holders[].role` | 권리자구분 | text | 17% | 공유자 |
| `gapgu[].holders[].share` | 지분 | text | 17% | 지분 2분의 1 |
| `gapgu[].holders[].name` | 공유자 | text | 17% | 반원인 |
| `gapgu[].holders[].reg_no` | 등록번호 | text | 17% | 580519-******* |
| `gapgu[].holders[].address` | 주소 | text | 17% | 대구광역시 수성구 수성로 401, 107동 2004호 (지산동, 센트레빌… |
| `gapgu[].note` | 거래가액 | text | 13% | 거래가액 금470,000,000원 |
| `gapgu[].claim_amount` | 청구금액 | amount | 30% | 금4,134,361원 |
| `gapgu[].creditor` | 채권자 | text | 33% | 주식회사삼성카드 130111-2186484 |
| `gapgu[].creditor_address` | 채권자주소 | text | 33% | 서울특별시 중구 국제금융로 331 |
| `fee` | 수수료 | amount | 43% | 1,000원 |
| `issue_date` | 발행일 | date | 43% | 2025년 5월 19일 |
| `seal.issuer` | 발급기관직인 | seal | 43% | 전산운영책임관인 |
| `issue_no` | 발행번호 | number | 53% | 88889704605527375125 |
| `confirm_no` | 발급확인번호 | text | 53% | NTOZ-IUSA-4727 |
| `issue_date_short` | 발행일 | date | 53% | 2025/05/19 |
| `eulgu[].deposit` | 전세금 | amount | 17% | 금345,000,000원 |
| `eulgu[].rent` | 차임 | text | 13% | 없음 |
| `eulgu[].scope` | 범위 | text | 17% | 주거용 건물의 전부 |
| `eulgu[].contract_date` | 임대차계약일자 | date | 13% | 2012년9월4일 |
| `eulgu[].resident_date` | 주민등록일자 | date | 13% | 2012년10월6일 |
| `eulgu[].possession_date` | 점유개시일자 | date | 13% | 2012년10월6일 |
| `eulgu[].fixed_date` | 확정일자 | date | 13% | 2012년10월7일 |
| `eulgu[].lessee` | 임차권자 | text | 13% | 박윤성 880417-******* |
| `eulgu[].lessee_address` | 임차권자주소 | text | 13% | 전라남도 여수시 좌수영로 575, 105동 604호 (문수동, 현대파크) |
| `summary.owners[].name` | 등기명의인 | text | 20% | 이민빈 (소유자) |
| `summary.owners[].reg_no` | (주민)등록번호 | text | 20% | 720524-******* |
| `summary.owners[].share` | 최종지분 | text | 20% | 단독소유 |
| `summary.owners[].address` | 주소 | text | 20% | 서울특별시 마포구 월드컵로 491-5, 118동 1203호 (상암동, e… |
| `summary.owners[].rank` | 순위번호 | number | 20% | 4 |
| `summary.rights[].rank` | 순위번호 | number | 13% | 1 |
| `summary.rights[].purpose` | 등기목적 | text | 13% | 근저당권설정 |
| `summary.rights[].receipt` | 접수정보 | text | 13% | 2025년6월21일 제78131호 |
| `summary.rights[].main` | 주요등기사항 | text | 13% | 채권최고액 금361,000,000원  근저당권자 중소기업은행 |
| `summary.rights[].target_owner` | 대상소유자 | text | 13% | 이민빈 |
| `page_label` | 쪽번호 | text | 20% | 2/2 |
| `gapgu[].change` | 변경사항 | text | 13% | 김태유의 주소 세종특별자치시 갈매로 202, 123동 2504호 (보람동… |
| `eulgu[].change` | 변경사항 | text | 27% | 채권최고액 금131,000,000원 |
| `gapgu[].right_holder` | 권리자 | text | 13% | 국민건강보험공단 |
| `gapgu[].trust_no` | 신탁원부 | text | 13% | 신탁원부 제2022-9693호 |
| `eulgu[].period` | 존속기간 | text | 10% | 1996년4월24일부터 1998년4월23일까지 |
| `eulgu[].jeonse_holder` | 전세권자 | text | 10% | 마예태 900930-******* |
| `eulgu[].jeonse_holder_address` | 전세권자주소 | text | 10% | 서울특별시 송파구 백제고분로 29, 120동 903호 (문정동, 롯데캐슬… |
| `gapgu[].agency` | 처분청 | text | 7% | 북대전세무서 |

## 집합건축물대장(전유부) (`building_register`) — 키 32개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `confirm_no` | 문서확인번호 | text | 100% | 3188-4949-1246-2345 |
| `unique_no` | 고유번호 | text | 100% | 4156211400-3-00870000 |
| `building_name` | 명칭 | text | 100% | 한신휴플러스에듀포레 제115동 |
| `unit_name` | 호명칭 | text | 100% | 115동 2104호 |
| `site_location` | 대지위치 | text | 100% | 경기도 수원시 영통구 원천동 |
| `jibun` | 지번 | text | 100% | 87 |
| `road_address` | 도로명주소 | text | 100% | 경기도 수원시 영통구 매탄로 376 |
| `exclusive[].kind` | 구분 | text | 100% | 주 |
| `exclusive[].floor` | 층별 | text | 100% | 21층 |
| `exclusive[].structure` | 구조 | text | 100% | 철근콘크리트구조 |
| `exclusive[].usage` | 용도 | text | 100% | 아파트 |
| `exclusive[].area` | 면적(㎡) | number | 100% | 101.84 |
| `common[].kind` | 구분 | text | 100% | 주 |
| `common[].floor` | 층별 | text | 100% | 각층 |
| `common[].structure` | 구조 | text | 100% | 철근콘크리트구조 |
| `common[].usage` | 용도 | text | 100% | 계단실,복도,승강기 |
| `common[].area` | 면적(㎡) | number | 100% | 24.60 |
| `owners[].name` | 성명(명칭) | text | 100% | 주식회사쌍용건설 |
| `owners[].rrn` | 주민(법인)등록번호 | rrn | 100% | 171512-4430096 |
| `owners[].address` | 주소 | text | 100% | 경기도 수원시 영통구 시청로 108 |
| `owners[].share` | 소유권지분 | text | 100% | 1/1 |
| `owners[].change_date` | 변동일 | date | 100% | 1994.11.04 |
| `owners[].change_cause` | 변동원인 | text | 100% | 소유권보존 |
| `house_prices[].base_date` | 기준일 | date | 87% | 2025.01.01 |
| `house_prices[].price` | 공동주택(아파트)가격 | amount | 87% | 359,000,000 |
| `officer` | 담당자 | text | 100% | 민원여권과 |
| `officer_phone` | 전화 | phone | 100% | 031-410-6139 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 수원시 영통구청장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 영통구청장인 |
| `owners_note` | 비고 | text | 37% | ※ 이 건축물대장은 현소유자만 표시한 것입니다. |
| `violation` | 위반건축물 | text | 3% | 위반건축물 |

## 토지대장 (`land_register`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `unique_no` | 고유번호 | text | 100% | 4156211400-10087-0000 |
| `drawing_no` | 도면번호 | number | 100% | 47 |
| `issue_no` | 발급번호 | number | 100% | 202644552441 |
| `location` | 토지소재 | text | 100% | 경기도 수원시 영통구 원천동 |
| `sheet_no` | 장번호 | text | 100% | 1-2 |
| `processed_time` | 처리시각 | text | 100% | 15시 41분 19초 |
| `jibun` | 지번 | text | 100% | 87 |
| `scale` | 축척 | text | 100% | 1:1200 |
| `issuer_name` | 발급자 | text | 100% | 인터넷민원 |
| `land[].category` | 지목 | text | 100% | (08)대 |
| `land[].area` | 면적 | number | 100% | 34,688.3 |
| `land[].reason` | 사유 | text | 100% | (20)1992년 03월 13일 등록전환 |
| `owners[].change_date` | 변동일자 | date | 100% | 1994년 11월 04일 |
| `owners[].change_cause` | 변동원인 | text | 100% | (01)소유권보존 |
| `owners[].address` | 주소 | text | 100% | 경기도 수원시 영통구 시청로 108 |
| `owners[].name` | 성명또는명칭 | text | 100% | 주식회사쌍용건설 |
| `owners[].reg_no` | 등록번호 | text | 100% | 171512-4430096 |
| `owners[].co_owners` | 공유자 | text | 83% | 외 1,344인 |
| `grades[].date` | 등급수정년월일 | text | 100% | 1984.07.01. 수정 |
| `grades[].grade` | 토지등급 | number | 100% | 149 |
| `land_prices[].base_date` | 개별공시지가기준일 | date | 100% | 2020/01/01 |
| `land_prices[].price` | 개별공시지가 | amount | 100% | 2,529,000 |
| `zoning` | 용도지역 | text | 100% | 준주거지역 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `issuer` | 발급기관 | text | 100% | 수원시 영통구청장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 영통구청장인 |

## 부동산 매매계약서 (`sales_contract`) — 키 50개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `property.location` | 소재지 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `property.land_category` | 지목 | text | 100% | 대 |
| `property.land_right` | 대지권 | text | 100% | 소유권대지권 31,054.7분의 54.47 |
| `property.land_area` | 면적 | text | 100% | 54.47㎡ |
| `property.structure` | 구조 | text | 100% | 철근콘크리트구조 |
| `property.usage` | 용도 | text | 100% | 공동주택(아파트) |
| `property.building_area` | 면적 | text | 100% | 101.84㎡ |
| `payment.price` | 매매대금 | amount | 100% | 금 오억육천만원정 (₩560,000,000) |
| `payment.down` | 계약금 | amount | 100% | 금 오천육백만원정 (₩56,000,000) |
| `payment.middle` | 중도금 | amount | 63% | 금 일억칠천만원정 (₩170,000,000) |
| `payment.middle_date` | 중도금지급일 | date | 63% | 2025년 10월 14일 |
| `payment.balance` | 잔금 | amount | 100% | 금 삼억삼천사백만원정 (₩334,000,000) |
| `payment.balance_date` | 잔금지급일 | date | 100% | 2025년 11월 03일 |
| `specials[]` | 특약사항 | text | 100% | 1. 현 시설물 상태의 계약이며, 매수인은 등기사항증명서 및 현장을 확인… |
| `contract_date` | 계약일 | date | 100% | 2025년 09월 16일 |
| `seller.address` | 주소 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `seller.rrn` | 주민등록번호 | rrn | 100% | 570508-1456825 |
| `seller.phone` | 전화 | phone | 100% | 010-6594-7883 |
| `seller.name` | 성명 | text | 100% | 박기우 |
| `seal.seller` | 매도인 | seal | 100% | 반원인 |
| `sign.seller` | 매도인 | signature | 100% | 여혜인 |
| `buyer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `buyer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `buyer.phone` | 전화 | phone | 100% | 010-5907-7253 |
| `buyer.name` | 성명 | text | 100% | 박찬연 |
| `seal.buyer` | 매수인 | seal | 100% | 강순준 |
| `sign.buyer` | 매수인 | signature | 100% | 박찬연 |
| `brokers[].office_address` | 사무소소재지 | text | 100% | 경기도 수원시 영통구 매탄로 29, 1층 108호 (원천동) |
| `brokers[].office_name` | 사무소명칭 | text | 100% | 한신휴공인중개사 |
| `brokers[].representative` | 대표 | text | 100% | 문채현 |
| `brokers[].reg_no` | 등록번호 | text | 100% | 29669-2012-02206 |
| `brokers[].phone` | 전화 | phone | 100% | 031-661-0605 |
| `co_seller.address` | 주소 | text | 23% | 대구광역시 수성구 수성로 401, 107동 2004호 (지산동, 센트레빌… |
| `co_seller.rrn` | 주민등록번호 | rrn | 23% | 590110-1645169 |
| `co_seller.phone` | 전화 | phone | 23% | 010-6479-6446 |
| `co_seller.name` | 성명 | text | 23% | 김찬민 |
| `seal.co_seller` | 공동매도인 | seal | 23% | 김찬민 |
| `sign.co_seller` | 공동매도인 | signature | 23% | 최희원 |
| `seller_agent.address` | 대리인주소 | text | 17% | 서울특별시 영등포구 국제금융로 322, 122동 2001호 (신길동, 한… |
| `seller_agent.rrn` | 대리인주민등록번호 | rrn | 17% | 650531-1503031 |
| `seller_agent.name` | 대리인성명 | text | 17% | 우건유 |
| `seal.seller_agent` | 매도인대리인 | seal | 17% | 석진연 |
| `sign.seller_agent` | 매도인대리인 | signature | 17% | 우건유 |
| `brokers[].assistant` | 소속공인중개사 | text | 43% | 현수은 |
| `co_buyer.address` | 주소 | text | 3% | 서울특별시 강남구 도곡로 458-8, 102동 1102호 (논현동, 우성… |
| `co_buyer.rrn` | 주민등록번호 | rrn | 3% | 820218-1260586 |
| `co_buyer.phone` | 전화 | phone | 3% | 010-9382-0528 |
| `co_buyer.name` | 성명 | text | 3% | 이석인 |
| `seal.co_buyer` | 공동매수인 | seal | 3% |  |
| `sign.co_buyer` | 공동매수인 | signature | 3% | 이석인 |

## 주택임대차표준계약서 (`lease_contract`) — 키 52개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `landlord_name` | 임대인 | text | 100% | 박기우 |
| `tenant_name` | 임차인 | text | 100% | 박찬연 |
| `house.location` | 소재지 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `house.land_category` | 지목 | text | 100% | 대 |
| `house.land_area` | 토지면적 | text | 100% | 31,054.7㎡ |
| `house.structure_usage` | 구조·용도 | text | 100% | 철근콘크리트구조 / 공동주택(아파트) |
| `house.building_area` | 건물면적 | text | 100% | 101.84㎡ |
| `house.lease_part` | 임차할부분 | text | 100% | 전부 (101.84㎡) |
| `contract_type` | 계약의종류 | checkbox | 100% | 보기: 신규 계약 / 합의에 의한 재계약 / 「주택임대차보호법」 제6조의3의 계약갱신요구권 행사에 의한 갱신계약 |
| `tax_arrears` | 미납국세·지방세 | text | 100% | 없음 |
| `prior_fixed_date` | 선순위확정일자현황 | text | 100% | 해당 없음 |
| `fixed_date.date` | 확정일자 | date | 100% | 2026.01.27 |
| `fixed_date.no` | 확정일자번호 | text | 100% | 2026-7849 |
| `fixed_date.office` | 확정일자부여기관 | text | 100% | 영통구 원천동행정복지센터 |
| `deposit` | 보증금 | amount | 100% | 금 삼억육천만원정 (₩360,000,000) |
| `down_payment` | 계약금 | amount | 100% | 금 삼천육백만원정 (₩36,000,000) |
| `balance` | 잔금 | amount | 100% | 금 삼억이천사백만원정 (₩324,000,000) |
| `balance_date` | 잔금지급일 | date | 100% | 2026년 03월 03일 |
| `management_fee` | 관리비 | text | 100% | 관리규약에 따라 관리주체가 부과하는 금액 |
| `handover_date` | 인도일 | date | 100% | 2026년 03월 03일 |
| `end_date` | 임대차종료일 | date | 100% | 2028년 03월 02일 |
| `specials[]` | 특약사항 | text | 100% | 1. 주택을 인도받은 임차인은 2026년 3월 3일까지 주민등록(전입신고… |
| `contract_date` | 계약일 | date | 100% | 2026년 01월 26일 |
| `landlord.address` | 주소 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `landlord.rrn` | 주민등록번호 | rrn | 100% | 570508-1456825 |
| `landlord.phone` | 전화 | phone | 100% | 010-6594-7883 |
| `landlord.name` | 성명 | text | 100% | 박기우 |
| `seal.landlord` | 임대인 | seal | 100% | 박기우 |
| `sign.landlord` | 임대인 | signature | 100% | 반원인 |
| `tenant.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `tenant.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `tenant.phone` | 전화 | phone | 100% | 010-5907-7253 |
| `tenant.name` | 성명 | text | 100% | 박찬연 |
| `seal.tenant` | 임차인 | seal | 100% | 현예지 |
| `sign.tenant` | 임차인 | signature | 100% | 박찬연 |
| `brokers[].office_address` | 사무소소재지 | text | 100% | 경기도 수원시 영통구 매탄로 68, 1층 111호 (원천동) |
| `brokers[].office_name` | 사무소명칭 | text | 100% | 한신휴공인중개사사무소 |
| `brokers[].representative` | 대표 | text | 100% | 위영지 |
| `brokers[].reg_no` | 등록번호 | text | 100% | 41835-2020-01056 |
| `brokers[].phone` | 전화 | phone | 100% | 031-885-2129 |
| `co_landlord.address` | 주소 | text | 17% | 대구광역시 수성구 수성로 401, 107동 2004호 (지산동, 센트레빌… |
| `co_landlord.rrn` | 주민등록번호 | rrn | 17% | 590110-1645169 |
| `co_landlord.phone` | 전화 | phone | 17% | 010-6479-6446 |
| `co_landlord.name` | 성명 | text | 17% | 김찬민 |
| `seal.co_landlord` | 공동임대인 | seal | 17% | 정건수 |
| `sign.co_landlord` | 공동임대인 | signature | 17% | 김찬민 |
| `brokers[].assistant` | 소속공인중개사 | text | 33% | 공건인 |
| `landlord_agent.address` | 대리인주소 | text | 10% | 부산광역시 해운대구 달맞이길 142, 114동 2403호 (중동, 센트레… |
| `landlord_agent.rrn` | 대리인주민등록번호 | rrn | 10% | 790510-2944862 |
| `landlord_agent.name` | 대리인성명 | text | 10% | 심정아 |
| `seal.landlord_agent` | 임대인대리인 | seal | 10% | 송영아 |
| `sign.landlord_agent` | 임대인대리인 | signature | 10% | 심정아 |

## 전입세대확인서 (`move_in_household_list`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 8136-8334-8254-1287 |
| `issue_date` | 발급일자 | date | 100% | 2026.01.31 |
| `kind` | 열람·교부구분 | text | 100% | 교부 |
| `address` | 건물또는시설소재지 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `jibun_address` | 지번주소 | text | 100% | 경기도 수원시 영통구 원천동 87 115동 2104호 |
| `households[].no` | 순번 | number | 100% | 1 |
| `households[].head_name` | 세대주성명 | text | 100% | 박*연 |
| `households[].move_in_date` | 전입일자 | date | 100% | 2025-11-11 |
| `households[].reg_type` | 등록구분 | text | 100% | 거주자 |
| `households[].first_name` | 최초전입자성명 | text | 100% | 박*연 |
| `households[].first_date` | 최초전입일자 | date | 100% | 2025-11-11 |
| `households[].first_reg_type` | 최초전입자등록구분 | text | 100% | 거주자 |
| `households[].cohabitants` | 동거인수 | number | 100% | 0 |
| `applicant.name` | 성명 | text | 100% | 박찬연 |
| `applicant.rrn` | 주민등록번호 | rrn | 100% | 900210-1****** |
| `applicant.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `applicant.purpose` | 열람·교부목적 | text | 100% | 금융기관 대출(주택담보대출) |
| `view_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 영통구 원천동장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 동장의인 |
| `cohabitants[].no` | 순번 | number | 33% | 1 |
| `cohabitants[].name` | 동거인성명 | text | 33% | 심*민 |
| `cohabitants[].move_in_date` | 전입일자 | date | 33% | 2010-02-25 |
| `cohabitants[].reg_type` | 등록구분 | text | 33% | 거주자 |
| `households[].unit` | 동·호 | text | 3% | 101호 |
