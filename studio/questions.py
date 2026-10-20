"""서식 한 건의 실제 single 생성기를 사용한 문항 미리보기와 공통 Q/A 표시 데이터."""
from pathlib import Path
import hashlib
import json

from docgen.bench.build import Builder
from docgen.bench.runner import oracle_output


def public_item(item: dict, root: Path) -> dict:
    urls = ["/preview/" + (root / p).resolve().relative_to(root.resolve()).as_posix() for p in item["images"]]
    return {**item, "image_urls": urls, "model_answer": oracle_output(item)}


def form_items(label: dict, preview_root: Path, fields_per_doc: int = 6, max_keys: int = 40) -> list[dict]:
    """Builder.single를 그대로 호출한다. 선택·자르기·질문·정답·채점을 별도로 재구현하지 않는다."""
    from os.path import relpath

    key = hashlib.sha1(json.dumps([label["images"], fields_per_doc, max_keys]).encode()).hexdigest()[:16]
    folder = preview_root / "_questions" / key
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "crops").mkdir(exist_ok=True)
    b = Builder.__new__(Builder)
    b.out, b.buf = folder, []
    r = {**label, "doc_id": label["doc_type"], "name": label["doc_name"],
         "sizes": [(p["width"], p["height"]) for p in label["pages"]],
         "images": [relpath(preview_root / p, folder) for p in label["images"]],
         "visible": set(label["visible"])}
    b.single(r, f"images/{r['doc_id']}_{r['seed']}", fields_per_doc, max_keys)
    items = []
    for rec in b.take():
        # 데이터셋 상대 경로를 미리보기 영역의 경로로 바꾼다.
        rec["images"] = [(folder / p).resolve().relative_to(preview_root.resolve()).as_posix() for p in rec["images"]]
        items.append(public_item(rec, preview_root))
    return items
