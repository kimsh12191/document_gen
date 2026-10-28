"""guide/tasks.md: every task with a real example, its full question, answer and fields.

Reads a docgen benchmark folder (`python -m docgen.bench build`) and an OCR prepared folder
(`python -m docgen.bench.ocr_prepare`), picks one example per task, per cross_check case and per review
rule, copies the images it needs into guide/examples/img/ and writes guide/tasks.md.

  python guide/examples/make_catalog.py --bench <bench 폴더> --ocr <prepared 폴더> [--ocr-json <OCR JSON 폴더>]

Run it where docgen can be imported (the docgen container, or any env with Pillow).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "ocr"), str(ROOT / "bank")]
OUT_MD = ROOT / "guide" / "tasks.md"
IMG = ROOT / "guide" / "examples" / "img"
MAX_SIDE = 1000
EXAMPLES: list[dict] = []  # what the slides show: one entry per example, the same data as tasks.md

OCR_TASKS = ["crop_ocr", "bbox_ocr", "grounding", "region_ocr", "spotting", "relation", "marked_ocr", "marked_box"]
BANK_TASKS = ["doc_check", "cross_check", "review", "kie", "marks", "classify", "ocr_page", "ocr_field"]
TITLE = {"crop_ocr": "잘라낸 글자 읽기", "bbox_ocr": "박스 안 글자 읽기", "grounding": "글자 위치 찾기",
         "region_ocr": "영역 안 글자 전부 읽기", "spotting": "전체 글자 + 위치", "relation": "옆 글자 찾기",
         "marked_ocr": "그린 박스 안 글자 읽기", "marked_box": "그린 박스의 좌표",
         "doc_check": "서류 구비 확인", "cross_check": "서류 대조", "review": "심사 질의", "kie": "정보 추출",
         "marks": "체크박스·도장·서명", "classify": "서류 분류", "ocr_page": "전체 받아쓰기", "ocr_field": "값 칸 읽기"}

# -- field dictionaries: every key that appears in an example must be described here ----------------
OCR_ROW = {
    "id": "문항 ID: `<페이지 ID>_v<사본 번호>_<과제>_<순번>`",
    "task": "과제 이름",
    "document_id": "원본 문서 ID (manifest). 학습·검증·벤치마크는 이 단위로 나뉜다",
    "page_id": "원본 페이지 ID (manifest)",
    "split": "train / val / benchmark",
    "view": "입력 이미지 종류: `clean` 깨끗한 사본, `aug` 노이즈 사본",
    "view_id": "이 문항이 쓴 사본 이미지의 ID",
    "view_ops": "노이즈 사본에 적용한 변환 목록 (예: `scale0.760` 축소, `blur` 흐림, `rotate…`, `jpeg…`). 깨끗한 사본은 []",
    "reference_type": "정답의 출처. `ocr_pseudo_unreviewed` = 사내 OCR 결과, 사람 검수 없음",
    "messages": "모델에게 보내는 질문 (user 한 턴). `<image>` 자리에 images[0]가 들어간다",
    "images": "모델 입력 이미지 경로 1개 (사본, 잘라낸 단어, 타일, 색 박스 그림 중 하나)",
    "context_image": "이 문항을 만든 사본 페이지 이미지 (잘라낸 이미지·타일의 원래 페이지)",
    "target": "정답 JSON 문자열. 글자 과제는 `{\"text\"}`, 박스 과제는 `{\"boxes\": [{\"bbox_2d\", \"label\"}]}`",
    "confidence": "정답 단어들의 사내 OCR 신뢰도 중 최솟값 (평가에서 0.95 이상/미만으로 나눠 봄)",
    "masked_words": "(spotting만) 신뢰도가 낮아 타일에서 배경색으로 지우고 정답에서 뺀 단어 수",
    "size": "정답 박스 높이 구간 `small`(<12) / `medium`(<25) / `large` (0~1000 좌표 기준, 평가에서 나눠 봄)",
}
BANK_COMMON = {
    "id": "문항 ID: `<과제>/<묶음 또는 서류 ID>/<구분>`. 두 번째 칸이 고객(묶음) 단위라서, 학습·평가의 고객 겹침 검사와 GRPO용 고객 분리에 쓰인다",
    "task": "과제 이름",
    "images": "질문 앞에 순서대로 넣는 이미지 (세트 폴더 기준 상대 경로). 여러 쪽 서류는 `_p1`, `_p2` …",
    "prompt": "질문 문장 (docgen/bench/prompts.py 의 틀에 값을 채운 것)",
    "answer": "정답",
    "eval": "채점에 쓰는 추가 정보",
    "meta": "결과를 나눠 보는 기준 (채점에는 안 쓰임)",
}
META = {
    "scenario": "업무 ID (예: `jeonse_loan`)", "task_name": "업무 이름 (질문에 들어가는 이름)",
    "bundle": "고객 묶음 ID `<업무>_<seed>`", "customer": "고객 성명 (질문에 들어감)",
    "n_missing": "필수 서류 중 뺀 개수 (0~2, 다른 고객 서류로 바꾼 것은 세지 않음)", "not_customer": "다른 고객 서류를 섞었는지",
    "not_required": "업무와 상관없는 서류를 끼워 넣었는지", "n_docs": "질문에 보여 준 서류 수",
    "case": "불일치 사례 ID", "category": "사례 분류: typo 오기 / other_person 타인 / amount 금액 / logic 관계 / format 표기만 다름",
    "perturbed": "값을 바꾼 변조 문항인지 (false = 같은 서류 조합의 정상 문항)",
    "rule": "심사 질의 규칙 ID (`case:<사례>` = 서류 대조 사례에서 만든 예/아니오 질문)",
    "skill": "능력 분류: 계산(비율) / 계산(합계) / 날짜 계산 / 표 계산 / 서류 대조",
    "doc_type": "서류 ID (guide/documents.md)", "doc_name": "서류 정식 명칭", "group": "서류 그룹",
    "condition": "촬영 조건: clean 원본 / scan 스캔 / photo 촬영 / fax 팩스", "writing": "글씨: print 인쇄체 / hand 손글씨",
    "n_pages": "쪽 수", "key": "값 칸의 정답 키", "label": "값 칸의 항목명", "kind": "값 종류 (이름·금액·날짜 …)",
    "corrected": "손글씨 정정(두 줄 긋고 고쳐 씀)이 있는 칸인지", "length": "정답 글자 수 (공백 제외)",
}
EVAL = {
    "required": "필수 서류 목록 (질문에 번호로 나열한 것)",
    "names": "모델 답의 서류명을 대응시킬 후보: 필수 서류 + 끼워 넣은 서류",
    "documents": "질문에 보여 준 서류명 (모델 답의 document 를 이 중 하나로 대응시킴)",
    "answer_type": "`number` 숫자 / `yesno` 예·아니오", "tol": "숫자 답의 허용 오차 (질문에 적은 반올림 자릿수에 맞춤)",
    "days": "유효기간 문항: 발급일부터 신청일까지 일수 (정답 계산 근거)",
    "fields": "키마다 `type`(값 타입), `norm`(정규화 값: 날짜 YYYY-MM-DD, 금액 정수 …), `kind`(값 종류). 타입별로 표기 차이를 맞춰 비교",
    "types": "키마다 `checkbox` / `checkbox_multi` / `seal` / `signature`",
}
ANSWER = {
    "doc_check": "`missing` 빠진 필수 서류 (타인 서류만 낸 것 포함), `not_required` 필수 목록에 없는 서류, `not_customer` 고객 본인 명의가 아닌 서류. 세 목록이 모두 맞아야 완전 일치",
    "cross_check": "`consistent` 불일치가 없으면 true. `issues[]`: `document` 문제 서류, `field` 항목명, `value` 그 서류에 적힌 값, `expected` 다른 서류에 적힌(맞아야 할) 값, `alt_documents` 짝 서류(이 서류를 짚어도 정답 인정, 학습 레코드에서는 뺌)",
    "review": "숫자(문자열) 또는 `예` / `아니오`",
    "kie": "`{키: 문서에 적힌 값 또는 null}`. 빈 칸은 null",
    "marks": "체크박스: 체크된 보기 글자 (없으면 null) · 복수 선택: 목록 · 도장/서명: true / false",
    "classify": "서류 정식 명칭",
    "ocr_page": "서류에 채워 넣은 값들 (한 줄에 하나). 채점은 이 값들이 받아쓴 글에 들어 있는 비율",
    "ocr_field": "잘라낸 값 칸에 적힌 글자",
}
SCORE = {
    "doc_check": "주 지표: 완전 일치. 함께: 세 목록 합친 F1, 목록별 일치. 서류명은 후보(eval.names) 중 비슷한 이름으로 대응",
    "cross_check": "정상 문항: consistent=true 면 1. 변조 문항: consistent=false 이고 issues 에 문제 서류(또는 짝 서류)와 값·원래 값·항목명 중 하나를 맞게 짚으면 1. 함께: 탐지, 위치, 오탐률",
    "review": "숫자: 단위(%, 배, 원 …)를 떼고 tol 안이면 정답. 예/아니오: 네·아니요도 인정",
    "kie": "주 지표: F1 (값이 있는 칸 기준, 빈 칸에 값을 지어내면 감점). 날짜·금액·번호는 타입별로 표기를 맞춰 비교",
    "marks": "항목별 정확도",
    "classify": "공백·문장부호를 뺀 뒤 정식 명칭과 같으면 정답",
    "ocr_page": "값 재현율 (공백 무시). recall_fuzzy 는 값 길이 20% 까지 틀려도 인정",
    "ocr_field": "완전 일치 (공백 정규화), CER 함께",
}
OCR_SCORE = {
    "crop_ocr": "글자: CER·완전 일치. GRPO 보상 0.7×문자 유사도+0.3×숫자 유사도",
    "bbox_ocr": "글자: CER·완전 일치·숫자 일치",
    "grounding": "박스: IoU 0.5 F1 등. 정답이 [] 이면 [] 일 때만 맞음. 보상 min(1, IoU/0.8) 짝별 soft F1",
    "region_ocr": "글자: CER·완전 일치 + 순서 무관 단어 F1",
    "spotting": "박스+글자: 위치+글자 F1. 보상 0.5×min(1,IoU/0.8)+0.5×글자 유사도",
    "relation": "박스+글자: 위치+글자 F1 (박스 하나)",
    "marked_ocr": "글자: CER·완전 일치",
    "marked_box": "박스+글자: IoU 0.75 F1 (그린 사각형이라 정답 좌표가 정확함)",
}
OCR_HOW = {
    "crop_ocr": "OCR 단어 하나의 박스를 위아래 여백과 함께 잘라낸 이미지(`crops/`)를 준다. 신뢰도 0.95 이상·잘리지 않은 단어만",
    "bbox_ocr": "사본 페이지 전체 + 단어 하나의 박스 좌표(0~1000)를 질문에 넣는다",
    "grounding": "사본 페이지 + 글자. 페이지에 같은 글자가 여러 번 있으면 전부가 정답. 약 10%는 같은 분리의 다른 페이지에서 가져온, 이 페이지에 없는 글자(정답 [])",
    "region_ocr": "여러 단어를 덮는 영역(단어를 자르지 않게 넓힘). 영역 안에 신뢰도 낮은 단어가 하나라도 있으면 버림. 줄은 세로로 겹치는 단어끼리 묶고 위→아래, 왼→오른쪽",
    "spotting": "페이지를 잘라낸 타일(`tiles/`), 타일당 단어 40개 이하. 신뢰도 낮은 단어는 배경색으로 지우고 정답에서 뺌",
    "relation": "기준 글자(페이지에 하나뿐이면 글자, 아니면 박스 좌표) + 방향(오른쪽·왼쪽·위·아래). 가장 가까운 이웃이 분명할 때만",
    "marked_ocr": "사본에 빨강·파랑·초록 사각형(최대 3개)을 그린 이미지(`marked/`). 30%는 좌표도 함께 알려 줌",
    "marked_box": "같은 그림에서 색 하나를 묻고, 직접 그린 사각형의 바깥 테두리 좌표와 글자를 답한다",
}


def jdump(v, ind: int = 0, width: int = 110) -> str:
    """JSON, every value shown in full: short parts on one line, long ones broken per key / item."""
    flat = json.dumps(v, ensure_ascii=False)
    if len(flat) + ind <= width or not isinstance(v, (dict, list)) or not v:
        return flat
    pad = " " * (ind + 1)
    if isinstance(v, dict):
        body = [f"{pad}{json.dumps(k, ensure_ascii=False)}: {jdump(x, ind + 1, width)}" for k, x in v.items()]
        return "{\n" + ",\n".join(body) + "\n" + " " * ind + "}"
    body = [pad + jdump(x, ind + 1, width) for x in v]
    return "[\n" + ",\n".join(body) + "\n" + " " * ind + "]"


def code(text: str, lang: str = "") -> str:
    fence = "````" if "```" in text else "```"
    return f"{fence}{lang}\n{text}\n{fence}\n"


def table(rows: list[tuple[str, str]], head=("키", "뜻")) -> str:
    out = [f"| {head[0]} | {head[1]} |", "|---|---|"]
    out += [f"| `{k}` | {v.replace('|', '/')} |" for k, v in rows]
    return "\n".join(out) + "\n"


def copy_image(src: Path, tag: str = "") -> str:
    """Downscale a copy into guide/examples/img/ (long side MAX_SIDE, JPEG) and return its path from guide/."""
    h = hashlib.sha1(src.read_bytes() + f":{tag}".encode()).hexdigest()[:8]  # same image -> same name, wherever it was built
    name = f"{re.sub(r'[^A-Za-z0-9_-]', '_', src.stem)[:60]}{('_' + tag) if tag else ''}_{h}.jpg"
    dst = IMG / name
    if not dst.exists():
        with Image.open(src) as im:
            im = im.convert("RGB")
            im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            im.save(dst, quality=82)
    return f"examples/img/{name}"


def overlay(src: Path, boxes: list[list[int]], query: list[int] | None, tag: str) -> str:
    """The input image with the answer boxes (green) and the box given in the question (blue)."""
    h = hashlib.sha1(src.read_bytes() + f":{tag}:{boxes}:{query}".encode()).hexdigest()[:8]
    dst = IMG / f"{re.sub(r'[^A-Za-z0-9_-]', '_', src.stem)[:50]}_{tag}_{h}.jpg"
    if not dst.exists():
        with Image.open(src) as im:
            im = im.convert("RGB")
            w, hh = im.size
            d = ImageDraw.Draw(im)
            lw = max(2, w // 400)
            sc = lambda b: [b[0] * w / 1000, b[1] * hh / 1000, b[2] * w / 1000, b[3] * hh / 1000]
            if query:
                d.rectangle(sc(query), outline=(30, 90, 220), width=lw)
            for b in boxes:
                d.rectangle(sc(b), outline=(20, 170, 60), width=lw)
            im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            im.save(dst, quality=82)
    return f"examples/img/{dst.name}"


def imgs_html(paths: list[str], width: int = 300) -> str:
    return "<p>" + " ".join(f'<a href="{p}"><img src="{p}" width="{width}"></a>' for p in paths) + "</p>\n"


# -- OCR -----------------------------------------------------------------------------------------------
def ocr_section(prep: Path, ocr_json: Path | None) -> str:
    from docgen.bench.ocr_metrics import answer_for

    rows = [json.loads(x) for x in (prep / "benchmark_tasks.jsonl").open(encoding="utf-8")]
    pages = [json.loads(x) for x in (prep / "pages.jsonl").open(encoding="utf-8")]
    sft = [json.loads(x) for x in (prep / "train_sft.jsonl").open(encoding="utf-8")]
    grpo = [json.loads(x) for x in (prep / "train_grpo.jsonl").open(encoding="utf-8")]
    manifest_cfg = json.loads((prep / "config.snapshot.json").read_text(encoding="utf-8"))
    out = ["## OCR 과제\n",
           "실제 학습은 내부망 서류 이미지를 사내 OCR에 돌린 결과로 했습니다. 이 문서의 예시는 실제 이미지를 문서에 넣을 수 없어서, "
           "합성 서류 이미지에 **사내 OCR과 같은 형식의 결과 JSON**을 붙이고 **실제 학습 코드(`docgen.bench.ocr_data.scan` → `docgen.bench.ocr_prepare`)로 만든** 것입니다. "
           "파일 구조·필드·질문·정답 형식은 실제 학습 데이터와 같습니다. 예시용 OCR 결과는 생성기 정답(값 칸·항목명 위치)에서 만들어서 단어가 아니라 줄 단위입니다.\n"]

    # inputs
    out.append("### 1-0. 입력 데이터\n")
    page = next(p for p in pages if p["split"] == "benchmark")
    src_img = Path(page.get("source_image") or page["image"])
    out.append("**① 페이지 이미지** (원본, 1장)\n")
    out.append(imgs_html([copy_image(src_img)], 420))
    if ocr_json:
        oj = ocr_json / (src_img.stem + ".json")
        if oj.exists():
            out.append(f"**② 사내 OCR 결과 JSON** (`{oj.name}`, 이 페이지 전체. 실제 사내 OCR 응답과 같은 키)\n")
            out.append("<details><summary>펼치기</summary>\n\n" + code(jdump(json.loads(oj.read_text(encoding='utf-8')), width=230), "json") + "</details>\n")
    man = next(json.loads(x) for x in Path(manifest_cfg["manifest"]).open(encoding="utf-8")
               if json.loads(x)["page_id"] == page["page_id"])
    out.append("**③ manifest.jsonl 한 줄** (`scan` 결과)\n")
    out.append(code(jdump(man), "json"))
    out.append(table([("document_id", "문서 ID. 같은 문서의 쪽은 같은 ID (파일 이름 정규식으로 뽑음)"),
                      ("page_id", "페이지 ID (이미지 상대 경로)"), ("image", "이미지 경로"),
                      ("ocr_json", "미리 만든 OCR JSON 경로 (없으면 prepare 가 사내 OCR 서버를 호출)"),
                      ("split", "scan 때 준 분리. prepare 가 benchmark_fraction·val_fraction 비율로 문서 단위 재배정")]))
    out.append("**④ pages.jsonl 한 줄** (`prepare` 가 OCR JSON 을 읽어 정리한 것: 글자, 픽셀 박스 `bbox`, 0~1000 박스 `bbox_norm`, 신뢰도, 읽는 순서)\n")
    out.append("<details><summary>펼치기</summary>\n\n" + code(jdump(page, width=230), "json") + "</details>\n")

    # slides show the first items of the two long lists (the label says how many); tasks.md has them all
    head = 3
    blocks = []
    if ocr_json and (ocr_json / (src_img.stem + ".json")).exists():
        raw = json.loads((ocr_json / (src_img.stem + ".json")).read_text(encoding="utf-8"))
        items = raw["data"]["basicData"][0]
        short = {**raw, "data": {"basicData": [items[:head]]}}
        blocks.append((f"사내 OCR 결과 JSON (이 페이지, basicData {len(items)}개 중 앞 {head}개)", jdump(short, width=150)))
    blocks.append(("manifest.jsonl 한 줄", jdump(man)))
    blocks.append((f"pages.jsonl 한 줄 (ocr {len(page['ocr'])}개 중 앞 {head}개)", jdump({**page, "ocr": page["ocr"][:head]}, width=150)))
    EXAMPLES.append({"part": "OCR", "no": "1-0", "title": "입력 데이터: 페이지 이미지 + 사내 OCR JSON → manifest → pages.jsonl",
                     "images": [copy_image(src_img)],
                     "notes": [("전체 목록", "guide/tasks.md 1-0 에 이 페이지의 OCR 결과 JSON 과 pages.jsonl 전체가 있습니다")],
                     "blocks": blocks})
    out.append("### 1-1. 문항 한 줄의 필드 (`*_tasks.jsonl`, 모든 OCR 과제 공통)\n")
    out.append(table(list(OCR_ROW.items())))

    for i, task in enumerate(OCR_TASKS, 2):
        cand = [r for r in rows if r["task"] == task]
        if not cand:
            raise SystemExit(f"no OCR example for {task}")
        want = "aug" if task in ("crop_ocr", "bbox_ocr") else "clean"  # two examples show the noisy copy
        r = next((x for x in cand if x["view"] == want), cand[0])
        missing = set(r) - set(OCR_ROW)
        if missing:
            raise SystemExit(f"undocumented OCR row keys: {missing}")
        target = json.loads(r["target"])
        prompt = r["messages"][0]["content"]
        q = re.search(r"bbox_2d=(\[[^\]]+\])", prompt)
        query = json.loads(q.group(1)) if q else None
        img = Path(r["images"][0])
        shots = [copy_image(img)]
        boxes = [b["bbox_2d"] for b in target.get("boxes", [])]
        if boxes or query:
            shots.append(overlay(img, boxes, query, task))
        out.append(f"### 1-{i}. {task} — {TITLE[task]}\n")
        out.append(f"**어떻게 만드나:** {OCR_HOW[task]}\n\n**채점:** {OCR_SCORE[task]}\n")
        out.append("**입력 이미지** (왼쪽) " + ("· 정답 박스 초록, 질문에 준 박스 파랑 (오른쪽)" if len(shots) > 1 else "") + "\n")
        out.append(imgs_html(shots, 360))
        out.append("**질문** (`messages[0].content`)\n")
        out.append(code(prompt))
        out.append("**정답** (`target`)\n")
        out.append(code(jdump(target), "json"))
        out.append("**학습할 때 모델이 내야 하는 답** (SFT 의 assistant 내용)\n")
        out.append(code(answer_for(task, r["target"])))
        out.append("**문항 한 줄 전체** (`benchmark_tasks.jsonl`)\n")
        out.append(code(jdump(r), "json"))
        EXAMPLES.append({"part": "OCR", "no": f"1-{i}", "title": f"{task} — {TITLE[task]}", "images": shots,
                         "notes": [("어떻게 만드나", OCR_HOW[task]), ("채점", OCR_SCORE[task])],
                         "blocks": [("질문 (messages[0].content)", prompt), ("정답 (target)", jdump(target)),
                                    ("모델이 내야 하는 답 (SFT)", answer_for(task, r["target"])),
                                    ("문항 한 줄 전체 (benchmark_tasks.jsonl)", jdump(r))]})

    out.append(f"### 1-{len(OCR_TASKS) + 2}. SFT 학습 샘플 한 줄 (`train_sft.jsonl`)\n")
    s = max(sft, key=lambda x: len(x["messages"]))
    g = next(x for x in grpo if x["task"] == "grounding")
    EXAMPLES.append({"part": "OCR", "no": f"1-{len(OCR_TASKS) + 2}", "title": "SFT 학습 샘플 한 줄과 GRPO 문제 한 줄",
                     "images": [copy_image(Path(s["images"][0]))],
                     "notes": [("SFT", "같은 이미지 질문 최대 8개를 한 대화로. 이미지는 첫 질문에만"),
                               ("GRPO", "질문만. 모델이 만든 답들을 target으로 채점해 보상")],
                     "blocks": [("train_sft.jsonl 한 줄", jdump(s)), ("train_grpo.jsonl 한 줄", jdump(g))]})
    out.append("같은 이미지에 대한 질문을 최대 8개까지 한 대화로 묶습니다. 이미지는 첫 질문에만 붙고, 답은 모두 학습합니다.\n")
    out.append(code(jdump(s), "json"))
    out.append(f"### 1-{len(OCR_TASKS) + 3}. GRPO 문제 한 줄 (`train_grpo.jsonl`)\n")
    out.append("질문만 있고 답은 없습니다. 모델이 답을 여러 개 만들면 `target`으로 보상을 계산합니다.\n")
    out.append(code(jdump(next(g for g in grpo if g["task"] == "grounding")), "json"))
    text = "\n".join(out)
    roots = {str(prep): "<prepared>", str(Path(manifest_cfg["cache_dir"])): "<ocr_cache>"}
    if ocr_json:
        roots[str(ocr_json)] = "<ocr_json>"
    roots[str(Path(man["image"]).parent)] = "<images>"
    def clean(s: str) -> str:
        for k, v in sorted(roots.items(), key=lambda kv: -len(kv[0])):
            s = s.replace(k, v)
        return s

    for e in EXAMPLES:
        if e["part"] == "OCR":
            e["blocks"] = [(k, clean(v)) for k, v in e["blocks"]]
    return clean(text)


# -- banking -------------------------------------------------------------------------------------------
def bank_record(item: dict) -> dict:
    from docgen.bench.build import swift_record
    return swift_record(item)


def bank_block(bench: Path, it: dict, heading: str, extra: str = "") -> str:
    out = [heading + "\n"]
    if extra:
        out.append(extra + "\n")
    shots = [copy_image(bench / p) for p in it["images"]]
    out.append(f"**입력 이미지** ({len(shots)}장, 질문 앞에 이 순서로)\n")
    out.append(imgs_html(shots, 220 if len(shots) > 3 else 300))
    out.append(" · ".join(f"{n}. `{Path(p).name}`" for n, p in enumerate(it["images"], 1)) + "\n")
    out.append("**질문** (`prompt`)\n")
    out.append(code(it["prompt"]))
    out.append("**정답** (`answer`)\n")
    out.append(code(jdump(it["answer"]) if not isinstance(it["answer"], str) else it["answer"], "json" if not isinstance(it["answer"], str) else ""))
    if it.get("eval"):
        out.append("**채점 정보** (`eval`)\n")
        out.append(code(jdump(it["eval"]), "json"))
    out.append("**나눠 보기 정보** (`meta`)\n")
    out.append(code(jdump(it["meta"]), "json"))
    out.append("**문항 한 줄 전체** (`tasks/" + it["task"] + ".jsonl`)\n")
    out.append("<details><summary>펼치기</summary>\n\n" + code(jdump(it), "json") + "</details>\n")
    out.append("**학습 레코드** (`swift/all.jsonl` 한 줄: 같은 문항을 질문 + 정답 답변 대화로 바꾼 것)\n")
    out.append(code(jdump(bank_record(it)), "json"))
    blocks = [("질문 (prompt)", it["prompt"]),
              ("정답 (answer)", it["answer"] if isinstance(it["answer"], str) else jdump(it["answer"]))]
    if it.get("eval"):
        blocks.append(("채점 정보 (eval)", jdump(it["eval"])))
    blocks += [("나눠 보기 정보 (meta)", jdump(it["meta"])), ("문항 ID (id)", it["id"])]
    rec_answer = bank_record(it)["messages"][1]["content"]
    plain = it["answer"] if isinstance(it["answer"], str) else json.dumps(it["answer"], ensure_ascii=False)
    record_note = ("학습 레코드", "질문 = '<image>' × 이미지 수 + prompt, 답 = " +
                   ("정답(answer)을 한 줄 JSON 으로 쓴 것" if rec_answer == plain else "아래 블록 (채점용 alt_documents 를 뺀 정답)"))
    if rec_answer != plain:
        blocks.append(("학습 레코드의 답 (swift/all.jsonl, assistant)", rec_answer))
    EXAMPLES.append({"part": "BANK", "no": heading.split()[1].rstrip("."), "title": heading.split(" ", 2)[2],
                     "images": shots, "notes": ([tuple(x.split(":** ", 1)) for x in re.split(r"\s*(?:\n\n| · )\s*", extra)
                                                 if x.startswith("**")] if extra else []) + [record_note],
                     "blocks": blocks})
    return "\n".join(out)


def check_keys(it: dict):
    for k in it.get("meta", {}):
        if k not in META:
            raise SystemExit(f"undocumented meta key {k} in {it['id']}")
    for k in (it.get("eval") or {}):
        if k not in EVAL:
            raise SystemExit(f"undocumented eval key {k} in {it['id']}")


def bank_section(bench: Path) -> str:
    from docgen.bench.cases import CASES
    from docgen.bench.rules import RULES

    items = {t: [json.loads(x) for x in (bench / "tasks" / f"{t}.jsonl").open(encoding="utf-8")] for t in BANK_TASKS
             if (bench / "tasks" / f"{t}.jsonl").exists()}
    meta = json.loads((bench / "meta.json").read_text(encoding="utf-8"))
    out = ["## 은행 업무 과제\n",
           f"예시는 `python -m docgen.bench build` 로 만든 실제 평가 세트 형식 그대로입니다 (세트 버전 {meta.get('version')}, "
           f"생성기 커밋 `{meta.get('generator_commit')}`). 학습 데이터(`--split train`)도 같은 형식이고, 고객만 다릅니다.\n"]
    out.append("### 2-0. 세트 폴더와 문항 한 줄의 필드\n")
    out.append(code("""<세트>/
  meta.json                 만든 설정, 생성기 커밋, 과제별 문항 수, split (test / train)
  images/<서류ID>_<seed>.jpg               서류 한 건 과제의 이미지 (여러 쪽이면 _p1, _p2 …)
  images/bundles/<묶음ID>/<서류ID>.png     업무 묶음의 서류 이미지
  images/bundles/<묶음ID>/<서류ID>_<사례>.png   값을 바꾼 사본 (other_person 은 다른 고객 서류)
  crops/                    값 칸을 잘라낸 이미지 (ocr_field)
  tasks/<과제>.jsonl        문항, 한 줄에 하나
  swift/all.jsonl           (학습 세트만) 같은 문항의 학습 레코드"""))
    out.append(table(list(BANK_COMMON.items())))
    out.append("**meta 키** (과제에 따라 일부만 있음)\n")
    out.append(table(list(META.items())))
    out.append("**eval 키**\n")
    out.append(table(list(EVAL.items())))

    picks = {}
    for t in BANK_TASKS:
        cand = items.get(t) or []
        if t == "doc_check":
            cand = sorted(cand, key=lambda x: -(x["meta"]["n_missing"] > 0) - x["meta"]["not_customer"] - x["meta"]["not_required"])
        if t == "cross_check":
            cand = [x for x in cand if x["meta"]["case"] == "lease_owner" and x["meta"]["perturbed"]] or cand
        if t == "review":
            cand = [x for x in cand if x["meta"]["rule"] == "ltv"] or cand
        if not cand:
            raise SystemExit(f"no example for {t}")
        picks[t] = cand[0]
    for i, t in enumerate(BANK_TASKS, 1):
        it = picks[t]
        check_keys(it)
        extra = f"**정답 형식:** {ANSWER[t]}\n\n**채점:** {SCORE[t]}"
        out.append(bank_block(bench, it, f"### 2-{i}. {t} — {TITLE[t]}", extra))

    # every cross_check case
    out.append("## 3부. 서류 대조 사례 14종 (cross_check 문항 하나씩)\n")
    out.append("사례마다 원본 서류에서 그 관계가 맞는지 먼저 확인하고, 50% 확률로 값 하나를 바꿔 다시 렌더링합니다(변조 문항). "
               "나머지는 같은 서류 조합 그대로 냅니다(정상 문항). 아래는 사례마다 변조 문항 하나입니다(`format_only` 는 항상 정상 문항). "
               "예/아니오로 물을 수 있는 사례는 같은 이미지로 심사 질의 문항(`review`, rule `case:<사례>`)도 만듭니다.\n")
    cc = items["cross_check"]
    for n, case in enumerate(CASES, 1):
        cand = [x for x in cc if x["meta"]["case"] == case.id and (x["meta"]["perturbed"] or case.id == "format_only")]
        if not cand:
            out.append(f"### 3-{n}. {case.id} — {case.title}\n\n이 세트에는 이 사례의 변조 문항이 없습니다. 세트를 더 크게 만들면 나옵니다.\n")
            continue
        it = cand[0]
        check_keys(it)
        extra = f"**분류:** `{case.category}` · **실제 사례 근거:** {case.basis}"
        out.append(bank_block(bench, it, f"### 3-{n}. {case.id} — {case.title}", extra))

    # every review rule
    out.append("## 4부. 심사 질의 규칙 (review 문항 하나씩)\n")
    out.append("정답은 서류의 정답 값으로 계산합니다. 질문에 반올림 자릿수·기준일·답 형식을 적어 정답이 하나로 정해집니다.\n")
    rv = items["review"]
    present = {x["meta"]["rule"] for x in rv}
    # computed rules (rules.py, plus doc_valid which build.py adds with an aged copy), then the case questions
    rule_ids = [r for r in [*RULES, "doc_valid"] if r in present] + [f"case:{c.id}" for c in CASES if f"case:{c.id}" in present]
    rule_ids = list(dict.fromkeys(rule_ids))
    missing = sorted(present - set(rule_ids))
    if missing:
        raise SystemExit(f"review rules not listed: {missing}")
    for n, rid in enumerate(rule_ids, 1):
        it = next(x for x in rv if x["meta"]["rule"] == rid)
        check_keys(it)
        out.append(bank_block(bench, it, f"### 4-{n}. {rid} ({it['meta']['skill']})"))
    return "\n".join(out)


HOWTO = """## 5부. 비슷한 문제를 새로 정의하려면

