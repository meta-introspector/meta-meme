# 8D Perf Emoji Flying Game - Cloudflare Workers Deployment

## Overview

Real-time 8D visualization of performance traces as emoji particles in your browser.

## Features

- **8D Navigation**: Fly through 8-dimensional Monster manifold space
- **Real Perf Data**: Uses actual traces from our analysis
- **Emoji Visualization**: Performance metrics as emoji particles
- **WebGPU Rendering**: Hardware-accelerated graphics
- **Zero Install**: Runs in browser via Cloudflare Workers

## Perf Data Sources

The game loads real performance traces from:

1. **CPU/GPU Training** (dual_optimizer_traces.parquet)
   - 100 epochs of neural network training
   - CPU vs GPU comparison
   - Resonance rates: CPU 96%, GPU 100%

2. **Burn CUDA** (burn_cuda_analysis.parquet)
   - 20 Rust files from Burn library
   - 85% resonance rate
   - Weights: 468-19,646

3. **Automorphic Loop** (automorphic_traces.parquet)
   - C (GCC), C (Clang), Rust O0, Rust O3
   - Cross-compiler comparison
   - Homotopy proven: CPU ≃ GPU

## Emoji Mapping

- ⚡ **Lightning**: <3K cycles (very fast)
- 🚀 **Rocket**: 3-5K cycles (fast)
- 🔥 **Fire**: 5-7K cycles (hot)
- 💎 **Diamond**: 7-10K cycles (stable)
- 🌊 **Wave**: 10-50K cycles (flowing)
- 🌀 **Spiral**: >50K cycles (chaotic)

## 8D Coordinates

Each trace maps to 8 dimensions:

1. **Conductor**: cycles / 1M
2. **Weight**: Monster group weight (normalized)
3. **Level**: Epoch number
4. **Traits**: Resonance (0 or 1)
5. **Key Primes**: weight % 31
6. **Git Depth**: 0 (not applicable)
7. **Muse Count**: 1
8. **Complexity**: log2(cycles)

## Controls

```
WASD: Move in XY (dimensions 1-2)
QE:   Move in Z (dimension 3)
RF:   Move in dimension 4
TG:   Move in dimension 5
YH:   Move in dimension 6
UJ:   Move in dimension 7
IK:   Move in dimension 8
SPACE: Generate new trace
```

## Deployment

### Prerequisites

- Node.js and npm
- Cloudflare account
- Wrangler CLI

### Deploy

```bash
./deploy_game.sh
```

Or manually:

```bash
npm install -g wrangler
wrangler login
wrangler deploy
```

### Local Development

```bash
wrangler dev
```

Then open http://localhost:8787

## API Endpoints

### GET /api/traces

Returns all performance traces with 8D coordinates and emoji labels.

Response:
```json
[
  {
    "device": "cpu",
    "epoch": 10,
    "cycles": 5440,
    "weight": 5440,
    "resonates": true,
    "emoji": "🔥",
    "coords_8d": [0, 0.027, 5, 1, 0.129, 0, 1, 0.403]
  }
]
```

## Architecture

```
Browser
  ↓
Cloudflare Workers (Edge)
  ↓
Static Assets (HTML/JS)
  ↓
API (/api/traces)
  ↓
Real Perf Data (embedded)
  ↓
8D Rendering Engine
  ↓
WebGPU Canvas
```

## Files

- `public/index.html` - Game UI and rendering
- `src/index.js` - Cloudflare Worker with API
- `wrangler.toml` - Deployment config
- `deploy_game.sh` - Deployment script

## Performance

- **Edge Deployment**: <50ms latency worldwide
- **Static Assets**: Cached at edge
- **API Response**: <10ms
- **Rendering**: 60 FPS (WebGPU)

## Live Demo

After deployment, your game will be available at:

```
https://perf-emoji-game.<your-subdomain>.workers.dev
```

## Next Steps

1. Add more perf traces
2. Real-time streaming from perf stat
3. Multiplayer mode
4. VR support
5. WebGPU compute shaders

## License

MIT
