# 「외국환서식관리프로그램」전자무역업무이용(신규,변경,해지)신청서 (`hf223`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf223 · card-hash: d7266a5cbd8f -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 5 (seed 1000000 로 그린 것) · **분류 정답:** 「외국환서식관리프로그램」전자무역업무이용(신규,변경,해지)신청서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf223 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.223 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 35칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `수수료결제계좌번호` | 수수료결제계좌번호 | number | 1쪽 [822, 623, 904, 634] | 늘 | 파일 key | 값 종류 `amount` | fields.json:797 | 묻기 |
| `NET12` | NET12 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:892 | 묻기 |
| `전자문서인증키` | 전자문서인증키 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1035 | 묻기 |
| `signer2.name` | 전자무역업무기본약관수령필 | text | - | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1114 | 묻기 |
| `date` | 작성일 | date | 1쪽 [510, 801, 715, 817] | 늘 | 파일 key | 작성일 | fields.json:1189 | 묻기 |
| `signer3.name` | 신청인 | text | 1쪽 [542, 825, 608, 837] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1215 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [462, 847, 812, 858] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:1234 | 묻기 |
| `기재사항` | 기재사항 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1247 | 묻기 |
| `계산서` | 계산서 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1262 | 묻기 |
| `발신업무` | 발신업무 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1277 | 묻기 |
| `eNego` | e-Nego | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1292 | 묻기 |
| `외화지급보증조건변경신청업무` | 외화지급보증/조건변경신청업무 | amount | 2쪽 [596, 631, 686, 642] | 늘 | 파일 key | 값 종류 `fx_amount` | fields.json:1713 | 묻기 |
| `상호대사일반응답` | 상호대사,일반응답 | text | 2쪽 [503, 662, 602, 674] | 늘 | 파일 key | 값 종류 `company` | fields.json:1727 | 묻기 |
| `계산서업무입금통지업무출금통지업무` | 계산서업무,입금통지업무,출금통지업무 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1765 | 묻기 |
| `계좌입금통지출금통지당발송금출금통지` | 계좌입금통지,출금통지,당발송금출금통지 | text | 2쪽 [666, 697, 805, 709] | 늘 | 파일 key | 값 종류 `account` | fields.json:1780 | 묻기 |
| `전자적매입신청업무` | 전자적매입신청업무 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1795 | 묻기 |
| `EDI` | EDI | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1842 | 묻기 |
| `계산서발급업무` | 계산서발급업무 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1857 | 묻기 |
| `eLC` | e-L/C | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1872 | 묻기 |
| `자동승인` | 자동승인 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1887 | 묻기 |
| `지급지시업무` | 지급지시업무 | text | 3쪽 [310, 684, 376, 695] | 늘 | 파일 key | 값 종류 `branch` | fields.json:1902 | 묻기 |
| `수수료결제계좌번호2` | 수수료결제계좌번호 | number | 3쪽 [820, 722, 912, 734] | 늘 | 파일 key | 값 종류 `amount` | fields.json:1965 | 묻기 |
| `NET122` | NET12 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2060 | 묻기 |
| `전자문서인증키2` | 전자문서인증키 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2155 | 묻기 |
| `date2` | 작성일 | date | 3쪽 [666, 249, 829, 265] | 늘 | 파일 key | 작성일 | fields.json:2172 | 묻기 |
| `기재사항2` | 기재사항 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2211 | 묻기 |
| `약정항목eLC통지업무` | 약정항목:e-L/C통지업무 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2258 | 묻기 |
| `customer.name` | 신청인 | text | 4쪽 [378, 452, 444, 463] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:2272 | 묻기 |
| `하나은행` | 하나은행 | text | 4쪽 [377, 500, 443, 512] | 늘 | 파일 key | 값 종류 `bank` | fields.json:2285 | 묻기 |
| `수수료결제계좌번호3` | 수수료결제계좌번호 | number | 4쪽 [821, 753, 912, 765] | 늘 | 파일 key | 값 종류 `amount` | fields.json:2332 | 묻기 |
| `상세수발신인식별자` | 상세수발신인식별자 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2347 | 묻기 |
| `상세수발신인식별자2` | 상세수발신인식별자 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2363 | 묻기 |
| `date3` | 작성일 | date | 4쪽 [666, 310, 829, 325] | 늘 | 파일 key | 작성일 | fields.json:2412 | 묻기 |
| `기재사항3` | 기재사항 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2451 | 묻기 |
| `계산서2` | 계산서 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2466 | 묻기 |

