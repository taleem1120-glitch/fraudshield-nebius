from core import CASES, sha256, assess, make_report, prompt_payload

def test_repeatable_hash():
    assert sha256({'a':1,'b':2}) == sha256({'b':2,'a':1})
def test_risk_ordering():
    assert assess(CASES[1])['score'] > assess(CASES[2])['score'] > assess(CASES[0])['score']
def test_no_unverified_ai_in_report():
    a=assess(CASES[0]); r=make_report(CASES[0],a,'claimed live response',False)
    assert r['ai_review'] is None and r['ai_provider_verified'] is False
def test_prompt_has_evidence():
    a=assess(CASES[1]); p=prompt_payload(CASES[1],a)
    assert p['record']['id']=='SYN-002' and p['rule_based_assessment']['sha256']==a['sha256']
