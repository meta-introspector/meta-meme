/**
 * Meta-Meme Cloudflare Worker
 * Serves compressed RDFa data and decompresses on request
 */

// Embedded config
const CONFIG = {
  app_url: "https://huggingface.co/spaces/introspector/meta-meme",
  solana_app_url: "https://solana.solfunmeme.com/app/",
  github_url: "https://github.com/meta-introspector/meta-meme"
};

// Embedded compressed data (base64)
const COMPRESSED_DATA = "H4sIANeAdmkC_6WS0WqDMBSG7_ceXq5ootbCGC1ju9kKg22wq0JmTzXMmJBGrHv6pdMWXR1rcyTgUc7_JZ_HudKw4TuP-KLagkcXtrrJjVE_5YNdAgy7FiBgInW2f973EXprGyeev5gfAV-f58Rt11g4F2dtvm8bi--267F4XdeTmnZZ4vuBvb0vn17SHATrgezq9O9YUXCp4OCTSiG4EVAa-8Yj9gpnySyy1WrVbspLAxnojvQHRmkpNy2BJiRMSHAJov04UKa6UQbWLScOSRgFCYn_BVkMVqeHcFFp4ziNe80M1mPAcBA55JEmlQGN_sV-UVxsjgSczxIKJe35sUYnHAenPgNn9SyLJm9EyRlS6xTk4DWA4MRe7dC3PM2lxg5shOSgNqQg3XJWoAc2hLgYHQA4mTfN-vNmWaYhYwZaTEBncRBGU3ohRlUfBU8foelOE0V0Oo64-gazriywHQgAAA==";

// HTML template
const HTML_TEMPLATE = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🎭 Meta-Meme: Formally Verified AI Muses</title>
  <style>
    body { font-family: system-ui; max-width: 800px; margin: 50px auto; padding: 20px; }
    h1 { color: #6b46c1; }
    .stats { background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0; }
    .url-box { background: #1f2937; color: #10b981; padding: 15px; border-radius: 8px; 
               overflow-x: auto; font-family: monospace; font-size: 12px; }
    button { background: #6b46c1; color: white; border: none; padding: 10px 20px; 
             border-radius: 6px; cursor: pointer; margin: 5px; }
    button:hover { background: #553c9a; }
    .links a { color: #6b46c1; text-decoration: none; margin-right: 15px; }
  </style>
</head>
<body>
  <h1>🎭 Meta-Meme: Formally Verified AI Muses</h1>
  <p><strong>79 Proofs Verified</strong> | <strong>8! Eigenvector Convergence</strong> | <strong>ZK+HME</strong></p>
  
  <div class="stats">
    <h3>📊 Compression Stats</h3>
    <p>Original: 2,110 bytes</p>
    <p>Compressed: 540 bytes</p>
    <p>Saved: 1,570 bytes (74.4% smaller)</p>
  </div>

  <h3>🔗 Compressed URL</h3>
  <div class="url-box" id="compressed-url"></div>
  <button onclick="copyUrl()">📋 Copy URL</button>
  <button onclick="decompressData()">🗜️ Decompress Data</button>

  <div id="decompressed" style="display:none; margin-top: 20px;">
    <h3>📦 Decompressed RDFa</h3>
    <pre class="url-box" id="rdfa-data"></pre>
  </div>

  <div class="links" style="margin-top: 30px;">
    <a href="${CONFIG.app_url}">🤗 HuggingFace</a>
    <a href="${CONFIG.solana_app_url}">🌐 Solana App</a>
    <a href="${CONFIG.github_url}">💻 GitHub</a>
  </div>

  <script>
    const compressedData = "${COMPRESSED_DATA}";
    const fullUrl = "${CONFIG.app_url}?compressed=" + compressedData;
    document.getElementById('compressed-url').textContent = fullUrl;

    function copyUrl() {
      navigator.clipboard.writeText(fullUrl);
      alert('✅ URL copied to clipboard!');
    }

    async function decompressData() {
      try {
        // Decode base64
        const binaryString = atob(compressedData.replace(/-/g, '+').replace(/_/g, '/'));
        const bytes = Uint8Array.from(binaryString, c => c.charCodeAt(0));
        
        // Decompress using DecompressionStream
        const stream = new Response(bytes).body.pipeThrough(
          new DecompressionStream('gzip')
        );
        const decompressed = await new Response(stream).text();
        
        document.getElementById('rdfa-data').textContent = decompressed;
        document.getElementById('decompressed').style.display = 'block';
      } catch (e) {
        alert('Error decompressing: ' + e.message);
      }
    }
  </script>
</body>
</html>`;

export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    // API endpoint for compressed data
    if (url.pathname === '/api/compressed') {
      return new Response(JSON.stringify({
        compressed: COMPRESSED_DATA,
        url: `${CONFIG.app_url}?compressed=${COMPRESSED_DATA}`,
        size: 540,
        original_size: 2110
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Serve HTML
    return new Response(HTML_TEMPLATE, {
      headers: { 'Content-Type': 'text/html' }
    });
  }
};
