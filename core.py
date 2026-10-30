"""Pure, deterministic, synthetic fraud evidence model. No customer data."""
import hashlib
import json
from datetime import datetime, timezone

CASES = [
    {'id':'SYN-001','amount':120,'velocity_1h':1,'new_device':False,'cross_border':False,'linked_accounts':0,'prior_disputes':0},
    {'id':'SYN-002','amount':9800,'velocity_1h':9,'new_device':True,'cross_border':True,'linked_accounts':5,'prior_disputes':2},
    {'id':'SYN-003','amount':600,'velocity_1h':4,'new_device':True,'cross_border':False,'linked_accounts':2,'prior_disputes':0},
]

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def sha256(obj):
    return hashlib.sha256(canonical(obj).encode('utf-8')).hexdigest()

def assess(tx):
    rules=[('Large value',25,tx['amount']>=5000),('High velocity',25,tx['velocity_1h']>=6),('Moderate velocity',12,3<=tx['velocity_1h']<6),('New device',16,tx['new_device']),('Cross-border',12,tx['cross_border']),('Linked account cluster',12,tx['linked_accounts']>=3),('Prior disputes',10,tx['prior_disputes']>0)]
    hits=[{'rule':name,'points':pts} for name,pts,hit in rules if hit]
    total=min(100,sum(x['points'] for x in hits))
    return {'score':total,'band':'High' if total>=60 else 'Review' if total>=25 else 'Low','hits':hits,'sha256':sha256(tx)}

def make_report(tx,assessment,analysis=None,provider_verified=False):
    record={'schema':'fraudshield-audit-v2','case':tx,'assessment':assessment,'ai_review':analysis if provider_verified else None,'ai_provider_verified':bool(provider_verified),'limitations':['All cases are synthetic','Score is heuristic, not a probability','No allegation or attribution is made'],'generated_utc':datetime.now(timezone.utc).isoformat()}
    record['report_sha256']=sha256(record)
    return record

def prompt_payload(tx,assessment):
    return {'record':tx,'rule_based_assessment':assessment,'instructions':'Return concise sections: indicators, benign alternatives, investigator checks, decision limits. Base statements only on provided synthetic evidence. Do not invent facts or claim fraud.'}
