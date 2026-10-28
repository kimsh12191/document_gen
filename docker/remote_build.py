"""다른 컨테이너·PC 에서 studio 에 데이터 생성을 맡긴다 (파이썬 표준 라이브러리만 씀. 이 파일만 복사해 가도 된다).

studio 를 sh docker/studio.sh --open 으로 띄워 두고, URL 은 --url 또는 환경변수 STUDIO_URL (예: http://10.0.0.5:8765).
사용 설명서: guide/README.md · 생성·학습 절차: guide/agent-workflow.md
서류별 추출·시나리오: guide/catalog.md (기계용 catalog.json)

보기
  python remote_build.py types [--group income] [--find 재직]     서식 ID 목록 (그룹·이름으로 거르기)
  python remote_build.py scenarios                                업무(시나리오) ID 와 필요 서류
  python remote_build.py recipes                                  저장된 레시피
  python remote_build.py jobs                                     생성 작업 목록
  python remote_build.py status <작업ID>                          작업 하나 (진행·로그 끝)
  python remote_build.py paths                                    데이터셋이 생기는 곳 (컨테이너 안 경로 ↔ 서버 경로)
  python remote_build.py catalog --form employment_certificate     서식별 추출 항목·연결 업무
  python remote_build.py composition <데이터셋ID> --out trace.json  생성된 전체/평가 문항 구성·재현 정보

만들기 (끝날 때까지 기다림. --no-wait 면 작업 ID 만 받고 끝)
  python remote_build.py build --name bench-1021 --recipe bank-bench          저장된 레시피 그대로 (벤치마크 통째)
  python remote_build.py build --name try1 --types resident_id_card,hf169 --per-doc 3
                                                                              특정 서식만 (업무 묶음 없음)
  python remote_build.py build --name loan1 --scenarios mortgage --bundles 20  특정 업무만 (단일 서류 없음)
  python remote_build.py build --name inc --types income --scenarios all --bundles 10 --split train
                                                                              그룹 + 업무, 학습용
  python remote_build.py build --name ocr1 --track ocr --types identity --per-doc 2 --unit line
                                                                              합성 OCR (쪽 전체 글자 정답)
  python remote_build.py build --name my1 --file my.json                      레시피 JSON 을 보내서

옵션으로 만들면 레시피를 remote-<name> 으로 studio 에 저장하고(docgen/recipes/), 그 레시피로 만든다.
결과: 서버의 <workspace_dir>/datasets/<name>/, studio ⑥ 데이터셋에 자동 등록. 이름이 이미 있으면 거절.
쓰는 API: GET /api/form-ids · /api/recipes/options · /api/recipes, PUT /api/recipes/{이름}, POST /api/builds, GET /api/builds · /api/jobs/{id}
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = ""


def call(path: str, method: str = "GET", body: dict | None = None, timeout: float = 120) -> dict | list:
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} → {e.code}: {e.read().decode('utf-8', 'replace')}")
    except urllib.error.URLError as e:
        sys.exit(f"{BASE} 에 연결하지 못했습니다 ({e.reason}). studio 를 --open 으로 띄웠는지, 주소·포트를 확인하세요")


def csv(v: str | None):
    """'all' 은 그대로, 'a,b' 는 목록, '' 는 빈 목록 (그 과제 없음)"""
    if v is None:
        return None
    return "all" if v == "all" else [x.strip() for x in v.split(",") if x.strip()]


def recipe_from_args(a) -> dict:
    r = {"about": f"remote_build.py 로 만듦: {a.name}", "track": a.track}
    if a.track == "bank":
        r["split"] = a.split or "test"
        # 서식·업무 중 하나만 주면 나머지는 빼서 그것만 만든다
        r["types"] = csv(a.types) if a.types is not None else ([] if a.scenarios is not None else "all")
        r["scenarios"] = csv(a.scenarios) if a.scenarios is not None else ([] if a.types is not None else "all")
        if a.bundles is not None:
            r["bundles"] = a.bundles
    else:
        r["split"] = a.split or "benchmark"
        r["types"] = csv(a.types) if a.types is not None else "all"
        r["unit"] = a.unit
    if a.per_doc is not None:
        r["per_doc"] = a.per_doc
    if a.conditions:
        r["conditions"] = {k: float(v) for k, v in (x.split("=") for x in a.conditions.split(","))}
    if a.exclude:
        r["exclude"] = csv(a.exclude)
    if a.reviewed_only:
        r["reviewed_only"] = True
    return r


def wait(job_id: str, poll: float) -> dict:
    last = None
    while True:
        time.sleep(poll)
        # /api/builds 는 studio 가 다시 떠서 "끊김"이 된 작업 중 끝난 것을 복구해 등록까지 한다
        j = next((x for x in call("/api/builds")["jobs"] if x["id"] == job_id), None) or call(f"/api/jobs/{job_id}")
        prog = call(f"/api/jobs/{job_id}").get("progress")
        line = f"  {j['status']} {j.get('stage') or ''} {'%d/%d' % tuple(prog) if prog else ''}".rstrip()
        if line != last:
            print(line, flush=True)
            last = line
        if j["status"] not in ("running", "interrupted"):
            return j


def cmd_build(a) -> None:
    if a.file:
        with open(a.file, encoding="utf-8") as f:
            r = json.load(f)
        recipe = a.recipe or f"remote-{a.name}"
    elif a.recipe and not any(v is not None for v in (a.types, a.scenarios, a.bundles, a.per_doc, a.conditions, a.exclude)):
        recipe, r = a.recipe, None
    else:
        recipe, r = a.recipe or f"remote-{a.name}", recipe_from_args(a)
    if r is not None:
        saved = call(f"/api/recipes/{recipe}", "PUT", r)
        print(f"레시피 저장: {saved.get('path', recipe)}")
        print(json.dumps({k: v for k, v in r.items() if k != "about"}, ensure_ascii=False))
    job = call("/api/builds", "POST", {"recipe": recipe, "name": a.name, "workers": a.workers})
    print(f"시작: {job['id']}  {job['title']}", flush=True)
    if a.no_wait:
        print(f"진행 보기: python remote_build.py status {job['id']}")
        return
    j = wait(job["id"], a.poll)
    print(json.dumps({k: j.get(k) for k in ("id", "status", "stage", "error", "result")}, ensure_ascii=False, indent=1))
    out = (j.get("info") or {}).get("out") or (job.get("info") or {}).get("out")
    if out and j["status"] == "done":
        show_path(out)
    if j["status"] != "done":
        print(call(f"/api/jobs/{job['id']}").get("log_tail", "")[-2000:])
        sys.exit(1)


def show_path(out: str) -> None:
    p = call("/api/paths")
    host = None
    for inside, h in p.get("mounts", []):
        if out == inside or out.startswith(inside.rstrip("/") + "/"):
            host = h.rstrip("/") + out[len(inside.rstrip("/")):]
    print(f"결과 폴더 (studio 컨테이너 안): {out}")
    print(f"결과 폴더 (서버):               {host or '알 수 없음 — 서버에서 sh docker/studio.sh rm 후 다시 띄우면 보임'}")


def cmd_paths(a) -> None:
    p = call("/api/paths")
    print(f"데이터셋 (studio 컨테이너 안): {p['datasets']}/<이름>/")
    print(f"데이터셋 (서버):               {(p.get('datasets_host') or '알 수 없음') + '/<이름>/'}")
    for inside, h in p.get("mounts", []):
        print(f"  {inside}  =  서버 {h}")
    print(f"studio 설정 파일: {p.get('config_file') or '없음 (기본값: 코드 폴더 안 studio_workspace/)'}")


def cmd_catalog(a) -> None:
    """현재 서류·추출 항목·연결 업무를 기계가 읽는 JSON으로 받는다."""
    path = f"/api/guide/forms/{urllib.parse.quote(a.form, safe='')}" if a.form else "/api/guide/catalog"
    data = call(path)
    content = json.dumps(data, ensure_ascii=False, indent=2)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        print(f"카탈로그 저장: {a.out}")
    else:
        print(content)


def cmd_composition(a) -> None:
    """등록한 데이터셋의 실제 생성 구성과 재현 정보를 조회한다."""
    data = call(f"/api/datasets/{urllib.parse.quote(a.dataset, safe='')}/composition")
    content = json.dumps(data, ensure_ascii=False, indent=2)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        print(f"데이터셋 구성 저장: {a.out}")
    else:
        print(content)


def cmd_types(a) -> None:
    rows = call("/api/form-ids")
    if a.group:
        rows = [x for x in rows if x["group"] == a.group]
    if a.find:
        rows = [x for x in rows if a.find in x["name"] or a.find in x["id"]]
    for x in rows:
        print(f"{x['id']:<40} {x['group']:<12} {x['name']}")
    groups = call("/api/recipes/options")["groups"]
    print(f"\n{len(rows)}종. --types 에 ID 를 쉼표로 잇거나, 그룹 이름을 씁니다: " + ", ".join(f"{k}({v})" for k, v in groups.items()))


def cmd_scenarios(a) -> None:
    for s in call("/api/recipes/options")["scenarios"]:
        print(f"{s['id']:<26} {s['name']}  ← {', '.join(s['docs'])}")


def cmd_recipes(a) -> None:
    for r in call("/api/recipes")["recipes"]:
        print(json.dumps(r, ensure_ascii=False) if not isinstance(r, str) else r)


def cmd_jobs(a) -> None:
    for j in call("/api/builds")["jobs"]:
        print(f"{j['id']}  {j['status']:<11} {j.get('title', '')}")


def cmd_status(a) -> None:
    j = call(f"/api/jobs/{a.job}")
    tail = j.pop("log_tail", "")
    print(json.dumps(j, ensure_ascii=False, indent=1))
    print("--- 로그 끝 ---\n" + tail[-1500:])


def main() -> None:
    global BASE
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="\n".join(__doc__.splitlines()[2:]))
    ap.add_argument("--url", default=os.environ.get("STUDIO_URL"), help="studio 주소 (또는 환경변수 STUDIO_URL)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="데이터셋 만들기")
    b.add_argument("--name", required=True, help="만들 데이터셋 이름 (폴더 이름. 이미 있으면 거절)")
    b.add_argument("--recipe", help="저장된 레시피 이름. 옵션과 같이 주면 그 이름으로 레시피를 저장(덮어씀)")
    b.add_argument("--file", help="레시피 JSON 파일을 보내서 만들기")
    b.add_argument("--track", choices=("bank", "ocr"), default="bank", help="bank: 은행 업무 (서식 문항 + 업무 묶음), ocr: 합성 OCR")
    b.add_argument("--types", help="서식: all | ID,ID,… | 그룹 (예: income). 빈 값('')이면 서식 과제 없음")
    b.add_argument("--scenarios", help="[bank] 업무: all | ID,ID,… 빈 값('')이면 업무 묶음 없음")
    b.add_argument("--bundles", type=int, help="[bank] 업무마다 고객 수 (기본 4)")
    b.add_argument("--per-doc", type=int, help="서식마다 만들 장 수 (기본 1)")
    b.add_argument("--split", help="bank: test(평가, 기본) | train,  ocr: benchmark(기본) | train")
    b.add_argument("--conditions", help="촬영 조건 비율, 합 1 (예: clean=0.5,scan=0.2,photo=0.15,fax=0.15)")
    b.add_argument("--exclude", help="뺄 서식 ID,ID")
    b.add_argument("--reviewed-only", action="store_true", help="studio 에서 검수 완료한 서식만")
    b.add_argument("--unit", choices=("word", "line"), default="word", help="[ocr] 정답 단위")
    b.add_argument("--workers", type=int, default=1, help="동시에 그리는 수 (서버 코어 수 안에서)")
    b.add_argument("--no-wait", action="store_true", help="시작만 하고 끝 (status 로 확인)")
    b.add_argument("--poll", type=float, default=10, help="진행 확인 간격(초)")
    t = sub.add_parser("types", help="서식 ID 목록")
    t.add_argument("--group")
    t.add_argument("--find", help="이름·ID 에 이 글자가 든 것만")
    sub.add_parser("scenarios", help="업무 ID 와 필요 서류")
    sub.add_parser("recipes", help="저장된 레시피")
    sub.add_parser("jobs", help="생성 작업 목록")
    sub.add_parser("paths", help="데이터셋이 생기는 곳 (컨테이너 안 ↔ 서버)")
    c = sub.add_parser("catalog", help="서류별 추출 항목·문항 키·연결 업무 JSON")
    c.add_argument("--form", help="서식 ID 하나만 조회 (생략하면 전체)")
    c.add_argument("--out", help="JSON을 UTF-8 파일로 저장")
    c = sub.add_parser("composition", help="데이터셋의 업무·시나리오·정답 구조별 구성 조회")
    c.add_argument("dataset", help="등록된 데이터셋 ID (통상 생성할 때의 --name)")
    c.add_argument("--out", help="구성 JSON을 UTF-8 파일로 저장")
    s = sub.add_parser("status", help="작업 하나의 상태·로그")
    s.add_argument("job")
    a = ap.parse_args()
    if not a.url:
        ap.error("--url 또는 STUDIO_URL 이 필요합니다 (예: http://10.0.0.5:8765)")
    BASE = a.url.rstrip("/")
    {"build": cmd_build, "types": cmd_types, "scenarios": cmd_scenarios, "recipes": cmd_recipes,
     "jobs": cmd_jobs, "status": cmd_status, "paths": cmd_paths, "catalog": cmd_catalog, "composition": cmd_composition}[a.cmd](a)


if __name__ == "__main__":
    main()
