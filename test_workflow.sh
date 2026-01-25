#!/usr/bin/env nix-shell
#!nix-shell -i bash -p act

echo "🧪 Testing GitHub Actions with nektos/act"
echo "=========================================="
echo ""

cd /mnt/data1/time2/time/2023/07/30/meta-meme

echo "Running workflow: docs.yml"
echo ""

# Run the build job only (skip deploy for local testing)
act -j build \
  --container-architecture linux/amd64 \
  -W .github/workflows/docs.yml \
  --verbose

echo ""
echo "✅ Test complete"
