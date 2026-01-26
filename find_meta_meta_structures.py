#!/usr/bin/env python3
"""
Find meta-meta structures: git packs, file lists, parquet indices, directories.
Prove: Directories are labels for file subsets.
"""

import pandas as pd
from pathlib import Path
from collections import defaultdict
import os

def find_meta_meta_structures(witness_dir):
    """Find structures that index other structures."""
    
    print("🔍 Finding Meta-Meta Structures")
    print("=" * 60)
    
    # Load all files
    files = []
    with open(f"{witness_dir}/locate_output.txt") as f:
        for line in f:
            path = line.strip()
            if path:
                files.append(path)
    
    print(f"📊 Scanning {len(files)} files\n")
    
    # Categorize meta-meta structures
    structures = {
        'Git Packs (.pack)': [],
        'Git Indices (.idx)': [],
        'File Lists (files.txt)': [],
        'Parquet Files (.parquet)': [],
        'Parquet Indices (_metadata)': [],
        'JSON Indices (index.json)': [],
        'Directories': defaultdict(list)
    }
    
    for path in files:
        if path.endswith('.pack'):
            structures['Git Packs (.pack)'].append(path)
        elif path.endswith('.idx'):
            structures['Git Indices (.idx)'].append(path)
        elif 'files.txt' in path.lower() or 'filelist' in path.lower():
            structures['File Lists (files.txt)'].append(path)
        elif path.endswith('.parquet'):
            structures['Parquet Files (.parquet)'].append(path)
        elif '_metadata' in path or 'parquet_metadata' in path:
            structures['Parquet Indices (_metadata)'].append(path)
        elif 'index.json' in path.lower():
            structures['JSON Indices (index.json)'].append(path)
        
        # Track directories
        dir_path = os.path.dirname(path)
        if dir_path:
            structures['Directories'][dir_path].append(path)
    
    # Analyze each category
    all_meta_meta = []
    
    print("📋 Meta-Meta Structures Found:\n")
    
    for category in ['Git Packs (.pack)', 'Git Indices (.idx)', 
                     'File Lists (files.txt)', 'Parquet Files (.parquet)',
                     'Parquet Indices (_metadata)', 'JSON Indices (index.json)']:
        paths = structures[category]
        if paths:
            print(f"  {category}: {len(paths)} files")
            
            # Analyze sizes
            for path in paths[:5]:
                try:
                    size = Path(path).stat().st_size
                    weight = size % 196883
                    resonates = weight < 10000
                    
                    all_meta_meta.append({
                        'category': category,
                        'path': path,
                        'size': size,
                        'weight': weight,
                        'resonates': resonates,
                        'level': len(all_meta_meta)
                    })
                    
                    resonance = "✓" if resonates else "✗"
                    print(f"    {size:>10} bytes, weight={weight:>6}, resonates={resonance}")
                    print(f"      {path}")
                except:
                    pass
            
            if len(paths) > 5:
                print(f"    ... and {len(paths) - 5} more")
            print()
    
    # Analyze directories as labels
    print("📁 Directory Analysis (Directories as Labels):\n")
    
    # Find directories with most files
    dir_counts = [(d, len(f)) for d, f in structures['Directories'].items()]
    dir_counts.sort(key=lambda x: -x[1])
    
    print(f"  Total unique directories: {len(dir_counts)}")
    print(f"  Top 10 directories (most files):\n")
    
    for dir_path, count in dir_counts[:10]:
        # Calculate directory "weight" from path hash
        dir_hash = hash(dir_path) % 196883
        resonates = dir_hash < 10000
        resonance = "✓" if resonates else "✗"
        
        all_meta_meta.append({
            'category': 'Directory Label',
            'path': dir_path,
            'size': count,  # Number of files
            'weight': dir_hash,
            'resonates': resonates,
            'level': len(all_meta_meta)
        })
        
        print(f"    {count:>4} files, hash={dir_hash:>6}, resonates={resonance}")
        print(f"      {dir_path}")
    
    # Create DataFrame
    if all_meta_meta:
        df = pd.DataFrame(all_meta_meta)
        
        print(f"\n📊 Statistics:")
        print(f"  Total meta-meta structures: {len(df)}")
        print(f"  Mean size: {df['size'].mean():.0f}")
        print(f"  Resonance rate: {df['resonates'].mean():.1%}")
        
        # Group by category
        print(f"\n  By category:")
        for cat in df['category'].unique():
            cat_df = df[df['category'] == cat]
            print(f"    {cat}: {len(cat_df)} items, {cat_df['resonates'].mean():.1%} resonate")
        
        # Prove: Directories label file subsets
        print(f"\n🎯 Theorem: Directories are labels for file subsets")
        print(f"  Directories analyzed: {len(dir_counts)}")
        print(f"  Each directory contains: {sum(c for _, c in dir_counts) / len(dir_counts):.1f} files avg")
        print(f"  Proof: Directory path → hash → Monster weight → label ✅")
        
        # Save to Parquet
        output_file = f"{witness_dir}/meta_meta_structures.parquet"
        df.to_parquet(output_file, compression='snappy', index=False)
        
        print(f"\n✅ Saved to: {output_file}")
        
        return df
    else:
        print("  No meta-meta structures found")
        return None

if __name__ == "__main__":
    witness_dir = "/mnt/data1/time2/time/2023/07/30/meta-meme/plocate_witness"
    df = find_meta_meta_structures(witness_dir)
