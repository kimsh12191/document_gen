"""표준 라벨 가져오기: 잘못된 GT/경로 차단, 원본 보존, 실제 Q/A·등록·OCR 재사용 검증."""
import asyncio
import copy
import json
import time
from pathlib import Path

import pytest
from fastapi import FastAPI, HTTPException
from PIL import Image

from docgen.ocr_export import item, page_document
from studio import labeled_data as L
from studio.api_labels import make_router
from studio.datasets import Registry, items
from studio.jobs import Jobs


@pytest.fixture
def source(tmp_path):
    root = tmp_path / 'input'
    L.write(root / 'meta.json', {'format': 'docgen-labels/1', 'name': 'labeled-test', 'real_data': True, 'gt': 'reviewed'})
    (root / 'images').mkdir()
    Image.new('RGB', (600, 800), 'white').save(root / 'images/id.png')
    fields = [
        {'key': 'name', 'label': '성명', 'type': 'text', 'value': '홍길동', 'page': 0, 'bbox': [60, 80, 180, 120]},
        {'key': 'issue_date', 'label': '발급일', 'type': 'date', 'value': '2026.10.20', 'page': 0, 'bbox': [60, 160, 240, 200]},
        {'key': 'seal.issuer', 'label': '직인', 'type': 'seal', 'value': '발급기관인', 'present': True, 'page': 0, 'bbox': [400, 600, 500, 700]},
    ]
    L.write(root / 'labels/id.json', {'id': 'id', 'doc_type': 'resident_id_card', 'doc_name': '주민등록증',
                                     'images': ['images/id.png'], 'pages': [{'width': 600, 'height': 800}], 'fields': fields})
    return root


def change(root, fn):
    p = root / 'labels/id.json'
    d = L.read(p)
    fn(d)
    L.write(p, d)


def out_dir(tmp_path, name='out'):
    out = tmp_path / name
    out.mkdir()
    return out


def test_valid_and_actual_example(source):
    c = L.inspect(str(source))
    assert c['ok'] and c['summary']['fields'] == 3 and not c['summary']['full_ocr']
    assert L.inspect(str(L.SCHEMAS / 'example'))['ok']


@pytest.mark.parametrize('mutation,location', [
    (lambda d: d['fields'][0].update(page=1), '.page'),
    (lambda d: d['fields'][0].update(bbox=[0, 0, 700, 10]), '.bbox'),
    (lambda d: d['fields'][0].update(bbox=[10, 20, 5, 40]), '.bbox'),
    (lambda d: d['fields'][0].update(value=123), '.value'),
    (lambda d: d['fields'][0].update(type='bad'), '.type'),
    (lambda d: d['fields'][0].update(page=True), '.page'),
    (lambda d: d['fields'][0].pop('page'), '.page'),
    (lambda d: d['fields'].append(copy.deepcopy(d['fields'][0])), '.key'),
    (lambda d: d['images'].__setitem__(0, '../outside.png'), '.images'),
    (lambda d: d['pages'][0].update(width=601), '.images'),
    (lambda d: d.update(id='mismatch'), '.id'),
    (lambda d: d.update(doc_type='unregistered'), '.doc_type'),
    (lambda d: d['fields'][2].pop('present'), '.present'),
])
def test_invalid_labels_aggregate_errors(source, mutation, location):
    change(source, mutation)
    c = L.inspect(str(source))
    assert not c['ok']
    assert any(location in e['path'] for e in c['errors']), c['errors']


def test_import_root_and_symlink_escape(source, tmp_path):
    assert not L.inspect(str(source), str(tmp_path / 'other'))['ok']
    assert L.inspect(str(source), str(tmp_path))['ok']
    outside = tmp_path / 'outside.json'
    outside.write_text('{}')
    with pytest.raises(ValueError):
        L.contained(source, '../outside.json')


def test_bundle_reference_and_identity_not_guessed(source):
    bf = source / 'bundles.jsonl'
    bf.write_text(json.dumps({'bundle_id': 'b', 'scenario': 'jeonse_loan', 'documents': ['missing']}))
    assert not L.inspect(str(source))['ok']
    bf.write_text(json.dumps({'bundle_id': 'b', 'scenario': 'jeonse_loan', 'documents': ['id']}))
    check = L.inspect(str(source))
    assert check['ok'] and any('not_customer' in w['message'] for w in check['warnings'])


