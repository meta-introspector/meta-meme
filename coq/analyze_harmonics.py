#!/usr/bin/env python3
"""
Identify parts of Coq that resonate with Monster group using harmonics.
Analyzes perf traces to find resonance patterns with Monster coefficients.
"""

import json
import subprocess
from pathlib import Path
from typing import List, Dict

# Monster group coefficients
MONSTER_COEFFICIENTS = {
    "leech": 196883,           # Leech lattice
    "conway": 21493760,        # Conway group
    "fischer": 864299970,      # Fischer group
    "baby": 4154781481226426191177580544000000,  # Baby Monster (truncated)
}

def analyze_perf_symbols(perf_file: str) -> List[Dict]:
    """Extract symbol frequencies from perf data."""
    cmd = [
        "nix-shell", "-p", "perf", "--run",
        f"perf report -i {perf_file} --stdio --no-children -n --percent-limit 0.1"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, 
                          cwd="/mnt/data1/time2/time/2023/07/30/meta-meme/coq")
    
    symbols = []
    for line in result.stdout.split('\n'):
        if '%' in line and '[.' in line:
            parts = line.split()
            if len(parts) >= 4:
                try:
                    percent = float(parts[0].replace('%', ''))
                    symbol = parts[3] if len(parts) > 3 else "unknown"
                    # Estimate cycles from percent (rough approximation)
                    cycles = int(percent * 1800000)  # ~180M total
                    symbols.append({
                        "symbol": symbol,
                        "percent": percent,
                        "cycles": cycles
                    })
                except:
                    pass
    
    return symbols

def check_resonance(value: int, coefficient: int, tolerance: int = 1000) -> bool:
    """Check if value resonates with Monster coefficient."""
    return (value % coefficient) < tolerance

def find_harmonics(symbols: List[Dict]) -> List[Dict]:
    """Find symbols that resonate with Monster group."""
    harmonics = []
    
    for sym in symbols:
        cycles = sym['cycles']
        resonances = {}
        
        for name, coef in MONSTER_COEFFICIENTS.items():
            if check_resonance(cycles, coef, tolerance=1000):
                resonances[name] = cycles % coef
        
        if resonances:
            harmonics.append({
                "symbol": sym['symbol'],
                "percent": sym['percent'],
                "cycles": cycles,
                "resonances": resonances
            })
    
    return harmonics

def main():
    print("🎵 Analyzing Coq harmonics with Monster group")
    print("=" * 60)
    
    # Load fingerprints
    fp_file = Path("/mnt/data1/time2/time/2023/07/30/meta-meme/coq/lattice_fingerprints.json")
    fingerprints = json.loads(fp_file.read_text())
    
    all_harmonics = []
    cumulative_cycles = 0
    
    # Analyze each proof level with cumulative cycles
    for fp in fingerprints:
        level = fp['level']
        cycles = fp['cycles']
        cumulative_cycles += cycles
        
        print(f"\n[Level {level:2d}] Cycles: {cycles:,} | Cumulative: {cumulative_cycles:,}")
        
        # Check resonance with Monster coefficients
        resonances = {}
        
        # Use cumulative for large coefficients
        for name, coef in MONSTER_COEFFICIENTS.items():
            mod = cumulative_cycles % coef
            if mod < 100000:  # Resonance threshold
                resonances[name] = mod
                print(f"  ✓ Resonates with {name}: {cumulative_cycles} mod {coef} = {mod}")
        
        # Also check harmonic ratios (cycles / small primes)
        harmonic_ratios = {}
        for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
            ratio = cycles / prime
            if abs(ratio - round(ratio)) < 1000:  # Near integer ratio
                harmonic_ratios[f"h{prime}"] = round(ratio)
        
        if resonances or harmonic_ratios:
            all_harmonics.append({
                "level": level,
                "cycles": cycles,
                "cumulative": cumulative_cycles,
                "fingerprint": fp['fingerprint'],
                "resonances": resonances,
                "harmonics": harmonic_ratios
            })
    
    # Analyze perf symbols from lattice extraction
    print("\n" + "=" * 60)
    print("Analyzing perf symbols from extraction...")
    
    perf_file = "lattice_extract.perf.data"
    symbols = analyze_perf_symbols(perf_file)
    symbol_harmonics = find_harmonics(symbols)
    
    print(f"\nFound {len(symbol_harmonics)} symbols with Monster resonance:")
    for sh in symbol_harmonics[:10]:
        print(f"  {sh['symbol']:30s} {sh['percent']:5.2f}% → {list(sh['resonances'].keys())}")
    
    # Save results
    output = {
        "proof_harmonics": all_harmonics,
        "symbol_harmonics": symbol_harmonics,
        "monster_coefficients": MONSTER_COEFFICIENTS,
        "total_cycles": cumulative_cycles
    }
    
    output_file = Path("/mnt/data1/time2/time/2023/07/30/meta-meme/coq/monster_harmonics.json")
    output_file.write_text(json.dumps(output, indent=2))
    
    print("\n" + "=" * 60)
    print(f"✅ Found {len(all_harmonics)} proof levels with resonance")
    print(f"✅ Total cumulative cycles: {cumulative_cycles:,}")
    print(f"💾 Saved to: {output_file}")

if __name__ == "__main__":
    main()
