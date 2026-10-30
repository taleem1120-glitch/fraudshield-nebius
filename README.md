# FraudShield AI — Evidence-First Agent

An independent open-source research prototype submitted to the **Nebius × NVIDIA Global AI Hackathon 2026** — Best Apps and Agents track.

## Live Demo

- **Application:** https://fraudshield-nebius.streamlit.app/
- **Source Code:** https://github.com/taleem1120-glitch/fraudshield-nebius
- **Demo Video:** https://youtu.be/4nViZzGMRuU

## Project Overview

FraudShield AI is an evidence-first fraud-risk triage prototype designed to demonstrate explainable screening, evidence integrity checks, and structured audit reporting.

The application uses three fully synthetic investigation scenarios: SYN-001, SYN-002, and SYN-003.

## Key Features

- Explainable deterministic fraud-risk scoring.
- Transparent detection rules and triggered indicators.
- SHA-256 fingerprints over canonicalized case records.
- Downloadable JSON audit reports with content hashes.
- Evidence-grounded prompt construction for NVIDIA Nemotron.
- Human oversight and explicit uncertainty handling.

## NVIDIA Nemotron and Nebius Integration

The project implements a configurable chat-completions API integration intended for NVIDIA Nemotron through Nebius Token Factory.

The AI review prompt requests:

1. Evidence-supported risk indicators.
2. Possible benign explanations.
3. Missing evidence and recommended investigator checks.
4. Explicit limitations on conclusions.

**Integration status:** Live Nemotron inference through Nebius has not yet been verified because account billing activation remains blocked by payment-card requirements. Support ticket: AISTUDIOSUP-2540.

No successful Nebius inference call, provider benchmark, GPU deployment, or production performance is claimed.

The deterministic screening engine and JSON audit reporting operate independently of the AI provider.

## Installation

Requirements: Python 3.10 or newer.

```bash
git clone https://github.com/taleem1120-glitch/fraudshield-nebius.git
cd fraudshield-nebius
python -m pip install -r requirements.txt
streamlit run app.py
```

## Optional Nebius Configuration

Only after officially obtaining API access, configure these server-side Streamlit secrets:

```toml
NEBIUS_API_KEY = "YOUR_PRIVATE_API_KEY"
NEBIUS_MODEL = "YOUR_VERIFIED_NVIDIA_MODEL_ID"
NEBIUS_BASE_URL = "https://api.tokenfactory.us-central1.nebius.com/v1/chat/completions"
```

Never publish a real API key in GitHub or screenshots.

## Testing

```bash
python -m pip install pytest
pytest -q
```

Unit tests cover deterministic hashes, risk ordering, evidence-grounded prompt construction, and isolation of unverified AI output.

Passing these tests does not establish successful live Nebius integration.

## Limitations

- All investigation scenarios are synthetic.
- Risk scores are heuristic, not calibrated fraud probabilities.
- SHA-256 hashes are not digital signatures or complete chain-of-custody guarantees.
- No allegation of wrongdoing is made.
- Human review is required.
- This prototype is not production-ready.

## License

MIT License. See [LICENSE](LICENSE).
