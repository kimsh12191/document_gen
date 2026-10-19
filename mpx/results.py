"""결과 한곳에서 보기: pipeline 출력 폴더의 표(.md)를 HTML 로 바꾸고, 첫 화면(index.html)에 모든 표·viewer 링크를 모은다.

  python -m mpx serve runs                      # 결과 페이지를 만들고 띄움 → http://127.0.0.1:7862/runs/index.html
  python -m mpx serve runs --host 0.0.0.0       # 다른 PC 에서 열기

viewer 는 쪽 이미지를 묶음 폴더에서 상대 경로로 불러오므로, 결과 폴더와 묶음 폴더(summary.json 의 data)를 함께 담는
가장 가까운 상위 폴더를 웹 서버의 뿌리로 한다. pipeline 이 끝날 때도 index.html 을 만들어 두므로 파일로 바로 열어도 된다
(결과 폴더와 묶음 폴더를 같은 구조로 옮겼다면).

첫 화면
  실행 정보   모델과 서버 주소, 모델 폴더의 기본 repetition_penalty (generation_config.json 이 있으면), 묶음 폴더
  모델 비교   compare/ 의 종합 점수표, 짝 비교, 통제 실험 비교, 관찰 분석, 묶음 viewer
  모델별      <이름>/ 의 분석, 점수표, 통제 실험 표와 viewer, 묶음 viewer
"""
from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path

from .viewer import CSS

PAGES = [  # (상대 경로, 제목, 설명)
    ("report/report.md", "종합 점수표", "문서 나누기, 항목, 행 F1, 비용"),
    ("report.md", "종합 점수표", "모델×방법별 문서 나누기, 항목, 행 F1, 비용"),
    ("paired.md", "짝 비교", "같은 행이 두 모델에서 각각 어떻게 됐나: 둘 다 / 한 모델만 빠뜨림, 특징별"),
    ("probes_compare.md", "통제 실험 비교", "실험 A~F 조건별 모델별 누락률"),
    ("probes/probes.md", "통제 실험", "실험 A~F 조건별 결과 분포, 누락률, 짝지은 비교"),
    ("probes_oracle/probes.md", "통제 실험 (정답 답)", "점검용"),
    ("probes_simulated/probes.md", "통제 실험 (오류 주입)", "점검용"),
    ("analysis.md", "관찰 분석", "결과 분포, 특징 구간별 누락률, 회귀 순위"),
    ("viewer/index.html", "묶음 viewer", "쪽 이미지, 정답, 답, 행마다 결과 기호"),
    ("probes/viewer.html", "통제 실험 viewer", "기준 쪽마다 조건별 행 결과"),
    ("probes_simulated/viewer.html", "통제 실험 viewer (오류 주입)", "점검용"),
]


def _e(v) -> str:
    return html.escape("" if v is None else str(v))


def _inline(s: str) -> str:
    s = _e(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f"<a href='{m.group(2)}'>{m.group(1)}</a>", s)
    return s


def md_to_html(md: str) -> str:
    """이 연구의 보고서가 쓰는 만큼만: 제목, 표, 목록, 문단, 굵게, 코드, 링크."""
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = block[0], [r for r in block[1:] if not all(re.fullmatch(r":?-+:?", c) for c in r)]
            num = [bool(re.fullmatch(r"[-—<>0-9.,%() \[\]]*", c)) for c in (body[0] if body else head)]
            out.append("<table><tr>" + "".join(f"<th>{_inline(c)}</th>" for c in head) + "</tr>")
            for r in body:
                out.append("<tr>" + "".join(f"<td{' style=text-align:right' if k < len(num) and num[k] else ''}>"
                                            f"{_inline(c)}</td>" for k, c in enumerate(r)) + "</tr>")
            out.append("</table>")
            continue
        if ln.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"<li>{_inline(lines[i][2:])}</li>")
                i += 1
            out.append("</ul>")
            continue
        m = re.match(r"(#{1,4}) (.*)", ln)
        if m:
            out.append(f"<h{len(m.group(1))}>{_inline(m.group(2))}</h{len(m.group(1))}>")
        elif ln.strip():
            out.append(f"<p>{_inline(ln)}</p>")
        i += 1
    return "\n".join(out)


