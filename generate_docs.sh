#!/bin/bash
echo "📚 Generating Lean4 Documentation with doc-gen4"
echo "================================================"
echo ""

# Check if lake is available
if ! command -v lake &> /dev/null; then
    echo "⚠️  Lake not found. Install with: curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh"
    exit 1
fi

echo "Step 1: Update dependencies"
lake update

echo ""
echo "Step 2: Build documentation"
lake build MetaMeme:docs

echo ""
echo "Step 3: Documentation generated in .lake/build/doc/"
echo ""
echo "To serve locally:"
echo "  cd .lake/build/doc && python3 -m http.server 8000"
echo ""
echo "To deploy to GitHub Pages:"
echo "  cp -r .lake/build/doc/* docs/"
echo "  git add docs/ && git commit -m 'Update documentation'"
echo ""
echo "✅ Documentation generation complete!"
