"""서식 초안 하네스 비교 시험: 이미 있는 서식을 그린 그림을 넣어 html 로 다시 만들고, 초안 점수와 다듬은 뒤 점수를 견준다.
내부망에서 실제 모델(vLLM)로 돌려 어떤 설정이 원본에 더 가까워지는지 숫자로 본다.

  python -m studio.draft_bench --provider <연결 이름> --sample 10 [--forms id1,id2] [--rounds 3]
                               [--conditions clean,scan] [--no-measure] [--seed 0] --out <폴더>

- 연결은 studio 설정과 같은 것 (studio/config.json 의 providers, 실문서 벤치마크 › OCR·모델 연결에 저장한 것).
- 서식은 --forms 로 고르거나 --sample 개를 A4 서식에서 무작위로 (--seed). 그렸을 때 한 쪽이 넘는 서식은 건너뛴다.
- --conditions: 입력 그림의 촬영 조건 (clean 원본, scan 스캔, photo 촬영, fax). 서식마다 조건별로 한 번씩 만든다.
- --no-measure: 다듬기에 코드가 잰 위치 차이를 주지 않는다 (겹침 그림만). 숫자의 효과를 볼 때.
- 키 추천은 하지 않는다 (모양만 본다).
결과: <out>/results.jsonl (서식·조건마다 회차별 점수, 걸린 시간), <out>/summary.md, 작업 폴더는 <out>/ws/analyzer/.
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from pathlib import Path

from . import form_draft as FD, real_benchmark as RB
from .config import ROOT, load, resolve_path


def source_image(form_id: str, condition: str, out: Path, seed: int) -> Path | None:
    """서식을 그려 첫 쪽 그림을 돌려준다. 한 쪽이 넘으면 None."""
    r = subprocess.run([sys.executable, "-m", "docgen.preview", form_id, "--seed", str(seed), "--condition", condition,
                        "--out", str(out)], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT), timeout=300)
    if r.returncode:
        print(f"  {form_id}: 그리기 실패 {(r.stderr or r.stdout).strip().splitlines()[-1:]}", flush=True)
        return None
    info = json.loads(r.stdout.strip().splitlines()[-1])
    return Path(info["images"][0]) if info["pages"] == 1 else None


def pick_forms(forms: str, sample: int, seed: int) -> list[str]:
    from docgen.registry import load_all

    reg = load_all()
    if forms:
        ids = [f.strip() for f in forms.split(",") if f.strip()]
        missing = [f for f in ids if f not in reg]
        if missing:
            raise SystemExit(f"없는 서식: {missing}")
        return ids
    pool = sorted(k for k, s in reg.items() if s.page == "a4")
    return random.Random(seed).sample(pool, min(sample, len(pool)))


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="studio.draft_bench", description="서식 초안 하네스 비교 시험")
    ap.add_argument("--provider", required=True)
    ap.add_argument("--forms", default="")
    ap.add_argument("--sample", type=int, default=10)
    ap.add_argument("--rounds", type=int, default=FD.ROUNDS)
    ap.add_argument("--conditions", default="clean")
    ap.add_argument("--no-measure", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    cfg = load()
    conn = RB.connection_config(resolve_path(cfg["workspace_dir"]), cfg)
    out = Path(a.out).resolve()
    ws = out / "ws"
    ws.mkdir(parents=True, exist_ok=True)
    rows = []
    for fid in pick_forms(a.forms, a.sample, a.seed):
        for cond in [c.strip() for c in a.conditions.split(",") if c.strip()]:
            src = source_image(fid, cond, out / "sources", a.seed)
            if src is None:
                print(f"{fid} ({cond}): 한 쪽 서식이 아니라 건너뜀", flush=True)
                continue
            print(f"== {fid} ({cond})", flush=True)
            d = FD.create(ws, conn, a.provider, src, "", "finance", "", False, "bench", a.rounds)
            job = RB.read(d / "job.json")
            job["target"]["measure"] = not a.no_measure
            RB.write(d / "job.json", job)
            t = time.time()
            row = {"form": fid, "condition": cond, "job": d.name, "rounds_max": a.rounds, "measure": not a.no_measure}
            try:
                FD.run(d, keys=False)
                hist = (RB.read(d / "draft" / "rounds.json", {}) or {}).get("rounds", [])
                scores = [h["score"] for h in hist if h.get("score") is not None]
                row.update(first=scores[0] if scores else None, best=max(scores) if scores else None,
                           rounds=len(hist) - 1 if hist else 0, history=[[h["n"], h.get("score"), h.get("kept")] for h in hist])
            except Exception as e:  # noqa: BLE001  한 서식이 실패해도 나머지는 계속
                row["error"] = f"{type(e).__name__}: {e}"
                print(f"  실패: {row['error']}", flush=True)
            row["seconds"] = round(time.time() - t, 1)
            rows.append(row)
            with open(out / "results.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    ok = [r for r in rows if r.get("best") is not None]
    avg = lambda k: round(sum(r[k] for r in ok) / len(ok), 1) if ok else None  # noqa: E731
    lines = [f"# 서식 초안 하네스 비교 ({a.provider}, 다듬기 최대 {a.rounds}회, 위치 숫자 {'없음' if a.no_measure else '있음'})", "",
             f"- 서식·조건 {len(rows)}개 중 성공 {len(ok)}개, 평균 초안 점수 {avg('first')} → 다듬은 뒤 {avg('best')}", "",
             "| 서식 | 조건 | 초안 | 최종 | 회차 | 초 | 오류 |", "|---|---|---|---|---|---|---|"]
    lines += [f"| {r['form']} | {r['condition']} | {r.get('first', '-')} | {r.get('best', '-')} | {r.get('rounds', '-')} | {r['seconds']} | "
              f"{r.get('error', '')[:60]} |" for r in rows]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
