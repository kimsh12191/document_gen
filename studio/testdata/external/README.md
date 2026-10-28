# 서류 넣기 시험용 외부 공개 문서

생성기(`docgen`)에 없는 양식으로 서류 넣기(studio/DESIGN.md 15절)의 "새 서식"·"원본 데이터로"·"건너뛰기"·키 사전 대기 탭을 시험한다.
`python -m studio.intake_testset`이 `bundle/`을 기본으로 섞는다(외환 업무 건에 인보이스·지급 청구서, 계좌개설 건에 다른 서류).

| 출처 | 라이선스 | 문서 | 라벨 |
|---|---|---|---|
| [invoice-x/invoice2data](https://github.com/invoice-x/invoice2data) `tests/compare` @9066f0d | MIT | 인보이스 11건 (영어·네덜란드어·프랑스어, EUR·USD·INR) | 원래 정답 JSON 값 (issuer, amount, date, invoice_number, iban, bic, vat …) |
| [docling-project/docling](https://github.com/docling-project/docling) `tests/data` @4f00195 | MIT | 스위스 QR 청구서(이미지) 1, 입력란 있는 PDF 1 | QR 청구서는 손으로 적은 값 8개(`sources.json`), PDF는 입력란 값 |
| [Unstructured-IO/unstructured](https://github.com/Unstructured-IO/unstructured) `example-docs/pdf` @07d978b | Apache-2.0 | 메모 1, 한국어 카드 안내문 1 | 없음 (건너뛰기 시험용) |

- `sources/` 원본, `licenses/` 라이선스 전문, `sources.json` 목록·라벨, `bundle/` 만들어 둔 묶음(쪽 이미지 150dpi · 사내 OCR 형식 OCR · 추출 결과 · `truth.json`에 출처 URL·SHA-256).
- 추출 키는 출처의 이름 그대로다(표준 키가 아님). 값 위치는 OCR 단어에서 찾아 붙였고, 문서에 안 찍힌 값(예: `mandate_id`)은 위치 없이 남는다 — `truth.json`의 `boxes`.
- 다시 만들기: `python -m studio.intake_external studio/testdata/external/bundle`. PDF 안 그림 속 글자는 로컬 OCR(`pip install rapidocr_onnxruntime`)이 있을 때만 OCR 에 들어간다. QR 청구서 이미지의 OCR은 같은 OCR로 미리 만들어 `sources/docling/qr_bill_example.ocr.json`에 두었다.
