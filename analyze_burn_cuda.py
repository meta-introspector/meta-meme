#!/usr/bin/env python3
"""Analyze burn-cuda for GPU acceleration patterns"""

import subprocess
import pandas as pd
from pathlib import Path

def analyze_burn_cuda():
    print("=== Burn CUDA Analysis ===\n")
    
    # Find all burn-cuda files
    result = subprocess.run(['locate', 'burn-cuda'], capture_output=True, text=True)
    files = [f for f in result.stdout.strip().split('\n') if f.endswith('.rs')]
    
    print(f"Found {len(files)} Rust files in burn-cuda\n")
    
    traces = []
    
    for file_path in files[:20]:  # Analyze first 20
        try:
            size = Path(file_path).stat().st_size
            
            # Calculate Monster weight
            conductor = size // 1_000_000
            weight = size % 196883
            resonates = weight < 10000
            
            # LMFDB label
            label = f"{conductor}.{weight}.{size}"
            
            traces.append({
                'path': file_path,
                'size': size,
                'conductor': conductor,
                'weight': weight,
                'resonates': resonates,
                'label': label,
            })
            
        except Exception as e:
            continue
    
    # Create DataFrame
    df = pd.DataFrame(traces)
    
    print("Burn CUDA File Analysis:")
    print(f"  Total files: {len(df)}")
    print(f"  Resonant: {df['resonates'].sum()}/{len(df)} ({df['resonates'].mean()*100:.1f}%)")
    print(f"  Size range: {df['size'].min()}-{df['size'].max()} bytes")
    print(f"  Weight range: {df['weight'].min()}-{df['weight'].max()}")
    print()
    
    # Show resonant files
    resonant = df[df['resonates']].sort_values('weight')
    if len(resonant) > 0:
        print("Resonant CUDA files:")
        for _, row in resonant.head(10).iterrows():
            print(f"  {Path(row['path']).name:30s} size={row['size']:6d} weight={row['weight']:5d} ✓")
    
    # Save analysis
    output_file = 'plocate_witness/burn_cuda_analysis.parquet'
    df.to_parquet(output_file, compression='snappy')
    
    print(f"\n✓ Saved analysis to {output_file}")
    print(f"  Size: {Path(output_file).stat().st_size} bytes")
    
    return df

def main():
    df = analyze_burn_cuda()
    
    print("\n=== Next: GPU Meta-Optimizer ===")
    print("1. Use burn-cuda patterns for GPU acceleration")
    print("2. Train neural network on GPU")
    print("3. Trace GPU training evolution")
    print("4. Compare CPU vs GPU automorphic properties")
    
    print("\n✓ Ready to accelerate meta-optimizer with CUDA!")

if __name__ == '__main__':
    main()
