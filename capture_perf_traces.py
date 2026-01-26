#!/usr/bin/env python3
"""Capture all perf traces to Parquet for self-recognition"""

import subprocess
import pandas as pd
import time
from pathlib import Path

def run_with_perf(binary, label):
    """Run binary with perf stat and capture metrics"""
    cmd = [
        'perf', 'stat', '-e',
        'cycles,instructions,cache-misses,branches,branch-misses',
        binary
    ]
    
    start = time.time_ns()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time_ns() - start
    
    # Parse perf output
    perf_output = result.stderr
    metrics = {
        'label': label,
        'binary': binary,
        'elapsed_ns': elapsed,
        'cycles': 0,
        'instructions': 0,
        'cache_misses': 0,
        'branches': 0,
        'branch_misses': 0,
    }
    
    for line in perf_output.split('\n'):
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        
        value = parts[0].replace(',', '')
        if not value.isdigit():
            continue
        value = int(value)
        
        if 'cycles' in line:
            metrics['cycles'] = value
        elif 'instructions' in line:
            metrics['instructions'] = value
        elif 'cache-misses' in line:
            metrics['cache_misses'] = value
        elif 'branches' in line and 'branch-misses' not in line:
            metrics['branches'] = value
        elif 'branch-misses' in line:
            metrics['branch_misses'] = value
    
    # Calculate Monster weight
    metrics['monster_weight'] = (metrics['cycles'] + metrics['instructions'] + metrics['cache_misses']) % 196883
    metrics['resonates'] = metrics['monster_weight'] < 10000
    
    return metrics

def main():
    print("=== Capturing Perf Traces to Parquet ===\n")
    
    traces = []
    
    # 1. C (GCC) - O0
    print("1. Capturing C (GCC) O0...")
    traces.append(run_with_perf('/tmp/automorphic_c_gcc', 'C_GCC_O0'))
    
    # 2. C (Clang) - O0
    print("2. Capturing C (Clang) O0...")
    traces.append(run_with_perf('/tmp/automorphic_c_clang', 'C_Clang_O0'))
    
    # 3. Rust - O0
    print("3. Capturing Rust O0...")
    traces.append(run_with_perf('./target/debug/perf_automorphic_loop', 'Rust_O0'))
    
    # 4. Rust - O3
    print("4. Capturing Rust O3...")
    traces.append(run_with_perf('./target/release/perf_automorphic_loop', 'Rust_O3'))
    
    # Create DataFrame
    df = pd.DataFrame(traces)
    
    # Save to Parquet
    output_file = 'plocate_witness/automorphic_traces.parquet'
    Path('plocate_witness').mkdir(exist_ok=True)
    df.to_parquet(output_file, compression='snappy')
    
    print(f"\n✓ Saved {len(traces)} traces to {output_file}")
    print(f"  Size: {Path(output_file).stat().st_size} bytes")
    
    # Display summary
    print("\n=== Trace Summary ===")
    print(df[['label', 'cycles', 'monster_weight', 'resonates']].to_string(index=False))
    
    print("\n✓ Ready for self-recognition")

if __name__ == '__main__':
    main()
