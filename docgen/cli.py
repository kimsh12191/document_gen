"""명령줄 진입점.

  python -m docgen list
  python -m docgen generate --types all --n 20 --out out --png
  python -m docgen generate --scenario mortgage --n 5 --out out --png
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

from .banks import BRANDS, LEGACY, supports
from .entities import BANKS, make_profile
from .registry import GROUPS, SCENARIO_EXTRA, SCENARIOS, load_all
from .render import render, to_nested

PROMPTS = [
    "이 문서의 종류를 판별하고, 문서에 기재된 모든 정보를 JSON으로 추출하세요.",
    "이미지 속 서류에서 항목과 값을 빠짐없이 JSON 형식으로 뽑아주세요.",
    "다음 은행 제출 서류를 읽고 문서 종류와 기재 내용을 구조화된 JSON으로 정리해 주세요.",
    "Extract all fields from this Korean document as JSON, including the document type.",
    "서류에 적힌 정보를 키-값 JSON으로 변환하세요. 문서 종류도 포함하세요.",
]


def cmd_list(args) -> None:
    reg = load_all()
    by_group: dict[str, list] = {}
    for s in reg.values():
        by_group.setdefault(s.group, []).append(s)
    if args.markdown:
        print(f"# 서류 목록 (총 {len(reg)}종)\n")
        print("`python -m docgen list --markdown > docs/DOCUMENTS.md` 로 자동 생성된 문서입니다.\n")
        for g, title in GROUPS.items():
            specs = by_group.get(g, [])
            if not specs:
                continue
            print(f"## {title} ({len(specs)}종)\n")
            print("| ID | 서류명 | 구분 | 설명 |\n|---|---|---|---|")
            for s in specs:
                cat = "은행 서식" if s.category == "internal" else "외부 발급"
                mark = " · 견본표시" if s.sample_mark else ""
                print(f"| `{s.id}` | {s.name} | {cat}{mark} | {s.description.splitlines()[0] if s.description else ''} |")
            print()
        print("## 업무 시나리오\n")
        print("| 시나리오 | 업무 | 서류 |\n|---|---|---|")
        for k, (name, ids) in SCENARIOS.items():
            print(f"| `{k}` | {name} | {', '.join(reg[i].name if i in reg else i for i in ids)} |")
        return
    for g, title in GROUPS.items():
        specs = by_group.get(g, [])
        print(f"\n[{title}] ({len(specs)})")
        for s in specs:
            cat = "은행서식" if s.category == "internal" else "외부발급"
            print(f"  {s.id:40s} {s.name}  ({cat}, {s.page})")
    print(f"\n총 {len(reg)}종")
    print("\n[시나리오]")
    for k, (name, ids) in SCENARIOS.items():
        print(f"  {k:28s} {name}: {', '.join(ids)}")


def _select(args, reg) -> list[str]:
    if args.scenario:
        ids = SCENARIOS[args.scenario][1]
    elif args.types in (None, "all"):
        ids = list(reg)
    else:
        ids = []
        for t in args.types.split(","):
            t = t.strip()
            ids += [s.id for s in reg.values() if s.group == t] if t in GROUPS else [t]
    missing = [i for i in ids if i not in reg]
    if missing:
        sys.exit(f"알 수 없는 서류: {missing}")
    bank = getattr(args, "bank", None)
    if bank in LEGACY:  # 옛 은행은 은행 서식만 (외부 발급 서류는 그 시기 서식이 아니므로 제외)
        keep = [i for i in ids if reg[i].group == "bank_form" and supports(bank, i)]
        if len(keep) < len(ids):
            print(f"참고: {bank}은 옛 은행이라 은행 서식 {len(keep)}종만 만듭니다 (제외 {len(ids) - len(keep)}종)", file=sys.stderr)
        if not keep:
            sys.exit(f"{bank} 서식으로 만들 수 있는 서류가 없습니다")
        ids = keep
    return ids


def _profile(seed: int, args):
    """--bank: 현행 은행이면 주거래은행으로 고정, 옛 은행이면 은행 서식만 그 은행·그 시기로 만든다."""
    bank = getattr(args, "bank", None)
    p = make_profile(seed, None if bank in LEGACY else bank)
    if bank:
        p.extra["form_bank"] = bank
    return p


def cmd_generate(args) -> None:
    reg = load_all()
    ids = _select(args, reg)
    out = Path(args.out)
    (out / "html").mkdir(parents=True, exist_ok=True)
    (out / "labels").mkdir(parents=True, exist_ok=True)
    if args.augment and not args.png:
        sys.exit("--augment 는 --png 와 함께 사용하세요")
    if args.png:
        (out / "images").mkdir(parents=True, exist_ok=True)

    renderer = None
    if args.png:
        from .image import ImageRenderer

        renderer = ImageRenderer(scale=args.scale).__enter__()

    manifest = open(out / "manifest.jsonl", "a", encoding="utf-8")
    vlm = open(out / "vlm.jsonl", "a", encoding="utf-8") if args.png else None
    n_done, overflow = 0, []
    try:
        for i in range(args.n):
            seed = args.seed + i
            profile = _profile(seed, args)  # 같은 i 의 서류들은 모두 같은 고객
            if args.scenario:
                profile.extra.update(scenario=args.scenario, **SCENARIO_EXTRA.get(args.scenario, {}))
            for doc_id in ids:
                spec = reg[doc_id]
                sid = f"{doc_id}_{seed:06d}"
                html, fields, _ = render(spec, profile, seed, sample_mark=args.sample_mark)
                gt = to_nested(fields)
                (out / "html" / f"{sid}.html").write_text(html, encoding="utf-8")
                label = {
                    "id": sid, "doc_type": doc_id, "doc_name": spec.name, "group": spec.group,
                    "category": spec.category, "profile_seed": seed, "scenario": args.scenario,
                    **({"bank": fields_bank(fields)} if spec.group == "bank_form" else {}),
                    "html": f"html/{sid}.html", "fields": fields, "gt": gt,
                }
                if renderer:
                    img = f"images/{sid}.png"
                    info = renderer.render(html, out / img)
                    boxes = {b["key"]: b["bbox"] for b in info["fields"]}
                    for fld in fields:
                        fld["bbox"] = boxes.get(fld["key"])
                    label.update(image=img, width=info["width"], height=info["height"])
                    if info["overflow"]:
                        overflow.append(sid)
                    answer = json.dumps({"document_type": spec.name, **gt}, ensure_ascii=False)
                    images = [(sid, img, "clean")]
                    if args.augment:
                        from PIL import Image

                        from .augment import augment

                        arng = random.Random(f"aug:{sid}")
                        base = Image.open(out / img)
                        for k in range(args.augment):
                            aug_img, preset = augment(base, arng)
                            aug_path = f"images/{sid}_aug{k}.jpg"
                            aug_img.save(out / aug_path, quality=95)
                            images.append((f"{sid}_aug{k}", aug_path, preset))
                        label["augmented"] = [{"image": p_, "preset": pr} for _, p_, pr in images[1:]]
                    for vid, vimg, preset in images:
                        prompt = random.Random(vid).choice(PROMPTS)
                        vlm.write(json.dumps({
                            "id": vid, "image": vimg, "doc_type": doc_id, "augment": preset,
                            "messages": [
                                {"role": "user", "content": [{"type": "image", "image": vimg}, {"type": "text", "text": prompt}]},
                                {"role": "assistant", "content": [{"type": "text", "text": answer}]},
                            ],
                        }, ensure_ascii=False) + "\n")
                (out / "labels" / f"{sid}.json").write_text(json.dumps(label, ensure_ascii=False, indent=1), encoding="utf-8")
                manifest.write(json.dumps({k: label[k] for k in label if k not in ("fields", "gt")}, ensure_ascii=False) + "\n")
                n_done += 1
            print(f"\r{i + 1}/{args.n} 고객 프로필 완료 ({n_done}건)", end="", file=sys.stderr)
    finally:
        print(file=sys.stderr)
        manifest.close()
        if vlm:
            vlm.close()
        if renderer:
            renderer.__exit__(None, None, None)
    print(f"{n_done}건 생성 → {out}")
    if overflow:
        print(f"경고: 페이지 밖으로 넘친 샘플 {len(overflow)}건: {overflow[:10]}")


def fields_bank(fields: list[dict]) -> str | None:
    """은행 서식에 찍힌 은행명 (manifest 용)."""
    return next((f["value"] for f in fields if f["key"] in ("bank", "bank.name")), None)


def _leaves(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _leaves(v, f"{prefix}{k}.")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from _leaves(v, f"{prefix}{i}.")
    else:
        yield prefix[:-1], obj


def cmd_check(args) -> None:
    """템플릿 검증: 여러 프로필로 렌더링해 예외/미표시 데이터/페이지 넘침을 확인한다."""
    reg = load_all()
    ids = _select(args, reg)
    problems = 0
    renderer = None
    if args.png:
        from .image import ImageRenderer

        renderer = ImageRenderer(scale=1.0).__enter__()
    try:
        for doc_id in ids:
            spec = reg[doc_id]
            unused: set[str] = set()
            n_fields = []
            for seed in range(args.seed, args.seed + args.n):
                try:
                    html, fields, data = render(spec, _profile(seed, args), seed)
                except Exception as e:  # noqa: BLE001
                    print(f"[FAIL] {doc_id} seed={seed}: {type(e).__name__}: {e}")
                    problems += 1
                    break
                shown = {f["key"] for f in fields}
                unused |= {k for k, _ in _leaves(data) if k not in shown}
                n_fields.append(len(fields))
                empty = [f["key"] for f in fields if not f["value"].strip()]
                if empty:
                    print(f"[WARN] {doc_id} seed={seed}: 빈 값 필드 {empty[:5]}")
                no_label = [f["key"] for f in fields if not f["label"]]
                if no_label and seed == args.seed:
                    print(f"[INFO] {doc_id}: 라벨 없는 필드 {len(no_label)}개 (예: {no_label[:3]})")
                if renderer and seed < args.seed + args.png_n:
                    info = renderer.render(html, Path(args.tmp) / f"{doc_id}_{seed}.png")
                    if info["overflow"]:
                        print(f"[FAIL] {doc_id} seed={seed}: 내용이 페이지 밖으로 넘침")
                        problems += 1
            if unused:
                print(f"[WARN] {doc_id}: 생성했지만 문서에 표시하지 않은 값 {sorted(unused)[:8]}")
            if n_fields:
                print(f"[ OK ] {doc_id:40s} {spec.name}  필드 {min(n_fields)}~{max(n_fields)}개")
    finally:
        if renderer:
            renderer.__exit__(None, None, None)
    if problems:
        sys.exit(f"문제 {problems}건")


def main(argv=None) -> None:
    BANK_CHOICES = sorted(set(BANKS) | set(BRANDS), key=lambda b: (b in LEGACY, b))
    ap = argparse.ArgumentParser(prog="docgen", description="은행 제출 서류 합성 데이터 생성기")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ls = sub.add_parser("list", help="서류/시나리오 목록")
    ls.add_argument("--markdown", action="store_true", help="마크다운 표로 출력")
    g = sub.add_parser("generate", help="샘플 생성")
    g.add_argument("--types", default="all", help="all | 서류ID,... | 그룹명(identity,income,...)")
    g.add_argument("--scenario", choices=list(SCENARIOS), help="업무 시나리오별 서류 묶음")
    g.add_argument("--n", type=int, default=10, help="고객 프로필 수 (서류별 샘플 수)")
    g.add_argument("--seed", type=int, default=0)
    g.add_argument("--out", default="out")
    g.add_argument("--png", action="store_true", help="PNG 이미지 + bbox + vlm.jsonl 생성 (Playwright 필요)")
    g.add_argument("--scale", type=float, default=2.0, help="PNG 배율 (2.0 ≈ 192dpi)")
    g.add_argument("--augment", type=int, default=0, metavar="K",
                   help="--png 와 함께: 샘플마다 스캔/촬영/팩스 느낌의 증강 이미지 K장 추가 (GT 동일)")
    g.add_argument("--bank", choices=BANK_CHOICES, metavar="은행",
                   help="은행 서식을 낼 은행 고정 (예: 하나은행). 옛 은행 외환은행·KEB하나은행은 그 시기 날짜의 은행 서식만 생성")
    g.add_argument("--sample-mark", action="store_true", help="모든 서류에 '견본' 워터마크 (신분증류는 항상 표시)")
    c = sub.add_parser("check", help="템플릿 검증 (예외, 미표시 값, 페이지 넘침)")
    c.add_argument("--types", default="all")
    c.add_argument("--scenario", choices=list(SCENARIOS))
    c.add_argument("--n", type=int, default=30, help="검사할 프로필 수")
    c.add_argument("--seed", type=int, default=0)
    c.add_argument("--bank", choices=BANK_CHOICES, metavar="은행", help="은행 서식을 낼 은행 고정")
    c.add_argument("--png", action="store_true", help="이미지 렌더링으로 페이지 넘침까지 검사")
    c.add_argument("--png-n", type=int, default=5, help="이미지로 검사할 프로필 수")
    c.add_argument("--tmp", default="/tmp", help="검사용 PNG 저장 위치")
    args = ap.parse_args(argv)
    {"list": cmd_list, "generate": cmd_generate, "check": cmd_check}[args.cmd](args)