def test_bank_conversion_preserves_gt_pixel_coordinates_and_no_fullpage_guess(source, tmp_path):
    before = {p.relative_to(source): p.read_bytes() for p in source.rglob('*') if p.is_file()}
    out = out_dir(tmp_path)
    L.build_bank(L.inspect(str(source)), out, list(L.BANK_TASKS), 'train')
    reg = Registry(tmp_path / 'ws')
    ds = reg.register(str(out))
    all_items = items(ds)
    assert ds['real_data'] and ds['gt'] == 'reviewed' and ds['source'] == 'results'
    assert 'ocr_page' not in all_items  # 값 칸을 쪽 전체 정답으로 취급하지 않는다.
    answer = all_items['kie'][0]['answer']
    assert next(a for a in answer if a['key'] == 'name') == {'key': 'name', 'value': '홍길동', 'bbox_2d': [100, 100, 300, 150], 'page': 1}
    assert all_items['marks'][0]['answer'][0]['value'] is True
    assert (out / 'swift/all.jsonl').is_file()
    assert before == {p.relative_to(source): p.read_bytes() for p in source.rglob('*') if p.is_file()}
    assert all((out / path).is_file() for records in all_items.values() for r in records for path in r['images'])


def test_value_only_and_null_fields_do_not_invent_boxes(source, tmp_path):
    def mutate(d):
        d['fields'][0].pop('bbox'); d['fields'][0].pop('page')
        d['fields'][1]['value'] = None
    change(source, mutate)
    out = out_dir(tmp_path)
    L.build_bank(L.inspect(str(source)), out, ['kie', 'ocr_field'], 'test')
    a = L.read(out / 'meta.json')
    assert 'ocr_field' not in a['counts']
    answers = json.loads((out / 'tasks/kie.jsonl').read_text(encoding='utf-8'))['answer']
    assert answers == [{'key': 'name', 'value': '홍길동'}, {'key': 'issue_date', 'value': None}]


def test_check_then_source_change_is_rejected(source, tmp_path):
    checked = L.inspect(str(source))
    change(source, lambda d: d['fields'][0].update(value='변경'))
    with pytest.raises(ValueError, match='다시 검사'):
        L.snapshot(checked, tmp_path / 'copy')


def test_bundle_doc_check_uses_explicit_membership(source, tmp_path):
    (source / 'bundles.jsonl').write_text(json.dumps({'bundle_id': 'b', 'scenario': 'jeonse_loan', 'documents': ['id'],
                                                    'customer': '홍길동', 'not_customer': ['id']}))
    out = out_dir(tmp_path)
    L.build_bank(L.inspect(str(source)), out, ['doc_check'], 'test')
    a = json.loads((out / 'tasks/doc_check.jsonl').read_text(encoding='utf-8'))['answer']
    assert '주민등록증' in a['missing'] and a['not_customer'] == ['주민등록증']
    b = json.loads((out / 'bundles.jsonl').read_text(encoding='utf-8'))
    from studio.bank_data import profile_view, consistency, bundle_summary
    assert profile_view(b) == [] and consistency(b) == [] and bundle_summary(b)['other'] == 1
    assert b['customer_seed'] is None


def add_ocr(source, full=True):
    meta = L.read(source / 'meta.json')
    meta['ocr_scope'] = 'full_page' if full else 'fields_only_example'
    L.write(source / 'meta.json', meta)
    L.write(source / 'ocr/id.json', page_document([
        item('홍길동', [60, 80, 180, 120], 1, 0), item('서울', [240, 80, 300, 120], 1, 0),
        item('2026.10.20', [60, 160, 240, 200], 1, 1), item('발급기관', [60, 220, 240, 260], 1, 2),
    ], 'id.png'))


def test_ocr_reuses_saved_gold_and_records_reviewed_accuracy(source, tmp_path, monkeypatch):
    add_ocr(source)
    c = L.inspect(str(source))
    assert c['summary']['full_ocr']
    import sys
    sys.path.insert(0, str(L.ROOT / 'training'))
    from bank_ocr import pipeline
    monkeypatch.setattr(pipeline, 'load_callable', lambda *_: pytest.fail('OCR must not be called'))
    out = out_dir(tmp_path)
    L.build_ocr(c, out, 'test')
    done = L.read(out / 'prepared/DONE.json')
    assert done['human_reviewed'] and done['page_counts']['benchmark'] == 1
    ds = Registry(tmp_path / 'ws').register(str(out / 'prepared'))
    assert ds['gt'] == 'reviewed' and ds['real_data']
    assert items(ds)['spotting']


