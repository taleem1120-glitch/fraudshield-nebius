FraudShield AI — Evidence-First Agent
An independent, open-source research prototype submitted to the Nebius × NVIDIA Global AI Hackathon 2026, Best Apps and Agents track.
Demonstration
App: https://fraudshield-nebius.streamlit.app/
Repository: https://github.com/taleem1120-glitch/fraudshield-nebius
Demo video: https://youtu.be/4nViZzGMRuU
What works today
The Streamlit app presents three synthetic investigation scenarios (SYN-001, SYN-002, SYN-003). The Python rules engine generates transparent risk scores and triggered controls. SHA-256 digests are computed over canonically serialized synthetic cases. Downloadable JSON audit reports contain assessments, limitations, and a report hash. These hashes detect modifications but are not digital signatures or a complete chain of custody.
NVIDIA / Nebius integration status
The code includes a configurable OpenAI-compatible chat-completions request to Nebius Token Factory, intended for an NVIDIA Nemotron model named in NEBIUS_MODEL. It constructs evidence-grounded prompts asking for indicators, benign alternatives, investigator checks, and decision limitations. The app marks a call verified only after receiving and parsing a nonempty response. Unverified model output is excluded from audit reports.
Live NVIDIA Nemotron inference through Nebius has not been verified. Billing activation currently requires a payment card, and promotional-credit access remains unresolved (support ticket AISTUDIOSUP-2540). No successful Nebius runtime call, latency result, GPU deployment, measured output quality, or production readiness is claimed. The deterministic screening and audit report run without a Nebius API key.
The integration is implemented in code but remains untested at runtime; this may mean the hackathon's hosting/inference requirement is not met.
Install and run
Python 3.10+ is recommended.
git clone https://github.com/taleem1120-glitch/fraudshield-nebius.git
cd fraudshield-nebius
python -m pip install -r requirements.txt
streamlit run app.py
Only if official API access is available, configure the following server-side Streamlit secrets (or environment variables):
NEBIUS_API_KEY = "YOUR_PRIVATE_KEY"
NEBIUS_MODEL = "YOUR_VERIFIED_NVIDIA_MODEL_ID_ON_NEBIUS"
NEBIUS_BASE_URL = "https://api.tokenfactory.us-central1.nebius.com/v1/chat/completions"
Check the active model catalog for a valid model ID. Never commit real credentials or expose them in a screen recording.
Tests
python -m pip install pytest
pytest -q
Included unit tests cover stable hashes, ordering of synthetic scores, isolation of unverified AI output, and the prompt's evidence contents. Passing these tests does not demonstrate a live Nebius connection.
Limitations
All test cases are synthetic. Risk scores are heuristics rather than calibrated fraud probabilities. This prototype does not allege wrongdoing by any person or transaction and is not ready for production fraud decisions. Human oversight is required.
License
MIT — see LICENSE.
