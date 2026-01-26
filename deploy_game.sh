#!/bin/bash
# Deploy 8D Perf Emoji Game to Cloudflare Workers

set -e

echo "=== Deploying 8D Perf Emoji Game to Cloudflare Workers ==="
echo

# Check if wrangler is available
if ! command -v wrangler &> /dev/null; then
    echo "Installing wrangler..."
    npm install -g wrangler
fi

# Login to Cloudflare (if not already)
echo "Checking Cloudflare authentication..."
wrangler whoami || wrangler login

# Deploy
echo
echo "Deploying to Cloudflare Workers..."
wrangler deploy

echo
echo "✓ Deployment complete!"
echo
echo "Your 8D Perf Emoji Game is now live at:"
echo "  https://perf-emoji-game.<your-subdomain>.workers.dev"
echo
echo "To test locally:"
echo "  wrangler dev"
echo
echo "Game features:"
echo "  - Real perf traces from our analysis"
echo "  - 8D navigation (8 keyboard controls)"
echo "  - Emoji visualization"
echo "  - WebGPU rendering"
echo
echo "Controls:"
echo "  WASD: XY, QE: Z, RF: dim4, TG: dim5"
echo "  YH: dim6, UJ: dim7, IK: dim8"
echo "  SPACE: Generate new trace"
