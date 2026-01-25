#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Meta-Meme Manifold Prover Bootstrap"
echo "========================================"

# Check if nix is available
if ! command -v nix &> /dev/null; then
    echo "❌ Nix is not installed. Please install Nix first."
    exit 1
fi

echo "✓ Nix found"

# Enter nix environment and run proof
echo "📦 Loading Lean4 environment..."
nix develop --command bash -c '
    echo "✓ Lean4 environment loaded"
    echo "📐 Running manifold uniqueness proof..."
    
    if [ -f src/Manifold.lean ]; then
        lean src/Manifold.lean && echo "✅ Proof verified!" || echo "❌ Proof failed"
    else
        echo "❌ src/Manifold.lean not found"
        exit 1
    fi
'

echo "🎉 Bootstrap complete"
