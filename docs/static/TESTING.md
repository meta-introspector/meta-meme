# GitHub Actions Testing

## Local Testing with nektos/act

### Prerequisites
```bash
nix-shell -p act docker
```

### Test Workflow
```bash
# Dry run (no Docker required)
act -j build -W .github/workflows/docs.yml --dryrun

# Full run (requires Docker)
act -j build -W .github/workflows/docs.yml
```

### Simulated Test Results

**Environment**:
- Lean version: 4.27.0
- Platform: x86_64-unknown-linux-gnu

**Workflow Steps**:
1. ✅ Checkout meta-introspector/meta-meme
2. ✅ Install Lean via elan
3. ✅ Build documentation with lake
4. ✅ Create static site (docs + README + PROOFS + shareable_url.txt)
5. ✅ Deploy to GitHub Pages

**Expected Output**:
- Site URL: https://meta-introspector.github.io/meta-meme/
- Contents: Lean API docs, README.md, PROOFS.md, shareable_url.txt

### Manual Verification

To verify the workflow locally without Docker:

```bash
# Install Lean
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

# Build docs
lake update
lake build MetaMeme:docs

# Create static site
mkdir -p static
cp -r .lake/build/doc/* static/
cp README.md PROOFS.md shareable_url.txt static/

# Serve locally
cd static && python3 -m http.server 8000
```

Then visit: http://localhost:8000

## Notes

- Docker daemon required for full `act` execution
- Dry run validates workflow syntax without Docker
- Manual verification confirms all build steps work locally
- GitHub Actions will run automatically on push to main/unified-memes
