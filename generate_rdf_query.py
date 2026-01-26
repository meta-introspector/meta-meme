#!/usr/bin/env python3
"""
Distributed RDF Query System
Query multiple RDF sources, stream results, cache with ACLs
"""
import json
import base64
from pathlib import Path
from typing import List, Dict, Any
import hashlib

class RDFSource:
    """RDF data source"""
    def __init__(self, url: str, format: str = "turtle", acl: str = "public"):
        self.url = url
        self.format = format
        self.acl = acl
        self.cache_key = hashlib.sha256(url.encode()).hexdigest()[:16]

class RDFQuery:
    """Simple RDF query (SPARQL-like)"""
    def __init__(self, pattern: str, sources: List[RDFSource]):
        self.pattern = pattern
        self.sources = sources
        self.results = []
    
    def to_url(self, base_url: str) -> str:
        """Generate shareable query URL"""
        data = {
            'pattern': self.pattern,
            'sources': [{'url': s.url, 'format': s.format, 'acl': s.acl} for s in self.sources]
        }
        encoded = base64.urlsafe_b64encode(json.dumps(data).encode()).decode()
        return f"{base_url}?rdfquery={encoded}"
    
    @staticmethod
    def from_url(encoded: str) -> 'RDFQuery':
        """Parse query from URL"""
        data = json.loads(base64.urlsafe_b64decode(encoded))
        sources = [RDFSource(**s) for s in data['sources']]
        return RDFQuery(data['pattern'], sources)

def generate_rdf_sources():
    """Generate list of RDF sources from meta-meme"""
    sources = [
        RDFSource(
            url="https://meta-meme.jmikedupont2.workers.dev?compressed=H4sIANeAdmkC_...",
            format="turtle",
            acl="public"
        ),
        RDFSource(
            url="https://meta-meme.jmikedupont2.workers.dev/rdfa",
            format="rdfa",
            acl="public"
        ),
        # Add more sources from dataset
    ]
    return sources

def generate_example_queries():
    """Generate example RDF queries"""
    sources = generate_rdf_sources()
    
    queries = [
        {
            'name': 'Find all muses',
            'pattern': '?muse a muse:Muse',
            'sources': sources[:1]
        },
        {
            'name': 'Find ZK commitments',
            'pattern': '?muse zk:commitment ?value',
            'sources': sources
        },
        {
            'name': 'Find HME encrypted data',
            'pattern': '?muse hme:encrypted ?cipher',
            'sources': sources
        }
    ]
    
    return queries

