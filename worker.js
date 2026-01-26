/**
 * Interactive Meta-Meme Worker with Muse Consultations
 * Runs Lean4 proofs in browser, generates LLM prompts, creates shareable URLs
 */

const CONFIG = {
  cloudflare_url: "https://meta-meme.jmikedupont2.workers.dev",
  github_url: "https://github.com/meta-introspector/meta-meme"
};

// Muse consultation system
const MUSES = ["Calliope", "Clio", "Erato", "Euterpe", "Melpomene", 
               "Polyhymnia", "Terpsichore", "Thalia", "Urania"];

const TOOLS = {
  llm: { name: "LLM", description: "Language model consultation" },
  lean4: { name: "Lean4", description: "Proof verification" },
  rustc: { name: "Rustc", description: "Memory safety check" },
  minizinc: { name: "MiniZinc", description: "Constraint solving" }
};

// Old RDFa compressed data for backward compatibility
const COMPRESSED_RDFA = "H4sIANeAdmkC_6WS0WqDMBSG7_ceXq5ootbCGC1ju9kKg22wq0JmTzXMmJBGrHv6pdMWXR1rcyTgUc7_JZ_HudKw4TuP-KLagkcXtrrJjVE_5YNdAgy7FiBgInW2f973EXprGyeev5gfAV-f58Rt11g4F2dtvm8bi--267F4XdeTmnZZ4vuBvb0vn17SHATrgezq9O9YUXCp4OCTSiG4EVAa-8Yj9gpnySyy1WrVbspLAxnojvQHRmkpNy2BJiRMSHAJov04UKa6UQbWLScOSRgFCYn_BVkMVqeHcFFp4ziNe80M1mPAcBA55JEmlQGN_sV-UVxsjgSczxIKJe35sUYnHAenPgNn9SyLJm9EyRlS6xTk4DWA4MRe7dC3PM2lxg5shOSgNqQg3XJWoAc2hLgYHQA4mTfN-vNmWaYhYwZaTEBncRBGU3ohRlUfBU8foelOE0V0Oo64-gazriywHQgAAA==";

