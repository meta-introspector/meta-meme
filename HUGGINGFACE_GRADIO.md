# HuggingFace Spaces - Gradio Deployment

## Clone and Deploy

```bash
# Clone the HF Space
git clone https://huggingface.co/spaces/introspector/meta-meme
cd meta-meme

# Copy files from meta-meme repo
cp /mnt/data1/time2/time/2023/07/30/meta-meme/app.py .
cp /mnt/data1/time2/time/2023/07/30/meta-meme/requirements.txt .
cp /mnt/data1/time2/time/2023/07/30/meta-meme/shareable_url.txt .
cp /mnt/data1/time2/time/2023/07/30/meta-meme/shareable_url_compressed.txt .
cp /mnt/data1/time2/time/2023/07/30/meta-meme/README_HF.md README.md

# Commit and push
git add .
git commit -m "Deploy Gradio Meta-Meme dashboard with JWT+RDFa"
git push
```

## Public URL

After deployment:
```
https://huggingface.co/spaces/introspector/meta-meme
```

## Features

### 📊 Muse Tasks Tab
- Select from 9 AI muses
- Choose 6 hackathon tasks
- Generate JWT tokens with RDFa encoding
- View JSON and HTML output

### 🔐 ZK Witness Tab
- Zero-knowledge commitment visualization
- Per-muse encrypted data
- HME aggregate display
- Public key: 65537

### 🔗 RDFa Export Tab
- Load original URL (2,110 bytes)
- Load compressed URL (520 bytes)
- View compression stats (75.4% reduction)

## Files Required

- ✅ `app.py` - Gradio application
- ✅ `requirements.txt` - Dependencies (gradio>=4.0.0)
- ✅ `README.md` - Space description (from README_HF.md)
- ✅ `shareable_url.txt` - Original RDFa
- ✅ `shareable_url_compressed.txt` - Compressed RDFa

## Gradio vs Streamlit

Both versions available:
- **Gradio**: https://huggingface.co/spaces/introspector/meta-meme
- **Streamlit**: https://meta-meme.streamlit.app