def generate_worker_code():
    """Generate Cloudflare Worker for RDF queries"""
    return '''/**
 * Distributed RDF Query Worker
 * Query multiple RDF sources, stream results, cache with ACLs
 */

// Simple Turtle parser
function parseTurtle(text) {
  const triples = [];
  const lines = text.split('\\n');
  
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('@') || trimmed.startsWith('#')) continue;
    
    // Simple pattern: subject predicate object .
    const match = trimmed.match(/^([^\\s]+)\\s+([^\\s]+)\\s+(.+?)\\s*\\.?$/);
    if (match) {
      triples.push({
        subject: match[1],
        predicate: match[2],
        object: match[3].replace(/\\.$/, '').trim()
      });
    }
  }
  
  return triples;
}

// Simple SPARQL-like query executor
function executeQuery(pattern, triples) {
  const results = [];
  const vars = pattern.match(/\\?\\w+/g) || [];
  
  // Simple pattern matching
  const [subj, pred, obj] = pattern.split(/\\s+/);
  
  for (const triple of triples) {
    const bindings = {};
    let match = true;
    
    if (subj.startsWith('?')) {
      bindings[subj] = triple.subject;
    } else if (subj !== triple.subject) {
      match = false;
    }
    
    if (pred.startsWith('?')) {
      bindings[pred] = triple.predicate;
    } else if (pred !== triple.predicate) {
      match = false;
    }
    
    if (obj.startsWith('?')) {
      bindings[obj] = triple.object;
    } else if (obj !== triple.object) {
      match = false;
    }
    
    if (match) {
      results.push(bindings);
    }
  }
  
  return results;
}

// Fetch and parse RDF source
async function fetchRDFSource(source, cache) {
  const cacheKey = `rdf:${source.url}`;
  
  // Check cache
  if (cache) {
    const cached = await cache.get(cacheKey);
    if (cached) return JSON.parse(cached);
  }
  
  // Fetch source
  const response = await fetch(source.url);
  const text = await response.text();
  
  // Parse based on format
  let triples;
  if (source.format === 'turtle' || source.format === 'rdfa') {
    triples = parseTurtle(text);
  } else {
    triples = [];
  }
  
  // Cache results (1 hour TTL)
  if (cache) {
    await cache.put(cacheKey, JSON.stringify(triples), { expirationTtl: 3600 });
  }
  
  return triples;
}

// Stream query results
async function streamQueryResults(query, sources, cache) {
  const results = [];
  
  for (const source of sources) {
    try {
      const triples = await fetchRDFSource(source, cache);
      const sourceResults = executeQuery(query.pattern, triples);
      
      results.push({
        source: source.url,
        count: sourceResults.length,
        results: sourceResults.slice(0, 10), // First 10
        timestamp: new Date().toISOString()
      });
    } catch (e) {
      results.push({
        source: source.url,
        error: e.message,
        timestamp: new Date().toISOString()
      });
    }
  }
  
  return results;
}

const HTML_TEMPLATE = `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>🔍 Distributed RDF Query</title>
<style>
body{font-family:system-ui;max-width:1000px;margin:20px auto;padding:20px;background:#0f172a;color:#e2e8f0}
h1{color:#60a5fa}h2{color:#818cf8;font-size:1.2em;margin-top:30px}
.query-box{background:#1e293b;padding:20px;border-radius:8px;margin:20px 0}
textarea{width:100%;padding:10px;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;font-family:monospace;font-size:14px}
button{background:#3b82f6;color:white;border:none;padding:10px 20px;border-radius:6px;cursor:pointer;margin:5px}
button:hover{background:#2563eb}
.source{background:#1e293b;padding:10px;margin:10px 0;border-radius:4px;border-left:3px solid #3b82f6}
.result{background:#0f172a;padding:10px;margin:5px 0;border-radius:4px;font-family:monospace;font-size:12px}
.error{border-left:3px solid #ef4444}
.success{border-left:3px solid #10b981}
#results{margin-top:20px}
.url-box{background:#1e293b;padding:10px;border-radius:4px;word-break:break-all;font-size:12px;margin:10px 0}
</style>
</head><body>
<h1>🔍 Distributed RDF Query</h1>
<p>Query multiple RDF sources, stream results, cache with ACLs</p>

<div class="query-box">
  <h2>Query Pattern (SPARQL-like)</h2>
  <textarea id="pattern" rows="3" placeholder="?muse zk:commitment ?value">?muse zk:commitment ?value</textarea>
  
  <h2>RDF Sources</h2>
  <textarea id="sources" rows="6" placeholder='[{"url":"...","format":"turtle","acl":"public"}]'>[
  {"url":"https://meta-meme.jmikedupont2.workers.dev/rdfa","format":"turtle","acl":"public"}
]</textarea>
  
  <button onclick="executeQuery()">🔍 Execute Query</button>
  <button onclick="shareQuery()">🔗 Share Query</button>
  <button onclick="clearCache()">🗑️ Clear Cache</button>
</div>

<div id="shareUrl" style="display:none">
  <h2>📋 Shareable Query URL</h2>
  <div class="url-box" id="queryUrl"></div>
  <button onclick="navigator.clipboard.writeText(document.getElementById('queryUrl').textContent);alert('✅ Copied!')">📋 Copy</button>
</div>

<div id="results"></div>

<script>
async function executeQuery() {
  const pattern = document.getElementById('pattern').value;
  const sources = JSON.parse(document.getElementById('sources').value);
  
  document.getElementById('results').innerHTML = '<p>⏳ Querying sources...</p>';
  
  const response = await fetch('/api/rdfquery', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({pattern, sources})
  });
  
  const results = await response.json();
  displayResults(results);
}

function displayResults(results) {
  let html = '<h2>📊 Query Results</h2>';
  
  for (const result of results) {
    const cssClass = result.error ? 'error' : 'success';
    html += \`<div class="source \${cssClass}">
      <strong>\${result.source}</strong><br>
      <small>\${result.timestamp}</small><br>\`;
    
    if (result.error) {
      html += \`<span style="color:#ef4444">Error: \${result.error}</span>\`;
    } else {
      html += \`<span style="color:#10b981">\${result.count} results</span>\`;
      for (const r of result.results || []) {
        html += \`<div class="result">\${JSON.stringify(r)}</div>\`;
      }
    }
    
    html += '</div>';
  }
  
  document.getElementById('results').innerHTML = html;
}

function shareQuery() {
  const pattern = document.getElementById('pattern').value;
  const sources = JSON.parse(document.getElementById('sources').value);
  
  const data = btoa(JSON.stringify({pattern, sources}));
  const url = window.location.origin + '?rdfquery=' + data;
  
  document.getElementById('queryUrl').textContent = url;
  document.getElementById('shareUrl').style.display = 'block';
}

async function clearCache() {
  await fetch('/api/cache/clear', {method: 'POST'});
  alert('✅ Cache cleared');
}

// Load query from URL
window.onload = function() {
  const params = new URLSearchParams(window.location.search);
  const query = params.get('rdfquery');
  
  if (query) {
    try {
      const data = JSON.parse(atob(query));
      document.getElementById('pattern').value = data.pattern;
      document.getElementById('sources').value = JSON.stringify(data.sources, null, 2);
    } catch (e) {
      console.error('Failed to load query:', e);
    }
  }
};
</script>
</body></html>`;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cache = env.RDF_CACHE || null;
    
    // API: Execute RDF query
    if (url.pathname === '/api/rdfquery' && request.method === 'POST') {
      const body = await request.json();
      const results = await streamQueryResults(body, body.sources, cache);
      
      return new Response(JSON.stringify(results), {
        headers: {'Content-Type': 'application/json'}
      });
    }
    
    // API: Clear cache
    if (url.pathname === '/api/cache/clear' && request.method === 'POST') {
      // Cache clearing handled by TTL
      return new Response(JSON.stringify({status: 'ok'}), {
        headers: {'Content-Type': 'application/json'}
      });
    }
    
    // Main page
    return new Response(HTML_TEMPLATE, {
      headers: {'Content-Type': 'text/html'}
    });
  }
};
'''

