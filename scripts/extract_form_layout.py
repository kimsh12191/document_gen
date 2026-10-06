"""하나은행 공개 서식 PDF → 기재란 '위치' 레이아웃 뽑기 (원본 배경 오버레이용).

  python scripts/extract_form_layout.py              # 전체
  python scripts/extract_form_layout.py --no 169     # 한 건만 (확인용, 결과를 화면에 요약)

서식 PDF 를 그대로 배경으로 깔고 그 위에 손님이 쓴 것처럼 값을 얹으려면,
값을 쓸 '자리'의 좌표가 필요하다. PDF 의 텍스트 레이어(글자 위치·색)와 표 선에서 뽑는다.

  text   라벨 셀 오른쪽(또는 머리글 아래)의 빈 칸        {label, rect, unit?, hint?, row?, group?}
  check  □ 보기 묶음                                     {label, options:[{text, box, rect}]}
  date   "년 월 일" 빈칸                                  {label, parts:{y, m, d}}
  sign   서명·날인 자리 "(서명 또는 인)"                   {label, name, mark}
  copy   자필 기재란 [가입자 자필기재 : 설명을 듣고 이해하였음] {label, rect, text}

좌표는 PDF 포인트 [x0, y0, x1, y1] (쪽 왼쪽 위 기준). 결과는 add_template/layouts/<분류>/<No>.json.
은행 전용칸(결재란·전산인자란·은행 사용란)은 고객이 쓰는 자리가 아니므로 뺀다.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "add_template" / "하나은행_서식자료"
OUT = ROOT / "add_template" / "layouts"

BOXES = "□☐◻"  # ■ 는 빈 서식에서 글머리표로만 쓰인다
# 결재·전산·은행 기재 칸 (고객 기재란이 아니다)
BANK_ONLY = re.compile(r"^(담당자?|책임자|관리자|부점장|지점장|검인|판매직원|본인확인|전산인자란|접수일자|접수번호|"
                       r"실명확인|확인자|취급자|승인|검토자?|결재|팀장|과장|대리|심사역|부서장|센터장|접수자|입력자|"
                       r"처리일자|처리자|영업점|조회자|확인|대조|합계)$")
BANK_AREA = re.compile(r"(은행\s*(사용|기재|확인)란|영업점\s*(사용|기재|확인)|은행\s*기재\s*사항|"
                       r"고객은\s*기재하지|직원\s*(기재|확인)란|은행사용란|For\s*Bank\s*Use|당행\s*(사용|기재)란)", re.I)
SENTENCE = re.compile(r"(합니다|바랍니다|하였|합은|입니다|습니다|십시오|하며|되며|않|경우에|드립니다|주시기|니다|[다요]\.$)")
SIGN_MARK = re.compile(r"^\(?(서명\s*또는\s*\(?인\)?|서명\s*/\s*인|인\s*/\s*서명|서명|인|날인|서명\s*또는\s*날인|"
                       r"인감날인|Signature|사인)\)?$")
UNITS = {"원", "%", "개월", "년", "월", "일", "회", "건", "명", "주", "개", "매", "좌", "USD", "원정", "천원", "백만원",
         "만원", "억원", "세", "일간", "개년", "시", "분", "㎡", "평"}
PUNCT = set("@-~/:().,·*")
# 빈칸 앞뒤에 인쇄된 군더더기: "금 ______ 원(₩ ______ )"
FILLER = re.compile(r"^(금|일금|원|원정|천원|만원|백만원|원\(₩|\(₩|₩|\\|\(|\)|%|USD)+$")


def filler(t: dict) -> bool:
    return bool(FILLER.match(t["text"])) or t["text"] in UNITS or set(t["text"]) <= PUNCT


def nfkc(s: str) -> str:
    return unicodedata.normalize("NFKC", s or "")


def squash(s: str) -> str:
    return re.sub(r"\s+", "", nfkc(s))


def is_gray(color: int) -> bool:
    """안내용 회색 글자 (예: '상품명 전체 자필기재', 'DC, 기업형IRP의 경우 회사명')."""
    r, g, b = (color >> 16) & 255, (color >> 8) & 255, color & 255
    # 흰 글씨(색칠한 칸의 라벨)는 안내 글자가 아니다
    return 110 < (r + g + b) / 3 < 225 and max(r, g, b) - min(r, g, b) < 60


def tokens(page) -> list[dict]:
    """글자 단위로 읽어 공백·색으로 끊은 낱말 목록. {text, rect, gray, size, line}."""
    out: list[dict] = []
    raw = page.get_text("rawdict")
    lid = 0
    for b in raw["blocks"]:
        for line in b.get("lines", []):
            lid += 1
            for sp in line["spans"]:
                gray = is_gray(sp["color"])
                cur: list = []

                def flush():
                    if cur:
                        x0 = min(c["bbox"][0] for c in cur)
                        y0 = min(c["bbox"][1] for c in cur)
                        x1 = max(c["bbox"][2] for c in cur)
                        y1 = max(c["bbox"][3] for c in cur)
                        out.append({"text": nfkc("".join(c["c"] for c in cur)), "rect": [x0, y0, x1, y1],
                                    "gray": gray, "size": sp["size"], "line": lid})
                        cur.clear()

                for ch in sp["chars"]:
                    c = ch["c"]
                    if c.isspace() or c == "\xa0":
                        flush()
                    elif c in BOXES:
                        flush()
                        cur.append(ch)
                        flush()
                    else:
                        cur.append(ch)
                flush()
    # 한 줄 안에서 이어지는 같은 색 낱말은 x 순서로 정렬해 둔다
    out.sort(key=lambda t: (t["line"], t["rect"][0]))
    return out


def inside(t: dict, r) -> bool:
    cx = (t["rect"][0] + t["rect"][2]) / 2
    cy = (t["rect"][1] + t["rect"][3]) / 2
    return r[0] - 0.5 <= cx <= r[2] + 0.5 and r[1] - 0.5 <= cy <= r[3] + 0.5


def vover(a, b) -> float:
    return max(0.0, min(a[3], b[3]) - max(a[1], b[1]))


def hover(a, b) -> float:
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0]))


def join_text(toks: list[dict]) -> str:
    """토큰을 줄 → x 순서로 이어 붙인다."""
    toks = sorted(toks, key=lambda t: (round(t["rect"][1] / 3), t["rect"][0]))
    return " ".join(t["text"] for t in toks).strip()


def clean_label(s: str) -> str:
    s = nfkc(s)
    s = re.sub(r"^[\s*※①-⑳\d.)]+(?=[가-힣A-Za-z(])", "", s)  # 앞 번호·기호
    s = re.sub(r"\s*[:：]\s*$", "", s)
    if s.endswith(")") and "(" not in s:
        s = s[:-1]
    s = re.sub(r"\s+", " ", s).strip()
    return s


def label_like(text: str) -> bool:
    t = squash(text)
    if not t or len(t) > 32 or any(c in t for c in BOXES):
        return False
    if SENTENCE.search(t) or t.startswith(("※", "*")):
        return False
    if re.fullmatch(r"[\d,.%\-~/:()@\s]+", t):
        return False
    return bool(re.search(r"[가-힣A-Za-z]", t))


# ---------------------------------------------------------------------------
# 체크박스 묶음
# ---------------------------------------------------------------------------

def box_options(toks: list[dict]) -> list[list[dict]]:
    """토큰들(한 셀 또는 한 줄)에서 □ 보기들을 뽑아 줄(같은 y) 단위 묶음으로 돌려준다.
    보기 글자는 □ 뒤부터 다음 □ 또는 큰 틈(18pt) 또는 ':' 까지."""
    lines: dict[int, list[dict]] = {}
    for t in sorted(toks, key=lambda t: (round((t["rect"][1] + t["rect"][3]) / 2 / 4), t["rect"][0])):
        key = round((t["rect"][1] + t["rect"][3]) / 2 / 4)
        # 가까운 줄 키로 합치기
        k = next((k for k in lines if abs(k - key) <= 1), key)
        lines.setdefault(k, []).append(t)
    groups = []
    for k in sorted(lines):
        row = sorted(lines[k], key=lambda t: t["rect"][0])
        opts = []
        i = 0
        while i < len(row):
            t = row[i]
            if t["text"] in BOXES:
                words = []
                j = i + 1
                last_x = t["rect"][2]
                while j < len(row) and row[j]["text"] not in BOXES and row[j]["rect"][0] - last_x < 18:
                    if row[j]["gray"]:
                        break
                    words.append(row[j])
                    last_x = row[j]["rect"][2]
                    if row[j]["text"].endswith((":", "：")):
                        break
                    j += 1
                text = clean_label(" ".join(w["text"] for w in words))
                text = re.split(r"\s*[※*]", text)[0][:40]
                rect = [t["rect"][0], min([t["rect"][1]] + [w["rect"][1] for w in words]),
                        max([t["rect"][2]] + [w["rect"][2] for w in words]),
                        max([t["rect"][3]] + [w["rect"][3] for w in words])]
                opts.append({"text": text, "box": [round(v, 1) for v in t["rect"]], "rect": [round(v, 1) for v in rect],
                             "line": k})
                i = j if j > i + 1 else i + 1
            else:
                i += 1
        if opts:
            groups.append(opts)
    return groups


# ---------------------------------------------------------------------------
# 쪽 하나 분석
# ---------------------------------------------------------------------------

def analyze_page(page, pno: int) -> dict:
    toks = tokens(page)
    W, H = page.rect.width, page.rect.height
    items: list[dict] = []
    used = set()  # 처리한 토큰 id

    try:
        tables = page.find_tables().tables
    except Exception:  # noqa: BLE001
        tables = []

    # 은행 전용 영역: '은행 사용란' 같은 머리 글자. 표 밖의 머리 글자면 바로 아래 표 전체,
    # 표 칸 안의 글자('은행기재란')면 그 칸만 뺀다. 회색 안내 글자도 같은 뜻이다.
    bank_rects: list[list[float]] = []
    line_texts: dict[int, list[dict]] = {}
    for t in toks:
        line_texts.setdefault(t["line"], []).append(t)
    all_cells = [list(c) for t in tables for c in t.cells if c]
    for lid, lt in line_texts.items():
        s = " ".join(x["text"] for x in lt)
        if not BANK_AREA.search(s):
            continue
        lr = bbox_of(lt)
        host = [c for c in all_cells if c[0] - 1 <= lr[0] and lr[2] <= c[2] + 1 and c[1] - 1 <= lr[1] and lr[3] <= c[3] + 1]
        if host:
            small = min(host, key=lambda c: (c[2] - c[0]) * (c[3] - c[1]))
            tb = next(t.bbox for t in tables if any(list(c) == small for c in t.cells if c))
            if abs(small[1] - tb[1]) < 2 and (small[2] - small[0]) > 0.8 * (tb[2] - tb[0]):
                bank_rects.append(list(tb))    # 표 머리 줄 전체가 '은행 사용란' → 표 전체
            else:
                bank_rects.append(small)
            continue
        for t in tables:
            tb = t.bbox
            if -2 <= tb[1] - lr[3] <= 30 and hover(tb, lr) > 0:
                bank_rects.append(list(tb))
        bank_rects.append([lr[0] - 4, lr[1] - 2, lr[2] + 4, lr[3] + 2])

    for t in tables:
        cells = [c for c in t.cells if c]
        heads = [squash(join_text([x for x in toks if inside(x, c)])) for c in cells]
        nonempty = [h for h in heads if h]
        if nonempty and sum(1 for h in nonempty if BANK_ONLY.match(h)) >= max(1, len(nonempty) * 0.6):
            bank_rects.append(list(t.bbox))
        elif "전산인자란" in "".join(heads) and len(nonempty) <= 2:
            bank_rects.append(list(t.bbox))

    def in_bank(r) -> bool:
        cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
        return any(b[0] - 1 <= cx <= b[2] + 1 and b[1] - 1 <= cy <= b[3] + 1 for b in bank_rects)

    for ti, t in enumerate(tables):
        if in_bank(t.bbox) and any(abs(t.bbox[k] - b[k]) < 2 for b in bank_rects for k in range(4)):
            for x in toks:
                if inside(x, t.bbox):
                    used.add(id(x))
            continue
        cells = []
        for c in t.cells:
            if not c:
                continue
            ct = [x for x in toks if inside(x, c) and id(x) not in used]
            dark = [x for x in ct if not x["gray"]]
            gray = [x for x in ct if x["gray"]]
            cells.append({"rect": list(c), "toks": ct, "dark": dark, "gray": gray,
                          "dtext": join_text(dark), "gtext": join_text(gray)})
        # 중복 셀 제거 (같은 rect)
        seen = set()
        uniq = []
        for c in cells:
            k = tuple(round(v) for v in c["rect"])
            if k not in seen:
                seen.add(k)
                uniq.append(c)
        cells = uniq

        def left_of(c):
            r = c["rect"]
            best = None
            for o in cells:
                if o is c:
                    continue
                q = o["rect"]
                if abs(q[2] - r[0]) < 2.5 and vover(q, r) > 0.5 * min(r[3] - r[1], q[3] - q[1]):
                    if best is None or vover(q, r) > vover(best["rect"], r):
                        best = o
            return best

        def col_header(c):
            """같은 열(c 의 가로 범위)을 따라 위로 올라가며 머리글 칸을 찾는다."""
            r = c["rect"]
            w = r[2] - r[0]
            ups = sorted((o for o in cells if o is not c and o["rect"][3] <= r[1] + 1.5
                          and (hover(o["rect"], r) > 0.6 * w or hover(o["rect"], r) > 0.6 * (o["rect"][2] - o["rect"][0]))),
                         key=lambda o: -o["rect"][3])
            for up in ups:
                wide = (up["rect"][2] - up["rect"][0]) > 1.6 * w
                boxed = any(x["text"] in BOXES for x in up["dark"])
                if not up["dark"] or wide or boxed:
                    continue
                if label_like(up["dtext"]):
                    return up
                if len(squash(up["dtext"])) <= 12:
                    return None  # 내용이 있는 짧은 칸(다른 라벨)을 만나면 머리글이 아니다
            return None

        sel_cols: dict[int, list[dict]] = {}
        for c in cells:
            r = c["rect"]
            if in_bank(r) or r[2] - r[0] < 8 or r[3] - r[1] < 6:
                continue
            boxes_in = [x for x in c["dark"] if x["text"] in BOXES]
            core = [x for x in c["dark"] if not filler(x) and x["text"] not in BOXES]
            lft = left_of(c)
            lft_label = clean_label(lft["dtext"]) if lft and lft["dark"] and label_like(lft["dtext"]) else None

            # ---- 체크박스 셀
            if boxes_in and len(boxes_in) == 1 and not core:
                # 선택 열: 칸에 □ 하나뿐 → 보기 글자는 같은 행 오른쪽 칸들 (디폴트옵션 포트폴리오 표)
                row_txt = [o["dtext"] for o in sorted(cells, key=lambda o: o["rect"][0])
                           if o is not c and o["rect"][0] >= r[2] - 1 and vover(o["rect"], r) > 0.6 * (r[3] - r[1])
                           and o["dark"]]
                if row_txt:
                    ob = [round(v, 1) for v in boxes_in[0]["rect"]]
                    sel_cols.setdefault(round(r[0]), []).append(
                        {"c": c, "opt": {"text": clean_label(row_txt[0])[:40], "box": ob, "rect": ob}})
                    for x in c["toks"]:
                        used.add(id(x))
                    continue
            if boxes_in:
                merged: list[dict] = []  # 앞에 설명 글자가 없는 줄은 앞 묶음에 이어 붙인다 (□SKT □LG / □KT □기타)
                for g in box_options(c["dark"]):
                    first = g[0]["box"]
                    fy = (first[1] + first[3]) / 2
                    pre = [x for x in c["dark"] if x["text"] not in BOXES and abs(
                        (x["rect"][1] + x["rect"][3]) / 2 - fy) < 4 and x["rect"][2] <= first[0] + 1]
                    name = clean_label(" ".join(x["text"] for x in sorted(pre, key=lambda x: x["rect"][0])))
                    if not pre and merged:
                        merged[-1]["options"] += g
                        continue
                    if not pre:  # 같은 칸 위쪽 줄의 글자 (서비스 통지 발송제외 신청 :)
                        up = [x for x in c["dark"] if x["text"] not in BOXES and x["rect"][3] <= first[1] + 1]
                        upn = clean_label(join_text(up)) if up else ""
                        if label_like(upn):
                            name = upn
                    merged.append({"t": "check", "page": pno, "label": name if label_like(name) else (lft_label or ""),
                                   "options": g, "cell": [round(v, 1) for v in r]})
                items += merged
                for x in c["toks"]:
                    used.add(id(x))
                continue

            # ---- 날짜 셀 ("년 월 일")
            ymd = [x for x in c["dark"] if x["text"] in ("년", "월", "일")]
            if len(ymd) == 3 and not [x for x in core if x["text"] not in ("년", "월", "일")]:
                items.append(date_item(ymd, r, pno, lft_label or "일자"))
                for x in c["toks"]:
                    used.add(id(x))
                continue

            # ---- 서명 셀 (회색/검정 "서명 또는 (인)" 만 든 빈 칸)
            alltext = squash(c["dtext"] + c["gtext"])
            if alltext and SIGN_MARK.match(alltext) and lft_label:
                mark = bbox_of(c["toks"])
                rowl = [o for o in cells if o["rect"][2] <= r[0] + 1 and o["dark"] and label_like(o["dtext"])
                        and vover(o["rect"], r) > 0.5 * (r[3] - r[1]) and (o["rect"][3] - o["rect"][1]) > 1.6 * (r[3] - r[1])]
                items.append({"t": "sign", "page": pno, "label": lft_label,
                              **({"section": " ".join(clean_label(o["dtext"]) for o in sorted(rowl, key=lambda o: o["rect"][0]))}
                                 if rowl else {}),
                              "name": [r[0] + 3, r[1] + 1, max(r[0] + 20, mark[0] - 4), r[3] - 1],
                              "mark": [round(v, 1) for v in mark]})
                for x in c["toks"]:
                    used.add(id(x))
                continue

            # ---- 값 칸
            if core:
                # 칸 안 왼쪽에 라벨이 있고 오른쪽이 비어 있는 칸 ("성 명 ______" 이 한 칸에 든 서식)
                lines_y = {round((x["rect"][1] + x["rect"][3]) / 2 / 4) for x in core}
                tx = bbox_of(c["dark"])
                below_empty = any(not o["dark"] and o["rect"][1] >= r[3] - 1.5 and o["rect"][1] - r[3] < 3
                                  and hover(o["rect"], r) > 0.8 * (r[2] - r[0]) for o in cells)
                if (len(lines_y) == 1 and label_like(c["dtext"]) and (r[2] - r[0]) > 90
                        and (tx[2] - r[0]) < 0.45 * (r[2] - r[0]) and r[2] - tx[2] > 60 and not below_empty
                        and not BANK_ONLY.match(squash(c["dtext"]))):
                    vr = [tx[2] + 6, r[1] + 1, r[2] - 3, r[3] - 1]
                    if (r[3] - r[1]) > 3.2 * (tx[3] - tx[1]):   # 키 큰 칸: 라벨 줄 높이에 맞춘다
                        vr = [tx[2] + 6, tx[1] - 4, r[2] - 3, tx[3] + 6]
                    it = {"t": "text", "page": pno, "label": clean_label(c["dtext"]),
                          "rect": [round(v, 1) for v in vr]}
                    if c["gtext"]:
                        it["hint"] = c["gtext"]
                    items.append(it)
                    for x in c["toks"]:
                        used.add(id(x))
                continue  # 이미 글자가 인쇄된 칸 (라벨·안내문)
            label, row, group = None, None, None
            hdr = col_header(c)
            # 구역 이름: 같은 행 맨 왼쪽의 세로로 합쳐진 라벨 칸 (대리인 / 위임인 / 기업부담금 …)
            rowl = [o for o in cells if o["rect"][2] <= r[0] + 1 and o["dark"] and label_like(o["dtext"])
                    and vover(o["rect"], r) > 0.5 * (r[3] - r[1])
                    and (o["rect"][3] - o["rect"][1]) > 1.6 * (r[3] - r[1])]
            # 왼쪽에 겹겹이 있으면 모두 잇는다 ("송금신청내용 받으실분(Beneficiary)")
            section = " ".join(clean_label(o["dtext"]) for o in sorted(rowl, key=lambda o: o["rect"][0])) if rowl else None
            is_row = False
            if lft_label and lft and (lft["rect"][3] - lft["rect"][1]) > 1.6 * (r[3] - r[1]) and hdr:
                label, group, is_row = clean_label(hdr["dtext"]), lft_label, True
            elif lft_label:
                label = lft_label
            elif hdr:
                label, is_row = clean_label(hdr["dtext"]), True
                group = clean_label(max(rowl, key=lambda o: o["rect"][0])["dtext"]) if rowl else None
            if not label:
                continue
            if BANK_ONLY.match(squash(label)):
                continue
            rr = list(r)
            unit = None
            units = [x for x in c["dark"] if x["text"] in UNITS or x["text"] in ("@",)]
            item = {"t": "text", "page": pno, "label": label}
            at = [x for x in c["dark"] if x["text"] == "@"]
            if at:
                item["at"] = [round(v, 1) for v in at[0]["rect"]]
            pre = [x for x in c["dark"] if x["text"] in ("금", "일금") and x["rect"][2] < r[0] + 0.3 * (r[2] - r[0])]
            if pre:
                rr[0] = max(x["rect"][2] for x in pre) + 3
            units = units + [x for x in c["dark"] if FILLER.match(x["text"]) and x["text"] not in ("금", "일금")]
            right_units = [x for x in units if (x["text"] in UNITS or FILLER.match(x["text"])) and x["rect"][0] > (r[0] + r[2]) / 2]
            if right_units:
                u = min(right_units, key=lambda x: x["rect"][0])
                rr[2] = u["rect"][0] - 2
                unit = "원" if u["text"].startswith("원") else u["text"]
            item["rect"] = [round(v, 1) for v in rr]
            if unit:
                item["unit"] = unit
            if c["gtext"]:
                item["hint"] = c["gtext"]
            if group:
                item["group"] = group
            if is_row:
                item["row"] = True
            if section and section != label:
                item["section"] = section
            items.append(item)
            for x in c["toks"]:
                used.add(id(x))
            for o in (lft, hdr):   # 라벨로 쓴 칸의 글자도 다시 쓰지 않는다
                if o is not None:
                    for x in o["toks"]:
                        used.add(id(x))

        for col in sel_cols.values():
            hdr = col_header(col[0]["c"])
            if len(col) == 1:
                items.append({"t": "check", "page": pno, "label": "", "options": [col[0]["opt"]]})
            else:
                items.append({"t": "check", "page": pno, "label": clean_label(hdr["dtext"]) if hdr else "선택",
                              "options": [x["opt"] for x in col], "pick": "one"})

    # ---- 표 밖: 체크박스 줄, 날짜 줄, 서명 줄, 자필 기재란
    rest = [x for x in toks if id(x) not in used and not in_bank(x["rect"])]
    by_line: dict[int, list[dict]] = {}
    for x in rest:
        by_line.setdefault(x["line"], []).append(x)
    # 같은 y 의 서로 다른 PDF line 을 하나의 시각적 줄로 합친다
    vis: list[list[dict]] = []
    for lt in sorted(by_line.values(), key=lambda lt: min(x["rect"][1] for x in lt)):
        cy = sum((x["rect"][1] + x["rect"][3]) / 2 for x in lt) / len(lt)
        for v in vis:
            vy = sum((x["rect"][1] + x["rect"][3]) / 2 for x in v) / len(v)
            if abs(vy - cy) < 3:
                v.extend(lt)
                break
        else:
            vis.append(list(lt))
    for lt in vis:
        lt.sort(key=lambda x: x["rect"][0])
        dark = [x for x in lt if not x["gray"]]
        s = " ".join(x["text"] for x in lt)
        if any(x["text"] in BOXES for x in dark):
            for g in box_options(dark):
                first = g[0]["box"]
                pre = [x for x in dark if x["text"] not in BOXES and x["rect"][2] <= first[0] + 1
                       and first[0] - x["rect"][2] < 160]
                name = clean_label(" ".join(x["text"] for x in pre[-6:]))
                items.append({"t": "check", "page": pno, "label": name if label_like(name) else "", "options": g})
            continue
        ymd = [x for x in dark if x["text"] in ("년", "월", "일")]
        if len(ymd) == 3 and ymd[0]["text"] == "년":
            gaps_ok = ymd[1]["rect"][0] - ymd[0]["rect"][2] > 8 and ymd[2]["rect"][0] - ymd[1]["rect"][2] > 8
            if gaps_ok:
                prev = [x for x in dark if x["rect"][2] <= ymd[0]["rect"][0] - 1]
                items.append(date_item(ymd, None, pno, "작성일", prev))
        # 콜론 뒤 빈칸: "금 액(AMOUNT) : ₩ ______", "성 명(NAME) : ______"
        if dark and not ymd and not re.search(r"\(\s*인\s*\)|서명", s):
            last = dark[-1]
            tail = last["text"] in ("₩", "\\", "$", "US$") and len(dark) > 1 and dark[-2]["text"].endswith((":", "："))
            if last["text"].endswith((":", "：")) or tail:
                lab_toks = [x for x in dark if x is not last] if tail else list(dark)
                # 앞쪽 큰 틈 이후만 라벨로
                cut = 0
                for k in range(1, len(lab_toks)):
                    if lab_toks[k]["rect"][0] - lab_toks[k - 1]["rect"][2] > 40:
                        cut = k
                lab_toks = lab_toks[cut:]
                label = clean_label(" ".join(x["text"] for x in lab_toks))
                lr = bbox_of(lt)
                right = min(W - 48, lr[0] + 430)
                if label_like(label) and right - lr[2] > 50:
                    for x in lt:
                        used.add(id(x))
                    items.append({"t": "text", "page": pno, "label": label,
                                  "rect": [round(v, 1) for v in [lr[2] + 5, lr[1] - 3, right, lr[3] + 3]],
                                  **({"unit": "원"} if tail and last["text"] == "₩" else {})})
        # "______ 지점 앞" : 취급 지점 이름 자리
        for k, x in enumerate(dark):
            if squash(x["text"]) in ("지점", "지점(부)", "지점(부)앞", "지점앞", "영업점") and (
                    k + 1 < len(dark) and squash(dark[k + 1]["text"]) in ("앞", "귀하", "귀중") or "앞" in x["text"]):
                prev_x = dark[k - 1]["rect"][2] if k else x["rect"][0] - 120
                if x["rect"][0] - prev_x > 30:
                    items.append({"t": "text", "page": pno, "label": "취급점",
                                  "rect": [round(v, 1) for v in [max(prev_x + 4, x["rect"][0] - 110), x["rect"][1] - 3,
                                                                 x["rect"][0] - 2, x["rect"][3] + 3]]})
        # 자필 기재: [가입자 자필기재 : 설 명 을 듣 고 이 해 하 였 음 ]
        if "자필" in s and any(x["gray"] for x in lt):
            gray = [x for x in lt if x["gray"]]
            phrase = squash("".join(x["text"] for x in gray))
            if len(phrase) >= 4 and "자필기재" not in phrase:
                r = bbox_of(gray)
                lab = [x for x in dark if x["rect"][2] <= r[0] + 1]
                items.append({"t": "copy", "page": pno, "label": clean_label(" ".join(x["text"] for x in lab[-3:]).lstrip("[")) or "자필기재",
                              "rect": [round(v, 1) for v in [r[0] - 4, r[1] - 3, r[2] + 4, r[3] + 3]], "text": phrase})
        # 서명 줄: "신청인   (서명 또는 인)" / "위임인 : 성명   (인)"
        for i, x in enumerate(lt):
            st = squash(x["text"])
            j = i
            if st.startswith("(") and not st.endswith(")"):
                # (서명 또는 인) 이 여러 토큰으로 끊겨 있다
                acc = st
                while j + 1 < len(lt) and not acc.endswith(")") and len(acc) < 14:
                    j += 1
                    acc += squash(lt[j]["text"])
                st = acc
            if not SIGN_MARK.match(st) or "(" not in st:
                continue
            mark = bbox_of(lt[i:j + 1])
            prev = [y for y in lt[:i] if not y["gray"]]
            if not prev:
                continue
            gap_left = prev[-1]["rect"][2]
            # 라벨: 서명 자리 왼쪽의 낱말들 (틈 이전까지)
            lab_toks = [prev[-1]]
            for y in reversed(prev[:-1]):
                if lab_toks[0]["rect"][0] - y["rect"][2] < 10:
                    lab_toks.insert(0, y)
                else:
                    break
            label = clean_label(" ".join(y["text"] for y in lab_toks))
            if not label_like(label):
                continue
            name = [gap_left + 4, mark[1] - 3, mark[0] - 4, mark[3] + 3]
            if name[2] - name[0] < 24:
                name = [gap_left + 2, mark[1] - 3, gap_left + 70, mark[3] + 3]
                if mark[0] - gap_left < 40:
                    name = None
            items.append({"t": "sign", "page": pno, "label": label,
                          "name": [round(v, 1) for v in name] if name else None,
                          "mark": [round(v, 1) for v in mark]})
            for y in lab_toks + lt[i:j + 1]:
                used.add(id(y))
        if any(x["text"] in ("년", "월", "일") for x in dark) or "자필" in s:
            for x in lt:
                used.add(id(x))

    # ---- 칸 안 라벨 + 오른쪽 빈자리 (표 인식이 칸을 다 못 나눈 서식): 선(그림)으로 칸 경계를 찾는다
    hs, vs = segments(page)
    rest = [x for x in toks if id(x) not in used and not x["gray"] and not in_bank(x["rect"])]
    for ph in phrases(rest, vs):
        label = clean_label(" ".join(x["text"] for x in ph))
        if not label_like(label) or len(squash(label)) > 20 or max(x["size"] for x in ph) >= 11.5:
            continue
        if len(squash(label)) < 2 or FILLER.match(squash(label)) or label.endswith("(") or "%" in label:
            continue
        if re.match(r"^(\(|\d+[.)]|[①-⑳])", ph[0]["text"]) or re.search(r"보존|귀하|귀중|은행|앞$|신청서|확인서|동의서|계약서", label):
            continue
        pr = bbox_of(ph)
        cy = (pr[1] + pr[3]) / 2
        borders = sorted(v[0] for v in vs if v[0] > pr[2] + 1 and v[1] - 1 <= cy <= v[2] + 1)
        start, right = pr[2] + 6, (borders[0] if borders else W - 40)
        if borders and borders[0] - pr[2] < 25:      # 라벨 칸의 오른쪽 선 → 값은 그 다음 칸
            start = borders[0] + 4
            right = borders[1] if len(borders) > 1 else W - 40
        band = [x for x in toks if x not in ph and start - 2 <= x["rect"][0] < right and not x["gray"]
                and abs((x["rect"][1] + x["rect"][3]) / 2 - cy) < 4]
        unit = None
        for x in sorted(band, key=lambda x: x["rect"][0]):
            if x["text"] in ("금", "일금") and x["rect"][0] < start + 20:
                start = x["rect"][2] + 3
            elif filler(x):
                if x["rect"][0] > (start + right) / 2:
                    right = min(right, x["rect"][0] - 2)
                    unit = unit or ("원" if x["text"].startswith("원") else x["text"])
            else:
                right = min(right, x["rect"][0] - 4)
                break
        if right - start < 50:
            continue
        top = max([h[0] for h in hs if h[0] < pr[1] + 1 and h[1] <= pr[2] + 20 and h[2] >= right - 20] + [-1])
        bot = min([h[0] for h in hs if h[0] > pr[3] - 1 and h[1] <= pr[2] + 20 and h[2] >= right - 20] + [1e9])
        in_table = any(t.bbox[0] - 1 <= pr[0] and pr[2] <= t.bbox[2] + 1 and t.bbox[1] - 1 <= pr[1] and pr[3] <= t.bbox[3] + 1
                       for t in tables)
        near = (pr[1] - top < 28) + (bot - pr[3] < 28)
        if near < (1 if in_table else 2):
            continue  # 선으로 둘러싸인 칸 안의 글자만 (본문 문장·제목 제외)
        left = max([v[0] for v in vs if v[0] < pr[0] - 1 and v[1] - 1 <= cy <= v[2] + 1] + [0])
        if left > 0 and abs((pr[0] - left) - (right - pr[2])) < 0.25 * (right - left):
            continue  # 칸 가운데 놓인 글자는 머리글 (값은 그 아래 칸)
        top = max(top, pr[1] - 8) if top >= 0 else pr[1] - 4
        bot = min(bot, pr[3] + 8) if bot < 1e8 else pr[3] + 4
        items.append({"t": "text", "page": pno, "label": label, **({"unit": unit} if unit else {}),
                      "rect": [round(v, 1) for v in [start, top + 1, right - 3, bot - 1]], "free": True})

    # 값 자리에 인쇄 글자가 걸치면 글자를 피한 가장 넓은 빈 구간으로 좁힌다 (못 찾으면 버린다)
    dark_all = [t for t in toks if not t["gray"]]
    kept = []
    for it in items:
        if it["t"] == "text":
            r = it["rect"]
            hits = [t for t in dark_all if hover(t["rect"], r) > 1 and vover(t["rect"], r) > 0.5 * (t["rect"][3] - t["rect"][1])
                    and t["text"] not in UNITS and t["text"] != "@" and not (it.get("at") and t["rect"] == it["at"])]
            if hits:
                xs = sorted((max(r[0], t["rect"][0] - 2), min(r[2], t["rect"][2] + 2)) for t in hits)
                gaps, cur = [], r[0]
                for a, b in xs:
                    if a > cur:
                        gaps.append((cur, a))
                    cur = max(cur, b)
                if r[2] > cur:
                    gaps.append((cur, r[2]))
                best = max(gaps, key=lambda g: g[1] - g[0], default=None)
                if not best or best[1] - best[0] < 28:
                    continue
                it["rect"] = [round(best[0] + 2, 1), r[1], round(best[1] - 2, 1), r[3]]
        kept.append(it)
    items = kept

    return {"width": round(W, 2), "height": round(H, 2), "items": items,
            "bank": [[round(v, 1) for v in b] for b in bank_rects]}


def segments(page) -> tuple[list[tuple], list[tuple]]:
    """그림에서 가로선 (y, x0, x1) 과 세로선 (x, y0, y1)."""
    hs, vs = [], []
    for d in page.get_drawings():
        for it in d["items"]:
            if it[0] == "l":
                a, b = it[1], it[2]
                if abs(a.y - b.y) < 1.2:
                    hs.append((a.y, min(a.x, b.x), max(a.x, b.x)))
                elif abs(a.x - b.x) < 1.2:
                    vs.append((a.x, min(a.y, b.y), max(a.y, b.y)))
            elif it[0] == "re":
                r = it[1]
                if r.height < 1.6:
                    hs.append(((r.y0 + r.y1) / 2, r.x0, r.x1))
                elif r.width < 1.6:
                    vs.append(((r.x0 + r.x1) / 2, r.y0, r.y1))
                else:
                    hs += [(r.y0, r.x0, r.x1), (r.y1, r.x0, r.x1)]
                    vs += [(r.x0, r.y0, r.y1), (r.x1, r.y0, r.y1)]
    return hs, vs


def phrases(toks: list[dict], vs: list[tuple] = ()) -> list[list[dict]]:
    """같은 줄에서 틈(10pt) 없이 이어지는 낱말 묶음. 세로선을 넘어가면 끊는다."""
    rows: list[list[dict]] = []
    for t in sorted(toks, key=lambda t: ((t["rect"][1] + t["rect"][3]) / 2, t["rect"][0])):
        cy = (t["rect"][1] + t["rect"][3]) / 2
        for row in rows:
            if abs((row[0]["rect"][1] + row[0]["rect"][3]) / 2 - cy) < 3:
                row.append(t)
                break
        else:
            rows.append([t])
    out = []
    for row in rows:
        row.sort(key=lambda t: t["rect"][0])
        cur = [row[0]]
        for t in row[1:]:
            gap = t["rect"][0] - cur[-1]["rect"][2]
            spaced = len(t["text"]) == 1 and len(cur[-1]["text"]) == 1   # 자간을 벌린 라벨 "기   한"
            cy = (t["rect"][1] + t["rect"][3]) / 2
            wall = any(cur[-1]["rect"][2] - 1 <= v[0] <= t["rect"][0] + 1 and v[1] - 1 <= cy <= v[2] + 1 for v in vs)
            if not wall and (gap < 10 or (spaced and gap < 70)):
                cur.append(t)
            else:
                out.append(cur)
                cur = [t]
        out.append(cur)
    return out


def bbox_of(toks: list[dict]) -> list[float]:
    return [min(t["rect"][0] for t in toks), min(t["rect"][1] for t in toks),
            max(t["rect"][2] for t in toks), max(t["rect"][3] for t in toks)]


def date_item(ymd: list[dict], cell, pno: int, label: str, prev: list[dict] | None = None) -> dict:
    y, m, d = sorted(ymd, key=lambda x: x["rect"][0])
    h0, h1 = min(t["rect"][1] for t in ymd) - 1, max(t["rect"][3] for t in ymd) + 1
    if cell:
        left = cell[0] + 3
    elif prev:
        left = prev[-1]["rect"][2] + 3
    else:
        left = y["rect"][0] - 40
    left = max(left, y["rect"][0] - 45)
    yy = bool(prev and prev[-1]["text"] in ("20", "19") and y["rect"][0] - prev[-1]["rect"][2] < 40)
    parts = {"y": [left, h0, y["rect"][0] - 1, h1],
             "m": [y["rect"][2] + 1, h0, m["rect"][0] - 1, h1],
             "d": [m["rect"][2] + 1, h0, d["rect"][0] - 1, h1]}
    return {"t": "date", "page": pno, "label": label, **({"yy": True} if yy else {}),
            "parts": {k: [round(v, 1) for v in r] for k, r in parts.items()}}


def extract(pdf: Path) -> dict:
    doc = pymupdf.open(pdf)
    pages = [analyze_page(p, i) for i, p in enumerate(doc)]
    doc.close()
    return {"pages": [{"width": p["width"], "height": p["height"], "bank": p["bank"]} for p in pages],
            "items": [it for p in pages for it in p["items"]]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no", type=int, nargs="*", help="이 번호의 서식만 처리")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    rows = list(csv.DictReader((SRC / "다운로드_결과.csv").read_text(encoding="utf-8-sig").splitlines(True)))
    out = Path(args.out)
    done = 0
    for r in rows:
        no = int(r["No"])
        if args.no and no not in args.no:
            continue
        if r["형식"] != "PDF":
            continue
        pdf = SRC / r["저장 파일"].replace("\\", "/")
        if not pdf.exists():
            continue
        try:
            lay = extract(pdf)
        except Exception as e:  # noqa: BLE001 - 깨진 PDF 는 건너뛴다
            print(f"  !! {no} {pdf.name}: {type(e).__name__} {e}", file=sys.stderr)
            continue
        lay = {"no": no, "class": r["분류"], "name": " ".join(r["서식명"].split()),
               "file": str(pdf.relative_to(ROOT)).replace("\\", "/"), **lay}
        d = out / r["분류"].replace("/", "_")
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{no:03d}.json").write_text(json.dumps(lay, ensure_ascii=False, indent=1), encoding="utf-8")
        done += 1
        kinds: dict[str, int] = {}
        for it in lay["items"]:
            kinds[it["t"]] = kinds.get(it["t"], 0) + 1
        print(f"{no:4d} {len(lay['pages'])}p {kinds}  {lay['name'][:40]}")
        if args.no:
            for it in lay["items"]:
                extra = it.get("text") or ", ".join(o["text"] for o in it.get("options", [])) or it.get("hint", "")
                print(f"   p{it['page']} {it['t']:5s} {it.get('label')!r:30s} {it.get('group') or ''} {extra[:60]}")
    print(f"\n완료 {done}건 → {out}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
