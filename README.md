# document_gen — 은행 제출 서류 합성 데이터 생성기

고객이 은행에 제출하는 서류 **70종**을 HTML 템플릿으로 재현했습니다. 가상 고객 데이터를 채워 넣어 **VLM 정보추출(Key Information Extraction) 학습 데이터**를 만듭니다.

- **외부 발급 서류 56종**: 신분증, 등·초본, 가족관계증명서, 소득금액증명원, 원천징수영수증, 등기부등본, 사업자등록증, 재무제표, 인보이스 등
- **은행 자체 서식 14종**: 대출신청서, 여신거래약정서, 근저당권설정계약서, 고객확인서(KYC), 해외송금신청서 등
- 전체 목록: [docs/DOCUMENTS.md](docs/DOCUMENTS.md)
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

## 사용법

```bash
# 서류·시나리오 목록
python -m docgen list

# 전 서류 x 고객 100명 → HTML + 정답 JSON
python -m docgen generate --n 100 --out out

# 이미지(PNG) + bbox + VLM 학습용 jsonl 까지
python -m docgen generate --n 100 --out out --png

# 샘플마다 스캔/촬영 증강 이미지 2장 추가
python -m docgen generate --n 100 --out out --png --augment 2

# 특정 서류나 그룹만
python -m docgen generate --types income_certificate,pay_stub --n 50 --out out --png
python -m docgen generate --types corporate,fx --n 50 --out out --png

# 업무 시나리오 단위 (같은 고객의 제출 서류 묶음)
python -m docgen generate --scenario mortgage --n 30 --out out --png

# 템플릿 검증 (예외, 표시되지 않은 값, 페이지 넘침)
python -m docgen check --png
```

시나리오는 8개입니다: `account_opening`, `personal_credit_loan`, `mortgage`, `jeonse_loan`, `sole_proprietor_loan`, `corporate_credit`, `fx_remittance`, `study_abroad_remittance`

## 출력 구조

```
out/
  html/<서류ID>_<seed>.html        렌더링된 HTML
  images/<서류ID>_<seed>.png       (--png) 이미지
  images/<서류ID>_<seed>_aug0.jpg  (--augment) 증강 이미지
  labels/<서류ID>_<seed>.json      정답 + 필드별 라벨/bbox
  manifest.jsonl                   샘플 목록
  vlm.jsonl                        (--png) VLM 학습용 대화 형식
```

같은 `seed`(파일명 숫자)를 가진 서류들은 같은 고객의 서류입니다.

### labels/*.json

```json
{
 "id": "employment_certificate_000007", "doc_type": "employment_certificate", "doc_name": "재직증명서",
 "group": "income", "category": "external", "profile_seed": 7,
 "fields": [
  {"key": "employee.name", "label": "성명", "value": "김소윤", "bbox": [262.5, 501.0, 310.4, 523.5]},
  ...
 ],
 "gt": {
  "doc_no": "제 2025-171 호",
  "employee": {"name": "김소윤", "rrn": "901121-2030821", "address": "광주광역시 서구 내방로 75, ..."},
  "employment": {"department": "경영지원팀", "position": "차장", "period": "2014년 12월 01일 ~ 현재"},
  "company": {"name": "(주)새한소프트", "biz_no": "458-86-13197", ...},
  "issue_date": "2025년 11월 29일"
 }
}
```

- `gt`: 중첩 JSON 정답. 반복 항목(거래내역, 가족, 품목 등)은 리스트입니다.
- `fields`: 평탄화된 필드 목록입니다.
  - `label`: 문서에 적힌 한글 항목명
  - `bbox`: 이미지 픽셀 좌표 `[x0, y0, x1, y1]`
  - 한글 키 기반 정답을 만들거나 grounding 학습을 할 때 씁니다.

### vlm.jsonl

```json
{"id": "...", "image": "images/....png", "doc_type": "...", "augment": "clean",
 "messages": [
  {"role": "user", "content": [{"type": "image", "image": "images/....png"}, {"type": "text", "text": "이 문서의 종류를 판별하고, ... JSON으로 추출하세요."}]},
  {"role": "assistant", "content": [{"type": "text", "text": "{\"document_type\": \"재직증명서\", ...}"}]}
 ]}
```

Qwen2-VL, InternVL 등 대화형 VLM 파인튜닝 포맷에 맞춰 바로 쓰거나 변환해서 쓸 수 있습니다.

## 구조

```
docgen/
  korean.py      이름(한글/한자/로마자), 주소, 주민·사업자·법인번호, 금액·날짜 포맷
  entities.py    고객 프로필 (본인·가족·직장·사업체·법인·부동산·계좌·해외거래처)
  registry.py    서류 등록(@doc), 그룹, 업무 시나리오
  render.py      Jinja2 렌더링 + GT 수집(f()), 랜덤 스타일
  image.py       Playwright 로 PNG + bbox
  augment.py     스캔/촬영/팩스 증강
  cli.py         list / generate / check
  docs/*.py      서류별 데이터 생성 함수 (그룹별 파일)
templates/
  _base.html.j2, _macros.html.j2   공통 레이아웃·매크로
  <그룹>/<서류ID>.html.j2          서류별 템플릿
scripts/make_samples.py            samples/ 갱신
tests/                             pytest
```

서류를 추가하거나 수정하는 방법은 [docs/TEMPLATE_GUIDE.md](docs/TEMPLATE_GUIDE.md)를 보세요.

## 알려진 한계

- **양식 재현도**: 실제 서식을 기억에 기반해 재현했습니다. 항목 구성과 표기 관행은 최대한 맞췄지만 별지 서식 번호, 일부 코드값(업종코드, 송금 거래코드 등), 세부 레이아웃은 실물과 다를 수 있습니다. 실제 서류 스캔본과 나란히 비교해 보정하는 것을 권합니다.
- **보험요율·세율**: 2026년 국민연금·건강보험 요율은 검증하지 않은 값입니다. 공제 항목은 합성값입니다.
- **페이지 범위**: 긴 서류(정관, 약정서, 등기부 등)는 첫 페이지나 핵심 페이지만 표현합니다. 신분증은 앞면만 있습니다.
- **필기 표현**: 손글씨 서명과 자필 기재란은 필기체 폰트가 아니라 일반 폰트를 기울여 흉내 냈습니다.
- **스캔·촬영 실제감**: 증강은 Pillow 기반의 단순한 효과입니다. 원근 왜곡이나 구겨짐은 없습니다.
- **조합의 개연성**: 한 고객이 근로자이면서 개인사업자이자 법인 대표로 생성됩니다. 서류별로는 문제가 없지만 시나리오를 넘나들면 비현실적인 조합이 됩니다.
