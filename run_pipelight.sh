#!/usr/bin/env nix-shell
#!nix-shell -i bash -p pipelight

echo "🚀 Running Pipelight: Meta-Meme Documentation Build"
echo "===================================================="
echo ""

cd /mnt/data1/time2/time/2023/07/30/meta-meme

# Run the docs pipeline
pipelight run docs

echo ""
echo "✅ Pipelight job complete"
echo ""
echo "Next steps:"
echo "  - Documentation built in static/"
echo "  - Changes committed to git"
echo "  - Pushed to origin/unified-memes"
echo "  - GitHub Actions will deploy to Pages"
