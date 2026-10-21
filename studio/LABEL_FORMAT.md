# 정답 라벨 표준 v1 — 생성 데이터와 외부 데이터 공통

**입력 라벨은 `docgen generate --png`의 `labels/*.json`과 같은 형태로 고정한다.** 사용자는 이 규격에 맞춰 이미지와 정답을 준비한다. 데이터마다 키·구조를 새로 협의하지 않는다. 기존 모델의 추론 결과 `pred/*.json`은 별도 후보 입력이며 정답 라벨과 구분한다.

규격 파일: [document.schema.json](static/label-format/v1/document.schema.json). 예제 전체: [example.zip](static/label-format/v1/example.zip). 예제는 저장소의 합성 주민등록증 이미지와 실제 생성 라벨을 사용한다. **예제 ZIP을 풀어 ④ 가져오기 → 라벨 있는 데이터에 폴더 경로를 넣으면 검사·확인 후 데이터셋을 생성해 ⑥에 자동 등록한다.** 원본 라벨을 편집하는 기능은 아직 없으며 오류·수정은 원본 JSON에 반영하고 다시 검사한다.

## 1. 준비할 폴더

```text
my-data/
  meta.json
  images/
    case_001_id_card.jpg
  labels/
    case_001_id_card.json
  ocr/                         쪽 전체 OCR 정답이 있을 때만
    case_001_id_card.json
  bundles.jsonl                업무 묶음이 필요할 때만
```

문서마다 `labels/<id>.json` 하나를 만든다. 여러 쪽은 라벨의 `images`에 쪽 순서대로 적는다. 이미지 경로는 데이터 루트 기준 상대 경로다. 이미지 파일명만으로 문서·쪽을 추정하지 않고 라벨의 명시적인 연결을 사용한다. 입력 이미지는 쪽별 PNG/JPG로 준비한다. 원본 PDF만 있는 현재 이미지 가져오기와 구분한다.

`meta.json`은 외부 반입 패키지 정보다. 아래는 사람이 확인한 실서류의 예시이며, 생성기의 개별 라벨에 이 메타 정보를 추가할 필요는 없다.

```json
{
  "format": "docgen-labels/1",
  "name": "내 라벨 데이터",
  "real_data": true,
  "gt": "reviewed"
}
```

studio가 내보낸 폴더(⑤ 라벨 검수, ④ 서류 넣기의 원본 데이터로)는 `from_batch`(가져온 묶음), `model`(추출 결과를 낸 모델), `split`(train·test)을 더 적는다. `gt: pseudo`이고 `model`이 있으면 그 폴더로 만든 데이터셋에서 그 모델의 답은 채점하지 않는다(자기 답으로 자기를 채점하는 꼴).

`gt`는 `reviewed`(사람 확인 정답), `pseudo`(모델 결과 등 미검수 후보), `exact`(합성 생성 정답)로 구분한다. 라벨 파일이 있다는 이유만으로 사람이 확인한 정답으로 간주하지 않는다. `real_data:true`에 `exact`를 사용할 수 없다. 합성 생성 폴더도 이 반입 `meta.json`을 추가하고 기존 개별 라벨은 그대로 사용한다. `ocr_scope: "full_page"`는 모든 쪽의 고정 인쇄 글자까지 OCR 정답으로 준비한 경우에만 추가한다. 예제의 `fields_only_example`은 쪽 전체 정답이 아니다.

## 2. 문서 라벨: 생성기의 `fields` 형식

```json
{
  "id": "case_001_id_card",
  "doc_type": "resident_id_card",
  "doc_name": "주민등록증",
  "images": ["images/case_001_id_card.jpg"],
  "pages": [{"width": 1000, "height": 630}],
  "fields": [
    {
      "key": "name",
      "label": "성명",
      "type": "text",
      "value": "홍길동",
      "norm": "홍길동",
      "page": 0,
      "bbox": [100, 120, 300, 160]
    },
    {
      "key": "issue_date",
      "label": "발급일",
      "type": "date",
      "value": "2026.10.20",
      "norm": "2026-10-20",
      "page": 0,
      "bbox": [400, 500, 600, 540]
    }
  ]
}
```

| 항목 | 규칙 |
|---|---|
| `id` | 데이터 안에서 고유한 문서 ID. `labels/<id>.json`과 맞춤 |
| `doc_type` | 서식 ID. 기존 서식은 생성기의 ID를 그대로 사용 |
| `doc_name` | 서류명. 예: 주민등록증 |
| `images` | 데이터 루트 기준 쪽 이미지 상대 경로, 쪽 순서대로 |
| `pages` | 같은 순서의 실제 이미지 픽셀 크기 `width`, `height` |
| `fields` | 항목 정답 배열. 원본 생성 라벨과 동일 |
| `key` | 생성기와 같은 항목 키. 예: 주민등록증 성명은 `name`. 임의로 `applicant.name`으로 바꾸지 않음 |
| `label` | 문서에 적힌 항목명. 없으면 `null` |
| `type` | 아래 타입 중 하나 |
| `value` | 문서 표시 문자열 그대로. 빈 칸은 `null`. 숫자도 원문 문자열로 저장 |
| `norm` | 정규화한 값. 날짜는 ISO 날짜, 금액은 숫자 등. 생성기의 `docgen.schema.infer` 기준. 생략 가능 |
| `page` | **0부터**. `images[page]`를 가리킴 |
| `bbox` | **이미지 픽셀** `[왼쪽, 위, 오른쪽, 아래]`. 해당 쪽 기준 |
| `label_bbox` | 항목명 위치가 있을 때 같은 픽셀 좌표. 값 위치와 구분 |

