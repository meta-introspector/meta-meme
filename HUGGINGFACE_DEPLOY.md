# HuggingFace Spaces Deployment

## Public URL

🤗 **Deploy to HuggingFace Spaces**: https://huggingface.co/spaces

## Expected Public URL

```
https://huggingface.co/spaces/meta-introspector/meta-meme
```

## Deployment Methods

### Method 1: Web UI (Easiest)

1. Go to https://huggingface.co/new-space
2. Fill in:
   - **Space name**: `meta-meme`
   - **License**: MIT
   - **SDK**: Streamlit
   - **Hardware**: CPU (free tier)
3. Click "Create Space"
4. Upload files:
   - `streamlit_app.py`
   - `requirements.txt`
   - `README_HF.md` (rename to `README.md`)
   - `.huggingface/config.yaml`
5. Space will auto-deploy

### Method 2: Git Push

```bash
# Clone your new space
git clone https://huggingface.co/spaces/meta-introspector/meta-meme
cd meta-meme

# Copy files from meta-meme repo
cp /path/to/meta-meme/streamlit_app.py .
cp /path/to/meta-meme/requirements.txt .
cp /path/to/meta-meme/README_HF.md README.md
mkdir -p .huggingface
cp /path/to/meta-meme/.huggingface/config.yaml .huggingface/

# Optional: copy shareable_url.txt for RDFa tab
cp /path/to/meta-meme/shareable_url.txt .

# Commit and push
git add .
git commit -m "Initial deployment: JWT+RDFa Streamlit dashboard"
git push
```

### Method 3: GitHub Sync

1. Create Space on HuggingFace
2. Go to Space Settings → "Repository"
3. Enable "Sync with GitHub"
4. Select: `meta-introspector/meta-meme` branch `unified-memes`
5. Auto-syncs on every push

## Required Files

- ✅ `streamlit_app.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `README_HF.md` - Space description (rename to README.md)
- ✅ `.huggingface/config.yaml` - Space configuration

## Configuration

```yaml
title: Meta-Meme Formally Verified AI Muses
emoji: 🎭
colorFrom: purple
colorTo: blue
sdk: streamlit
sdk_version: "1.30.0"
app_file: streamlit_app.py
pinned: false
license: mit
```

## Public URLs

After deployment, your space will be available at:

- **Main**: https://huggingface.co/spaces/meta-introspector/meta-meme
- **Direct App**: https://meta-introspector-meta-meme.hf.space

## Features Deployed

- 🎭 9 AI Muses task assignment
- 🔐 ZK Witness + HME visualization  
- 🔗 RDFa/Turtle export
- 📊 79 verified proofs
- 🔢 8! eigenvector convergence
