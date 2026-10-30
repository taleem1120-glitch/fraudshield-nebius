# FraudShield AI — Nebius Edition

Independent prototype for Nebius x NVIDIA Global AI Hackathon 2026. The original PayPal AI FraudShield repository is unchanged.

- Synthetic, deterministic fraud-risk examples.
- SHA-256 fingerprint of each synthetic record.
- Nebius Token Factory chat endpoint integration via the standard OpenAI-compatible API.
- Live provider inference **not yet tested**. A valid NVIDIA open-source model ID available in Nebius, activated credits and a secret API key are required.

Run locally with `pip install -r requirements.txt` and `streamlit run app.py`.

For hosting, set `NEBIUS_API_KEY` and `NEBIUS_MODEL` in the platform's server-side secrets. Never put tokens in GitHub or screenshots.

The heuristic is not a calibrated probability and does not establish fraud.
