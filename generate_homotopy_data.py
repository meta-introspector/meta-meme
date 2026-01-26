#!/usr/bin/env python3
"""Generate MiniZinc data file from perf traces"""

import pandas as pd

def generate_minizinc_data():
    # Load traces
    df = pd.read_parquet('plocate_witness/dual_optimizer_traces.parquet')
    
    cpu_df = df[df['device'] == 'cpu'].sort_values('epoch')
    gpu_df = df[df['device'] == 'gpu'].sort_values('epoch')
    
    cpu_weights = cpu_df['monster_weight'].tolist()
    gpu_weights = gpu_df['monster_weight'].tolist()
    
    # Generate .dzn file
    with open('minizinc/homotopy_data.dzn', 'w') as f:
        f.write(f"n_epochs = {len(cpu_weights)};\n\n")
        
        f.write("cpu_weights = [\n")
        for i, w in enumerate(cpu_weights):
            f.write(f"  {w}")
            if i < len(cpu_weights) - 1:
                f.write(",\n")
        f.write("\n];\n\n")
        
        f.write("gpu_weights = [\n")
        for i, w in enumerate(gpu_weights):
            f.write(f"  {w}")
            if i < len(gpu_weights) - 1:
                f.write(",\n")
        f.write("\n];\n")
    
    print("✓ Generated minizinc/homotopy_data.dzn")
    print(f"  CPU epochs: {len(cpu_weights)}")
    print(f"  GPU epochs: {len(gpu_weights)}")

if __name__ == '__main__':
    generate_minizinc_data()
