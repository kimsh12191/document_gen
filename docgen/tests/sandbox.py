"""테스트용 서식 폴더: 새 서식과 사람 수정이 저장소(docgen/forms)에 쓰이지 않게 임시 폴더로 돌린다."""
import shutil

from docgen import formdir


def forms_sandbox(monkeypatch, tmp_path, *copy_ids, variants=False, fields=True):
    """formdir.NEW_FORMS 를 임시 폴더로. copy_ids 서식은 그 폴더로 복사해 둬서(사람 수정 regions.json 빼고, variants=False 면
    레이아웃 변형도, fields=False 면 칸 목록 fields.json 도 빼고 — 칸 목록을 만들기 전 꼴) 그 서식에 쓰는 것도 임시 폴더로 간다.
    임시 폴더를 돌려준다."""
    root = tmp_path / "forms"
    root.mkdir(exist_ok=True)
    for doc_id in copy_ids:
        src = formdir.folder(doc_id)
        skip = {"regions.json"} | (set() if variants else {"variants"}) | (set() if fields else {"fields.json"})
        shutil.copytree(src, root / doc_id, ignore=lambda d, names: [n for n in names if n in skip and d == str(src)])
    monkeypatch.setattr(formdir, "NEW_FORMS", root)
    return root
