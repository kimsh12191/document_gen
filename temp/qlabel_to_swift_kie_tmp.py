"""임시 변환: qlabel 라벨 JSON (그림마다 태그 → 글자·위치) → ms-swift .jsonl (kie, 값과 위치). 그림은 그대로 두고 경로만 적는다.

라벨 꼴 — [그림 경로, {태그: [칸, …]}] 쌍의 목록 ({그림 경로: {태그: …}} 사전도 받는다):
  [["/{img_dir}/images/20260122013229_0105EUC250300021_1_3.png",
    {"BANK_ISSUE_CODE": [{"text": "KOEXKRSE",
                          "bbox_2d": [[1658, 2346], [303.2, 1785.1], [410.6, 1785.1], [410.6, 1807.0], [303.2, 1807.0]]}],
     "APPLICANT_NAME":  [{"text": "HENGLI PETROCHEMICAL INTERNATIONAL PTE. LTD.", "bbox_2d": [...]}]}],
   …]
  - 경로의 {img_dir} 은 --img-dir 로 바꾼다 (앞의 / 는 무시).
  - bbox_2d 첫 점 = 그림 크기 [너비, 높이], 나머지 네 점 = 칸의 꼭짓점 (픽셀). 꼭짓점의 최소·최대로 [x1, y1, x2, y2].
    그림 파일의 실제 크기가 라벨의 크기와 다르면 (줄인 사본 등) 그 비율로 꼭짓점을 맞추고 알려 준다.
    첫 점 없이 꼭짓점만 있거나 [x1, y1, x2, y2] 네 수만 있어도 된다 (그때 크기는 그림 파일에서).

한 줄: {"messages": [{"role": "user", "content": "<image>질문"}, {"role": "assistant", "content": "[{…}, …]"}], "images": ["/절대/경로.png"]}
  질문: 합성 kie 와 같은 문장 (docgen/bench/prompts.py 의 P_KIE: 값과 위치를 묻는다) + '- 키: 항목명' 줄.
        묻는 항목은 그 그림의 라벨에 있는 태그만 (그림마다 다르다). 40개를 넘으면 40개씩 나눠 여러 줄 (합성 kie 와 같음).
  정답: [{"key": 태그, "value": 글자, "bbox_2d": [x1, y1, x2, y2], "page": 1}, …] — 좌표는 그 그림 기준 0~1000 정수
        (Qwen2-VL·Qwen3-VL 방식, 합성 데이터와 같은 변환 docgen.bench.metrics.normalize_box). 글자가 빈 태그는 {"key": 태그, "value": null}.
        한 태그에 칸이 여럿이면 (기본 --multi join) 글자를 공백으로 이어 한 값, 위치는 칸들을 감싸는 박스.
        --multi number 면 칸마다 따로: 태그, 태그#2, … (같은 항목명 중 n번째 칸 — pairs_to_swift_kie_tmp.py·합성 kie 와 같은 표기)
  채점 (평가 세트로 쓸 때): train/scorers/kie_list_scorer.py — 정답에 위치가 있으므로 값+위치 점수 vl_f1 이 주 지표
        {"id": "real-<이름>", "format": "swift-fields", "gt": "reviewed", "paths": ["<출력.jsonl>"], "scorer": "../scorers/kie_list_scorer.py:score"}
  학습: 파이프라인 설정 data.train 에 {"path": "<출력.jsonl>", "format": "swift-fields", "scorer": "../scorers/kie_list_scorer.py:score"}
        또는 swift sft --dataset <출력.jsonl> 로 바로.

  python temp/qlabel_to_swift_kie_tmp.py <라벨.json> [<라벨2.json> …] <출력.jsonl> --img-dir <폴더>
        [--labels labels.json] [--multi join|number] [--val-ratio 0.05] [--no-check-images]
  python temp/qlabel_to_swift_kie_tmp.py keys <라벨.json> [… ] > labels.json      태그 목록·나온 횟수 (항목명을 따로 붙일 때)

- --labels: {"태그": "항목명"} 표 (예: {"APPLICANT_NAME": "신청인 상호"}). 없으면 항목명 = 태그.
- --val-ratio: 그 비율의 그림을 <출력>.val.jsonl 로 (그림 이름으로 고정해서 나눔 — 한 그림의 줄이 양쪽에 들어가지 않는다).
- --no-check-images: 그림 파일을 열지 않는다 (없는 그림도 그대로 적고, 크기는 bbox_2d 첫 점). 기본은 열어서 크기를 확인하고,
  없는 그림은 건너뛰고 수와 예를 알려 준다.
- 출력 파일이 이미 있으면 멈춘다 (덮어쓰지 않음). 실서류 그림은 이 컴퓨터 안에서만 읽는다 (어디에도 보내지 않음).
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # 저장소 최상위 (docgen)

from docgen.bench.metrics import normalize_box  # noqa: E402
from docgen.bench.prompts import P_KIE, item_line  # noqa: E402

MAX_ITEMS = 40


def load(paths):
    """라벨 파일들 → [(그림 경로 글자, {태그: [칸]})]."""
    out = []
    for p in paths:
        data = json.loads(Path(p).read_text(encoding="utf-8-sig"))
        for row in data.items() if isinstance(data, dict) else data:
            if not (isinstance(row, (list, tuple)) and len(row) == 2 and isinstance(row[1], dict)):
                raise ValueError(f"{p}: [그림 경로, {{태그: [...]}}] 꼴이 아닌 줄: {str(row)[:120]}")
            out.append((str(row[0]), row[1]))
    return out


def image_path(raw, img_dir):
    if "{img_dir}" in raw:
        return Path(img_dir) / raw.split("{img_dir}", 1)[1].lstrip("/\\")
    return Path(raw) if Path(raw).is_absolute() else Path(img_dir) / raw


def parse_box(b):
    """라벨 bbox_2d → (라벨에 적힌 그림 크기 또는 None, 픽셀 [x1, y1, x2, y2])."""
    if all(isinstance(v, (int, float)) for v in b):
        if len(b) != 4:
            raise ValueError(f"bbox_2d 수가 {len(b)}개")
        x1, y1, x2, y2 = map(float, b)
        return None, [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
    pts = [tuple(map(float, q)) for q in b]
    size = None
    if len(pts) in (3, 5):   # 첫 점 = 그림 크기
        size, pts = pts[0], pts[1:]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    return size, [min(xs), min(ys), max(xs), max(ys)]


def _union(boxes):
    return [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]


def _text(c):
    t = c.get("text")
    t = "" if t is None else str(t).strip()
    return t or None


def gold_of(tags, real_size, multi, notes):
    """한 그림의 태그들 → 정답 목록 (라벨의 태그 순서)."""
    out = []
    for key, cells in tags.items():
        cells = cells if isinstance(cells, list) else [cells]
        parsed = []
        for c in cells:
            if not isinstance(c, dict):
                continue
            box, size = None, real_size
            if c.get("bbox_2d"):
                label_size, box = parse_box(c["bbox_2d"])
                size = real_size or label_size
                if size is None:
                    raise ValueError("그림 크기를 모름 (그림 파일도, bbox_2d 첫 점도 없음)")
                if real_size and label_size and tuple(round(v) for v in label_size) != tuple(real_size):
                    sx, sy = real_size[0] / label_size[0], real_size[1] / label_size[1]
                    box = [box[0] * sx, box[1] * sy, box[2] * sx, box[3] * sy]
                    notes.add(f"라벨 크기 {tuple(round(v) for v in label_size)} ≠ 그림 {tuple(real_size)}")
            parsed.append((_text(c), box, size))
        filled = [p for p in parsed if p[0] is not None]
        if not filled:
            out.append({"key": key, "value": None})
            continue
        groups = [[p] for p in filled] if multi == "number" else [filled]
        for n, g in enumerate(groups, 1):
            e = {"key": key if n == 1 else f"{key}#{n}", "value": " ".join(p[0] for p in g)}
            boxes = [p[1] for p in g if p[1] is not None]
            if boxes:
                w, h = g[0][2]
                e["bbox_2d"] = normalize_box(_union(boxes), w, h)
                e["page"] = 1
            out.append(e)
    return out


def label_of(key, labels):
    base, _, n = key.partition("#")
    lab = labels.get(key) or labels.get(base) or base
    return f"{lab} (같은 항목명 중 {n}번째 칸)" if n else lab


def records(image, gold):
    out = []
    for i in range(0, len(gold), MAX_ITEMS):
        part = gold[i:i + MAX_ITEMS]
        items = "\n".join(item_line(g["key"], g["_label"], "") for g in part)
        ans = [{k: v for k, v in g.items() if k != "_label"} for g in part]
        out.append({"messages": [{"role": "user", "content": "<image>" + P_KIE.format(items=items)},
                                 {"role": "assistant", "content": json.dumps(ans, ensure_ascii=False)}],
                    "images": [str(image)]})
    return out


def is_val(name, ratio):
    return ratio > 0 and int(hashlib.sha1(name.encode()).hexdigest()[:8], 16) / 0x100000000 < ratio


def cmd_convert(srcs, dst, img_dir, labels_path=None, multi="join", val_ratio=0.0, check=True):
    dst = Path(dst)
    val_dst = dst.with_suffix(".val.jsonl")
    for p in [dst] + ([val_dst] if val_ratio > 0 else []):
        if p.exists():
            sys.exit(f"{p} 가 이미 있습니다 (덮어쓰지 않습니다)")
    labels = {k: v for k, v in json.loads(Path(labels_path).read_text(encoding="utf-8")).items() if v} if labels_path else {}
    out = {"train": [], "val": []}
    missing, bad, notes = [], [], set()
    n_img, n_field, n_null, n_box, tags_seen = 0, 0, 0, 0, Counter()
    for raw, tags in load(srcs):
        img = image_path(raw, img_dir)
        real_size = None
        if check:
            if not img.is_file():
                missing.append(str(img))
                continue
            from PIL import Image

            with Image.open(img) as im:
                real_size = im.size
        if not tags:
            bad.append(f"{img.name}: 태그 없음")
            continue
        try:
            gold = gold_of(tags, real_size, multi, notes)
        except (ValueError, TypeError, IndexError) as exc:
            bad.append(f"{img.name}: {exc}")
            continue
        for g in gold:
            g["_label"] = label_of(g["key"], labels)
        out["val" if is_val(img.name, val_ratio) else "train"] += records(img.resolve() if check else img, gold)
        n_img += 1
        n_field += len(gold)
        n_null += sum(g["value"] is None for g in gold)
        n_box += sum("bbox_2d" in g for g in gold)
        tags_seen.update(list(tags))
    if not out["train"] and not out["val"]:
        sys.exit(f"바꾼 그림이 없습니다 (그림 없음 {len(missing)}, 읽기 실패 {len(bad)}"
                 + (f", 예: {(bad or missing)[0]}" if bad or missing else "") + ")")
    dst.parent.mkdir(parents=True, exist_ok=True)
    for path, rows in [(dst, out["train"])] + ([(val_dst, out["val"])] if val_ratio > 0 else []):
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print(f"그림 {n_img}장 → {dst} {len(out['train'])}줄"
          + (f", {val_dst} {len(out['val'])}줄" if val_ratio > 0 else "")
          + f" (항목 {n_field}개 중 null {n_null}개, 위치 있음 {n_box}개, 태그 {len(tags_seen)}종)")
    if missing:
        print(f"그림 파일이 없어 건너뜀 {len(missing)}장 (예: {missing[0]}) — --img-dir 확인")
    if bad:
        print(f"읽지 못해 건너뜀 {len(bad)}장 (예: {bad[0]})")
    for n in sorted(notes)[:5]:
        print(f"크기 맞춤: {n}")


def cmd_keys(srcs):
    count = Counter()
    for _, tags in load(srcs):
        count.update(list(tags))
    print(json.dumps({k: "" for k, _ in count.most_common()}, ensure_ascii=False, indent=1))
    print(f"태그 {len(count)}종 (많이 나온 순, 횟수: {dict(count.most_common(5))} …). 값 칸에 항목명을 채워 --labels 로 넘기세요.",
          file=sys.stderr)


def main(argv):
    if argv and argv[0] == "keys" and len(argv) >= 2:
        return cmd_keys(argv[1:])
    flags = {"--no-check-images"}
    opts, pos, i = {}, [], 0
    while i < len(argv):
        a = argv[i]
        if a in flags:
            opts[a] = True
            i += 1
        elif a.startswith("--") and i + 1 < len(argv):
            opts[a] = argv[i + 1]
            i += 2
        else:
            pos.append(a)
            i += 1
    known = {"--img-dir", "--labels", "--multi", "--val-ratio", "--no-check-images"}
    if len(pos) < 2 or not set(opts) <= known or "--img-dir" not in opts or opts.get("--multi", "join") not in ("join", "number"):
        sys.exit(__doc__)
    return cmd_convert(pos[:-1], pos[-1], opts["--img-dir"], opts.get("--labels"), opts.get("--multi", "join"),
                       float(opts.get("--val-ratio", 0)), not opts.get("--no-check-images"))


if __name__ == "__main__":
    main(sys.argv[1:])