`images`와 `pages`의 길이는 같아야 한다. 좌표는 이미지와 같은 크기·회전 기준으로 적고, 좌상단 ≤ 우하단 및 이미지 범위를 검사한다. 위치가 없는 값 전용 라벨은 `page`·`bbox`를 생략할 수 있다. 그 항목은 값 추출에만 쓰고 위치 평가·크롭 OCR에는 쓰지 않는다. `null`은 실제 빈 칸 정답이며 미라벨링 표시가 아니다. 라벨링하지 않은 항목은 `fields`에 넣지 않는다.

타입: `text`, `date`, `month`, `datetime`, `amount`, `amount_korean`, `number`, `percent`, `rrn`, `biz_no`, `corp_reg_no`, `phone`, `account_no`, `checkbox`, `checkbox_multi`, `seal`, `signature`.

서식별 정확한 키·타입은 [guide/fields/README.md](../guide/fields/README.md)와 [guide/fields/fields.json](../guide/fields/fields.json)을 따른다. 새 서식은 먼저 키를 정의하고 그 키를 라벨·추출 질문·비교 작업에서 함께 쓴다. `rows[].amount` 같은 사전 표기는 실제 라벨에서 `rows.0.amount`처럼 순번을 사용한다.

## 3. 체크박스·도장·서명

체크박스는 보기 전체와 선택 여부를 `options`에 저장한다. `bbox`는 보기 글자의 위치, `box_bbox`는 체크 상자의 위치다. 단일 선택 `value`는 선택한 보기 문자열, 선택이 없으면 `null`이다. 복수 선택은 `checkbox_multi`와 각 보기의 `checked`를 사용하며 선택 정답은 `options`에서 만든다.

```json
{
  "key": "consent",
  "label": "동의 여부",
  "type": "checkbox",
  "value": "동의",
  "page": 0,
  "options": [
    {"text": "동의", "checked": true, "box_bbox": [100, 300, 120, 320]},
    {"text": "미동의", "checked": false, "box_bbox": [200, 300, 220, 320]}
  ]
}
```

도장·서명은 **원본 라벨의 `present`**에 유무를 쓴다. `value`는 생성기와 같이 도장 글자·서명 문자열 또는 `null`이다. 모델 답의 boolean `value`와 혼동하지 않는다.

```json
{"key":"seal.issuer","label":"발급기관직인","type":"seal","value":"발급기관인","present":true,"page":0,"bbox":[700,450,800,550]}
```

## 4. OCR 정답도 생성기와 같은 형식

**항목 라벨 `fields`와 쪽 전체 OCR 정답은 별도다.** `fields`만으로는 제목·표 머리글·안내문 등 쪽 전체 OCR 정답을 채울 수 없다. 쪽 전체 OCR 데이터셋에는 이미지 한 쪽마다 `docgen.ocr_export.page_document`와 같은 아래 JSON을 준비한다. 여러 쪽은 이미지와 같은 상대 경로·확장자 없는 이름을 사용한다.

```json
{
  "filename": "case_001_id_card.jpg",
  "success": "Y",
  "data": {
    "basicData": [[{
      "text": "홍길동",
      "confidence": 1.0,
      "line_num": 0,
      "bounding": {
        "shape": "rectangle",
        "vertices": [
          {"x":100,"y":120}, {"x":300,"y":120},
          {"x":300,"y":160}, {"x":100,"y":160}
        ]
      }
    }]]
  }
}
```

좌표는 쪽 이미지 픽셀이다. 박스 꼭짓점 순서는 좌상→우상→우하→좌하다. 검수한 정답은 `confidence:1.0`으로 적을 수 있다. 같은 줄은 같은 `line_num`을 사용한다. 예제 ZIP에는 이 원본 구조의 **값 칸·항목명 OCR 일부 예시**만 포함하며 쪽 전체 OCR 정답으로 취급하지 않는다.

## 5. 시나리오 묶음

`bundles.jsonl`은 한 줄에 접수 건 하나다. `documents`에는 위 문서 라벨의 `id`를 쓴다. 필수 서류 목록은 시나리오 정의에서 읽고, 제출하지 않은 서류는 `documents`에 넣지 않는다.

```json
{"bundle_id":"case_001","scenario":"jeonse_loan","customer":"홍길동","documents":["case_001_id_card","case_001_lease"],"not_customer":[]}
```

