"""Deterministic, offline evidence metadata audit. No market validation is implied."""
import json
from pathlib import Path
from urllib.parse import urlparse

SUPPORTED = {'user_need','competitor','differentiation','distribution','pricing','feasibility'}
KINDS = {'primary','user_report','independent','founder_claim','investor_claim','analyst_inference'}

def evaluate(case: dict) -> dict:
    entries=case.get('evidence', [])
    errors=[]; ids=set(); good=[]
    for e in entries:
        eid=e.get('id')
        if not eid or eid in ids: errors.append(f'missing or duplicate evidence id: {eid}')
        ids.add(eid)
        p=urlparse(e.get('url',''))
        if p.scheme not in {'http','https'} or not p.netloc: errors.append(f'invalid source URL for {eid}')
        if e.get('type') not in KINDS: errors.append(f'invalid evidence type for {eid}')
        if e.get('dimension') not in SUPPORTED: errors.append(f'invalid dimension for {eid}')
        if e.get('stance') not in {'supports','contradicts','context'}: errors.append(f'invalid stance for {eid}')
        if not e.get('observed_at'): errors.append(f'missing observed_at for {eid}')
        if not e.get('claim'): errors.append(f'missing claim for {eid}')
        if not any(x.endswith(f' for {eid}') for x in errors): good.append(e)
    independent=[e for e in good if e['type'] in {'user_report','independent','primary'}]
    need=[e for e in independent if e['dimension']=='user_need' and e['stance']=='supports']
    counter=[e for e in good if e['stance']=='contradicts']
    alternatives=[e for e in good if e['dimension']=='competitor']
    funding=[e for e in good if e['type']=='investor_claim']
    flags=[]
    if not need: flags.append('NO_INDEPENDENT_USER_NEED_EVIDENCE')
    if not alternatives: flags.append('COMPETITOR_COVERAGE_MISSING')
    if not counter: flags.append('NO_COUNTEREVIDENCE_RECORDED')
    if funding and not need: flags.append('INVESTOR_SIGNAL_NOT_DEMAND_VALIDATION')
    status='invalid_input' if errors else ('evidence_review_ready' if need and alternatives and counter else 'insufficient_evidence')
    return {'case_id':case.get('id'),'status':status,'evidence_count':len(good),
            'supporting_user_need_evidence_ids':[e['id'] for e in need],
            'competitor_evidence_ids':[e['id'] for e in alternatives],
            'counterevidence_ids':[e['id'] for e in counter],
            'risk_flags':flags,'input_errors':errors,
            'limitations':['Checks metadata only, not whether URLs or claims are true.',
                           'evidence_review_ready is not proof of market demand or product-market fit.',
                           'No web retrieval or LLM inference is performed.']}
def evaluate_file(path):
    return evaluate(json.loads(Path(path).read_text(encoding='utf-8')))
