"""실제 라벨 묶음의 구비·직접 추출/비교·계산 문항. 이미지 변조와 합성 고객 생성은 하지 않는다."""
import random

from docgen.bench import processing as P
from docgen.bench.prompts import P_DOC_CHECK, P_REVIEW
from docgen.bench.rules import Bundle, RULES, r_doc_valid


def build_bundles(check, documents, tasks):
    items, records = [], []
    for source in check['bundles']:
        sid, bid = source['scenario'], source['bundle_id']
        scenario = check['scenarios'][sid]
        docs = {documents[did]['doc_id']: documents[did] for did in source['documents']}
        conf = P.validate(scenario.get('processing'), scenario['docs'])
        meta = {'scenario': sid, 'task_name': scenario['name'], 'bundle': bid, 'customer': source.get('customer') or bid,
                'source': 'results', 'gt': check['meta']['gt']}
        record = {'bundle_id': bid, 'scenario': sid, 'task_name': scenario['name'], 'customer': meta['customer'],
                  'customer_seed': None, 'source': 'labels', 'plan': None, 'variants': [], 'doc_check': None,
                  'processing': conf, 'processing_results': [], 'items': [],
                  'docs': [{k: d[k] for k in ('doc_id', 'document_id', 'name', 'images', 'condition', 'fields')} for d in docs.values()]}
        def emit(task, suffix, dids, prompt, answer, evaluation, first_page=False):
            if task not in tasks:
                return
            images = [im for did in dict.fromkeys(dids) for im in (docs[did]['images'][:1] if first_page else docs[did]['images'])]
            item = {'id': f'{task}/{bid}/{suffix}', 'task': task, 'images': images, 'prompt': prompt,
                    'answer': answer, 'eval': evaluation, 'meta': meta}
            items.append(item)
            record['items'].append(item['id'])
        required = scenario['docs']
        if conf['doc_check'] and 'doc_check' in tasks:
            if 'not_customer' not in source:
                record['processing_results'].append({'id': 'doc_check', 'status': 'skipped', 'reason': '타인 서류 목록 not_customer 미확인'})
            else:
                from docgen.registry import load_all

                reg = load_all()
                foreign = {documents[x]['doc_id'] for x in source['not_customer']}
                missing = [did for did in required if did not in docs or did in foreign]
                extra = [did for did in docs if did not in required]
                name = lambda did: docs[did]['name'] if did in docs else reg[did].name
                answer = {'missing': [name(did) for did in missing], 'not_required': [name(did) for did in extra],
                          'not_customer': [name(did) for did in docs if did in foreign]}
                record['doc_check'] = {'missing': missing, 'not_required': extra, 'not_customer': sorted(foreign)}
                record['processing_results'].append({'id': 'doc_check', 'status': 'ready', 'answer': answer})
                prompt = P_DOC_CHECK.format(customer=meta['customer'], task=scenario['name'],
                                            required='\n'.join(f'{i + 1}. {name(did)}' for i, did in enumerate(required)))
                emit('doc_check', 'submitted', list(docs), prompt, answer,
                     {'required': [name(did) for did in required], 'names': [d['name'] for d in docs.values()]}, True)
        for result in P.execute(conf, docs):
            record['processing_results'].append({k: v for k, v in result.items() if k != 'item'})
            if item := result.get('item'):
                prompt = item.get('prompt') or P_REVIEW.format(task=scenario['name'], pages=sum(len(docs[d]['images']) for d in item['docs']), question=item['question'])
                emit(item['task'], 'operation_' + result['id'], item['docs'], prompt, item['answer'], item['eval'])
        if 'review' in tasks and conf['review']:
            class ObservedBundle(Bundle):
                def __init__(self):
                    super().__init__(sid, docs)
                    self.missing_numbers = False
                def num(self, doc, key):
                    value = super().num(doc, key)
                    if value is None:
                        self.missing_numbers = True
                    return value
            for rid, fn in {**RULES, 'doc_valid': r_doc_valid}.items():
                if not P.selected(conf, 'rule_ids', rid):
                    continue
                observed = ObservedBundle()
                q = fn(observed, random.Random(f'labeled:{bid}:{rid}'))
                if q is None or observed.missing_numbers:
                    record['processing_results'].append({'id': rid, 'status': 'skipped', 'reason': '계산에 필요한 라벨이 없습니다'})
                    continue
                prompt = P_REVIEW.format(task=scenario['name'], pages=sum(len(docs[d]['images']) for d in q['docs']), question=q['question'])
                emit('review', rid, q['docs'], prompt, q['answer'], {'answer_type': q['answer_type'], 'tol': q['tol'], **q.get('info', {})})
                record['processing_results'].append({'id': rid, 'status': 'ready', 'answer': q['answer']})
        if conf['cross_check']:
            record['processing_results'].append({'id': 'cross_check', 'status': 'skipped',
                'reason': '합성 변조 사례는 실서류에 적용하지 않습니다. ③의 직접 필드 비교 작업으로 실제 라벨을 비교하세요'})
        records.append(record)
    return items, records