## 표 `변경신청_목록` (표 과제 table·table_read·table_find·table_qa) — 3열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `변경신청_목록.*.변경항목` | 변경항목 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:137 | 묻기 |
| `변경신청_목록.*.변경전` | 변경전 | text | 1쪽 [450, 670, 521, 682] (1행) | 늘 | 파일 key | 값 종류 `note` | fields.json:812 | 묻기 |
| `변경신청_목록.*.변경후` | 변경후 | text | 1쪽 [689, 670, 759, 682] (1행) | 늘 | 파일 key | 값 종류 `note` | fields.json:955 | 묻기 |

## 표 `지급지시업무관련출금계좌_목록` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `지급지시업무관련출금계좌_목록.*.예금과목` | 예금과목 | text | 1쪽 [317, 554, 421, 566] (1행) | 늘 | 파일 key | 값 종류 `product` | fields.json:653 | 묻기 |
| `지급지시업무관련출금계좌_목록.*.계좌번호` | 계좌번호 | text | 1쪽 [450, 554, 589, 566] (1행) | 늘 | 파일 key | 값 종류 `account` | fields.json:749 | 묻기 |
| `지급지시업무관련출금계좌_목록.*.예금주` | 예금주 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:907 | 묻기 |
| `지급지시업무관련출금계좌_목록.*.통화` | 통화 | text | 1쪽 [855, 554, 885, 566] (1행) | 늘 | 파일 key | 값 종류 `currency` | fields.json:1052 | 묻기 |

## 표 `신청인_목록` (표 과제 table·table_read·table_find·table_qa) — 3열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `신청인_목록.*.수발신인식별자` | 수발신인식별자 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:701 | 묻기 |
| `신청인_목록.*.상세수발신식별자` | 상세수발신식별자 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:844 | 묻기 |
| `신청인_목록.*.전자문서인증키` | 전자문서인증키 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:987 | 묻기 |

