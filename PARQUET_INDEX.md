# Parquet Index - 425K+ Files

## Major Caches

### 1. Toolchain Analysis (~12 files)
**Location**: `~/.local/share/toolchain-analysis/`
- `bash/` - Bash toolchain analysis
- `cargo/` - Cargo/Rust toolchain
- `gcc/` - GCC compiler analysis  
- `rustc/` - Rustc compiler analysis

**Files per toolchain**:
- `byte_provenance.parquet` - Byte-level provenance
- `markov_symbol_scores.parquet` - Symbol scoring
- `nix_store_grammars.parquet` - Nix store grammars

### 2. Nix Controller (~425K files)
**Location**: `~/nix-controller/`
- `index.parquet` - Main index
- `data/` - Massive dataset cache
  - `author_stats.parquet`
  - `binary_markov_model.parquet`
  - `commit_timeline.parquet`
  - `const_declarations.parquet`
  - `fn_declarations.parquet`
  - `impl_declarations.parquet`
  - `keyword_table.parquet`
  - `markov_fingerprints.parquet`
  - `rust_lattice/` - Multi-layer AST analysis
    - `layer0_raw/ast.parquet/` - Parsing, type inference, name resolution phases
  - `object_groups/` - Grouped objects
  - `metadata/` - Metadata cache
  - `unique_value_index/` - Value indexing
  - `user_timelines/` - User activity timelines

### 3. Meta-Introspector (~14 files)
**Location**: `~/meta-introspector/`
- Performance metrics: `bash_bootstrap_perf.parquet`, `coq_perf.parquet`, etc.
- Nix builds: `nix_build_logs.parquet`, `nix_build_logs_all.parquet`
- Markov chains: `markov_symbol_scores.parquet`
- Grammars: `nix_store_grammars.parquet`

### 4. Meta-Meme (1 file)
**Location**: `./meta-meme-consultations.parquet`
- 2,177 muse consultation URLs
- 782 KB

## Total Statistics

- **Total Files**: 425,915 parquet files
- **Major Caches**: 4 locations
- **Largest Cache**: nix-controller (~425K files)
- **Categories**: toolchain analysis, Rust lattice, consultations, performance

## Parquet-of-Parquet Strategy

### Phase 1: Index Major Caches
1. Toolchain analysis (12 files)
2. Meta-introspector (14 files)
3. Meta-meme consultations (1 file)
4. Nix-controller index (1 file)

### Phase 2: Query Rust Lattice
- 425K AST parquet files
- Multi-phase analysis (parsing, type inference, name resolution)
- Layer 0 raw data

### Phase 3: Distributed RDF Queries
- Serve parquet files as RDF sources
- Query across all caches
- Share results via URLs

## RDF Integration

Each parquet file can be:
1. Loaded as RDF triples
2. Queried via SPARQL-like patterns
3. Cached at edge (Cloudflare Workers)
4. Shared via consultation URLs

## Next Steps

1. Create parquet-of-parquet index (27 key files)
2. Add to trust KB as RDF sources
3. Enable distributed queries
4. Deploy to edge workers
