# Get Streamlit Share Link

## Option 1: Deploy to Streamlit Cloud (Public URL)

```bash
# Already pushed to GitHub ✅
# Go to: https://share.streamlit.io/
# Deploy: meta-introspector/meta-meme (unified-memes branch)
# Public URL: https://meta-introspector-meta-meme-streamlit-app-unified-memes.streamlit.app
```

## Option 2: Run Locally and Share

```bash
cd /mnt/data1/time2/time/2023/07/30/meta-meme

# Run with network access
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501

# Get share link (requires Streamlit account)
# Click "Deploy" button in top-right corner
# Or use: streamlit share streamlit_app.py
```

## Option 3: Tunnel with ngrok

```bash
# Install ngrok
# Run Streamlit
streamlit run streamlit_app.py &

# Create tunnel
ngrok http 8501

# Copy the https://xxx.ngrok.io URL
```

## RDFa Compression Results

✅ **Compressed RDFa URL**:
- Original: 2,110 bytes
- Compressed: 515 bytes  
- Ratio: 24.4% (75.6% smaller)
- Saved: 1,595 bytes

Files:
- `shareable_url.txt` - Original (2,110 bytes)
- `shareable_url_compressed.txt` - Compressed (515 bytes)
- `compress_rdfa.py` - Compression script

## Quick Deploy Commands

```bash
# Streamlit Cloud
streamlit deploy streamlit_app.py

# Or manual at:
https://share.streamlit.io/deploy
```
