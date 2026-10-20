"""생성기 공통 v1 라벨 검사와 데이터셋 변환. 렌더링·OCR 서버 호출 없이 기존 정답을 쓴다."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
import shutil
import sys
import time
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / 'studio/static/label-format/v1'
BANK_TASKS = ('classify', 'kie', 'marks', 'ocr_field', 'doc_check', 'review')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f'유한하지 않은 수: {x}')))


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


def contained(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name or '\\' in name or re.match(r'^[A-Za-z]:', name):
        raise ValueError('데이터 루트 기준 / 구분 상대 경로여야 합니다')
    p = (root / name).resolve()
    if Path(name).is_absolute() or '..' in name.split('/') or not p.is_relative_to(root.resolve()):
        raise ValueError('데이터 폴더 밖의 경로는 사용할 수 없습니다')
    return p


def schema_errors(value, schema, where='$'):
    """배포한 v1 Schema가 사용하는 키워드를 검사한다. 별도 패키지 설치가 필요 없다."""
    out = []
    typ = schema.get('type')
    types = typ if isinstance(typ, list) else [typ] if typ else []
    def finite(v):
        try:
            return math.isfinite(v)
        except OverflowError:
            return False
    matches = {'object': isinstance(value, dict), 'array': isinstance(value, list), 'string': isinstance(value, str),
               'integer': isinstance(value, int) and not isinstance(value, bool),
               'number': isinstance(value, (int, float)) and not isinstance(value, bool) and finite(value),
               'null': value is None, 'boolean': isinstance(value, bool)}
    if types and not any(matches[t] for t in types):
        return [(where, f'타입은 {"/".join(types)}이어야 합니다')]
    if 'const' in schema and (type(value) is not type(schema['const']) or value != schema['const']):
        out.append((where, f"값은 {schema['const']!r}이어야 합니다"))
    if 'enum' in schema and value not in schema['enum']:
        out.append((where, '허용되지 않은 값입니다'))
    if isinstance(value, dict):
        for k in schema.get('required', []):
            if k not in value:
                out.append((f'{where}.{k}', '필수 항목입니다'))
        for k, v in value.items():
            out.extend(schema_errors(v, schema.get('properties', {}).get(k, {}), f'{where}.{k}'))
        for k, deps in schema.get('dependentRequired', {}).items():
            if k in value:
                out.extend((f'{where}.{dep}', f'{k}가 있으면 필수입니다') for dep in deps if dep not in value)
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0) or len(value) > schema.get('maxItems', float('inf')):
            out.append((where, '배열 길이가 규격과 다릅니다'))
        if schema.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            out.append((where, '배열에 중복이 있습니다'))
        for i, v in enumerate(value):
            out.extend(schema_errors(v, schema.get('items', {}), f'{where}[{i}]'))
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0) or ('pattern' in schema and not re.search(schema['pattern'], value)):
            out.append((where, '비어 있거나 허용되지 않은 문자열·경로입니다'))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if not finite(value) or value < schema.get('minimum', -float('inf')) or value > schema.get('maximum', float('inf')):
            out.append((where, '허용 범위를 벗어난 수입니다'))
    for sub in schema.get('allOf', []):
        out.extend(schema_errors(value, sub, where))
    if 'if' in schema and not schema_errors(value, schema['if'], where):
        out.extend(schema_errors(value, schema.get('then', {}), where))
    return out


def inspect(source: str, import_dir: str | None = None) -> dict:
    from docgen.registry import SCENARIOS, SCENARIO_PROCESSING, load_all

    root = Path(source).expanduser().resolve()
    errors, warnings, files, docs, bundles = [], [], {}, [], []
    def error(file, key, message):
        if len(errors) < 200:
            errors.append({'file': str(file), 'path': key, 'message': message})
    def warning(file, key, message):
        if len(warnings) < 200:
            warnings.append({'file': str(file), 'path': key, 'message': message})
    if not root.is_dir() or (import_dir and not root.is_relative_to(Path(import_dir).expanduser().resolve())):
        error('', '$', '폴더가 없거나 설정의 import_dir 밖입니다. ZIP은 먼저 압축을 푸세요')
        return {'ok': False, 'errors': errors, 'warnings': [], 'source': str(root)}
    def load(rel, kind):
        try:
            path = contained(root, rel)
            raw = path.read_bytes()
            data = json.loads(raw.decode('utf-8-sig'), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f'유한하지 않은 수: {x}')))
            files[rel] = hashlib.sha256(raw).hexdigest()
            for key, msg in schema_errors(data, read(SCHEMAS / f'{kind}.schema.json')):
                error(rel, key, msg)
            return data
        except (OSError, ValueError, TypeError) as e:
            error(rel, '$', str(e))
            return None
    meta = load('meta.json', 'meta')
    if not isinstance(meta, dict) or schema_errors(meta, read(SCHEMAS / 'meta.schema.json')):
        return {'ok': False, 'errors': errors, 'warnings': warnings, 'source': str(root)}
    if meta['real_data'] and meta['gt'] == 'exact':
        error('meta.json', '$.gt', '실서류에는 생성 정답 exact를 쓸 수 없습니다. reviewed 또는 pseudo를 지정하세요')
    reg = load_all()
    dictionary = read(ROOT / 'guide/fields/fields.json')
    labels_dir = contained(root, 'labels')
    label_files = sorted(labels_dir.rglob('*.json')) if labels_dir.is_dir() else []
    if not label_files:
        error('labels', '$', 'labels/ 아래 문서 라벨 JSON이 없습니다')
    ids, image_owner = set(), {}
    ocr_count = 0
    for lf in label_files:
        rel = lf.relative_to(root).as_posix()
        d = load(rel, 'document')
        if not isinstance(d, dict) or schema_errors(d, read(SCHEMAS / 'document.schema.json')):
            continue
        did = d['id']
        if did != lf.relative_to(labels_dir).with_suffix('').as_posix() or did in ids:
            error(rel, '$.id', '문서 ID가 중복되거나 labels/<id>.json 이름과 다릅니다')
        ids.add(did)
        if d['doc_type'] not in reg:
            error(rel, '$.doc_type', '등록되지 않은 서식 ID입니다. 먼저 ① 서식에서 등록하세요')
        if len(d['pages']) != len(d['images']):
            error(rel, '$.pages', 'images와 pages의 쪽 수가 다릅니다')
            continue
        ocrs = []
        for i, (name, page) in enumerate(zip(d['images'], d['pages'])):
            try:
                image = contained(root, name)
                raw_image = image.read_bytes()
                with Image.open(io.BytesIO(raw_image)) as im:
                    if getattr(im, 'n_frames', 1) != 1 or im.getexif().get(274, 1) != 1:
                        raise ValueError('여러 프레임 또는 EXIF 회전 이미지입니다. 쪽별 정방향 이미지로 저장하세요')
                    if im.size != (page['width'], page['height']):
                        raise ValueError(f'실제 이미지 크기 {im.size}와 pages 크기가 다릅니다')
                    im.load()
                if image in image_owner:
                    raise ValueError(f'이미 다른 문서에서 사용한 이미지입니다: {image_owner[image]}')
                image_owner[image] = did
                files[name] = hashlib.sha256(raw_image).hexdigest()
            except (OSError, ValueError) as e:
                error(rel, f'$.images[{i}]', str(e))
            # images/ 접두사를 제외한 상대 경로를 ocr/ 아래에서 찾는다.
            orel = 'ocr/' + str(Path(name.removeprefix('images/')).with_suffix('.json')).replace('\\', '/')
            try:
                exists = contained(root, orel).is_file()
            except ValueError:
                exists = False
            if exists:
                o = load(orel, 'ocr')
                if o is not None and not schema_errors(o, read(SCHEMAS / 'ocr.schema.json')):
                    for line in o['data']['basicData']:
                        for word in line:
                            if any(pt['x'] > page['width'] or pt['y'] > page['height'] for pt in word['bounding']['vertices']):
                                error(orel, '$.data.basicData', 'OCR 위치가 이미지 범위를 벗어났습니다')
                    ocr_count += 1
                ocrs.append(orel)
            else:
                ocrs.append(None)
        keys = set()
        known = {f['key'] for f in dictionary.get(d['doc_type'], {}).get('keys', [])}
        for i, f in enumerate(d['fields']):
            key = f'$.fields[{i}]'
            if f['key'] in keys:
                error(rel, key + '.key', '항목 키가 중복됩니다')
            keys.add(f['key'])
            generic = re.sub(r'\.\d+(?=\.|$)', '[]', f['key'])
            if known and f['key'] not in known and generic not in known:
                warning(rel, key + '.key', f"서식 사전에 없는 키입니다. 새 항목인지 확인하세요: {f['key']}")
            pg = f.get('page')
            if pg is not None and not 0 <= pg < len(d['pages']):
                error(rel, key + '.page', '쪽 번호가 범위를 벗어났습니다 (0부터 시작)')
                continue
            boxes = [(key + '.' + k, f[k]) for k in ('bbox', 'label_bbox') if k in f]
            for j, op in enumerate(f.get('options', [])):
                boxes += [(f'{key}.options[{j}].{k}', op[k]) for k in ('bbox', 'box_bbox') if k in op]
            for loc, box in boxes:
                if pg is None:
                    error(rel, loc, '위치가 있으면 page가 필요합니다')
                else:
                    x0, y0, x1, y1 = box
                    size = d['pages'][pg]
                    if not (0 <= x0 < x1 <= size['width'] and 0 <= y0 < y1 <= size['height']):
                        error(rel, loc, '좌표 순서 또는 이미지 범위가 잘못되었습니다')
            if f['type'] == 'checkbox' and sum(o['checked'] for o in f.get('options', [])) > 1:
                error(rel, key, '단일 선택 체크박스에 여러 보기가 선택되었습니다')
            if f['type'] in ('checkbox', 'checkbox_multi') and not f.get('options'):
                warning(rel, key, '보기가 없어 체크 문항을 만들지 않습니다')
        docs.append({'file': rel, 'label': d, 'ocr': ocrs})
    bf = root / 'bundles.jsonl'
    if bf.exists():
        try:
            contained(root, 'bundles.jsonl')
            bundle_bytes = bf.read_bytes()
            files['bundles.jsonl'] = hashlib.sha256(bundle_bytes).hexdigest()
            seen = set()
            lookup = {d['label']['id']: d['label'] for d in docs}
            for line, raw in enumerate(bundle_bytes.decode('utf-8-sig').splitlines(), 1):
                if not raw.strip():
                    continue
                try:
                    b = json.loads(raw)
                except ValueError as e:
                    error('bundles.jsonl', f'line {line}', str(e)); continue
                errs = schema_errors(b, read(SCHEMAS / 'bundle.schema.json'))
                for key, msg in errs:
                    error('bundles.jsonl', f'line {line} {key}', msg)
                if errs:
                    continue
                if b['bundle_id'] in seen:
                    error('bundles.jsonl', f'line {line}', '묶음 ID가 중복됩니다')
                if any(x in b['bundle_id'] for x in ('/', '\\')):
                    error('bundles.jsonl', f'line {line}', '묶음 ID에는 경로 구분자를 쓸 수 없습니다')
                seen.add(b['bundle_id'])
                if b['scenario'] not in SCENARIOS:
                    error('bundles.jsonl', f'line {line}', '등록되지 않은 시나리오입니다. ③에서 먼저 저장하세요')
                if any(d not in lookup for d in b['documents']):
                    error('bundles.jsonl', f'line {line}', 'labels/에 없는 문서 ID를 참조합니다')
                kinds = [lookup[d]['doc_type'] for d in b['documents'] if d in lookup]
                if len(set(kinds)) != len(kinds):
                    error('bundles.jsonl', f'line {line}', '한 묶음에 같은 서식이 여러 건 있습니다. 현재는 서식별 문서 한 건을 지원합니다')
                others = b.get('not_customer')
                if others is not None and (not isinstance(others, list) or any(x not in b['documents'] for x in others)):
                    error('bundles.jsonl', f'line {line}', 'not_customer에는 제출 문서 ID 목록을 적으세요')
                if 'customer' in b and (not isinstance(b['customer'], str) or not b['customer'].strip()):
                    error('bundles.jsonl', f'line {line}', 'customer는 비어 있지 않은 고객명입니다')
                if others is None:
                    warning('bundles.jsonl', f'line {line}', 'not_customer가 없어 구비 문항은 생략합니다. 명의 확인 후 타인 서류 ID 목록 또는 []를 적으세요')
                bundles.append(b)
        except (OSError, ValueError) as e:
            error('bundles.jsonl', '$', str(e))
    n_pages = sum(len(d['label']['images']) for d in docs)
    full_ocr = meta.get('ocr_scope') == 'full_page' and ocr_count == n_pages and n_pages > 0
    if not full_ocr:
        warning('meta.json', '$.ocr_scope', 'OCR 세트는 모든 쪽의 OCR 정답과 ocr_scope:full_page가 있어야 생성합니다. 항목 추출은 계속 가능합니다')
    fingerprint = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    scenarios = {b['scenario']: {'name': SCENARIOS[b['scenario']][0], 'docs': SCENARIOS[b['scenario']][1],
                  'processing': SCENARIO_PROCESSING.get(b['scenario'])} for b in bundles if b['scenario'] in SCENARIOS}
    return {'ok': not errors, 'errors': errors, 'warnings': warnings, 'source': str(root), 'meta': meta,
            'documents': docs, 'bundles': bundles, 'scenarios': scenarios, 'files': files, 'fingerprint': fingerprint,
            'summary': {'documents': len(docs), 'pages': n_pages, 'fields': sum(len(d['label']['fields']) for d in docs),
                        'bundles': len(bundles), 'ocr_pages': ocr_count, 'full_ocr': full_ocr}}


def snapshot(check: dict, dest: Path):
    """검사 시점과 같은 파일만 복사한다. 원본 폴더에는 쓰지 않는다."""
    root = Path(check['source'])
    for rel, expected in check['files'].items():
        src = contained(root, rel)
        target = contained(dest, rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, target)
        if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            raise ValueError(f'검사 후 파일이 바뀌었습니다. 다시 검사하세요: {rel}')


def build_bank(check: dict, out: Path, tasks: list[str], split: str):
    from docgen.bench.build import Builder, VERSION, swift_record
    from docgen.schema import infer
    from .labeled_bundles import build_bundles

    snapshot(check, out / 'input')
    b = Builder.__new__(Builder)
    b.out, b.buf = out, []
    (out / 'crops').mkdir(exist_ok=True)
    records, docs = [], {}
    for n, row in enumerate(check['documents'], 1):
        d = row['label']
        fields = json.loads(json.dumps(d['fields']))
        for f in fields:
            if 'norm' not in f and f['type'] not in ('seal', 'signature', 'checkbox_multi'):
                _, f['norm'] = infer(f['key'], f['value'], f['type'])
        r = {'doc_id': d['doc_type'], 'name': d['doc_name'], 'group': 'labeled', 'condition': 'original', 'writing': 'unknown',
             'images': ['input/' + im for im in d['images']], 'sizes': [(p['width'], p['height']) for p in d['pages']],
             'pages': d['pages'], 'fields': fields, 'raw_keys': [f['key'] for f in fields],
             'visible': {f['key'] for f in fields if f['value'] is not None}, 'document_id': d['id']}
        docs[d['id']] = r
        b.single(r, 'images/' + hashlib.sha256(d['id'].encode()).hexdigest()[:24], len(fields), len(fields))
        for item in b.take():
            if item['task'] in tasks:
                item['meta'].update(document_id=d['id'], source='results', gt=check['meta']['gt'])
                records.append(item)
        print(f'서류 {n}/{len(check["documents"])}', flush=True)
    bundled, bundle_records = build_bundles(check, docs, tasks)
    records.extend(bundled)
    counts = {}
    (out / 'tasks').mkdir(exist_ok=True)
    for task in BANK_TASKS:
        items = [r for r in records if r['task'] == task]
        if not items:
            continue
        counts[task] = len(items)
        (out / 'tasks' / f'{task}.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in items), encoding='utf-8')
    if not records:
        raise ValueError('선택한 과제로 생성할 수 있는 문항이 없습니다. 라벨과 과제를 확인하세요')
    if split == 'train':
        (out / 'swift').mkdir(exist_ok=True)
        (out / 'swift/all.jsonl').write_text(''.join(json.dumps(swift_record(r), ensure_ascii=False) + '\n' for r in records), encoding='utf-8')
    (out / 'bundles.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in bundle_records), encoding='utf-8')
    meta = {'version': VERSION, 'split': split, 'created': time.strftime('%Y-%m-%d %H:%M:%S'), 'counts': counts,
            'doc_names': {d['label']['doc_type']: d['label']['doc_name'] for d in check['documents']},
            'studio': {'source': 'results', 'gt': check['meta']['gt'], 'real_data': check['meta']['real_data']},
            'settings': {'label_format': 'docgen-labels/1', 'fingerprint': check['fingerprint'], 'tasks': tasks}}
    write(out / 'meta.json', meta)
    # 복구가 완료 파일·문항 수를 검사할 수 있도록 dataset.json은 마지막에 쓴다.
    write(out / 'dataset.json', {**meta, 'source_path': check['source'], 'label_format': 'docgen-labels/1'})


def build_ocr(check: dict, out: Path, split: str):
    if not check['summary']['full_ocr']:
        raise ValueError('쪽 전체 OCR 정답과 meta.json의 ocr_scope:full_page가 필요합니다')
    if split == 'train' and check['summary']['documents'] < 2:
        raise ValueError('OCR 학습용은 평가 분리를 위해 서로 다른 문서가 2건 이상 필요합니다')
    snapshot(check, out / 'input')
    rows = []
    for row in check['documents']:
        d = row['label']
        for page, (im, ocr) in enumerate(zip(d['images'], row['ocr'])):
            rows.append({'document_id': d['id'], 'page_id': f'{d["id"]}/p{page + 1}',
                         'image': str((out / 'input' / im).resolve()), 'ocr_json': str((out / 'input' / ocr).resolve()),
                         'split': 'benchmark' if split == 'test' else 'train'})
    manifest = out / 'manifest.jsonl'
    manifest.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
    cfg = read(ROOT / 'ocr/config.example.json')
    cfg.update(manifest=str(manifest.resolve()), output_dir=str((out / 'prepared').resolve()),
               cache_dir=str((out / 'ocr_cache').resolve()), ocr_callable='internal_ocr_adapter:ocr_from_file',
               ocr_revision='docgen-labels-v1-' + check['fingerprint'][:16], val_fraction=0,
               benchmark_fraction=0 if split == 'test' else 0.1, benchmark_only=split == 'test',
               reference_type={'exact': 'synthetic_exact', 'reviewed': 'human_reviewed', 'pseudo': 'ocr_pseudo_unreviewed'}[check['meta']['gt']],
               studio={'source': 'results', 'gt': check['meta']['gt'], 'real_data': check['meta']['real_data']})
    if check['meta']['gt'] in ('reviewed', 'exact'):
        cfg['filters'] = {s: {'min_confidence': 0, 'min_length': 1, 'max_length': 100} for s in ('train', 'benchmark')}
    write(out / 'config.json', cfg)
    write(out / 'import_set.json', {'source': 'results', 'gt': check['meta']['gt'], 'real_data': check['meta']['real_data'],
                                  'label_format': 'docgen-labels/1', 'fingerprint': check['fingerprint']})
    sys.path.insert(0, str(ROOT / 'ocr'))
    from bank_ocr.pipeline import prepare
    prepare(str(out / 'config.json'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--request', required=True)
    req = read(Path(ap.parse_args().request))
    check = read(Path(req['check']))
    # 처리 설정은 검사 때 고정한 것을 사용한다. 원본 내용은 복사 시 해시로 재확인한다.
    if not check.get('ok'):
        raise ValueError('유효한 검사 결과가 아닙니다')
    out = Path(req['out'])
    if req['track'] == 'bank':
        build_bank(check, out, req['tasks'], req['split'])
    else:
        build_ocr(check, out, req['split'])


if __name__ == '__main__':
    main()
