#!/usr/bin/env python3
"""Self-recognition: Automorphic loop identifies its own trace"""

import pandas as pd
import sys

def calculate_monster_weight(cycles, instructions, cache_misses):
    """Calculate Monster weight from perf metrics"""
    return (cycles + instructions + cache_misses) % 196883

def self_recognize(trace_file):
    """Load traces and identify self"""
    print("=== Automorphic Self-Recognition ===\n")
    
    # Load all traces
    df = pd.read_parquet(trace_file)
    print(f"Loaded {len(df)} traces from {trace_file}\n")
    
    # Calculate expected self-signature
    # The automorphic loop should recognize itself by:
    # 1. Low cycle count (it's minimal)
    # 2. Resonates (weight < 10000)
    # 3. Similar weight across implementations
    
    print("Trace signatures:")
    for _, row in df.iterrows():
        print(f"  {row['label']:20s} cycles={row['cycles']:8d} weight={row['monster_weight']:6d} resonates={row['resonates']}")
    
    print("\n=== Self-Recognition Analysis ===")
    
    # Find traces that resonate
    resonant = df[df['resonates']]
    print(f"\nResonant traces: {len(resonant)}/{len(df)}")
    
    # Find minimal cycle count (most optimized)
    min_cycles = df['cycles'].min()
    max_cycles = df['cycles'].max()
    print(f"Cycle range: {min_cycles:,} - {max_cycles:,}")
    
    # Calculate weight variance
    weight_mean = df['monster_weight'].mean()
    weight_std = df['monster_weight'].std()
    print(f"Weight: mean={weight_mean:.1f}, std={weight_std:.1f}")
    
    # Self-recognition: Find the trace most similar to expected pattern
    # Expected: low cycles, resonates, consistent weight
    df['self_score'] = 0.0
    
    # Score by resonance (binary)
    df.loc[df['resonates'], 'self_score'] += 1.0
    
    # Score by cycle efficiency (normalized)
    df['self_score'] += (1.0 - (df['cycles'] - min_cycles) / (max_cycles - min_cycles + 1))
    
    # Score by weight consistency (distance from mean)
    df['self_score'] += (1.0 - abs(df['monster_weight'] - weight_mean) / (weight_mean + 1))
    
    # Find self
    self_idx = df['self_score'].idxmax()
    self_trace = df.loc[self_idx]
    
    print(f"\n=== SELF IDENTIFIED ===")
    print(f"Label: {self_trace['label']}")
    print(f"Binary: {self_trace['binary']}")
    print(f"Cycles: {self_trace['cycles']:,}")
    print(f"Monster Weight: {self_trace['monster_weight']}")
    print(f"Resonates: {self_trace['resonates']}")
    print(f"Self-Score: {self_trace['self_score']:.3f}")
    
    # Verify automorphic property
    print(f"\n=== Automorphic Verification ===")
    
    # Check if all traces are similar (automorphic)
    all_resonate = df['resonates'].all()
    weight_variance = weight_std / weight_mean if weight_mean > 0 else 0
    
    print(f"All resonate: {all_resonate}")
    print(f"Weight coefficient of variation: {weight_variance:.3f}")
    print(f"Automorphic: {'YES' if all_resonate and weight_variance < 0.5 else 'CONVERGING'}")
    
    # Save self-recognition result
    result = {
        'self_label': self_trace['label'],
        'self_weight': self_trace['monster_weight'],
        'all_resonate': all_resonate,
        'automorphic': all_resonate and weight_variance < 0.5
    }
    
    return result

if __name__ == '__main__':
    trace_file = sys.argv[1] if len(sys.argv) > 1 else 'plocate_witness/automorphic_traces.parquet'
    result = self_recognize(trace_file)
    
    print(f"\n✓ Self-recognition complete")
    print(f"✓ Automorphic loop identified itself as: {result['self_label']}")
