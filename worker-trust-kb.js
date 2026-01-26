/**
 * Trust Knowledge Base Worker
 * Serves trusted sources as queryable RDF
 */

const TRUST_KB = {
  "trust_network": {
    "version": "1.0.0",
    "created": "2026-01-26",
    "sources": {
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
    },
    "trust_level": "verified",
    "acl": "public"
  },
  "rdf_sources": [
    {
      "url": "https://github.com/meta-introspector",
      "category": "github_orgs",
      "format": "turtle",
      "acl": "public",
      "trusted": true
    },
    {
      "url": "https://github.com/jmikedupont2",
      "category": "github_orgs",
      "format": "turtle",
      "acl": "public",
      "trusted": true
    },
    {
      "url": "https://github.com/Escaped-RDFa",
      "category": "github_orgs",
      "format": "turtle",
      "acl": "public",
      "trusted": true
    },
    {
      "url": "https://huggingface.co/introspector",
      "category": "huggingface",
      "format": "turtle",
      "acl": "public",
      "trusted": true
    },
    {
      "url": "https://huggingface.co/spaces/introspector/meta-meme",
      "category": "huggingface",
      "format": "turtle",
      "acl": "public",
      "trusted": true
    },
    {
      "url": "https://huggingface.co/datasets/introspector/meta-meme",
      "category": "huggingface",
      "format": "turtle",
      "acl": "public",
      "trusted": true
    },
    {
      "url": "https://meta-meme.jmikedupont2.workers.dev/rdfa",
      "category": "cloudflare",
      "format": "turtle",
      "acl": "public",
      "trusted": true
    },
    {
      "url": "https://meta-meme-dev.jmikedupont2.workers.dev/rdfa",
      "category": "cloudflare",
      "format": "turtle",
      "acl": "public",
      "trusted": true
    }
  ]
};

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
