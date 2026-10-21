"""다른 컨테이너·PC 에서 studio 에 데이터 생성을 맡기는 예 (파이썬 표준 라이브러리만 씀. 이 파일만 복사해 가도 된다).

studio 를 sh docker/studio.sh --open 으로 띄워 두고:

  python remote_build.py --url http://<서버IP>:8765 --recipe bank-bench --name bench-1021
  python remote_build.py --url http://<서버IP>:8765 --recipe my-recipe --file my-recipe.json --name my-1021   레시피를 보내고 만들기
  python remote_build.py --url http://<서버IP>:8765 --list                                                  레시피 목록

끝나면 studio ⑥ 데이터셋에 자동 등록되고, 결과는 서버의 <workspace_dir>/datasets/<name>/ 에 생긴다.
쓰는 API: PUT /api/recipes/{이름}, POST /api/builds {recipe, name, workers}, GET /api/builds, GET /api/jobs/{id}
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request


def call(url: str, method: str = "GET", body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {url} → {e.code}: {e.read().decode('utf-8', 'replace')}")


def build(base: str, recipe: str, name: str, workers: int = 1, poll: float = 10) -> dict:
    """생성을 시작하고 끝날 때까지 기다린다. 끝난 작업(job.json 내용)을 돌려준다."""
    job = call(f"{base}/api/builds", "POST", {"recipe": recipe, "name": name, "workers": workers})
    print(f"시작: {job['id']}  {job['title']}", flush=True)
    while True:
        time.sleep(poll)
        # /api/builds 는 studio 가 다시 떠서 "끊김"이 된 작업 중 끝난 것을 복구해 등록까지 한다
        j = next((x for x in call(f"{base}/api/builds")["jobs"] if x["id"] == job["id"]), None) \
            or call(f"{base}/api/jobs/{job['id']}")
        prog = j.get("progress") or call(f"{base}/api/jobs/{job['id']}").get("progress")
        print(f"  {j['status']} {j.get('stage', '')} {'%d/%d' % tuple(prog) if prog else ''}", flush=True)
        if j["status"] != "running":
            return j


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--url", required=True, help="studio 주소, 예: http://10.0.0.5:8765")
    ap.add_argument("--recipe", help="레시피 이름 (docgen/recipes/<이름>.json)")
    ap.add_argument("--file", help="이 레시피 JSON 을 먼저 studio 에 저장 (같은 이름이 있으면 덮어씀)")
    ap.add_argument("--name", help="만들 데이터셋 이름 (폴더 이름. 이미 있으면 거절)")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--list", action="store_true", help="레시피 목록만 보기")
    a = ap.parse_args()
    base = a.url.rstrip("/")
    if a.list:
        for r in call(f"{base}/api/recipes")["recipes"]:
            print(r if isinstance(r, str) else json.dumps(r, ensure_ascii=False))
        return
    if not (a.recipe and a.name):
        ap.error("--recipe 와 --name 이 필요합니다")
    if a.file:
        with open(a.file, encoding="utf-8") as f:
            call(f"{base}/api/recipes/{a.recipe}", "PUT", json.load(f))
    j = build(base, a.recipe, a.name, a.workers)
    print(json.dumps({k: j.get(k) for k in ("id", "status", "stage", "error", "result")}, ensure_ascii=False, indent=1))
    sys.exit(0 if j["status"] == "done" else 1)


if __name__ == "__main__":
    main()
