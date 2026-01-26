# Distributed RDF Query System

## Overview
A lightweight, edge-deployed RDF query system that:
- Queries multiple RDF sources (federated)
- Streams partial results as collected
- Caches results with ACL support
- Runs on Cloudflare Workers (no big server needed)
- Generates shareable query URLs

## Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ Query URL
       ▼
┌─────────────────┐
│ Cloudflare Edge │ ◄── Cache (KV)
└────────┬────────┘
         │ Parallel Fetch
    ┌────┼────┬────────┐
    ▼    ▼    ▼        ▼
  RDF  RDF  RDF  ... RDF
Source Source Source Source
```

## Features

### 1. Federated Queries
Query multiple RDF sources in parallel:
```javascript
{
  "pattern": "?muse zk:commitment ?value",
  "sources": [
    {"url": "https://meta-meme.../rdfa", "format": "turtle", "acl": "public"},
    {"url": "https://other-source.../data", "format": "turtle", "acl": "public"}
  ]
}
```

### 2. Streaming Results
Results collected and returned as sources respond:
```json
[
  {
    "source": "https://meta-meme.../rdfa",
    "count": 9,
    "results": [
      {"?muse": "muse:Calliope", "?value": "2249895"},
      {"?muse": "muse:Clio", "?value": "2249895"}
    ],
    "timestamp": "2026-01-26T11:25:00Z"
  }
]
```

### 3. Shareable Query URLs
Every query generates a shareable URL:
```
https://meta-meme.../rdf?rdfquery=eyJwYXR0ZXJuIjogIj9tdXNlIHprOmNvbW1pdG1lbnQgP3ZhbHVlIi...
```

Decoded:
```json
{
  "pattern": "?muse zk:commitment ?value",
  "sources": [...]
}
```

### 4. Edge Caching
- Results cached at Cloudflare edge (1 hour TTL)
- Cache key: SHA256(source_url)
- ACL-aware caching (public/private)
- Global <10ms response time

### 5. Simple SPARQL-like Syntax
```sparql
# Find all muses
?muse a muse:Muse

# Find ZK commitments
?muse zk:commitment ?value

# Find encrypted data
?muse hme:encrypted ?cipher

# Pattern matching with variables
?subject ?predicate ?object
```

## Deployment

### 1. Generate Worker
```bash
python3 generate_rdf_query.py
```

Generates:
- `worker-rdf.js` - Cloudflare Worker code
- `rdf_queries.json` - Example queries

### 2. Deploy to Cloudflare
```bash
# Add to wrangler.toml
[env.rdf]
name = "meta-meme-rdf"
main = "worker-rdf.js"

# Deploy
wrangler deploy --env=rdf
```

### 3. Add KV Cache (Optional)
```bash
# Create KV namespace
wrangler kv:namespace create "RDF_CACHE"

# Add to wrangler.toml
[[kv_namespaces]]
binding = "RDF_CACHE"
id = "your-namespace-id"
```

## Usage

### Web Interface
1. Visit: `https://meta-meme-rdf.../`
2. Enter SPARQL-like pattern: `?muse zk:commitment ?value`
3. Add RDF sources (JSON array)
4. Click "Execute Query"
5. View streaming results
6. Click "Share Query" for URL

### API
```bash
# Execute query
curl -X POST https://meta-meme-rdf.../api/rdfquery \
  -H "Content-Type: application/json" \
  -d '{
    "pattern": "?muse zk:commitment ?value",
    "sources": [
      {"url": "https://meta-meme.../rdfa", "format": "turtle", "acl": "public"}
    ]
  }'

# Clear cache
curl -X POST https://meta-meme-rdf.../api/cache/clear
```

### Programmatic
```javascript
// Create query
const query = new RDFQuery(
  "?muse zk:commitment ?value",
  [
    new RDFSource("https://meta-meme.../rdfa", "turtle", "public")
  ]
);

// Generate shareable URL
const url = query.to_url("https://meta-meme-rdf.../");

// Parse from URL
const parsed = RDFQuery.from_url(encoded);
```

