"""공식 HTML 추가가 실제 출처·생성값·Studio 분류를 유지하는지 확인한다."""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

import pytest

from docgen.entities import make_profile
from docgen.htmlform import check, load_form
from docgen.preview import source_files
from docgen.registry import load_all
from docgen.render import render
from docgen.sources import lookup_profile

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = json.loads((ROOT/'manual/official_html_sources.json').read_text(encoding='utf8'))['forms']


@pytest.mark.parametrize('entry', ENTRIES, ids=lambda e: e['id'])
def test_official_source_and_render(entry):
    assert urlsplit(entry['url']).scheme == 'https'
    assert urlsplit(entry['url']).hostname in {'www.law.go.kr', 'image.kebhana.com', 'biz.kebhana.com'}
    assert hashlib.sha256((ROOT/entry['source_file']).read_bytes()).hexdigest() == entry['sha256']
    assert entry['online_verification']['matches_local']
    spec = load_all()[entry['id']]
    assert spec.template == '@form/'+entry['id']
    assert '공식대조' not in spec.name  # 출처 배지는 문서 분류 정답에 섞지 않는다.
    for seed in [3, 17]:
        p = make_profile(seed, bank='하나은행')
        html, raw, data = render(spec, p, seed)
        assert raw
        assert '합성 데이터 · 견본' in html
        assert 'class="bg"' not in html
        assert 'class="printed"' in html
        assert not check(load_form(entry['id']), raw, data)
        for field in entry.get('fields', {}).values():
            if field['source'].startswith('profile.'):
                assert lookup_profile(p, field['source']) is not None, field


def test_hana_clone_tracks_parent_layout_and_common_templates():
    paths = {p.name for p in source_files('hana_official_003')}
    assert '003.json' in paths
    assert '_official_base.html.j2' in paths
    assert '_official_values.html.j2' in paths


def test_studio_shows_source_separately_from_document_name():
    from studio.catalog import form_detail

    d = form_detail('gov_income')
    assert d['name'] == '소득금액증명'
    assert d['official_source']['publisher']
    assert d['official_source']['online_verification']['matches_local']


def test_hana_account_opening_uses_birth_in_birth_cell():
    p = make_profile(3)
    _, fields, _ = render(load_all()['hana_official_003'], p, 3)
    values = {f['key']:f['value'] for f in fields}
    assert values['official.name'] == p.person.name
    assert values['official.birth'] == p.person.birth.strftime('%Y.%m.%d')
    assert 'official.rrn' not in values


def test_official_compiler_refuses_unrequested_overwrite():
    from docgen.scripts.build_official_html import compile_form

    with pytest.raises(FileExistsError, match='편집한 서식 보호'):
        compile_form(ENTRIES[0])
