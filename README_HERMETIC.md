# Hermetic Build System

## Overview
Pure, reproducible builds using Nix + GitHub Actions + HuggingFace datasets.

## Components

### 1. Nix Shell Environment
```bash
nix-shell -p lean4 minizinc cargo rustc python3
```

### 2. GitHub Actions Workflow
- `.github/workflows/hermetic-build.yml`
- Runs on every push to `unified-memes`
- Downloads datasets from HuggingFace
- Builds Lean4 proofs
- Runs MiniZinc models
- Generates parquet schema index
- Validates datasets

### 3. HuggingFace Datasets
- `introspector/meta-meme` - 2,177 consultation URLs
- All data fetched from HF (no local dependencies)

### 4. Outputs
- `orbit_results.txt` - Schema orbit analysis
- `equivalence_results.txt` - Schema equivalence proofs
- `schema_index.txt` - Parquet schema index
- `parquet_schema_index.parquet` - Full schema catalog

## Local Testing with Act

```bash
# Install act (GitHub Actions runner)
nix-shell -p act

# Run workflow locally
act -j build

# Run specific step
act -j build -s "Download HuggingFace datasets"
```

## Hermetic Properties

1. **Reproducible**: Same inputs → same outputs
2. **Pure**: No side effects, no network (except HF download)
3. **Cacheable**: Nix cache via Cachix
4. **Portable**: Runs anywhere with Nix
5. **Verifiable**: All proofs checked by Lean4

## Dataset Validation

```bash
# Validate all HuggingFace datasets
python3 validate_hf_datasets.py

# Sync to local parquet
python3 validate_hf_datasets.py --sync
```

## Build Steps

1. **Download**: Fetch datasets from HuggingFace
2. **Validate**: Check schema, columns, row counts
3. **Build**: Compile Lean4 proofs
4. **Solve**: Run MiniZinc constraint models
5. **Index**: Generate parquet schema catalog
6. **Verify**: Check all proofs pass

## Artifacts

All build artifacts uploaded to GitHub Actions:
- Lean4 proof outputs
- MiniZinc solutions
- Parquet schema index
- Validation reports

## Usage

### Trigger Build
```bash
git push origin unified-memes
```

### Download Artifacts
```bash
gh run download <run-id>
```

### Local Build
```bash
nix-shell --run "
  lake build &&
  minizinc minizinc/schema_orbit.mzn &&
  cd parquet_tools && cargo run --release
"
```

## Dependencies

All managed by Nix:
- Lean4 4.x
- MiniZinc 2.x
- Rust/Cargo latest
- Python 3.10+
- HuggingFace Hub

## Next Steps

1. Add more HuggingFace datasets
2. Implement dataset sync pipeline
3. Add proof caching
4. Deploy to Cloudflare Workers
5. Create dataset validator tool
