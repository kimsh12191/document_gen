# document_gen — 은행 제출 서류 합성 데이터 생성기

고객이 은행에 제출하는 서류 **476종**을 재현했습니다. 가상 고객 데이터를 채워 넣어 **VLM 정보추출(Key Information Extraction) 학습 데이터**를 만듭니다.

- **외부 발급 서류 56종**: 신분증, 등·초본, 가족관계증명서, 소득금액증명원, 원천징수영수증, 등기부등본, 사업자등록증, 재무제표, 인보이스 등
- **은행 서식 14종 (HTML 템플릿)**: 대출신청서, 여신거래약정서, 근저당권설정계약서, 고객확인서(KYC), 해외송금신청서 등
  - 은행별 표기(은행명·법인명칭·서식번호 줄·결재란·인쇄색·계좌번호)가 다르게 나옵니다.
  - **하나은행**과 옛 은행 **KEB하나은행(2015~2020)**, **외환은행(~2015.8)** 서식도 만듭니다. 옛 은행 서식은 그 시기 날짜와 제도로 만들어집니다. → [docs/realism/bank_brands.md](docs/realism/bank_brands.md)
- **하나은행 원본 서식 406종**: 하나은행 공개 서식 PDF를 그대로 배경으로 깔고 손님이 쓴 것처럼 값을 얹습니다. 서식 모양은 원본과 똑같습니다. → [하나은행 원본 서식](#하나은행-원본-서식-원본-pdf-오버레이)

| | 종수 | 방식 |
|---|---:|---|
| **HTML 템플릿** | 70 | 서식마다 Jinja2 템플릿과 전용 생성 함수를 둡니다. 글꼴·선·여백이 샘플마다 바뀝니다. |
| **원본 PDF 오버레이** | 406 | 원본 PDF가 배경이고, PDF에서 찾은 기재 자리에 손글씨/인쇄체로 값을 씁니다. |

- 전체 목록: [docs/DOCUMENTS.md](docs/DOCUMENTS.md)
- 하나은행 공개 서식 441건 대응표: [docs/FORM_MAP.md](docs/FORM_MAP.md)
- 서류별 샘플 이미지와 정답: [samples/](samples/)

모든 데이터는 학습용 **합성 데이터**이며 실존 인물·사업자와 무관합니다.

## 특징

| | |
|---|---|
| **정답이 문서와 항상 일치** | 템플릿의 모든 값은 `f("경로")`로 출력되고, 화면에 찍힌 문자열이 그대로 GT로 기록됩니다. |
| **고객 단위 일관성** | 같은 고객 프로필로 만든 서류들은 이름·주민번호·주소·회사·소득·부동산·계좌가 서로 맞습니다. 급여명세서 실수령액은 통장 급여 입금액과 같고, 등기부 근저당은 대출 약정과 같은 식입니다. |
| **숫자 정합성** | 합계, 세액(누진세율·4대보험), 잔액 흐름, 대차대조(자산=부채+자본), 환율 환산, 한글 금액(`금 이억일천사백만원정`)이 계산으로 맞춰집니다. |
| **식별번호 형식** | 주민번호, 사업자번호, 법인등록번호는 체크섬까지 맞는 형식으로 생성됩니다(값은 랜덤). 여권 MRZ도 ICAO 체크디지트를 적용합니다. |
| **시각 다양성** | 샘플마다 폰트(나눔·Noto·명조 계열), 글자 크기, 선 굵기, 배경색, 여백이 바뀝니다. 서류 안에서도 열람용/발급용, 마스킹 여부, 선택 항목 등이 랜덤입니다. |
| **형식 변형·여러 쪽** | 사람마다 사정이 다른 경우가 랜덤으로 섞입니다. 이사가 잦은 초본, 근저당이 반복된 등기부, 임원 변경이 많은 법인등기부, 품목이 많은 인보이스처럼 내용이 길면 자동으로 여러 쪽이 됩니다. 말소·개명·이혼·특약·손글씨 정정 같은 특수 상황도 나옵니다. → [서식 변형](#서식-변형-여러-쪽특수-상황) |
| **스캔·촬영 증강** | 기울기, 배경, 조명, 흐림, 노이즈, 팩스, JPEG 압축 효과를 줍니다. |
| **위조 방지** | 신분증, 여권, 인감증명서 등 신원 서류는 항상 "견본 SAMPLE" 워터마크가 들어갑니다. 실제 기관 로고·관인·보안패턴은 넣지 않습니다. |

## 설치

```bash
pip install -r requirements.txt
python -m playwright install chromium     # PNG 렌더링에 필요 (HTML만 만들 땐 불필요)
# 한글 폰트: Ubuntu 기준
sudo apt-get install fonts-nanum fonts-noto-cjk
```

Chromium을 이미 설치했다면 `CHROMIUM_PATH=/path/to/chrome`으로 지정할 수 있습니다.

`pymupdf`는 하나은행 원본 서식(`hana` 그룹)의 배경 이미지를 만들고 기재 자리를 뽑는 데 씁니다.

## 사용법

```bash
# 서류·시나리오 목록
python -m docgen list

# 전 서류 x 고객 100명 → HTML + 정답 JSON (476종 x 100명이라 오래 걸립니다)
python -m docgen generate --n 100 --out out

# 이미지(PNG) + 위치 + ms-swift 학습 jsonl 까지
python -m docgen generate --n 100 --out out --png

# 샘플마다 스캔/촬영 증강 이미지 2장 추가
python -m docgen generate --n 100 --out out --png --augment 2

# 특정 서류나 그룹만
python -m docgen generate --types income_certificate,pay_stub --n 50 --out out --png
python -m docgen generate --types corporate,fx --n 50 --out out --png

# 은행 서식을 특정 은행으로 (하나은행, KEB하나은행, 외환은행, 국민은행, ...)
python -m docgen generate --types bank_form --bank 하나은행 --n 50 --out out --png
python -m docgen generate --types hana --n 30 --out out --png              # 하나은행 원본 서식 406종
python -m docgen generate --bank 외환은행 --n 50 --out out --png   # 옛 은행: 은행 서식만 생성

# 업무 시나리오 단위 (같은 고객의 제출 서류 묶음)
python -m docgen generate --scenario mortgage --n 30 --out out --png

# 템플릿 검증 (예외, 표시되지 않은 값, 페이지 넘침)
python -m docgen check --png
```

시나리오는 12개입니다: `account_opening`, `personal_credit_loan`, `mortgage`, `jeonse_loan`, `sole_proprietor_loan`, `corporate_credit`, `fx_remittance`, `study_abroad_remittance`, `irp_opening`, `retirement_payout`, `efinance_signup`, `inheritance`

## 벤치마크 (OCR·은행업무)

같은 생성기로 **고정된 평가 세트**를 만들어 모델을 잽니다. 과제는 OCR(값 칸 인식, 전체 받아쓰기), 문서 이해(분류, 정보 추출, 체크·도장·서명), 은행 업무(서류 구비 확인, 서류 간 대조, 심사 질의)입니다. 서류 간 대조는 실제 심사 사례를 바탕으로 한 불일치 14종(오기, 타인 서류, 소득 부풀리기, 임대인≠등기부 소유자, 업계약 등)을 일부러 섞어 만듭니다. 자세한 내용은 [docs/BENCHMARK.md](docs/BENCHMARK.md)에 있습니다.

```bash
python -m docgen.bench build --out bench_out                                   # 평가 세트
python -m docgen.bench run --bench bench_out --pred preds/my_model \
    --base-url http://localhost:8000/v1 --model <모델>                          # OpenAI 호환 API 로 예측
python -m docgen.bench eval --bench bench_out --pred preds/my_model            # 채점 → report.md
```

평가 세트는 고객 seed 1,000,000 이상을 씁니다. 학습 데이터는 그보다 작은 seed로 만드세요.

## 출력 구조

```
out/
  html/<서류ID>_<seed>.html              렌더링된 HTML
  images/<서류ID>_<seed>.png             (--png) 이미지. 여러 쪽이면 _p1.png, _p2.png ...
  images/<서류ID>_<seed>_aug0.jpg        (--augment) 스캔·촬영 증강 이미지
  labels/<서류ID>_<seed>.json            정답 + 필드별 타입·정규화 값·위치
  manifest.jsonl                         샘플 목록
  swift/<과제>.jsonl, swift/all.jsonl    (--png) ms-swift 학습 데이터
```

같은 `seed`(파일명 숫자)를 가진 서류들은 같은 고객의 서류입니다. 은행 서식의 label·manifest에는 서식을 낸 은행이 `bank`로 기록됩니다.

`--bank`를 주지 않으면 고객의 약 10%는 외환은행, 6%는 KEB하나은행 서식으로 만들어집니다(시나리오 생성 제외). 이 서식들은 2011~2020년 날짜이므로 같은 고객의 외부 발급 서류와 날짜가 맞지 않습니다.

### labels/*.json

```json
{
 "id": "loan_application_000003", "doc_type": "loan_application", "doc_name": "대출거래신청서",
 "images": ["images/loan_application_000003.png"], "pages": [{"width": 1588, "height": 2246}],
 "fields": [
  {"key": "loan.amount", "label": "대출신청금액", "type": "amount", "value": "56,000,000",
   "norm": 56000000, "page": 0, "bbox": [x0, y0, x1, y1], "label_bbox": [x0, y0, x1, y1]},
  {"key": "loan.rate_type", "label": "금리방식", "type": "checkbox", "value": "변동", "page": 0,
   "options": [{"text": "고정", "checked": false, "box_bbox": [...], "bbox": [...]},
               {"text": "변동", "checked": true,  "box_bbox": [...], "bbox": [...]}]},
  {"key": "seal.applicant", "label": "신청인", "type": "seal", "present": true, "kind": "인감",
   "value": "김나우", "anchor": "signature", "page": 0, "bbox": [...]},
  {"key": "sign.applicant", "label": "신청인", "type": "signature", "present": false, "page": 0, "bbox": [...]}
 ],
 "gt": {"loan": {"amount": "56,000,000", "rate_type": "변동"}, "seal": {"applicant": true}, "sign": {"applicant": false}}
}
```

- **좌표:** 이미지 픽셀 `[x0, y0, x1, y1]`, 해당 쪽(`page`, 0부터) 왼쪽 위 기준입니다.
- **값(`value`)과 정규화 값(`norm`):** `value`는 문서에 찍힌 그대로, `norm`은 날짜 `YYYY-MM-DD`, 금액 정수, 전화번호 숫자 등입니다. 빈 칸은 `null`입니다.
- **체크박스:** 보기마다 체크 여부와 □/■ 칸 위치(`box_bbox`)가 있습니다. 정답 값은 체크된 보기입니다.
- **도장·서명:** `seal.<자리>`, `sign.<자리>`. 서명란은 랜덤으로 도장 / 서명 / 빈 칸이 되고, 없을 때도 그 자리 위치가 기록됩니다.
- **키 목록과 규칙:** 서류별 전체 키·항목명·타입은 [docs/SCHEMA.md](docs/SCHEMA.md)(기계용 `schema/schema.json`)에 있습니다.
- **좌표 확인:** `python scripts/visualize_labels.py out/labels/<파일>.json` 으로 위치를 그린 이미지를 만듭니다.

### swift/*.jsonl (ms-swift 학습용)

Qwen-VL 계열을 ms-swift로 학습하는 형식입니다. 한 줄이 학습 샘플 하나입니다.

```json
{"id": "loan_application_000003:kie", "task": "kie", "augment": "clean",
 "images": ["images/loan_application_000003.png"],
 "messages": [{"role": "user", "content": "<image>이 문서의 종류를 판별하고, ... JSON으로 추출하세요."},
              {"role": "assistant", "content": "{\"document_type\": \"대출거래신청서\", \"loan\": {...}}"}]}
```

| 과제 | 질문 | 답 |
|---|---|---|
| `kie` | 전체 추출 | 서류 종류 + 전체 정답 JSON (빈 칸 null, 도장·서명 true/false) |
| `kie_keys` | 지정한 키 목록 (문서에 없는 키도 가끔 섞음) | 그 키들만 평탄 JSON, 없으면 null |
| `grounding` | 위치 포함 추출 | `[{"key", "label", "value", "bbox_2d"}]` |
| `marks` | 체크박스·도장·서명 판별 | 체크 상태·날인·서명 여부와 위치 |
| `qa` | 항목 하나 질문 | 값 또는 예/아니오 |

- **좌표(`bbox_2d`):** 기본은 0~1000 상대 좌표 정수입니다(Qwen2-VL·Qwen3-VL 방식). `--coord pixel`이면 픽셀 좌표입니다. 학습할 모델 버전의 좌표 방식을 한 번 확인하세요.
- **여러 쪽 서류:** `<image>`가 쪽 수만큼 들어가고, 위치 답에 `page`(1부터)가 붙습니다.
- **증강 이미지:** 회전·이동·축소를 위치 정답에도 똑같이 적용하므로 `grounding`/`marks`에도 씁니다.
- **경로:** `images`는 출력 폴더 기준 상대 경로입니다. 학습은 출력 폴더에서 실행하거나 경로를 바꿔 쓰세요.
- 일부 과제만: `--tasks kie,kie_keys`

```bash
python -m docgen generate --n 500 --out out --png --augment 2
cd out && swift sft --model <Qwen-VL 모델> --dataset swift/all.jsonl ...
```

## 서식 변형 (여러 쪽·특수 상황)

서류마다 실제로 생기는 예외적인 경우가 정해진 확률로 섞여 나옵니다. 서류별 경우·확률·새 키는 [docs/variants/](docs/variants/)에 있습니다.

- **내용이 많은 경우(heavy):** 서류마다 15~35% 확률입니다. 주소이력 20~40건, 거래 수백 줄, 품목 20~60개처럼 내용이 길어집니다.
- **여러 쪽 나눔:** 브라우저에서 자동으로 합니다 ([docgen/paginate.js](docgen/paginate.js)).
  - 표는 줄 단위로 자르고 머리글 줄을 다음 쪽에 반복합니다.
  - 발급번호 줄은 쪽마다 다시 찍힙니다.
  - 쪽 번호와 "다음 쪽에 계속"이 들어갑니다. 영문 서류는 "Page 1 of 3"입니다.
  - 발급기관과 직인은 마지막 쪽에 옵니다.
- **특수 상황(special):** 서류마다 2~5가지가 있고, 각각 5~30% 확률입니다.
  - 예: 등기부 말소사항(빨간 밑줄·취소선), 초본 개명, 가족관계 이혼·재혼·사망, 법인 상호·본점 변경, 계약서 특약, 납세 유예, 신용장 거래.
- **손글씨 정정:** 고객이 손으로 쓰는 서식(은행 서식, 계약서, 위임장, 서면 신고서)에서 4~8% 확률로 나옵니다.
  - 틀린 값에 두 줄을 긋고, 옆에 바른 값과 작은 정정 도장을 찍습니다.
  - 정답은 바른 값이고, 라벨의 `corrected_from`에 틀린 값이 남습니다.
- **같은 고객의 서류는 같은 사정을 공유합니다.** 예를 들어 상호 변경일은 등기부, 정관, 사업자등록증에서 같습니다.

확률을 바꾸려면 환경변수를 씁니다.

```bash
DOCGEN_HEAVY=1 python -m docgen generate ...          # 내용이 많은 경우를 항상 (0 이면 끔)
DOCGEN_SPECIAL=all python -m docgen generate ...      # 특수 상황을 모두 켬 (none 이면 끔, 이름,이름 이면 그것만)
```

**학습 시 참고 (Qwen-VL):**
- 여러 쪽 서류는 이미지 여러 장이 한 샘플에 들어갑니다.
  - 쪽마다 이미지 토큰이 들고, 긴 서류는 3~4쪽까지 나옵니다.
  - ms-swift의 `MAX_PIXELS`(이미지 한 장의 최대 픽셀)와 `--max_length`를 함께 정하세요.
- 기본 `--scale 2.0`이면 A4 한 쪽이 약 1588×2246 픽셀(1.5면 1190×1684)입니다.
  - `MAX_PIXELS=1003520`(약 1280개의 28×28 칸)이면 쪽당 약 1280 토큰입니다.
  - 등기부·명세서처럼 글자가 작은 서류는 해상도를 너무 줄이면 읽기 어려우니 확인해 보세요.

## 하나은행 원본 서식 (원본 PDF 오버레이)

`add_template/하나은행_서식자료/` 의 하나은행 공개 서식 PDF는 **원본을 그대로 배경으로 깔고 값만 얹어** 만듭니다. HTML로 서식을 다시 그리지 않으므로 이미지 속 서식은 원본과 똑같습니다. 서류 ID는 `hf<No>`(No는 엑셀 목록 번호), 그룹은 `hana`입니다.

```bash
python -m docgen generate --types hana --n 1 --png --out out     # 원본 서식 전부
python -m docgen generate --types hf169 --n 3 --png --out out    # 한 서식만
```

1. **기재 자리 뽑기** — [scripts/extract_form_layout.py](scripts/extract_form_layout.py)가 PDF의 글자(위치·색)와 표 선에서 고객이 쓰는 자리를 찾아 `add_template/layouts/<분류>/<No>.json`에 저장합니다.
   - `text`: 라벨 칸 오른쪽(또는 머리글 아래)의 빈 칸, 같은 칸 안 라벨 오른쪽 빈자리, `성명 : ____` 같은 콜론 뒤 빈칸
   - `check`: `□` 보기 묶음 (`□` 위치와 보기 글자 위치)
   - `date`: `년 월 일` 빈칸, `sign`: `(서명 또는 인)` 자리, `copy`: 회색 안내 문구를 따라 쓰는 자필 기재란
   - 회색 안내 글자(`상품명 전체 자필기재`)는 빈 칸으로, 결재란·전산인자란·은행 사용란은 고객 칸이 아닌 것으로 봅니다.
2. **값 채우기** — [docgen/realform.py](docgen/realform.py)가 항목명으로 값을 정합니다.
   - 성명·생년월일·주소·전화·계좌 같은 항목은 고객 프로필에서 가져옵니다(같은 고객의 다른 서류와 일치).
   - `대리인`·`받는 분` 구역의 성명·연락처는 대리인·해외 수취인 값으로 바뀝니다.
   - 나머지는 항목명 끝말로 종류(날짜·금액·비율·번호·상품명·회사명 …)를 정하고, 뜻을 모르는 칸은 비워 둡니다.
   - 표의 반복 행(상품명·매수비율 …)은 위에서부터 몇 줄만 채우고, 비율은 합이 100이 되게 나눕니다.
3. **그리기** — [templates/\_real_form.html.j2](templates/_real_form.html.j2)가 쪽마다 PDF 이미지를 깔고 값을 절대 위치로 얹습니다.
   - 글씨: 서류마다 손글씨(나눔손글씨 펜·붓, 하이멜로디, 감자꽃 — `fonts/`, OFL) 70%, 인쇄체 30%. 손글씨는 글자마다 조금씩 기울고 흔들립니다.
   - 체크: 손으로 그은 V(SVG), ■ 칠하기, ○ 중 하나. 도장·서명은 기존 서류와 같은 모양입니다.
   - 배경 PNG는 처음 쓸 때 PDF에서 만들어 `~/.cache/docgen/bg/`에 둡니다. 배경과 글꼴은 렌더러가 `https://docgen.local/` 주소로 넘겨 줍니다(HTML만 열면 배경이 보이지 않습니다).
4. **정답** — 다른 서류와 같은 `f()` 규약이라 GT·위치·ms-swift 학습 데이터가 그대로 나옵니다. 키는 표준 항목은 영어 경로(`customer.name`, `account`, `agent.name`), 서식 고유 항목은 한글 항목명(`매수비율`), 표 행은 `기업부담금_목록.0.상품명` 꼴입니다.

서식별 등록 여부와 찾은 자리 수는 [docs/FORM_MAP.md](docs/FORM_MAP.md)에 있습니다 (`python scripts/form_map.py > docs/FORM_MAP.md`).
PDF가 바뀌거나 추출 규칙을 고치면 `python scripts/extract_form_layout.py`(전체) 또는 `--no 169`(한 건, 결과 요약 출력)로 다시 뽑습니다.

## 구조

```
docgen/
  korean.py      이름(한글/한자/로마자), 주소, 주민·사업자·법인번호, 금액·날짜 포맷
  entities.py    고객 프로필 (본인·가족·직장·사업체·법인·부동산·계좌·해외거래처)
  registry.py    서류 등록(@doc), 그룹, 업무 시나리오
  banks.py       은행별 서식 표기, 옛 은행(외환·KEB하나) 시기 이동
  render.py      Jinja2 렌더링 + GT 수집(f(), 체크박스·도장·서명 기록), 랜덤 스타일
  schema.py      타입 추론·정규화 값·키 통일, 위치 합치기
  swift.py       ms-swift 학습 레코드 (과제별)
  image.py       Playwright 로 PNG + 위치 (값·항목명·체크칸·도장)
  paginate.js    넘친 쪽을 여러 쪽으로 나눔 (머리글 줄 반복, 쪽 번호)
  augment.py     스캔/촬영/팩스 증강
  cli.py         list / generate / check
  bench/         벤치마크: 평가 세트 만들기(build), 모델 실행(run), 채점(eval) — docs/BENCHMARK.md
  realform.py    하나은행 원본 서식 오버레이 — 레이아웃 → 값 → 렌더링 지시, 배경·글꼴 제공
  docs/*.py      서류별 데이터 생성 함수 (그룹별 파일, docs/real_forms.py 가 원본 서식 전부를 등록)
templates/
  _base.html.j2, _macros.html.j2   공통 레이아웃·매크로
  _real_form.html.j2               원본 서식 오버레이 템플릿
  <그룹>/<서류ID>.html.j2          서류별 수제 템플릿
  bank_form/_loan_parts.html.j2    서식번호 줄(FORMS 표)·결재란·은행 사용란 — 은행 서식 전 그룹이 공유
add_template/하나은행_서식자료/    원본 서식 PDF (공개 서식) 와 다운로드 결과
add_template/layouts/             PDF 에서 뽑은 기재 자리 (생성 파일)
fonts/                             손글씨 글꼴 (woff2, SIL OFL)
scripts/extract_form_layout.py     서식 PDF → 기재 자리 레이아웃
scripts/form_map.py                서식별 등록 여부 → docs/FORM_MAP.md
scripts/make_samples.py            samples/ 갱신 (변형 샘플은 samples/variants/, 은행별은 samples/bank_variants/)
scripts/build_schema.py            docs/SCHEMA.md, schema/schema.json 갱신
scripts/visualize_labels.py        라벨 위치를 이미지에 그려 확인
tests/                             pytest
```

은행이 직접 쓰는 서식 그룹(`bank_form`)은 `registry.BANK_FORM_GROUPS`로 묶여 있습니다. 이 그룹의 서류는 렌더링할 때 서식을 낸 은행(옛 은행 포함)에 맞춰 프로필이 바뀌고, 템플릿에 서식 문맥 `bk`가 들어갑니다. 그룹을 새로 만들 때 이 집합에 넣어 주면 같은 동작을 받습니다.

서류를 추가하거나 수정하는 방법은 [docs/TEMPLATE_GUIDE.md](docs/TEMPLATE_GUIDE.md)를 보세요.

## 서식 현실화 현황

HTML 템플릿 70종을 실제 서식과 비교해 서식 번호, 항목 구성·순서, 라벨 문구, 고정 문구를 맞췄습니다. (하나은행 원본 서식 406종은 원본 PDF 자체를 쓰므로 해당 없음.) 비교 대상은 법령 별지 서식, 은행연합회 표준, 공공기관 발급본입니다. 서류별 근거, 출처, 수정 내용은 [docs/REALISM_STATUS.md](docs/REALISM_STATUS.md)에 있습니다. 담당 그룹별 원본과 메모는 `docs/realism/*.md`에 있습니다.

- **반영(검색근거) 69종:** 웹 검색 결과를 두 곳 이상에서 교차 확인해 반영했습니다. 원본 서식 이미지·PDF를 직접 열어 대조하지는 못했습니다. 작업 환경의 네트워크 정책으로 law.go.kr, gov.kr, kfb.or.kr 등에 접속할 수 없었기 때문입니다.
- **보류 1종(부채증명서):** 은행별 실제 표 구성을 확인하지 못해 기존 서식을 유지했습니다.
- **원본 대조 방법:** 해당 도메인 접속을 허용하거나 실제 서류 스캔본을 주면 칸 배치까지 대조해 `반영(원본대조)`로 올릴 수 있습니다.

현실화 과정에서 일부 GT 키가 바뀌었습니다. 예를 들어 위임장 `agent.rrn`은 `agent.birth`가 되었고, FATCA `us_person`은 `residence_category`가 되었습니다. 서류별 변경 내역은 `docs/realism/*.md`에 있습니다.

## 알려진 한계

- **원본 서식의 기재 자리 인식:** PDF의 글자·선으로 자리를 찾으므로 복잡한 서식(은행거래신청서처럼 칸이 촘촘하고 색이 많은 것)은 일부 칸을 못 찾아 빈칸으로 남습니다. 표 인식이 칸을 잘못 나눈 곳은 값이 칸 경계에 걸치기도 합니다. 서식별 찾은 자리 수는 [docs/FORM_MAP.md](docs/FORM_MAP.md)에 있습니다.
- **원본 서식의 값:** 성명·주소·계좌 등 표준 항목은 고객 프로필과 이어지지만, 서식 고유 항목(채권번호·HS코드 …)은 항목명으로 종류만 추론한 값이고 뜻을 모르는 칸은 비워 둡니다. 서식 고유 항목의 키는 한글 항목명입니다.
- **원본 서식에서 빠진 것:** XLS·DOC·EXE 원본, 고객 기재란이 없는 인쇄물(약관·안내장 등), 글자 인코딩이 깨진 영문 서식 1종 등 35종은 넣지 않았습니다. [docs/FORM_MAP.md](docs/FORM_MAP.md)에 표시돼 있습니다.
- **확인하지 못한 세부 항목:** 표의 칸 배치, 일부 안내 문구, 서식 번호의 최신 개정일 등은 검색으로 확인하지 못했습니다. 은행 서식의 서식번호 일부는 형식만 실제와 같은 임의값입니다.
- **긴 서류와 신분증:** 내용이 길면 여러 쪽으로 나오지만, 약정서 약관 전문처럼 매우 긴 고정 문구는 일부만 넣었습니다. 신분증은 앞면만 있습니다.
- **필기 표현:** 서명은 선으로 그린 낙서 모양입니다. 원본 서식의 손글씨는 손글씨 글꼴 4종이라 사람마다 다른 필체의 다양성은 제한적입니다. HTML 템플릿 서류의 자필 기재란은 일반 폰트로 흉내 냈습니다.
- **변형 문구:** 말소 표시 방식, 공증 문구, 감면 코드 등 일부 특수 상황의 문구는 실제 서식으로 확인하지 못한 추정입니다. 서류별 메모는 [docs/variants/](docs/variants/)에 있습니다.
- **스캔·촬영 실제감:** 증강은 Pillow 기반의 단순한 효과입니다. 원근 왜곡이나 구겨짐은 없습니다.
- **조합의 개연성:** 한 고객이 근로자이면서 개인사업자이자 법인 대표로 생성됩니다. 서류별로는 문제가 없지만 시나리오를 넘나들면 비현실적인 조합이 됩니다.