| 바꾸고 싶은 것 | 고칠 곳 |
|---|---|
| 질문 문장 | `docgen/bench/prompts.py` (평가·학습·studio 가 같이 씀. `guide/questions.md` 와 테스트도 같이 고침) |
| 새 서류 대조 사례 | `docgen/bench/cases.py` 의 `CASES` 에 `Case(id, 제목, 분류, 근거, 함수)` 추가. 함수는 원본에서 관계가 맞는지 확인하고, 바꿀 서류·키·값과 짝 서류를 돌려줌 |
| 새 심사 질의 규칙 | `docgen/bench/rules.py` 의 `RULES` 에 함수 추가. `{"question", "answer", "answer_type", "tol", "docs", "skill"}` 를 돌려줌 |
| 업무와 필수 서류 | `docgen/registry.py` 의 `SCENARIOS` |
| 문항 만드는 방식 (빼는 서류 수, 타인 서류 비율 등) | `docgen/bench/build.py` 의 `doc_check`, `cross_checks`, `single` |
| 채점 | `docgen/bench/evaluate.py` (OCR 과제 포함, GRPO 보상도 같은 `evaluate.reward`: `train/reward_plugin.py`) |
| OCR 과제 질문·만드는 방식 | `docgen/bench/ocr_tasks.py` (`PROMPTS`, 과제별 함수), 개수는 OCR 준비 설정의 `tasks_per_view` (`docgen/bench/ocr_config.example.json`) |

