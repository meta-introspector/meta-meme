# Parquet Schema Complexity Ordering (LMFDB-inspired)

## Complexity Metrics

Inspired by the L-functions and Modular Forms Database (LMFDB), we order parquet schemas by:

### 1. Conductor (Size & Scale)
- File size (MB) × 0.1
- Row count / 1,000,000
- Measures: data volume, computational cost

### 2. Weight (Dimensionality)
- Column count × 2
- Measures: feature richness, schema width

### 3. Level (Nesting Depth)
- Nested/compound columns × 3
- Columns with `.` or `_` separators
- Measures: structural complexity

### 4. Traits (Metadata Richness)
- Git repo tracked: +1
- Git commit tracked: +1
- Known creator process: +1
- Measures: provenance quality

### 5. Key Primes (Unique Identifiers)
- Columns with id/key/hash/uuid × 5
- Measures: relational potential, indexability

**Total Complexity** = conductor + weight + level + traits + key_primes

## Top 20 Most Complex Schemas

| Rank | File | Complexity | Conductor | Weight | Level | Traits | Primes |
|------|------|------------|-----------|--------|-------|--------|--------|
| 1 | commit_timeline.parquet | 158.1 | 137.1 | 5 | 1 | 3 | 1 |
| 2 | blob_metadata.parquet | 83.9 | 66.9 | 4 | 2 | 3 | 0 |
| 3 | files.parquet | 70.3 | 47.3 | 7 | 2 | 3 | 0 |
| 4 | functions_all.parquet | 48.2 | 15.2 | 8 | 3 | 3 | 1 |
| 5 | zos_tasks.parquet | 47.0 | 0.0 | 12 | 5 | 3 | 1 |
| 6-14 | super_git_index_*.parquet | 42-46 | 22-26 | 3 | 2 | 3 | 1 |
| 15-16 | nix_build_logs*.parquet | 42.0 | 0.0 | 9 | 7 | 3 | 0 |

## Statistics

- **Total schemas**: 423,925
- **Mean complexity**: 18.93
- **Median complexity**: 19.00
- **Max complexity**: 158.10 (commit_timeline.parquet)
- **Min complexity**: 8.00

## By Creator Process

| Creator | Files | Avg Complexity |
|---------|-------|----------------|
| nix-controller | 423,901 | 18.93 |
| nix-build-logger | 2 | 42.00 |
| meta-introspector | 5 | 40.18 |
| markov-model-builder | 7 | 19.92 |
| performance-profiler | 9 | 11.00 |
| meta-meme-generator | 1 | 20.08 |

## Key Insights

### Highest Conductor (Size)
- **commit_timeline.parquet**: 137.1 (massive git history)
- **blob_metadata.parquet**: 66.9 (git blob metadata)
- **files.parquet**: 47.3 (file system index)

### Highest Weight (Columns)
- **zos_tasks.parquet**: 12 columns (task management)
- **nix_build_logs*.parquet**: 9 columns (build metadata)
- **functions_all.parquet**: 8 columns (function analysis)

### Highest Level (Nesting)
- **nix_build_logs*.parquet**: 7 (deeply nested build data)
- **zos_tasks.parquet**: 5 (complex task structure)
- **functions_all.parquet**: 3 (function metadata)

### Most Key Primes (Identifiers)
- All git-related files have primary keys
- User timeline files (1 key per file)
- Function/declaration files (1 key per file)

## Usage

### Query by Complexity
```python
import pandas as pd

df = pd.read_parquet('parquet_schema_ordered.parquet')

# Top 10 most complex
top10 = df.head(10)

# Filter by complexity threshold
complex_schemas = df[df['complexity'] > 50]

# Filter by creator
nix_schemas = df[df['creator_process'] == 'nix-controller']
```

### RDF Queries
```sparql
# Find high-complexity schemas
?schema complexity:score ?score .
FILTER(?score > 50)

# Find schemas with many key primes
?schema complexity:key_primes ?primes .
FILTER(?primes > 2)
```

## Applications

1. **Query Optimization**: Prioritize simpler schemas for fast queries
2. **Caching Strategy**: Cache high-complexity schemas at edge
3. **Distributed Processing**: Shard by complexity for load balancing
4. **Schema Evolution**: Track complexity changes over time
5. **Data Discovery**: Find richest datasets by complexity

## Files Generated

- `parquet_schema_ordered.parquet` - Ordered by complexity
- `parquet_schemas_ordered.json` - Full schemas with metrics
- `order_schema_complexity.py` - Complexity calculator

## Next Steps

1. Add to RDF trust network as queryable source
2. Create complexity-based query router
3. Deploy to Cloudflare Workers for edge queries
4. Visualize complexity distribution
5. Track complexity evolution via git commits
