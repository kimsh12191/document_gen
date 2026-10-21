"""④ 가져오기 › 라벨 있는 데이터 API: 표준 라벨 v1 폴더 검사 → 확인 → 생성 작업·자동 등록 (DESIGN.md 9.7.2).

검사·변환은 studio/labeled_data.py, 화면은 static/js/labeled-import.js, 규격은 studio/LABEL_FORMAT.md.

  POST /api/labeled-imports/check {path}                   폴더 검사. 통과하면 token (검사 결과는 <workspace_dir>/labeled_imports/<token>/check.json)
  GET  /api/labeled-imports/{token}/image?doc=&page=       검사한 문서의 쪽 그림 (정답 미리보기)
  POST /api/labeled-imports/{token}/build {name, track: bank|ocr, split: test|train, tasks, confirmed}
                                                           원본이 검사 때와 같은지 다시 확인하고 python -m studio.labeled_data 작업 → ⑥ 자동 등록
"""
import re
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import labeled_data as L
from .build_registration import register_output
from .importer import _slug
from .jobs import python


def make_router(reg, jobs, guard, cfg):
    r = APIRouter()
    checks = reg.ws / 'labeled_imports'

    def checked(token):
        if not re.fullmatch(r'[0-9a-f]{32}', token):
            raise HTTPException(404, '검사 결과가 없습니다')
        path = checks / token / 'check.json'
        if not path.is_file():
            raise HTTPException(404, '검사 결과가 없습니다. 다시 검사하세요')
        return path, L.read(path)

    class CheckReq(BaseModel):
        path: str

    @r.post('/api/labeled-imports/check')
    def check(req: CheckReq):
        report = guard(L.inspect, req.path, cfg.get('import_dir'))
        if report['ok']:
            token = uuid.uuid4().hex
            L.write(checks / token / 'check.json', report)
            report = {**report, 'token': token}
        # 파일 해시·시나리오 내부 정보는 저장만 한다. 화면에는 필요한 라벨·검사 요약만 보낸다.
        return {k: v for k, v in report.items() if k not in ('files', 'scenarios', 'fingerprint')}

    @r.get('/api/labeled-imports/{token}/image')
    def image(token: str, doc: str, page: int = 0):
        _, report = checked(token)
        d = next((d['label'] for d in report['documents'] if d['label']['id'] == doc), None)
        if d is None or not 0 <= page < len(d['images']):
            raise HTTPException(404, '검사한 문서의 쪽이 없습니다')
        path = guard(L.contained, Path(report['source']), d['images'][page])
        return FileResponse(path)

    class BuildReq(BaseModel):
        name: str
        split: str = 'test'
        tasks: list[str] = ['classify', 'kie', 'marks', 'ocr_field', 'doc_check', 'review']   # 'ocr' = 쪽 OCR 8과제
        confirmed: bool = False

    @r.post('/api/labeled-imports/{token}/build')
    def build(token: str, req: BuildReq):
        path, report = checked(token)
        if not req.confirmed:
            raise HTTPException(400, '라벨과 문서 연결을 확인한 뒤 등록하세요')
        if req.split not in ('test', 'train'):
            raise HTTPException(400, '용도가 잘못되었습니다')
        if not req.tasks or any(t not in (*L.BANK_TASKS, L.OCR) for t in req.tasks):
            raise HTTPException(400, '지원하는 과제를 하나 이상 고르세요')
        ocr = L.OCR in req.tasks
        if ocr and not report['summary']['full_ocr']:
            raise HTTPException(400, '쪽 OCR 과제는 모든 쪽의 OCR 정답과 ocr_scope:full_page가 필요합니다')
        if ocr and req.split == 'train' and report['summary']['documents'] < 2:
            raise HTTPException(400, 'OCR 학습용은 문서가 2건 이상 필요합니다')
        if not req.name.strip():
            raise HTTPException(400, '데이터셋 이름을 입력하세요')
        current = guard(L.inspect, report['source'], cfg.get('import_dir'))
        if not current['ok'] or current.get('fingerprint') != report['fingerprint']:
            raise HTTPException(409, '검사 후 원본 파일이 바뀌었습니다. 다시 검사하세요')
        out = reg.ws / 'datasets' / _slug(req.name)
        try:
            out.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            raise HTTPException(400, '같은 이름의 결과 폴더가 있습니다. 다른 이름을 입력하세요')
        request = checks / token / (uuid.uuid4().hex + '.json')
        L.write(request, {'check': str(path.resolve()), 'out': str(out.resolve()),
                          'split': req.split, 'tasks': list(dict.fromkeys(req.tasks))})
        bank = any(t in L.BANK_TASKS for t in req.tasks)
        spec = {'path': str(out.resolve()), 'name': _slug(req.name),
                'meta': {'source': 'results', 'gt': report['meta']['gt'], 'real_data': report['meta']['real_data'],
                         'dataset_json': 'dataset.json' if bank else 'ocr/import_set.json',
                         'purpose': f'표준 라벨 가져오기: {report["meta"]["name"]}'}}
        job = jobs.start('build_tasks', f'라벨 데이터 가져오기: {req.name}',
                         [python(), '-m', 'studio.labeled_data', '--request', str(request.resolve())],
                         lambda job: register_output(reg, spec), {'dataset': spec, 'label_import': token})
        return {'job': job['id'], 'name': _slug(req.name)}

    return r
