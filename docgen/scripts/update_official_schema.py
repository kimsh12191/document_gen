"""공식 대조 HTML의 항목만 guide/fields/fields.json에 추가·갱신한다.

기존 서식 항목은 바꾸지 않는다. 문서 전체 재생성은 build_schema.py를 쓴다.
python -m docgen.scripts.update_official_schema [--n 30]
"""
import argparse
import collections
import json
import re
from pathlib import Path

from docgen.entities import make_profile
from docgen.registry import load_all
from docgen.render import render
from docgen.schema import build_fields

ROOT = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--n', type=int, default=30)
    args = ap.parse_args()
    if args.n < 1:
        ap.error('--n은 1 이상')
    manifest = json.loads((ROOT/'docgen/manual/official_html_sources.json').read_text(encoding='utf8'))
    target = ROOT/'guide/fields/fields.json'
    schema = json.loads(target.read_text(encoding='utf8')) if target.exists() else {}
    reg = load_all()
    for entry in manifest['forms']:
        spec = reg[entry['id']]
        stats = {}
        for seed in range(args.n):
            _, raw, _ = render(spec, make_profile(seed), seed)
            seen = set()
            for f in build_fields(raw):
                key = re.sub(r'\.\d+(?=\.|$)', '[]', f['key'])
                st = stats.setdefault(key, {'labels': collections.Counter(), 'types': collections.Counter(),
                                            'n': 0, 'example': None, 'options': []})
                if key not in seen:
                    st['n'] += 1
                    seen.add(key)
                st['labels'][f.get('label')] += 1
                st['types'][f['type']] += 1
                if st['example'] is None and f.get('value') is not None:
                    st['example'] = f['value']
                for option in f.get('options') or []:
                    if option['text'] not in st['options']:
                        st['options'].append(option['text'])
        schema[spec.id] = {'name': spec.name, 'group': spec.group, 'keys': [
            {'key': k, 'label': st['labels'].most_common(1)[0][0], 'type': st['types'].most_common(1)[0][0],
             'fill_rate': round(st['n']/args.n, 2), 'example': st['example'],
             **({'options': st['options']} if st['options'] else {})} for k, st in stats.items()]}
    target.write_text(json.dumps(schema, ensure_ascii=False, indent=1), encoding='utf8')
    print(f'{len(manifest["forms"])}종 항목 갱신, 나머지 항목 보존')


if __name__ == '__main__':
    main()
