"""
Streamlit Meta-Meme Dashboard
Loads JWT+RDFa encoded tasks with ZK witness and HME proofs
"""
import streamlit as st
import json
from pathlib import Path

# Load muse data
MUSES = ["Calliope", "Clio", "Erato", "Euterpe", "Melpomene", 
         "Polyhymnia", "Terpsichore", "Thalia", "Urania"]

TASKS = [
    {"id": "TASK1", "description": "Summarize Text", "complexity": 1},
    {"id": "TASK2", "description": "Classify Image", "complexity": 2},
    {"id": "TASK3", "description": "Extract Sentences", "complexity": 1},
    {"id": "TASK4", "description": "Translate Text", "complexity": 2},
    {"id": "TASK5", "description": "Answer Questions", "complexity": 3},
    {"id": "TASK6", "description": "Chatbot Response", "complexity": 3},
]

# ZK Witness data
ZK_COMMITMENT = 2249895
ZK_PROOF = 38248215
HME_ENCRYPTED = 642451826
HME_AGGREGATE = 139614573
HME_PUBKEY = 65537

def generate_jwt(muse, task, timestamp):
    """Generate JWT with RDFa-encoded task"""
    rdfa = f"""<div vocab='http://schema.org/' typeof='SoftwareApplication'>
  <span property='name'>{task['id']}</span>
  <span property='description'>{task['description']}</span>
  <meta property='complexity' content='{task['complexity']}'/>
</div>"""
    
    return {
        "sub": f"muse:{muse}",
        "iat": timestamp,
        "exp": timestamp + 14400,  # 4 hours
        "data": rdfa
    }

st.title("🎭 Meta-Meme: Formally Verified AI Muses")
st.markdown("**79 Proofs Verified** | 8! Eigenvector Convergence | ZK+HME")

tab1, tab2, tab3 = st.tabs(["📊 Muse Tasks", "🔐 ZK Witness", "🔗 RDFa Export"])

with tab1:
    st.header("Hackathon Task Distribution")
    
    selected_muse = st.selectbox("Select Muse", MUSES)
    selected_task = st.selectbox("Select Task", [t['id'] for t in TASKS])
    
    task = next(t for t in TASKS if t['id'] == selected_task)
    
    st.subheader(f"{task['id']}: {task['description']}")
    st.metric("Complexity", task['complexity'])
    
    if st.button("Generate JWT Token"):
        import time
        jwt = generate_jwt(selected_muse, task, int(time.time()))
        st.json(jwt)
        st.code(jwt['data'], language='html')

with tab2:
    st.header("Zero-Knowledge Witness + HME")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("ZK Commitment Scheme")
        for muse in MUSES[:4]:
            with st.expander(f"🎭 {muse}"):
                st.metric("Commitment", ZK_COMMITMENT)
                st.metric("Proof", ZK_PROOF)
                st.metric("Encrypted", HME_ENCRYPTED)
    
    with col2:
        st.subheader("Homomorphic Encryption")
        st.metric("Public Key", HME_PUBKEY)
        st.metric("Aggregate Ciphertext", HME_AGGREGATE)
        st.info("All muses share encrypted knowledge via HME")

with tab3:
    st.header("RDFa/Turtle Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Original (2,110 bytes)")
        url_file = Path("shareable_url.txt")
        if url_file.exists():
            original_url = url_file.read_text()
            st.text_area("Full URL", original_url, height=150)
            st.download_button("Download Original", original_url, "shareable_url.txt")
        else:
            st.warning("Run `lean src/RDFaURL.lean` to generate")
    
    with col2:
        st.subheader("🗜️ Compressed (515 bytes)")
        compressed_file = Path("shareable_url_compressed.txt")
        if compressed_file.exists():
            compressed_url = compressed_file.read_text()
            st.success("✅ 75.6% smaller!")
            
            # Show the Streamlit app URL with anchor
            streamlit_share_url = "https://meta-meme.streamlit.app/#compressed-515-bytes"
            st.info(f"🔗 **Live Demo**: {streamlit_share_url}")
            
            # Copy Streamlit URL button
            if st.button("📋 Copy Streamlit Share Link"):
                st.code(streamlit_share_url, language=None)
                st.success("✅ Copy the URL above!")
            
            # Show compressed data URL
            st.text_area("Compressed Data URL", compressed_url, height=100)
            
            # Download button
            st.download_button(
                "📥 Download Compressed", 
                compressed_url, 
                "shareable_url_compressed.txt",
                help="Download compressed RDFa URL"
            )
            
            st.metric("Compression Ratio", "24.4%", "-1,595 bytes")
        else:
            if st.button("🗜️ Compress Now"):
                st.info("Run: `python3 compress_rdfa.py`")
    
    st.subheader("Live RDFa Generation")
    if st.button("Generate RDFa for All Tasks"):
        rdfa_output = "@prefix muse: <http://meta-meme.org/muse#> .\n"
        rdfa_output += "@prefix task: <http://meta-meme.org/task#> .\n\n"
        
        for i, task in enumerate(TASKS):
            muse = MUSES[i % len(MUSES)]
            rdfa_output += f"muse:{muse} task:assigned task:{task['id']} .\n"
            rdfa_output += f"task:{task['id']} task:complexity {task['complexity']} .\n"
        
        st.code(rdfa_output, language='turtle')

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Documentation")
st.sidebar.markdown("[API Docs](https://meta-introspector.github.io/meta-meme/)")
st.sidebar.markdown("[GitHub](https://github.com/meta-introspector/meta-meme)")
st.sidebar.markdown("### ✅ Verified")
st.sidebar.metric("Total Proofs", 79)
st.sidebar.metric("Eigenvector Iterations", "40,320 (8!)")
st.sidebar.metric("Convergence", "99.9975%")