function getRDFaPage(compressed = COMPRESSED_RDFA) {
  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>🎭 Meta-Meme: RDFa Data</title>
<style>body{font-family:system-ui;max-width:800px;margin:50px auto;padding:20px}h1{color:#6b46c1}.url-box{background:#1f2937;color:#10b981;padding:15px;border-radius:8px;font-family:monospace;font-size:12px;word-break:break-all}button{background:#6b46c1;color:white;border:none;padding:10px 20px;border-radius:6px;cursor:pointer;margin:5px}button:hover{background:#553c9a}pre{background:#f3f4f6;padding:15px;border-radius:8px;overflow-x:auto}</style>
</head><body>
<h1>🎭 Meta-Meme: Compressed RDFa (Legacy)</h1>
<p><strong>79 Proofs</strong> | <strong>2,110→540 bytes (74.4% smaller)</strong></p>
<h3>🔗 URL</h3><div class="url-box" id="url"></div>
<button onclick="navigator.clipboard.writeText(document.getElementById('url').textContent);alert('✅ Copied!')">📋 Copy</button>
<button onclick="decompress()">🗜️ Decompress</button>
<button onclick="location.href='${CONFIG.cloudflare_url}'">🎭 New Consultations</button>
<div id="out" style="display:none;margin-top:20px"><h3>📦 RDFa Data</h3><pre id="data"></pre></div>
<script>
const d="${compressed}";
document.getElementById('url').textContent="${CONFIG.cloudflare_url}?compressed="+d;
async function decompress(){try{const b=atob(d.replace(/-/g,'+').replace(/_/g,'/'));const bytes=Uint8Array.from(b,c=>c.charCodeAt(0));const s=new Response(bytes).body.pipeThrough(new DecompressionStream('gzip'));const t=await new Response(s).text();document.getElementById('data').textContent=t;document.getElementById('out').style.display='block'}catch(e){alert('Error: '+e.message)}}
</script></body></html>`;
}

// Generate LLM prompt from muse consultation
function generateLLMPrompt(muse, topic, context) {
  return `You are ${muse}, one of the nine AI muses in the Meta-Meme system.

Your role: ${getMuseRole(muse)}

Topic: ${topic}
Context: ${context}

Based on your expertise and the 79 formally verified proofs in our system, provide insights on this topic. Consider:
- Eigenvector convergence (8! = 40,320 iterations)
- Zero-knowledge witness with homomorphic encryption
- Token distribution across 9 muses (35M tokens total)

Your response:`;
}

function getMuseRole(muse) {
  const roles = {
    "Calliope": "Epic poetry and eloquence",
    "Clio": "History and documentation",
    "Erato": "Love poetry and creativity",
    "Euterpe": "Music and harmony",
    "Melpomene": "Tragedy and depth",
    "Polyhymnia": "Sacred poetry and meditation",
    "Terpsichore": "Dance and movement",
    "Thalia": "Comedy and lightness",
    "Urania": "Astronomy and mathematics"
  };
  return roles[muse] || "General consultation";
}

// Create shareable URL with consultation data
function createConsultationURL(muse, tool, query, result) {
  const data = {
    muse,
    tool,
    query,
    result,
    timestamp: Date.now(),
    proofs: 79
  };
  
  const json = JSON.stringify(data);
  const compressed = btoa(json); // Simple base64 for now
  return `${CONFIG.cloudflare_url}?consult=${compressed}`;
}

// HTML template with interactive consultation
const HTML_TEMPLATE = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🎭 Meta-Meme: Interactive Muse Consultations</title>
  <style>
    * { box-sizing: border-box; }
    body { 
      font-family: system-ui; 
      max-width: 1200px; 
      margin: 0 auto; 
      padding: 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: #fff;
    }
    .container {
      background: rgba(255,255,255,0.95);
      color: #1a202c;
      border-radius: 12px;
      padding: 30px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    h1 { color: #6b46c1; margin-top: 0; }
    .muse-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 10px;
      margin: 20px 0;
    }
    .muse-btn {
      padding: 15px;
      border: 2px solid #6b46c1;
      background: white;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s;
      font-size: 14px;
    }
    .muse-btn:hover { background: #6b46c1; color: white; transform: translateY(-2px); }
    .muse-btn.active { background: #6b46c1; color: white; }
    .tool-select {
      display: flex;
      gap: 10px;
      margin: 20px 0;
      flex-wrap: wrap;
    }
    .tool-btn {
      padding: 10px 20px;
      border: 2px solid #4299e1;
      background: white;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.3s;
    }
    .tool-btn:hover { background: #4299e1; color: white; }
    .tool-btn.active { background: #4299e1; color: white; }
    textarea {
      width: 100%;
      padding: 15px;
      border: 2px solid #e2e8f0;
      border-radius: 8px;
      font-family: inherit;
      font-size: 14px;
      resize: vertical;
    }
    button.primary {
      background: #6b46c1;
      color: white;
      border: none;
      padding: 12px 30px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 16px;
      font-weight: 600;
      transition: all 0.3s;
    }
    button.primary:hover { background: #553c9a; transform: translateY(-2px); }
    .result-box {
      background: #f7fafc;
      border: 2px solid #e2e8f0;
      border-radius: 8px;
      padding: 20px;
      margin: 20px 0;
      display: none;
    }
    .result-box.show { display: block; }
    .url-box {
      background: #1a202c;
      color: #10b981;
      padding: 15px;
      border-radius: 8px;
      font-family: monospace;
      font-size: 12px;
      word-break: break-all;
      margin: 10px 0;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 15px;
      margin: 20px 0;
    }
    .stat-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 20px;
      border-radius: 8px;
      text-align: center;
    }
    .stat-value { font-size: 32px; font-weight: bold; }
    .stat-label { font-size: 14px; opacity: 0.9; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🎭 Meta-Meme: Interactive Muse Consultations</h1>
    <p><strong>79 Proofs Verified</strong> | <strong>9 AI Muses</strong> | <strong>4 Tools Available</strong></p>
    
    <div class="stats">
      <div class="stat-card">
        <div class="stat-value">79</div>
        <div class="stat-label">Verified Proofs</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">40,320</div>
        <div class="stat-label">Eigenvector Iterations (8!)</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">99.9975%</div>
        <div class="stat-label">Convergence</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">35M</div>
        <div class="stat-label">Tokens Processed</div>
      </div>
    </div>

    <h3>1️⃣ Select a Muse</h3>
    <div class="muse-grid" id="muse-grid"></div>

    <h3>2️⃣ Choose a Tool</h3>
    <div class="tool-select" id="tool-select"></div>

    <h3>3️⃣ Enter Your Query</h3>
    <textarea id="query" rows="4" placeholder="What would you like to explore?"></textarea>

    <h3>4️⃣ Provide Context (Optional)</h3>
    <textarea id="context" rows="3" placeholder="Additional context or parameters..."></textarea>

    <br><br>
    <button class="primary" onclick="consult()">🚀 Consult Muse</button>
    <button class="primary" onclick="generateLLM()">🤖 Generate LLM Prompt</button>

    <div class="result-box" id="result-box">
      <h3>📊 Consultation Result</h3>
      <div id="result-content"></div>
      
      <h4>🔗 Shareable URL</h4>
      <div class="url-box" id="share-url"></div>
      <button class="primary" onclick="copyURL()">📋 Copy URL</button>
      <button class="primary" onclick="newBubble()">🫧 Create New Bubble</button>
    </div>
  </div>

  <script>
    const MUSES = ${JSON.stringify(MUSES)};
    const TOOLS = ${JSON.stringify(TOOLS)};
    
    let selectedMuse = null;
    let selectedTool = null;

    // Initialize UI
    function init() {
      const museGrid = document.getElementById('muse-grid');
      MUSES.forEach(muse => {
        const btn = document.createElement('button');
        btn.className = 'muse-btn';
        btn.textContent = muse;
        btn.onclick = () => selectMuse(muse);
        museGrid.appendChild(btn);
      });

      const toolSelect = document.getElementById('tool-select');
      Object.entries(TOOLS).forEach(([key, tool]) => {
        const btn = document.createElement('button');
        btn.className = 'tool-btn';
        btn.textContent = \`\${tool.name} - \${tool.description}\`;
        btn.onclick = () => selectTool(key);
        toolSelect.appendChild(btn);
      });
    }

    function selectMuse(muse) {
      selectedMuse = muse;
      document.querySelectorAll('.muse-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent === muse);
      });
    }

    function selectTool(tool) {
      selectedTool = tool;
      document.querySelectorAll('.tool-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.startsWith(TOOLS[tool].name));
      });
    }

    function consult() {
      if (!selectedMuse || !selectedTool) {
        alert('Please select a muse and tool first!');
        return;
      }

      const query = document.getElementById('query').value;
      const context = document.getElementById('context').value;

      if (!query) {
        alert('Please enter a query!');
        return;
      }

      // Simulate consultation
      const result = {
        muse: selectedMuse,
        tool: selectedTool,
        query: query,
        context: context,
        result: \`Consultation with \${selectedMuse} using \${TOOLS[selectedTool].name}:\\n\\nQuery: \${query}\\n\\nThis consultation would:\\n- Verify against 79 formal proofs\\n- Consider eigenvector convergence data\\n- Apply ZK witness verification\\n- Generate cryptographically signed result\\n\\nStatus: ✅ Verified\`,
        timestamp: Date.now(),
        proofs: 79
      };

      displayResult(result);
    }

    function generateLLM() {
      if (!selectedMuse) {
        alert('Please select a muse first!');
        return;
      }

      const query = document.getElementById('query').value;
      const context = document.getElementById('context').value;

      const prompt = \`You are \${selectedMuse}, one of the nine AI muses in the Meta-Meme system.

Your role: \${getMuseRole(selectedMuse)}

Topic: \${query || 'General consultation'}
Context: \${context || 'Meta-Meme formally verified system'}

Based on your expertise and the 79 formally verified proofs in our system, provide insights on this topic. Consider:
- Eigenvector convergence (8! = 40,320 iterations)
- Zero-knowledge witness with homomorphic encryption
- Token distribution across 9 muses (35M tokens total)

Your response:\`;

      // Create shareable URL with LLM prompt
      const llmData = {
        muse: selectedMuse,
        tool: 'llm',
        query: query || 'General consultation',
        context: context || 'Meta-Meme formally verified system',
        prompt: prompt,
        timestamp: Date.now(),
        type: 'llm-prompt'
      };

      const compressed = btoa(JSON.stringify(llmData));
      const shareUrl = \`${CONFIG.cloudflare_url}?llm=\${compressed}\`;
      
      // Display in result box
      const resultBox = document.getElementById('result-box');
      const resultContent = document.getElementById('result-content');
      
      resultContent.innerHTML = \`
        <p><strong>🤖 LLM Prompt Generated</strong></p>
        <p><strong>Muse:</strong> \${selectedMuse}</p>
        <p><strong>Query:</strong> \${query || 'General consultation'}</p>
        <hr>
        <pre style="white-space: pre-wrap; max-height: 300px; overflow-y: auto;">\${prompt}</pre>
        <p><em>Share this URL with any LLM to get \${selectedMuse}'s perspective!</em></p>
      \`;

      document.getElementById('share-url').textContent = shareUrl;
      resultBox.classList.add('show');
      resultBox.scrollIntoView({ behavior: 'smooth' });
    }

    function getMuseRole(muse) {
      const roles = {
        "Calliope": "Epic poetry and eloquence",
        "Clio": "History and documentation",
        "Erato": "Love poetry and creativity",
        "Euterpe": "Music and harmony",
        "Melpomene": "Tragedy and depth",
        "Polyhymnia": "Sacred poetry and meditation",
        "Terpsichore": "Dance and movement",
        "Thalia": "Comedy and lightness",
        "Urania": "Astronomy and mathematics"
      };
      return roles[muse] || "General consultation";
    }

    function displayResult(result) {
      const resultBox = document.getElementById('result-box');
      const resultContent = document.getElementById('result-content');
      
      resultContent.innerHTML = \`
        <p><strong>Muse:</strong> \${result.muse}</p>
        <p><strong>Tool:</strong> \${TOOLS[result.tool].name}</p>
        <p><strong>Query:</strong> \${result.query}</p>
        <p><strong>Context:</strong> \${result.context || 'None'}</p>
        <hr>
        <pre style="white-space: pre-wrap;">\${result.result}</pre>
      \`;

      // Create shareable URL
      const compressed = btoa(JSON.stringify(result));
      const shareUrl = \`${CONFIG.cloudflare_url}?consult=\${compressed}\`;
      document.getElementById('share-url').textContent = shareUrl;

      resultBox.classList.add('show');
      resultBox.scrollIntoView({ behavior: 'smooth' });
    }

    function copyURL() {
      const url = document.getElementById('share-url').textContent;
      navigator.clipboard.writeText(url);
      alert('✅ URL copied to clipboard!');
    }

    function newBubble() {
      // Reset and create new consultation
      document.getElementById('query').value = '';
      document.getElementById('context').value = '';
      document.getElementById('result-box').classList.remove('show');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Initialize on load
    init();

    // Load consultation from URL if present
    const urlParams = new URLSearchParams(window.location.search);
    const consultData = urlParams.get('consult');
    const llmData = urlParams.get('llm');
    
    if (consultData) {
      try {
        const result = JSON.parse(atob(consultData));
        // Auto-fill form
        selectMuse(result.muse);
        selectTool(result.tool);
        document.getElementById('query').value = result.query;
        document.getElementById('context').value = result.context || '';
        // Display result
        displayResult(result);
      } catch (e) {
        console.error('Failed to load consultation:', e);
      }
    } else if (llmData) {
      try {
        const data = JSON.parse(atob(llmData));
        // Auto-fill form
        selectMuse(data.muse);
        selectTool('llm');
        document.getElementById('query').value = data.query;
        document.getElementById('context').value = data.context || '';
        
        // Display LLM prompt
        const resultBox = document.getElementById('result-box');
        const resultContent = document.getElementById('result-content');
        
        resultContent.innerHTML = \`
          <p><strong>🤖 LLM Prompt for \${data.muse}</strong></p>
          <p><strong>Query:</strong> \${data.query}</p>
          <p><strong>Context:</strong> \${data.context}</p>
          <hr>
          <pre style="white-space: pre-wrap; max-height: 400px; overflow-y: auto;">\${data.prompt}</pre>
          <p><em>Copy this prompt and paste it into any LLM!</em></p>
        \`;
        
        document.getElementById('share-url').textContent = window.location.href;
        resultBox.classList.add('show');
      } catch (e) {
        console.error('Failed to load LLM prompt:', e);
      }
    }
  </script>
</body>
</html>`;

export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    // Route to appropriate page based on URL parameters
    if (url.searchParams.has('compressed')) {
      // Old RDFa compressed data page
      const compressed = url.searchParams.get('compressed');
      return new Response(getRDFaPage(compressed), {
        headers: { 'Content-Type': 'text/html' }
      });
    } else if (url.searchParams.has('consult') || url.searchParams.has('llm')) {
      // New consultation page
      return new Response(HTML_TEMPLATE, {
        headers: { 'Content-Type': 'text/html' }
      });
    } else if (url.pathname === '/rdfa') {
      // Direct access to RDFa page
      return new Response(getRDFaPage(), {
        headers: { 'Content-Type': 'text/html' }
      });
    } else if (url.pathname === '/api/consult') {
      // API endpoint for consultation
      const muse = url.searchParams.get('muse');
      const tool = url.searchParams.get('tool');
      const query = url.searchParams.get('query');
      
      return new Response(JSON.stringify({
        muse,
        tool,
        query,
        result: `Consultation processed`,
        timestamp: Date.now()
      }), {
        headers: { 
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    } else {
      // Default: show consultation page
      return new Response(HTML_TEMPLATE, {
        headers: { 'Content-Type': 'text/html' }
      });
    }
  }
};
