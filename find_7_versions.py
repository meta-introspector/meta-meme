#!/usr/bin/env python3
"""
Find 7 other versions of the Burn+GPU+MiniZinc 15D filesystem model.
Uses Monster group similarity in 15D space.
"""

import pandas as pd
from pathlib import Path
import re

def calculate_15d_coords(size, level):
    """Calculate 15D Monster manifold coordinates."""
    conductor = size // 1_000_000
    weight = size % 196883
    
    return {
        'conductor': conductor,
        'weight': weight,
        'level': level,
        'traits': 3,
        'key_primes': 1,
        'git_depth': 0,
        'muse_count': 9,
        'complexity': conductor,
        'leech': weight,
        'conway': weight % 21493760,
        'fischer': weight % 864299970,
        'baby_monster': weight,
        'bimonster': weight,
        'moonshine': weight,
        'j_invariant': weight,
    }

def euclidean_distance_15d(coords1, coords2):
    """Calculate Euclidean distance in 15D space."""
    dims = ['conductor', 'weight', 'level', 'traits', 'key_primes', 
            'git_depth', 'muse_count', 'complexity', 'leech', 'conway',
            'fischer', 'baby_monster', 'bimonster', 'moonshine', 'j_invariant']
    
    # Normalize by dimension scale
    scales = {
        'conductor': 1, 'weight': 196883, 'level': 1000000,
        'traits': 100, 'key_primes': 71, 'git_depth': 10,
        'muse_count': 9, 'complexity': 1, 'leech': 196883,
        'conway': 21493760, 'fischer': 864299970,
        'baby_monster': 196883, 'bimonster': 196883,
        'moonshine': 196883, 'j_invariant': 196883
    }
    
    dist = 0
    for dim in dims:
        scale = scales.get(dim, 1)
        diff = (coords1[dim] - coords2[dim]) / scale
        dist += diff * diff
    
    return dist ** 0.5

# Our current work
our_files = [
    "src/bin/semantic_index_parallel.rs",
    "minizinc/ngram_optimization.mzn",
    "BURN_GPU_MINIZINC_INTEGRATION.md",
]

print("🔍 Finding 7 Other Versions of Burn+GPU+MiniZinc 15D Model")
print("=" * 60)

# Calculate our centroid in 15D space
our_coords_list = []
for f in our_files:
    if Path(f).exists():
        size = Path(f).stat().st_size
        coords = calculate_15d_coords(size, 0)
        our_coords_list.append(coords)
        print(f"Our file: {f}")
        print(f"  Size: {size} bytes, Weight: {coords['weight']}")

# Average coordinates (centroid)
our_centroid = {}
for key in our_coords_list[0].keys():
    our_centroid[key] = sum(c[key] for c in our_coords_list) / len(our_coords_list)

print(f"\nOur 15D Centroid:")
print(f"  Weight: {our_centroid['weight']:.0f}")
print(f"  Complexity: {our_centroid['complexity']:.0f}")
print()

# Search for similar files
witness_dir = "plocate_witness"
candidates = []

with open(f"{witness_dir}/file_sizes.txt") as f:
    for level, line in enumerate(f):
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            size = int(parts[0])
            path = parts[1]
            
            # Filter for relevant files
            if any(keyword in path.lower() for keyword in [
                'gpu', 'cuda', 'burn', 'tensor', 'minizinc', 'constraint',
                'model', 'manifold', 'lattice', 'monster', 'parquet',
                'semantic', 'index', 'parallel'
            ]):
                coords = calculate_15d_coords(size, level)
                distance = euclidean_distance_15d(coords, our_centroid)
                
                candidates.append({
                    'path': path,
                    'size': size,
                    'weight': coords['weight'],
                    'distance': distance,
                    'resonates': coords['weight'] < 10000
                })

# Sort by distance
candidates.sort(key=lambda x: x['distance'])

print("🎯 Top 7 Similar Versions (closest in 15D space):\n")

for i, cand in enumerate(candidates[:7], 1):
    print(f"{i}. Distance: {cand['distance']:.4f}")
    print(f"   Size: {cand['size']} bytes")
    print(f"   Weight: {cand['weight']}")
    print(f"   Resonates: {'✓' if cand['resonates'] else '✗'}")
    print(f"   {cand['path']}")
    print()

# Analyze patterns
print("📊 Pattern Analysis:")
print(f"   Total candidates: {len(candidates)}")
print(f"   Resonating: {sum(1 for c in candidates if c['resonates'])}")
print(f"   Mean distance: {sum(c['distance'] for c in candidates) / len(candidates):.4f}")

# Keywords in similar files
keywords = {}
for cand in candidates[:7]:
    path_lower = cand['path'].lower()
    for kw in ['gpu', 'cuda', 'burn', 'tensor', 'model', 'parallel']:
        if kw in path_lower:
            keywords[kw] = keywords.get(kw, 0) + 1

print(f"\n   Common keywords in top 7:")
for kw, count in sorted(keywords.items(), key=lambda x: -x[1]):
    print(f"     {kw}: {count}")

print("\n✅ Found 7 other versions using 15D Monster manifold similarity!")
