# 부동산 서류 변형 목록 (real_estate)

등기 이력(소유자 변동, 근저당 설정·말소, 공유, 신탁, 가압류 등)은 `_facts(p)` → `_history()` 에서 **프로필 단위로** 정한다.
그래서 같은 고객이면 등기부·토지대장·건축물대장·매매/임대차계약서의 소유자·근저당·공유자가 서로 맞는다.
매수인 근저당(소유권 이전된 경우, 대출 목적이 주택구입자금)은 은행 서식 `_plan_personal()` 의 채권최고액·은행·지점과 같다.

| 서류 | 경우 | 확률 | 새 키 | 설명 |
|---|---|---|---|---|
| 공통(_facts) | heavy: 이력이 많은 물건 | 0.3 | – | 중간 소유자 2~5명, 소유자마다 근저당 1~3회 대환(설정 후 옛 근저당 말소), 가압류·압류와 말소, 임의경매개시결정과 취하, 근저당권 변경 등 |
| 공통(_facts) | joint_owner 매도인 부부 공유 | 0.15 | `gapgu[].holders[]`, `co_seller`, `co_landlord` | 취득 때 공유(각 2분의 1) 또는 나중에 `소유권일부이전`(증여) |
| 공통(_facts) | joint_buyer 매수인 부부 공동명의 | 0.2 | `co_buyer` | 소유권 이전된 경우 매수인+배우자 각 2분의 1 |
| 등기부 | reg_seizure 가압류·압류 후 말소 | 0.15 | `gapgu[].claim_amount`, `creditor`, `creditor_address`, `right_holder`, `agency` | 말소된 줄은 빨간 실선, `N번가압류등기말소` 별도 순위 |
| 등기부 | reg_active_seizure 말소 안 된 가압류 | 0.05 | 위와 같음, `summary.gapgu_rights[]` | 매도인 명의 현재 가압류. 계약서 특약에 "갑구 N번 가압류 해제" |
| 등기부 | reg_trust 담보신탁 후 신탁재산의귀속 | 0.07 | `gapgu[].trust_no` | 수탁자 앞 소유권이전 + 신탁 줄, 귀속 이전 + `N번신탁등기말소` |
| 등기부 | reg_jeonse 전세권설정·말소 | 0.1 | `eulgu[].deposit`, `scope`, `period`, `jeonse_holder`, `jeonse_holder_address` | 소유자가 살지 않던 시기 |
| 등기부 | reg_lease_order 임차권등기명령·말소 | 0.06 | `eulgu[].deposit`, `rent`, `scope`, `contract_date`, `resident_date`, `possession_date`, `fixed_date`, `lessee`, `lessee_address` | `주택임차권`, 말소는 `N번주택임차권등기말소` |
| 등기부 | reg_mort_change 근저당권변경(부기) | 0.15 | `eulgu[].change` | `N-1 N번근저당권변경` 채권최고액 감액. 합병(외환→하나 2015.9.1, 농협중앙회→농협은행 2012.3.2)이면 `N번근저당권이전` (`mortgagee`) |
| 등기부 | reg_addr_change 등기명의인표시변경 | 0.12 | `gapgu[].change` | `N-1 N번등기명의인표시변경`(전거), 원래 주소에 빨간 실선 |
| 등기부 | 요약 페이지(주요 등기사항 요약) | 0.18 (rng) | `summary.gapgu_rights[]`, `page_label` | 말소되지 않은 사항만: 현재 소유자(공유 지분), 남은 가압류, 남은 근저당(변경 후 최고액·이전 후 근저당권자)·전세권·임차권 |
| 등기부 | 여러 쪽 | heavy 따라 | – | 부동산 표시 줄·바닥글(발행번호/열람일시)이 쪽마다 반복, 갑구/을구 제목과 열 머리글 반복, 쪽 번호 `1/3` |
| 건축물대장 | heavy: 공용부분 다수 + 공시가격 6~9년 | 0.25 | – | 세로로 쌓는 배치(소유자현황 여러 쪽) |
| 건축물대장 | owner_history 소유자 변동 전체 표시 | 0.3 | `owners[]` (기존 `owner` → 목록) | 보존·이전·일부이전·등기명의인표시변경. 아니면 현소유자만 + `owners_note` |
| 건축물대장 | violation 위반건축물 표시 | 0.08 | `violation` | 제목 왼쪽 노란 바탕 빨간 글씨 |
| 토지대장 | heavy: 분할·합병·지목변경 이력 | 0.2 | – | 토지표시 3~6줄. 소유자 이력은 등기 이력 그대로(주소변경 `(11)` 포함) |
| 매매계약서 | heavy: 특약 다수 | 0.25 | – | 특약 9~16개, 2쪽 |
| 매매계약서 | agent 매도인 대리인 | 0.1 | `seller_agent.{address,rrn,name}` | 대리인 줄 기재 + 특약 |
| 매매계약서 | co_broker 공동중개 | 0.35 | `brokers[1]` | 중개사 2곳 |
| 매매계약서 | hand_special 손글씨 추가 특약 | 0.12 | `specials[]` 마지막 | 파란 손글씨 |
| 매매계약서 | 정정 | fix 0.03~0.05 | (`corrected`) | 금액·날짜·전화. 도장 글자 = 매수인 |
| 매매계약서 | 서명/날인 | sigspot | `seal.*`, `sign.*` | 매도인·공동매도인·매수인·공동매수인·대리인 |
| 임대차계약서 | heavy: 특약 다수 | 0.2 | – | 특약 8~13개 |
| 임대차계약서 | agent / co_broker / hand_special / 정정 / 공유 임대인 | 0.12 / 0.35 / 0.12 / 0.03~0.05 / joint_owner | `landlord_agent`, `co_landlord` | 매매계약서와 같음 |
| 전입세대확인서 | heavy: 건물 전체 열람(다세대·오피스텔) 14~28세대 | 0.2 | `households[].unit` | 여러 쪽, 머리글 반복. 아파트는 제외 |
| 전입세대확인서 | multi_household 건물 전체 열람 4~9세대 | 0.15 | `households[].unit` | 동·호 열 추가, 지번주소에 호 없음 |
| 전입세대확인서 | cohabitant 동거인 1~2명 | 0.12 | `cohabitants[]` | |
| 전입세대확인서 | unknown_resident 거주불명자 | 0.05 | – | 등록구분 `거주불명자` |