이 파일은 외부 라벨 문서들을 연결하는 입력 목록이다. 생성기가 저장하는 결과 `bundles.jsonl`의 `docs`(해결된 문서·필드), 문항 ID·처리 결과 등은 문항 생성 후 채우는 출력 정보다. 사용자가 합성 seed·변조 이력 등을 꾸며 넣을 필요는 없다.

`customer`는 고객명(선택), `not_customer`는 명의 확인 후 타인으로 확인한 제출 문서 ID 목록이다. 타인 서류가 없으면 `[]`로 쓴다. 이 목록이 없으면 명의 미확인으로 **구비 문항을 생략**한다. 타인 명의의 필수 서류만 냈으면 그 서류를 missing과 not_customer 모두에 넣는다. 같은 서식 문서가 한 묶음에 여러 개 있으면 현재는 모호한 비교를 막기 위해 오류로 처리한다. `scenario`는 ③에 저장된 ID여야 한다.

③의 직접 추출/비교 작업과 기존 계산 규칙을 실제 라벨에 적용한다. 필요한 라벨·근거가 없으면 작업 결과에 생략 사유를 남긴다. 합성 변조 대조 사례로 `cross_check` 정답을 꾸며 내지 않는다. 가져온 묶음은 ⑥의 업무 묶음 탭에서 원본·문항·처리 결과를 확인하며 합성 seed 재생성 버튼은 표시하지 않는다.

## 6. question / answer는 같은 생성 규칙에서 만든다

원본 라벨과 모델 정답은 역할이 다르다. 입력 규격은 원본 생성 라벨로 고정하고, Q/A를 만들 때 기존 생성기·과제 계약을 사용한다.

| 원본 라벨 | 생성 문항 |
|---|---|
| `doc_name` | 문서 분류의 문자열 정답 |
| `fields`: 키·값·항목명·위치 | KIE 질문의 항목 목록과 답 |
| `options[].checked`, `present` | 체크·도장·서명 답 |
| 값 위치 + 이미지 | 값 칸 OCR 크롭·정답 |
| 쪽 전체 OCR JSON | 쪽 전체 OCR 과제 정답 |
| 묶음 문서·시나리오·규칙 | 구비·대조·심사 Q/A |

KIE/marks **모델 답**은 기존 계약대로 `bbox_2d` 0~1000, `page` 1부터다. 원본의 픽셀 `bbox`와 0부터 시작하는 `page`를 문항 생성 때 변환한다. 도장·서명 답은 `present`에서 boolean `value`로 변환한다. 실제 질문 필드명은 `prompt`이며 답은 `answer`, 채점 정보는 `eval`이다. 사용자가 이 세트를 문서마다 수동으로 작성하지 않는다.

## 7. 가져오기 UI의 적용 규칙

현재 제공하는 입력 흐름:

1. **④ 가져오기 → 라벨 있는 데이터**에서 데이터 루트 폴더 경로 입력. ZIP은 먼저 압축을 푼다.
2. 문서 ID·이미지 짝·쪽 수·이미지 크기·필드 타입·좌표·키를 검사. 잘못된 파일과 항목 경로를 한 번에 표시한다.
3. 정답 출처·검수 상태를 확인. 이미 확인한 정답은 불필요하게 OCR을 다시 호출하거나 추론 값으로 덮어쓰지 않는다.
4. 문서·쪽을 고르고 이미지의 정답 박스와 필드 값을 확인한다. 미등록 서식은 오류, 사전에 없는 새 키는 확인 사항으로 표시한다.
5. 데이터셋 이름·은행 업무/OCR·평가/학습·과제를 선택하고 정답 종류·문서·묶음 연결 확인란을 체크한다. OCR은 모든 쪽의 OCR 정답과 `ocr_scope:full_page`가 필요하다.
6. **데이터셋 만들고 등록** → ⑥에서 진행 확인 → 완료 후 목록에 자동 등록. 묶음 처리 결과와 실제 Q/A는 생성된 데이터셋에서 확인한다.

검사 후 파일이 바뀌면 다시 검사해야 한다. 원본은 읽기만 하고 출력 `input/`에 해시를 확인하며 복사한다. 은행 업무는 생성기의 동일 문항 코드를 사용하고 OCR은 저장된 정답으로 OCR 준비(`docgen.bench.ocr_prepare`)를 실행해 같은 데이터셋에 쪽 OCR 8과제를 더한다. OCR 서버와 렌더링 브라우저가 없어도 동작한다. 은행 업무 학습용은 `swift/all.jsonl`을 함께 생성한다. OCR 학습용은 문서 2건 이상을 문서 단위로 학습/평가 분리한다.

표준 경로에는 임의 JSON 키 대응 단계를 요구하지 않는다. 기존 `RESULTS_FORMAT.md`의 임의 OCR·모델 결과 매핑은 보조 경로로 유지한다. v1의 키·타입·좌표·쪽 번호 의미를 바꾸는 변경은 새 버전으로 낸다.