def _page(title: str, body: str) -> str:
    return (f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{_e(title)}</title>"
            f"<style>{CSS}p{{font-size:13px;max-width:1100px}}code{{background:#f4f4f6;padding:0 3px}}"
            f".home{{font-size:12px}}</style></head><body>{body}</body></html>")


def _render(md_path: Path, home: str) -> Path:
    out = md_path.with_suffix(".html")
    body = f"<p class='home'><a href='{home}'>← 결과 첫 화면</a></p>" + md_to_html(md_path.read_text(encoding="utf-8"))
    out.write_text(_page(md_path.stem, body), encoding="utf-8")
    return out


def _section(root: Path, d: Path, title: str) -> list[str]:
    items = []
    for rel, name, desc in PAGES:
        p = d / rel
        if not p.exists():
            continue
        if p.suffix == ".md":
            p = _render(p, os.path.relpath(root / "index.html", p.parent).replace(os.sep, "/"))
        href = os.path.relpath(p, root).replace(os.sep, "/")
        items.append(f"<tr><td><a href='{_e(href)}'>{_e(name)}</a></td><td class='muted'>{_e(desc)}</td></tr>")
    return [f"<h2>{_e(title)}</h2>", "<table>" + "".join(items) + "</table>"] if items else []


def _penalty(d: Path):
    g = d / "generation_config.json"
    if not g.exists():
        return "—"
    try:
        return json.loads(g.read_text(encoding="utf-8")).get("repetition_penalty", "1.0 (값 없음)")
    except (OSError, ValueError):
        return "읽지 못함"


def build(out) -> Path:
    """<out>/index.html 을 만든다. <out> 은 pipeline 출력 폴더 (--models 면 모델별 하위 폴더와 compare/ 가 있음)."""
    out = Path(out)
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8")) if (out / "summary.json").exists() else {}
    models = summary.get("models") or {}
    L = ["<h1>실험 결과</h1>", f"<p class='muted'>{_e(out.resolve())}</p>", "<h2>실행 정보</h2>"]
    info = [("묶음 폴더", summary.get("data", "—"))]
    if summary.get("seconds"):
        info.append(("걸린 시간(초)", ", ".join(f"{k} {v}" for k, v in summary["seconds"].items())))
    L.append("<table>" + "".join(f"<tr><th>{_e(k)}</th><td>{_e(v)}</td></tr>" for k, v in info) + "</table>")
    if models:
        L.append("<table><tr><th>모델</th><th>서버 모델 이름</th><th>주소</th><th>기본 repetition_penalty</th></tr>"
                 + "".join(f"<tr><td>{_e(n)}</td><td>{_e(m.get('served'))}</td><td>{_e(m.get('url'))}</td>"
                           f"<td>{_e(_penalty(out / n))}</td></tr>" for n, m in models.items()) + "</table>")
        pens = {float(str(v).split()[0]) for v in map(_penalty, (out / n for n in models)) if v not in ("—", "읽지 못함")}
        if len(pens) > 1:
            L.append("<p class='bad'>모델마다 기본 repetition_penalty 가 다르다: 관찰 실행의 모델 차이에 디코딩 설정 차이가 섞여 있다. "
                     "같은 설정 비교는 통제 실험 F 를 본다.</p>")
    if (out / "compare").exists():
        L += _section(out, out / "compare", "모델 비교")
    for n in models:
        L += _section(out, out / n, f"모델: {n}")
    if not models:
        L += _section(out, out, "결과")
    index = out / "index.html"
    index.write_text(_page("실험 결과", "\n".join(L)), encoding="utf-8")
    return index


def serve(out, port: int = 7862, host: str = "127.0.0.1") -> None:
    import functools
    import http.server

    out = Path(out).resolve()
    index = build(out)
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8")) if (out / "summary.json").exists() else {}
    roots = [out] + ([Path(summary["data"]).resolve()] if summary.get("data") else [])
    root = Path(os.path.commonpath(roots))
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    print(f"http://{host}:{port}/{index.relative_to(root).as_posix()}  (Ctrl+C 로 종료)")
    http.server.ThreadingHTTPServer((host, port), handler).serve_forever()