def test_fields_only_ocr_cannot_be_exported_as_full_page(source, tmp_path):
    add_ocr(source, False)
    c = L.inspect(str(source))
    assert c['ok'] and not c['summary']['full_ocr']
    with pytest.raises(ValueError, match='쪽 전체'):
        L.build_ocr(c, out_dir(tmp_path), 'test')


def test_bundle_uses_saved_custom_extract_and_compare_with_real_values(source, tmp_path, monkeypatch):
    from docgen.registry import SCENARIO_PROCESSING

    monkeypatch.setitem(SCENARIO_PROCESSING, 'jeonse_loan', {'doc_check': False, 'cross_check': False, 'review': False,
        'operations': [
            {'id': 'name', 'kind': 'extract', 'left': {'doc': 'resident_id_card', 'key': 'name'}},
            {'id': 'same_date', 'kind': 'compare', 'left': {'doc': 'resident_id_card', 'key': 'issue_date'},
             'right': {'doc': 'resident_id_card', 'key': 'issue_date'}, 'operator': 'equal'},
        ]})
    (source / 'bundles.jsonl').write_text(json.dumps({'bundle_id': 'b', 'scenario': 'jeonse_loan', 'documents': ['id']}))
    out = out_dir(tmp_path)
    L.build_bank(L.inspect(str(source)), out, ['kie', 'review'], 'test')
    rows = [json.loads(s) for s in (out / 'tasks/kie.jsonl').read_text(encoding='utf-8').splitlines()]
    extract = next(r for r in rows if r['id'].endswith('/operation_name'))
    assert extract['answer'][0] == {'key': 'name', 'value': '홍길동', 'bbox_2d': [100, 100, 300, 150], 'page': 1}
    compare = json.loads((out / 'tasks/review.jsonl').read_text(encoding='utf-8'))
    assert compare['answer'] == '예' and compare['eval']['answer_type'] == 'yesno'
    assert compare['images'] == ['input/images/id.png']


def post(app, path, body):
    async def call():
        messages = []
        received = False
        async def receive():
            nonlocal received
            if received:
                await asyncio.sleep(0)
                return {'type': 'http.disconnect'}
            received = True
            return {'type': 'http.request', 'body': json.dumps(body).encode(), 'more_body': False}
        async def send(message):
            messages.append(message)
        await app({'type': 'http', 'asgi': {'version': '3.0'}, 'http_version': '1.1', 'method': 'POST',
                   'scheme': 'http', 'path': path, 'raw_path': path.encode(), 'query_string': b'',
                   'headers': [(b'content-type', b'application/json')], 'server': ('test', 80), 'client': ('test', 1), 'root_path': ''}, receive, send)
        return messages[0]['status'], json.loads(b''.join(m.get('body', b'') for m in messages[1:]))
    return asyncio.run(call())


def test_api_check_confirmation_source_change_and_actual_job_autoregistration(source, tmp_path):
    ws = tmp_path / 'ws'
    reg, jobs = Registry(ws), Jobs(ws, L.ROOT)
    def guard(fn, *args):
        try:
            return fn(*args)
        except ValueError as e:
            raise HTTPException(400, str(e))
    app = FastAPI()
    app.include_router(make_router(reg, jobs, guard, {}))
    status, r = post(app, '/api/labeled-imports/check', {'path': str(source)})
    assert status == 200 and r['ok'] and 'fingerprint' not in r
    token = r['token']
    body = {'name': 'imported', 'track': 'bank', 'tasks': ['kie'], 'confirmed': False}
    assert post(app, f'/api/labeled-imports/{token}/build', body)[0] == 400
    body['confirmed'] = True
    status, created = post(app, f'/api/labeled-imports/{token}/build', body)
    assert status == 200
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        j = jobs.get(created['job'])
        if j['status'] != 'running':
            break
        time.sleep(0.05)
    assert j['status'] == 'done', j
    ds = reg.get(j['result']['dataset'])
    assert ds['gt'] == 'reviewed' and ds['real_data'] and ds['source'] == 'results'
    assert items(ds)['kie'][0]['answer'][0]['value'] == '홍길동'
    change(source, lambda d: d['fields'][0].update(value='변경'))
    body['name'] = 'changed'
    assert post(app, f'/api/labeled-imports/{token}/build', body)[0] == 409
    assert not (ws / 'datasets/changed').exists()
