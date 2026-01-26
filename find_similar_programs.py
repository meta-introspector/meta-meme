#!/usr/bin/env python3
"""
Find programs similar to semantic_index_parallel.rs
Uses file size and Monster weight as similarity metric.
"""

import pandas as pd
from pathlib import Path

# Our program's properties
our_file = "src/bin/semantic_index_parallel.rs"
our_size = Path(our_file).stat().st_size
our_weight = our_size % 196883
our_conductor = our_size // 1_000_000

print(f"🔍 Finding programs similar to {our_file}")
print(f"   Size: {our_size} bytes")
print(f"   Weight: {our_weight}")
print(f"   Conductor: {our_conductor}")
print()

# Load existing file data
witness_dir = "plocate_witness"
files = []

with open(f"{witness_dir}/file_sizes.txt") as f:
    for line in f:
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            size = int(parts[0])
            path = parts[1]
            weight = size % 196883
            conductor = size // 1_000_000
            
            # Similarity: how close in weight
            similarity = 1.0 / (1.0 + abs(weight - our_weight))
            
            files.append({
                'path': path,
                'size': size,
                'weight': weight,
                'conductor': conductor,
                'similarity': similarity,
                'size_diff': abs(size - our_size)
            })

df = pd.DataFrame(files)

# Find most similar
print("🎯 Top 10 Most Similar Programs (by Monster weight):\n")
similar = df.nlargest(10, 'similarity')

for i, row in similar.iterrows():
    print(f"{row['similarity']:.4f} similarity")
    print(f"  Size: {row['size']} bytes (diff: {row['size_diff']})")
    print(f"  Weight: {row['weight']} (ours: {our_weight})")
    print(f"  {row['path']}")
    print()

# Find by size
print("📏 Top 10 Most Similar by Size:\n")
by_size = df.nsmallest(10, 'size_diff')

for i, row in by_size.iterrows():
    print(f"Size diff: {row['size_diff']} bytes")
    print(f"  Size: {row['size']} bytes (ours: {our_size})")
    print(f"  Weight: {row['weight']}")
    print(f"  {row['path']}")
    print()

print("✅ Self-referential search complete!")
print(f"   Found {len(df)} files to compare")
print(f"   Our program resonates with {(our_weight < 10000)} (weight < 10000)")
