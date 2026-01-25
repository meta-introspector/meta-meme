#!/bin/bash
set -e

echo "🔧 Updating systemd services for Meta-Meme integration"
echo "======================================================="
echo ""

# Check current services
echo "📊 Current ZOS services:"
systemctl list-units --type=service --state=running | grep zos || true
echo ""

# Create updated zos service with meta-meme integration
cat > /tmp/zos-metameme.service << 'EOF'
[Unit]
Description=ZOS Server with Meta-Meme Integration
After=network.target
Wants=meta-meme-muses.service

[Service]
Type=simple
User=mdupont
WorkingDirectory=/home/mdupont/meta-introspector/repos/zos-qa
Environment="ZOS_ENV=production"
Environment="ZOS_NODE_ID=metameme-node"
Environment="METAMEME_PATH=/mnt/data1/time2/time/2023/07/30/meta-meme"
Environment="MUSE_AGENTS=9"
Environment="LEAN_PATH=/mnt/data1/time2/time/2023/07/30/meta-meme/src"
ExecStart=/home/mdupont/meta-introspector/repos/zos-qa/target/release/zos_server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Created /tmp/zos-metameme.service"
echo "✅ Created /tmp/meta-meme-muses.service"
echo ""
echo "📝 To install, run as root:"
echo "   sudo cp /tmp/zos-metameme.service /etc/systemd/system/"
echo "   sudo cp /tmp/meta-meme-muses.service /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable zos-metameme.service"
echo "   sudo systemctl enable meta-meme-muses.service"
echo "   sudo systemctl start zos-metameme.service"
echo "   sudo systemctl start meta-meme-muses.service"
echo ""
echo "🔍 Current service status:"
systemctl status zos-zos.service --no-pager -l | head -15
