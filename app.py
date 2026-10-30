import os
import json
import urllib.request
import urllib.error
import streamlit as st
from core import CASES, assess, make_report, prompt_payload

st.set_page_config(page_title='FraudShield | Evidence-first AI',page_icon='🛡️',layout='wide')
st.title('🛡️ FraudShield AI — Evidence-First Agent')
st.caption('Nebius × NVIDIA | synthetic investigation lab | deterministic evidence before AI interpretation')
st.info('This is an educational prototype using synthetic data; results are NOT evidence of fraud or calibrated probabilities.')

case=st.selectbox('Choose an investigation scenario',CASES,format_func=lambda x: x['id']+' — '+('High-risk synthetic' if x['id']=='SYN-002' else 'Synthetic test'))
assessment=assess(case)
col1,col2,col3=st.columns(3)
col1.metric('Rule score',str(assessment['score'])+'/100')
col2.metric('Triage band',assessment['band'])
col3.metric('Triggered controls',len(assessment['hits']))
with st.expander('Stage 1 · Evidence intake and provenance',expanded=True):
    st.json(case)
    st.code(assessment['sha256'],language=None)
    st.caption('SHA-256 over canonicalized input; repeatable on same payload. Not blockchain evidence.')
with st.expander('Stage 2 · Explainable deterministic screening',expanded=True):
    st.dataframe(assessment['hits'],use_container_width=True,hide_index=True)
    st.caption('Human review required. A score is not a fraud probability.')

st.subheader('Stage 3 · NVIDIA Nemotron evidence review')

def secret(name,default=''):
    try: return st.secrets.get(name,os.getenv(name,default))
    except Exception: return os.getenv(name,default)

key=secret('NEBIUS_API_KEY')
default_model=secret('NEBIUS_MODEL','nvidia/nemotron-3-super-120b-a12b')
model=st.text_input('Nebius catalog model ID',value=default_model)
endpoint=secret('NEBIUS_BASE_URL','https://api.tokenfactory.us-central1.nebius.com/v1/chat/completions')
if not key:
    st.warning('Live Nemotron inference is NOT active: add NEBIUS_API_KEY under Streamlit App settings → Secrets. Never expose keys in GitHub or screenshots.')
else:
    st.success('Server-side API secret detected. A successful provider response is still required to confirm live integration.')

if 'ai_result' not in st.session_state or st.session_state.get('last_case')!=case['id']:
    st.session_state.ai_result=None
    st.session_state.live_verified=False
    st.session_state.last_case=case['id']

if st.button('Run live evidence-grounded Nemotron review',disabled=not bool(key and model)):
    payload={'model':model,'temperature':0.1,'max_tokens':650,'messages':[
      {'role':'system','content':'You are a forensic triage assistant. Only use supplied synthetic evidence. Distinguish indicators from proof. Include benign explanations, missing data and next steps. Do not invent external findings.'},
      {'role':'user','content':json.dumps(prompt_payload(case,assessment))}
    ]}
    req=urllib.request.Request(endpoint,data=json.dumps(payload).encode('utf-8'),headers={'Content-Type':'application/json','Authorization':'Bearer '+key},method='POST')
    try:
        with st.spinner('Awaiting Nebius NVIDIA response...'):
            with urllib.request.urlopen(req,timeout=35) as r: res=json.load(r)
        content=res['choices'][0]['message']['content']
        if not content: raise ValueError('empty response')
        st.session_state.ai_result=content
        st.session_state.live_verified=True
        st.success('Live Nebius response received and parsed')
    except (urllib.error.URLError,urllib.error.HTTPError,TimeoutError,KeyError,ValueError) as e:
        st.session_state.ai_result=None
        st.session_state.live_verified=False
        st.error('Provider call failed. Check billing, credits, correct model ID, API key and endpoint.')
        st.caption(type(e).__name__)
if st.session_state.ai_result:
    st.markdown(st.session_state.ai_result)
else:
    st.caption('No live model response recorded. The synthetic rules and audit report work offline; this alone does not satisfy hackathon runtime requirements.')

st.subheader('Stage 4 · Signed-by-hash audit export')
report=make_report(case,assessment,st.session_state.ai_result,st.session_state.live_verified)
st.download_button('Download reproducible JSON audit',data=json.dumps(report,indent=2),file_name=f"{case['id']}-audit.json",mime='application/json')
st.caption('Report hash detects changes to report content; it is not a cryptographic digital signature or chain of custody.')