## 체크·도장·서명 (marks) — 37칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.이용신청` | 이용신청 | checkbox (지급지시업무 ( / 무서류무역송금) (지급지시용 비밀번호) | 1쪽 [215, 492, 356, 506] | 늘 | 파일 key | 보기 중 고름: 지급지시업무 ( / 무서류무역송금) (지급지시용 비밀번호 | fields.json:61 | 묻기 |
| `check.이용신청2` | 이용신청 | checkbox (goGlobal 전용 지급지시업무) | 1쪽 [215, 512, 456, 526] | 늘 | 파일 key | 보기 중 고름: goGlobal 전용 지급지시업무 | fields.json:107 | 묻기 |
| `check.지정사업자` | 지정사업자 | checkbox (KTNet) | 1쪽 [424, 300, 497, 313] | 늘 | 파일 key | 보기 중 고름: KTNet | fields.json:169 | 묻기 |
| `check.EDI` | EDI | checkbox (승인업무 / 수입업무 / 신용장통지 / 내국신용장업무 / 계산서 및 입출금 통지업무 / 수출업무 / 상호대사 / 일반응답 / TSU 업무 / 단독e-L/C 통지업무 / 외화지급보증업무) | 1쪽 [570, 336, 663, 350] | 늘 | 파일 key | 보기 중 고름: 승인업무 / 수입업무 / 신용장통지 / 내국신용장업무 / 계산서 및 입출금 통지업무 / 수출업무 / 상호대사 / 일반응답 / TSU 업무 / 단독e-L/C 통지업무 / 외화지급보증업무 | fields.json:199 | 묻기 |
| `check.계산서발신업무` | 계산서발신업무 | checkbox (수출환어음매입 / 신용장개설 / 내국신용장개설 / 수출입금통지 / 타발송금입금통지 / 계좌입금통지 / 출금통지 / 당발송금출금통지) | 1쪽 [319, 408, 412, 422] | 늘 | 파일 key | 보기 중 고름: 수출환어음매입 / 신용장개설 / 내국신용장개설 / 수출입금통지 / 타발송금입금통지 / 계좌입금통지 / 출금통지 / 당발송금출금통지 | fields.json:389 | 묻기 |
| `check.기반사업자` | 기반사업자 | checkbox (uTradeHub) | 1쪽 [424, 427, 537, 441] | 늘 | 파일 key | 보기 중 고름: uTradeHub | fields.json:531 | 묻기 |
| `check.eNego` | e-Nego | checkbox (e-Nego 업무 / e-L/C 통지업무) | 1쪽 [493, 450, 645, 464] | 늘 | 파일 key | 보기 중 고름: e-Nego 업무 / e-L/C 통지업무 | fields.json:561 | 묻기 |
| `check.자동승인` | 자동승인 | checkbox (구매확인서승인 / 내국신용장개설승인) | 1쪽 [319, 471, 462, 485] | 늘 | 파일 key | 보기 중 고름: 구매확인서승인 / 내국신용장개설승인 | fields.json:607 | 묻기 |
| `seal.signer` | 인감대조 | seal | 1쪽 [850, 834, 908, 875] | 늘 | 표 행 (묶음·키 설명 '인감대조') | 값 종류 `seal` | fields.json:1100 | 묻기 |
| `sign.signer` | 인감대조 | signature | 1쪽 [833, 831, 925, 879] | 늘 | 표 행 (묶음·키 설명 '인감대조') | 값 종류 `seal` | fields.json:1100 | 묻기 |
| `seal.signer2` | 전자무역업무기본약관수령필 | seal | 1쪽 [728, 901, 756, 914] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1114 | 묻기 |
| `sign.signer2` | 전자무역업무기본약관수령필 | signature | 1쪽 [728, 901, 756, 914] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1114 | 묻기 |
| `check.전자무역업무기본약관에따라아래와같이` | 『전자무역업무기본약관』에따라아래와같이( | checkbox (신규, / 변경, / 해지)신청합니다.) | 1쪽 [649, 158, 902, 170] | 늘 | 파일 key | 보기 중 고름: 신규, / 변경, / 해지)신청합니다. | fields.json:1133 | 묻기 |
| `seal.signer3` | 신청인 | seal | 1쪽 [698, 813, 730, 849] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1215 | 묻기 |
| `sign.signer3` | 신청인 | signature | 1쪽 [700, 824, 729, 837] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1215 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [646, 81, 733, 122] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [646, 81, 733, 122] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [733, 81, 815, 122] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [733, 81, 815, 122] | 늘 | - | - | - | 묻기 |
| `check.승인업무` | 승인업무 | checkbox (승인업무) | 2쪽 [88, 377, 181, 391] | 늘 | 파일 key | 보기 중 고름: 승인업무 | fields.json:1307 | 묻기 |
| `check.수입업무` | 수입업무 | checkbox (수입업무) | 2쪽 [88, 417, 181, 431] | 늘 | 파일 key | 보기 중 고름: 수입업무 | fields.json:1337 | 묻기 |
| `check.LC통지업무` | L/C통지업무(EDI) | checkbox (L/C 통지업무(EDI)) | 2쪽 [88, 456, 247, 470] | 늘 | 파일 key | 보기 중 고름: L/C 통지업무(EDI) | fields.json:1367 | 묻기 |
| `check.내국신용장업무` | 내국신용장업무 | checkbox (내국신용장업무) | 2쪽 [88, 488, 231, 502] | 늘 | 파일 key | 보기 중 고름: 내국신용장업무 | fields.json:1397 | 묻기 |
| `check.계산서및입출금통지업무` | 계산서및입출금통지업무 | checkbox (계산서 및 입출금 통지업무) | 2쪽 [88, 520, 302, 534] | 늘 | 파일 key | 보기 중 고름: 계산서 및 입출금 통지업무 | fields.json:1427 | 묻기 |
| `check.지급지시업무` | 지급지시업무 | checkbox (지급지시업무) | 2쪽 [88, 559, 214, 573] | 늘 | 파일 key | 보기 중 고름: 지급지시업무 | fields.json:1457 | 묻기 |
| `check.수출업무` | 수출업무 | checkbox (수출업무) | 2쪽 [88, 598, 181, 612] | 늘 | 파일 key | 보기 중 고름: 수출업무 | fields.json:1487 | 묻기 |
| `check.외화지급보증업무` | 외화지급보증업무 | checkbox (외화지급보증업무) | 2쪽 [88, 629, 248, 643] | 늘 | 파일 key | 보기 중 고름: 외화지급보증업무 | fields.json:1517 | 묻기 |
| `check.상호대사` | 상호대사 | checkbox (상호대사 / 일반응답) | 2쪽 [189, 661, 282, 675] | 늘 | 파일 key | 보기 중 고름: 상호대사 / 일반응답 | fields.json:1547 | 묻기 |
| `check.계산서발신업무2` | 계산서발신업무 | checkbox (계산서발신업무) | 2쪽 [88, 692, 231, 706] | 늘 | 파일 key | 보기 중 고름: 계산서발신업무 | fields.json:1593 | 묻기 |
| `check.자동승인업무` | 자동승인업무 | checkbox (자동승인업무) | 2쪽 [88, 724, 214, 738] | 늘 | 파일 key | 보기 중 고름: 자동승인업무 | fields.json:1623 | 묻기 |
| `check.eLC통지업무` | e-L/C통지업무 | checkbox (e-L/C 통지업무) | 2쪽 [88, 755, 229, 769] | 늘 | 파일 key | 보기 중 고름: e-L/C 통지업무 | fields.json:1653 | 묻기 |
| `check.eNego업무` | e-Nego업무 | checkbox (e-Nego 업무) | 2쪽 [88, 787, 211, 801] | 늘 | 파일 key | 보기 중 고름: e-Nego 업무 | fields.json:1683 | 묻기 |
| `check.Ο처리하실업무의` | Ο처리하실업무의 | checkbox (에 V 표시를 하십시오) | 2쪽 [269, 308, 435, 321] | 늘 | 파일 key | 보기 중 고름: 에 V 표시를 하십시오 | fields.json:1741 | 묻기 |
| `seal.signer4` | 지점 | seal | 3쪽 [876, 302, 905, 316] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:2198 | 묻기 |
| `sign.signer4` | 지점 | signature | 3쪽 [876, 302, 905, 316] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:2198 | 묻기 |
| `seal.signer5` | 지점 | seal | 4쪽 [876, 363, 905, 376] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:2438 | 묻기 |
| `sign.signer5` | 지점 | signature | 4쪽 [876, 363, 905, 376] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:2438 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
- **고칠 곳:** html·코드 서식은 템플릿 줄(칸 자리·키·항목명)과 fields.json 줄(값 출처·질문 설정 q), 원본 서식은 fields.json 의 그 칸(박스 `rect`·항목명·키·값·q). html·코드 서식에서 fields.json 에 줄이 없는 칸의 질문 설정은 fields.json 맨 위 `"q": {"키": {…}}` 묶음에.

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 공통 `docgen/forms/_common/questions.json`.

### 서류 분류 `classify` · 채점 acc

질문:

```
이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. 설명 없이 서류명만 한 줄로 답하세요.
```

답:

```json
"「외국환서식관리프로그램」전자무역업무이용(신규,변경,해지)신청서"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf223 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf223` → `python -m docgen.formdir card hf223` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 키 설명이 그대로 키) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf223 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf223 --show` · `python -m docgen.preview hf223 --out work/hf223`