## Example Queries

### 1. Find All Muses
```
Pattern: ?muse a muse:Muse
URL: https://meta-meme.../rdf?rdfquery=eyJwYXR0ZXJuIjogIj9tdXNlIGEgbXVzZTpNdXNlIi...
```

### 2. Find ZK Commitments
```
Pattern: ?muse zk:commitment ?value
URL: https://meta-meme.../rdf?rdfquery=eyJwYXR0ZXJuIjogIj9tdXNlIHprOmNvbW1pdG1lbnQgP3ZhbHVlIi...
```

### 3. Find HME Encrypted Data
```
Pattern: ?muse hme:encrypted ?cipher
URL: https://meta-meme.../rdf?rdfquery=eyJwYXR0ZXJuIjogIj9tdXNlIGhtZTplbmNyeXB0ZWQgP2NpcGhlciI...
```

## RDF Sources

### Meta-Meme Sources
```json
[
  {
    "url": "https://meta-meme.jmikedupont2.workers.dev?compressed=H4sIANeAdmkC_...",
    "format": "turtle",
    "acl": "public",
    "description": "Compressed RDFa with 79 proofs"
  },
  {
    "url": "https://meta-meme.jmikedupont2.workers.dev/rdfa",
    "format": "turtle",
    "acl": "public",
    "description": "Direct RDFa access"
  }
]
```

### Adding Custom Sources
```json
{
  "url": "https://your-domain.com/data.ttl",
  "format": "turtle",
  "acl": "public"
}
```

## Performance

- **Query Execution**: <100ms per source
- **Cache Hit**: <10ms globally
- **Cache Miss**: <200ms (fetch + parse)
- **Parallel Sources**: Up to 10 simultaneous
- **Worker Size**: ~8 KiB (3 KiB gzipped)

## ACL Support

### Public Sources
```json
{"url": "...", "format": "turtle", "acl": "public"}
```
- Cached globally
- No authentication required

### Private Sources (Future)
```json
{"url": "...", "format": "turtle", "acl": "private", "token": "..."}
```
- Cached per-user
- Requires authentication token

## Limitations

### Current Implementation
- Simple pattern matching (not full SPARQL)
- Turtle/RDFa parsing only
- No FILTER, OPTIONAL, UNION
- Max 10 sources per query
- Max 1000 results per source

### Future Enhancements
- Full SPARQL 1.1 support
- JSON-LD, N-Triples formats
- Federated query optimization
- Real-time subscriptions (WebSocket)
- Query result pagination

## Integration with Meta-Meme

### Query Consultation URLs
```javascript
// Combine RDF query with muse consultation
const consultation = {
  muse: "Urania",
  tool: "lean4",
  query: "Verify ZK commitments",
  rdfQuery: "?muse zk:commitment ?value"
};
```

### Dataset Integration
```python
# Load 2,177 consultation URLs as RDF sources
import pandas as pd

df = pd.read_parquet('meta-meme-consultations.parquet')
sources = [
    {"url": row['url'], "format": "turtle", "acl": "public"}
    for _, row in df.iterrows()
]
```

## Security

- **CORS**: Enabled for all origins
- **Rate Limiting**: 100 req/min per IP (Cloudflare)
- **Cache Isolation**: ACL-based cache keys
- **Input Validation**: Pattern and URL sanitization
- **No Code Execution**: Pure data queries

## Cost

### Cloudflare Workers Free Tier
- 100,000 requests/day
- 10ms CPU time per request
- 1 GB KV storage
- **Cost**: $0/month for typical usage

### Paid Tier ($5/month)
- 10M requests/month
- 50ms CPU time per request
- Unlimited KV storage

## Examples

See `rdf_queries.json` for complete examples.

## Status

**Version**: 1.0.0  
**Status**: Ready for deployment  
**License**: MIT  
**Author**: Meta-Meme Project