실제 서류로 같은 형식의 문항을 만들면 코드 수정 없이 파이프라인에 연결됩니다. 위 `2-0` 의 폴더 구조와 필드를 그대로 따르면 됩니다.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bench", required=True, type=Path)
    ap.add_argument("--ocr", required=True, type=Path)
    ap.add_argument("--ocr-json", type=Path)
    ap.add_argument("--dump", type=Path, help="Also write the examples as JSON (for the presentation slides)")
    a = ap.parse_args()
    if IMG.exists():
        shutil.rmtree(IMG)
    IMG.mkdir(parents=True)
    head = """# 과제 정의: 실제 데이터 예시 전부

학습·평가에 쓴 **모든 과제**를 실제 데이터 한 건씩으로 보여 줍니다. 질문 전문, 정답 전문, 채점 정보, 나눠 보기 정보, 학습 레코드를 줄이지 않고 그대로 실었습니다. 이 문서만 보고 같은 형식의 문제를 다시 만들 수 있게 하는 것이 목적입니다.

- 이 문서는 `bash guide/examples/make_examples.sh <작업 폴더> --docs` 로 자동 생성합니다(예시 데이터 생성부터 이 문서·발표 부록까지, 명령과 바꾼 설정값이 스크립트 안에 그대로 있음). 직접 고치지 말고 다시 생성하세요.
- 이미지는 문서 크기 때문에 긴 변 1000px 로 줄인 사본입니다(`guide/examples/img/`). 모델이 보는 크기는 학습 설정(긴 변 2300·짧은 변 1600, 문항당 이미지 합 12,000토큰)을 따릅니다.

**목차**
- [OCR 과제](#ocr-과제) — 입력 데이터, 문항 필드, 과제 8종, SFT·GRPO 행
- [은행 업무 과제](#은행-업무-과제) — 세트 구조, 필드 사전, 과제 8종
- [3부. 서류 대조 사례 14종](#3부-서류-대조-사례-14종-cross_check-문항-하나씩)
- [4부. 심사 질의 규칙](#4부-심사-질의-규칙-review-문항-하나씩)
- [5부. 비슷한 문제를 새로 정의하려면](#5부-비슷한-문제를-새로-정의하려면)
"""
    text = "\n".join([head, ocr_section(a.ocr, a.ocr_json), bank_section(a.bench), HOWTO])
    OUT_MD.write_text(text, encoding="utf-8")
    if a.dump:
        for e in EXAMPLES:
            e["notes"] = [(k.strip("*"), v) for k, v in e["notes"]]
        a.dump.write_text(json.dumps(EXAMPLES, ensure_ascii=False, indent=1), encoding="utf-8")
    n = len(list(IMG.iterdir()))
    size = sum(p.stat().st_size for p in IMG.iterdir()) / 1e6
    print(f"{OUT_MD} ({len(text.splitlines())} lines), {n} images {size:.1f} MB")


if __name__ == "__main__":
    main()
