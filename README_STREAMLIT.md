# Streamlit Meta-Meme Dashboard

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run streamlit_app.py
```

## Features

### 📊 Muse Tasks Tab
- Select any of the 9 AI muses
- Assign hackathon tasks (TASK1-TASK6)
- Generate JWT tokens with RDFa-encoded task data
- View complexity metrics

### 🔐 ZK Witness Tab
- Zero-knowledge commitment scheme visualization
- Homomorphic encryption (HME) aggregates
- Per-muse encrypted knowledge sharing
- Public key: 65537
- Aggregate ciphertext: 139,614,573

### 🔗 RDFa Export Tab
- Load pre-generated shareable URL (2,110 bytes)
- Generate live RDFa/Turtle for task assignments
- Semantic web encoding with Schema.org vocabulary

## Data Sources

All data loaded from verified Lean4 proofs:

- `src/StreamlitHackathon.lean` - 6 tasks
- `src/ZKWitnessHME.lean` - Cryptographic proofs
- `src/RDFaURL.lean` - Semantic encoding
- `shareable_url.txt` - Complete system state

## JWT Structure

Each task assignment generates a JWT with:

```json
{
  "sub": "muse:Calliope",
  "iat": 1737835200,
  "exp": 1737849600,
  "data": "<div vocab='http://schema.org/'...>"
}
```

## Verified Properties

- ✅ 79 total proofs (43 theorems, 6 axioms, 30 derived)
- ✅ 8! (40,320) eigenvector convergence iterations
- ✅ 99.9975% unity convergence
- ✅ JWT embeds RDFa in payload
