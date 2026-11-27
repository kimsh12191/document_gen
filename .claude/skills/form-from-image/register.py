"""초안 서식을 등록 폴더로 옮긴다 (form-from-image 스킬 7단계 — 사람이 하라고 할 때만).

    python .claude/skills/form-from-image/register.py <초안 폴더> --to public|private [--id <서식 ID>] [--real]

  public   docgen/forms/<ID>/                    빈 서식·공개 견본에서 만든 것
  private  $DOCGEN_PRIVATE_FORMS/<ID>/           실서류에서 만든 것 (studio 설정 private_forms_dir). --real 이면 public 은 거부

하는 일 (하나라도 안 되면 아무것도 옮기지 않는다):
  1. 서식 ID 확인 (형식, 이미 있는 서식·폴더면 거부 — 덮어쓰지 않음)
  2. check.py 검사 통과 확인
  3. 옮기기: template.html.j2 → look/template.html.j2 · form.json 의 fields·lists → fields.json · 나머지 → form.json ·
     source*.png · generate.py (있으면). layout.json·grid_*·page_*·view_*·render_*·fields.md·report.md·check*·run.json 등 작업 파일은 옮기지 않는다
  4. python -m docgen.formdir card <ID> (서식 카드 FORM.md) · check <ID>
마지막 줄에 JSON. 성공 0, 거부·실패 1. 등록은 검수가 아니다: studio 서식 › 서식 다시 읽기 → 생성 사례 › 미리보기/검수.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import check  # noqa: E402

ID_RX = re.compile(r"[a-z][a-z0-9_]{2,50}")


class RegisterError(RuntimeError):
    pass


def target(form_id: str, to: str) -> Path:
    if to == "public":
        return ROOT / "docgen" / "forms" / form_id
    if to == "private":
        base = os.environ.get("DOCGEN_PRIVATE_FORMS")
        if not base:
            raise RegisterError("비공개 서식 폴더가 정해져 있지 않습니다 (환경 변수 DOCGEN_PRIVATE_FORMS, studio 설정 private_forms_dir)")
        return Path(base).expanduser() / form_id
    raise RegisterError("--to 는 public 또는 private")


def _formdir(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "docgen.formdir", *args], cwd=ROOT, capture_output=True, text=True, timeout=600)


def register(draft: Path | str, to: str, form_id: str | None = None, real: bool = False, log=print) -> dict:
    draft = Path(draft).resolve()
    form_id = form_id or draft.name
    if not ID_RX.fullmatch(form_id):
        raise RegisterError("서식 ID 는 영어 소문자로 시작, 소문자·숫자·밑줄 3~51자")
    if real and to != "private":
        raise RegisterError("실서류에서 만든 서식은 비공개 폴더(private)에만 등록합니다")
    dest = target(form_id, to)
    if dest.exists():
        raise RegisterError(f"이미 있는 폴더입니다 (덮어쓰지 않음): {dest}")
    p = _formdir("path", form_id)
    if "없습니다" not in p.stdout + p.stderr:
        raise RegisterError(f"이미 있는 서식 ID 입니다: {form_id}")
    try:
        form = json.loads((draft / "form.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise RegisterError(f"form.json 을 읽지 못했습니다: {e}")
    if not (draft / "template.html.j2").exists() or not form.get("fields"):
        raise RegisterError("template.html.j2 와 form.json 의 fields 가 있어야 합니다")
    log("검사 (check.py) …")
    result = check.run(draft, draft / "check_register")
    if not result["passed"]:
        raise RegisterError("검사를 통과하지 못해 등록하지 않습니다:\n" + "\n".join(result["problems"]))

    body = {"engine": "html", "unit": "px", "fields": form.pop("fields"), "lists": form.pop("lists", {}) or {}}
    form.setdefault("origin", "analyzer")
    form.setdefault("page", "a4")
    sources = check.sources(draft)
    if sources:
        form["source_image"] = sources[0].name
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=f".{form_id}.", dir=dest.parent))   # 다 만든 뒤 한 번에 이름을 바꾼다
    try:
        (tmp / "look").mkdir()
        shutil.copy(draft / "template.html.j2", tmp / "look" / "template.html.j2")
        (tmp / "fields.json").write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        (tmp / "form.json").write_text(json.dumps(form, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        copied = ["look/template.html.j2", "fields.json", "form.json"]
        for f in [*sources, draft / "generate.py"]:
            if f.exists():
                shutil.copy(f, tmp / f.name)
                copied.append(f.name)
        tmp.rename(dest)
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    log(f"등록: {dest}")
    card = _formdir("card", form_id)
    chk = _formdir("check", form_id)
    return {"id": form_id, "to": to, "path": str(dest), "files": copied,
            "card": {"ok": card.returncode == 0, "out": (card.stdout + card.stderr).strip()[-1500:]},
            "formdir_check": {"ok": chk.returncode == 0 and "문제 있는 서식 0개" in chk.stdout, "out": (chk.stdout + chk.stderr).strip()[-3000:]},
            "warnings": result["warnings"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("draft")
    ap.add_argument("--to", required=True, choices=["public", "private"])
    ap.add_argument("--id", help="서식 ID (기본: 초안 폴더 이름)")
    ap.add_argument("--real", action="store_true", help="실서류에서 만든 서식 (public 거부)")
    a = ap.parse_args()
    try:
        out = register(a.draft, a.to, a.id, a.real)
    except RegisterError as e:
        print(f"등록하지 않음: {e}")
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)
    print(out["formdir_check"]["out"])
    print(json.dumps({"ok": True, **{k: out[k] for k in ("id", "to", "path", "files")}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
