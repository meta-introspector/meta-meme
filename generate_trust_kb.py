#!/usr/bin/env python3
"""
Add trusted GitHub orgs and HuggingFace URLs to knowledge base
Then make them queryable RDF sources
"""
import json
from pathlib import Path

# Trusted sources
TRUSTED_SOURCES = {
    "github_orgs": [
        "https://github.com/meta-introspector",
        "https://github.com/jmikedupont2",
        "https://github.com/Escaped-RDFa"
    ],
    "huggingface": [
        "https://huggingface.co/introspector",
        "https://huggingface.co/spaces/introspector/meta-meme",
        "https://huggingface.co/datasets/introspector/meta-meme"
    ],
    "cloudflare": [
        "https://meta-meme.jmikedupont2.workers.dev",
        "https://meta-meme-dev.jmikedupont2.workers.dev"
    ],
    "local_repos": [
        "/mnt/data1/time2/time/2023/07/30/meta-meme",
        "/mnt/data1/nix/source/github/jmikedupont2/orgs/Escaped-RDFa/namespace"
    ]
}

def generate_trust_kb():
    """Generate trust knowledge base"""
    kb = {
        "trust_network": {
            "version": "1.0.0",
            "created": "2026-01-26",
            "sources": TRUSTED_SOURCES,
            "trust_level": "verified",
            "acl": "public"
        },
        "rdf_sources": []
    }
    
    # Convert to RDF sources
    for category, urls in TRUSTED_SOURCES.items():
        for url in urls:
            if url.startswith("http"):
                kb["rdf_sources"].append({
                    "url": f"{url}/rdfa" if "workers.dev" in url else url,
                    "category": category,
                    "format": "turtle",
                    "acl": "public",
                    "trusted": True
                })
    
    return kb

def generate_trust_queries():
    """Generate queries for trusted sources"""
    return [
        {
            "name": "Find all trusted sources",
            "pattern": "?source trust:verified true",
            "description": "List all verified trusted sources"
        },
        {
            "name": "Query GitHub orgs",
            "pattern": "?repo trust:category 'github_orgs'",
            "description": "Find all GitHub organization repositories"
        },
        {
            "name": "Query HuggingFace spaces",
            "pattern": "?space trust:category 'huggingface'",
            "description": "Find all HuggingFace spaces and datasets"
        }
    ]

def generate_kb_worker():
    """Generate worker that serves KB as RDF"""
    return '''/**
 * Trust Knowledge Base Worker
 * Serves trusted sources as queryable RDF
 */

const TRUST_KB = ''' + json.dumps(generate_trust_kb(), indent=2) + ''';

// Convert KB to RDF/Turtle
function kbToTurtle() {
  let turtle = `@prefix trust: <http://meta-meme.org/trust#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

`;

  // Add sources
  TRUST_KB.rdf_sources.forEach((source, i) => {
    const id = `trust:source${i}`;
    turtle += `
${id} a trust:Source ;
  trust:url "${source.url}" ;
  trust:category "${source.category}" ;
  trust:format "${source.format}" ;
  trust:acl "${source.acl}" ;
  trust:verified "true"^^xsd:boolean .
`;
  });

  return turtle;
}

// Serve KB as RDF
export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    // Serve as Turtle
    if (url.pathname === '/rdfa' || url.pathname === '/turtle') {
      return new Response(kbToTurtle(), {
        headers: { 'Content-Type': 'text/turtle' }
      });
    }
    
    // Serve as JSON
    if (url.pathname === '/json') {
      return new Response(JSON.stringify(TRUST_KB, null, 2), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Default: HTML with links
    const html = `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>🔐 Trust Knowledge Base</title>
<style>
body{font-family:system-ui;max-width:800px;margin:50px auto;padding:20px;background:#0f172a;color:#e2e8f0}
h1{color:#60a5fa}h2{color:#818cf8;margin-top:30px}
.source{background:#1e293b;padding:15px;margin:10px 0;border-radius:8px;border-left:3px solid #10b981}
a{color:#60a5fa;text-decoration:none}a:hover{text-decoration:underline}
.category{display:inline-block;background:#334155;padding:4px 8px;border-radius:4px;font-size:12px;margin-right:5px}
</style>
</head><body>
<h1>🔐 Trust Knowledge Base</h1>
<p>Verified trusted sources for Meta-Meme RDF queries</p>

<h2>📊 Formats</h2>
<ul>
  <li><a href="/rdfa">RDF/Turtle</a> - Semantic data format</li>
  <li><a href="/json">JSON</a> - Machine-readable format</li>
</ul>

<h2>🔍 Trusted Sources</h2>
${TRUST_KB.rdf_sources.map(s => `
<div class="source">
  <span class="category">${s.category}</span>
  <a href="${s.url}" target="_blank">${s.url}</a>
</div>
`).join('')}

<h2>🔗 Query This KB</h2>
<p>Use in RDF queries:</p>
<pre style="background:#1e293b;padding:15px;border-radius:8px;overflow-x:auto">{
  "pattern": "?source trust:verified true",
  "sources": [{
    "url": "${new URL(request.url).origin}/rdfa",
    "format": "turtle",
    "acl": "public"
  }]
}</pre>

</body></html>`;
    
    return new Response(html, {
      headers: { 'Content-Type': 'text/html' }
    });
  }
};
''';

def main():
    print("🔐 Trust Knowledge Base Generator")
    print("=" * 50)
    
    # Generate KB
    kb = generate_trust_kb()
    Path('trust_kb.json').write_text(json.dumps(kb, indent=2))
    print(f"✅ Generated trust_kb.json ({len(kb['rdf_sources'])} sources)")
    
    # Generate queries
    queries = generate_trust_queries()
    Path('trust_queries.json').write_text(json.dumps(queries, indent=2))
    print(f"✅ Generated trust_queries.json ({len(queries)} queries)")
    
    # Generate worker
    worker = generate_kb_worker()
    Path('worker-trust-kb.js').write_text(worker)
    print("✅ Generated worker-trust-kb.js")
    
    print("\n📊 Trust Network:")
    for category, urls in TRUSTED_SOURCES.items():
        print(f"  {category}: {len(urls)} sources")
    
    print("\n🚀 Deploy:")
    print("  wrangler deploy --name meta-meme-trust worker-trust-kb.js")
    
    print("\n🔍 Query:")
    print("  curl https://meta-meme-trust.../rdfa")
    print("  curl https://meta-meme-trust.../json")

if __name__ == '__main__':
    main()
