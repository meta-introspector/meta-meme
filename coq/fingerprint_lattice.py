#!/usr/bin/env python3
"""
Observe MetaCoq operating on each lattice order and fingerprint it.
Captures perf data for each proof level 0→71.
"""

import subprocess
import json
import hashlib
from pathlib import Path

ZOS_PRIMES = [0, 1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

def compile_proof(level: int) -> dict:
    """Compile single proof with perf monitoring."""
    coq_code = f"""
Require Import Nat.
Definition proof_{level} : nat := {level}.
Theorem proof_{level}_valid : proof_{level} = {level}.
Proof. reflexivity. Qed.
"""
    
    # Write temp file
    temp_file = Path(f"/tmp/proof_{level}.v")
    temp_file.write_text(coq_code)
    
    # Compile with perf
    cmd = [
        "nix-shell", "-p", "coq_8_18", "perf", "--run",
        f"perf stat -e cycles,instructions,cache-misses coqc {temp_file} 2>&1"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/mnt/data1/time2/time/2023/07/30/meta-meme/coq")
    
    # Parse perf output
    cycles = 0
    instructions = 0
    cache_misses = 0
    
    for line in result.stdout.split('\n'):
        if 'cycles' in line and 'cpu_core' in line:
            cycles = int(line.split()[0].replace(',', ''))
        elif 'instructions' in line and 'cpu_core' in line:
            instructions = int(line.split()[0].replace(',', ''))
        elif 'cache-misses' in line and 'cpu_core' in line:
            cache_misses = int(line.split()[0].replace(',', ''))
    
    # Fingerprint: hash of perf metrics
    fingerprint_data = f"{level}:{cycles}:{instructions}:{cache_misses}"
    fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
    
    return {
        "level": level,
        "cycles": cycles,
        "instructions": instructions,
        "cache_misses": cache_misses,
        "fingerprint": fingerprint,
        "complexity": level
    }

def main():
    print("🔬 Observing MetaCoq on lattice orders 0→71")
    print("=" * 60)
    
    fingerprints = []
    
    for level in ZOS_PRIMES:
        print(f"[{level:2d}/71] Compiling proof_{level}...", end=" ", flush=True)
        
        try:
            fp = compile_proof(level)
            fingerprints.append(fp)
            print(f"✓ {fp['fingerprint']} ({fp['cycles']:,} cycles)")
        except Exception as e:
            print(f"✗ {e}")
    
    # Save fingerprints
    output_file = Path("/mnt/data1/time2/time/2023/07/30/meta-meme/coq/lattice_fingerprints.json")
    output_file.write_text(json.dumps(fingerprints, indent=2))
    
    print("\n" + "=" * 60)
    print(f"✅ Fingerprinted {len(fingerprints)} proofs")
    print(f"📊 Total cycles: {sum(f['cycles'] for f in fingerprints):,}")
    print(f"💾 Saved to: {output_file}")
    
    # Print fingerprint lattice
    print("\nFingerprint Lattice:")
    for fp in fingerprints[:10]:  # First 10
        print(f"  {fp['level']:2d} → {fp['fingerprint']} ({fp['cycles']:,} cycles)")
    print(f"  ...")
    for fp in fingerprints[-3:]:  # Last 3
        print(f"  {fp['level']:2d} → {fp['fingerprint']} ({fp['cycles']:,} cycles)")

if __name__ == "__main__":
    main()
