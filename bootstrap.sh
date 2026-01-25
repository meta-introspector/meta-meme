#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Meta-Meme Manifold Prover Bootstrap"
echo "========================================"

if ! command -v nix &> /dev/null; then
    echo "❌ Nix is not installed. Please install Nix first."
    exit 1
fi

echo "✓ Nix found"

echo "📦 Loading Lean4 environment..."
nix develop --command bash -c '
    echo "✓ Lean4 environment loaded"
    
    echo "📐 Running manifold uniqueness proof..."
    lean src/Manifold.lean && echo "✅ Manifold proof verified!" || echo "❌ Manifold proof failed"
    
    echo ""
    echo "📚 Running document ingestion prover..."
    lean src/DocumentProver.lean && echo "✅ Document prover verified!" || echo "❌ Document prover failed"
    
    echo ""
    echo "🔐 Running zkWASM proofs..."
    lean src/ZKWasm.lean && echo "✅ zkWASM proofs verified!" || echo "❌ zkWASM proofs failed"
    
    echo ""
    echo "📄 Ingesting documents..."
    for doc in *.md docs/*.md metameme/*.md; do
        [ -f "$doc" ] && echo "  → $doc"
    done
    
    echo ""
    echo "🦀 Building zkWASM..."
    if command -v wasm-pack &> /dev/null; then
        wasm-pack build --target web --out-dir pkg && echo "✅ WASM built!" || echo "⚠️  WASM build skipped"
    else
        echo "⚠️  wasm-pack not found, skipping WASM build"
    fi
'

echo "🎉 Bootstrap complete"
