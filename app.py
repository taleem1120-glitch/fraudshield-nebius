import os, json, hashlib, urllib.request, urllib.error
import streamlit as st

st.set_page_config(page_title='FraudShield AI — Nebius', page_icon='🛡️')
st.title('🛡️ FraudShield AI — Nebius Edition')
st.caption('Synthetic transaction triage and evidence-grounded NVIDIA model explanation')
DATA = [
 {'id':'SYN-001','amount':120,'velocity_1h':1,'new_device':False,'cross_border':False},
 {'id':'SYN-002','amount':9800,'velocity_1h':9,'new_device':True,'cross_border':True},
 {'id':'SYN-003','amount':600,'velocity_1h':4,'new_device':True,'cross_border':False},
]
ix=st.selectbox('Synthetic case',range(len(DATA)),format_func=lambda i:DATA[i]['id'])
tx=DATA[ix]
score=min(100, (25 if tx['amount']>=5000 else 0)+(30 if tx['velocity_1h']>=6 else 12 if tx['velocity_1h']>=3 else 0)+(20 if tx['new_device'] else 0)+(15 if tx['cross_border'] else 0))
hash_=hashlib.sha256(json.dumps(tx,sort_keys=True).encode()).hexdigest()
st.json(tx)
st.metric('Heuristic risk score (not probability)',f'{score}/100')
st.text('Evidence SHA-256: '+hash_)
st.warning('Synthetic demonstration only. No actual customer data, no proof of fraud.')
st.subheader('Live NVIDIA model via Nebius Token Factory')
model=st.text_input('Exact NVIDIA open-source model ID from Nebius catalog', value=os.getenv('NEBIUS_MODEL',''))
key=os.getenv('NEBIUS_API_KEY','')
if not key: st.info('Add NEBIUS_API_KEY in server-side secrets. Never enter it in a public form or commit it.')
if st.button('Analyze with Nebius', disabled=not(key and model)):
 payload={'model':model,'temperature':0.1,'max_tokens':350,'messages':[
  {'role':'system','content':'Analyze only the supplied synthetic record and transparent score. Explain risk, uncertainty and suggested checks. Do not invent evidence.'},
  {'role':'user','content':json.dumps({'transaction':tx,'risk_score':score,'sha256':hash_})}
 ]}
 req=urllib.request.Request('https://api.tokenfactory.nebius.com/v1/chat/completions', data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=30) as response: result=json.load(response)
  st.success('Live Nebius inference succeeded')
  st.write(result['choices'][0]['message']['content'])
 except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,KeyError) as e:
  st.error('Nebius call failed; check API access, credit balance, model ID and secret configuration.')
  st.caption(type(e).__name__)
