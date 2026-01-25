# @metameme/lattice

Pure function lattice with mathematical properties and proofs encoded in URLs.

## Installation

```bash
npm install @metameme/lattice
```

## Usage

```typescript
import { Lattice, URLProof } from '@metameme/lattice';

// Create lattice
const lattice = new Lattice();

// Add pure function with proof
lattice.add('hash', (x: string) => x.length, {
  id: 1,
  theorem: "∀x. hash(x) ≥ 0",
  proof: "trivial",
  hash: "abc123"
});

// Encode to URL
const url = lattice.toURL('https://metameme.org/lattice');
// → https://metameme.org/lattice?props=hash&proofs=abc123

// Decode from URL
const restored = Lattice.fromURL(url);

// URL sharding
const shards = URLProof.shard(url, 3);
// → ['https://metameme.org/lattice/shard/0', ...]
```

## Features

- **Pure Functions**: All functions are pure and composable
- **URL-Encoded Proofs**: Mathematical properties in URL fragments
- **Proof Sharding**: Split proofs across multiple URL shards
- **Sandbox Safe**: Run in any JavaScript sandbox
- **Lean4 Backend**: Formal verification via Lean4

## URL Format

```
https://base.url?props=fn1;fn2&proofs=hash1,hash2#proof/1/hash/data
```

- `props`: Semicolon-separated function names
- `proofs`: Comma-separated proof hashes
- Fragment: Base64-encoded proof shard

## License

AGPL-3.0 - See LICENSE file for details