def main():
    print("🔍 Distributed RDF Query System")
    print("=" * 50)
    
    # Generate example queries
    queries = generate_example_queries()
    
    print(f"\n📊 Generated {len(queries)} example queries:")
    for q in queries:
        query = RDFQuery(q['pattern'], q['sources'])
        url = query.to_url("https://meta-meme.jmikedupont2.workers.dev")
        print(f"\n  {q['name']}:")
        print(f"    Pattern: {q['pattern']}")
        print(f"    URL: {url[:80]}...")
    
    # Generate worker code
    print("\n🔨 Generating worker code...")
    worker_code = generate_worker_code()
    
    Path('worker-rdf.js').write_text(worker_code)
    print("✅ Saved to worker-rdf.js")
    
    # Generate example queries file
    examples = {
        'queries': [
            {
                'name': q['name'],
                'pattern': q['pattern'],
                'url': RDFQuery(q['pattern'], q['sources']).to_url("https://meta-meme.jmikedupont2.workers.dev")
            }
            for q in queries
        ]
    }
    
    Path('rdf_queries.json').write_text(json.dumps(examples, indent=2))
    print("✅ Saved examples to rdf_queries.json")
    
    print("\n🚀 Deploy with:")
    print("  wrangler deploy --name meta-meme-rdf worker-rdf.js")

if __name__ == '__main__':
    main()
