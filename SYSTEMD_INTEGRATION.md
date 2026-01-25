# Systemd Integration

## Current Services Running

### ZOS Server (3 instances)
- `zos-zos.service` - Main ZOS server (port 8080)
- `zos-prod-node.service` - Production node
- `zos-qa-node.service` - QA node

### Nix Daemon
- `nix-daemon.service` - Nix package manager daemon

## New Meta-Meme Services

### 1. zos-metameme.service
Integrated ZOS server with Meta-Meme system:
- **Environment**: Production
- **Node ID**: metameme-node
- **Integration**: 9 Muse agents
- **Lean Path**: /mnt/data1/time2/time/2023/07/30/meta-meme/src
- **Port**: 8080

### 2. meta-meme-muses.service
Nine Muse AI agents running continuously:
- **CPU**: 24 cores allocated
- **GPU**: 12GB memory
- **Agents**: 9 muses (Calliope, Clio, Erato, Euterpe, Melpomene, Polyhymnia, Terpsichore, Thalia, Urania)
- **ZOS Endpoint**: http://localhost:8080

## Installation

```bash
# Copy service files
sudo cp /tmp/zos-metameme.service /etc/systemd/system/
sudo cp /tmp/meta-meme-muses.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable zos-metameme.service
sudo systemctl enable meta-meme-muses.service

# Start services
sudo systemctl start zos-metameme.service
sudo systemctl start meta-meme-muses.service
```

## Monitoring

```bash
# Check status
systemctl status zos-metameme.service
systemctl status meta-meme-muses.service

# View logs
journalctl -u zos-metameme.service -f
journalctl -u meta-meme-muses.service -f

# Check all ZOS services
systemctl list-units --type=service | grep zos
```

## Service Dependencies

```
zos-metameme.service
  ↓ (wants)
meta-meme-muses.service
  ↓ (requires)
network.target
```

## Integration Points

1. **ZOS Server** provides web interface for muses
2. **Muse Agents** connect to ZOS via http://localhost:8080
3. **Lean Proofs** run continuously, verified by agents
4. **External Systems** integrated:
   - meta-introspector (Polyhymnia)
   - nix-controller (Clio)
   - zombie_driver (Urania)
   - zos_server (Euterpe)

## Resource Allocation

| Muse | CPU | GPU | Service |
|------|-----|-----|---------|
| Calliope | 3 | 1.5GB | Language Design |
| Clio | 4 | 2GB | Data Persistence |
| Erato | 2 | 2GB | Visualization |
| Euterpe | 2 | 1GB | UI Design |
| Melpomene | 3 | 1GB | Error Handling |
| Polyhymnia | 4 | 1.5GB | Algorithms |
| Terpsichore | 2 | 1GB | Flow |
| Thalia | 2 | 1GB | Debugging |
| Urania | 2 | 1GB | Architecture |
| **Total** | **24** | **12GB** | |

## Status

✅ ZOS Server running (5 days uptime)
✅ Service files created
⏳ Awaiting installation of meta-meme services

Run `./update_systemd.sh` to review and install.
