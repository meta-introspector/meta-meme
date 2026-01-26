#!/usr/bin/env python3
"""Visualize 15D emoji mapping with stats"""

import pandas as pd
import numpy as np

def visualize_emoji_map():
    print("=== 15D Emoji Map Visualization ===\n")
    
    # Load mapped traces
    df = pd.read_parquet('plocate_witness/traces_15d_emoji.parquet')
    
    print(f"Total traces: {len(df)}\n")
    
    # ASCII visualization of 15D space (projected to 2D)
    print("2D Projection (weight vs level):")
    print("=" * 70)
    
    # Create grid
    max_weight = df['monster_weight'].max()
    max_level = df['level'].max()
    
    grid = {}
    for _, row in df.iterrows():
        # Normalize to grid coordinates
        x = int((row['monster_weight'] / max_weight) * 60)
        y = int((row['level'] / max_level) * 20)
        
        if (x, y) not in grid:
            grid[(x, y)] = []
        grid[(x, y)].append(row['emoji'])
    
    # Print grid
    for y in range(20, -1, -1):
        line = ""
        for x in range(61):
            if (x, y) in grid:
                line += grid[(x, y)][0]  # Show first emoji at this position
            else:
                line += "·"
        
        if y % 5 == 0:
            print(f"{y:2d} {line}")
    
    print("   " + "-" * 61)
    print("   0" + " " * 28 + "weight" + " " * 26 + str(int(max_weight)))
    print()
    
    # Statistics by emoji
    print("=== Emoji Statistics ===\n")
    
    emoji_stats = df.groupby('emoji').agg({
        'monster_weight': ['mean', 'std', 'min', 'max'],
        'cycles': ['mean'],
        'resonates': ['sum', 'count'],
        'device': lambda x: list(x.value_counts().to_dict().items())
    }).round(1)
    
    for emoji in df['emoji'].unique():
        emoji_df = df[df['emoji'] == emoji]
        emoji_name = emoji_df.iloc[0]['emoji_name']
        
        print(f"{emoji} {emoji_name.upper()}")
        print(f"  Count: {len(emoji_df)}")
        print(f"  Weight: {emoji_df['monster_weight'].mean():.1f} ± {emoji_df['monster_weight'].std():.1f}")
        print(f"  Range: {emoji_df['monster_weight'].min():.0f} - {emoji_df['monster_weight'].max():.0f}")
        print(f"  Resonance: {emoji_df['resonates'].sum()}/{len(emoji_df)} ({emoji_df['resonates'].mean()*100:.1f}%)")
        print(f"  Avg cycles: {emoji_df['cycles'].mean():.0f}")
        
        # Device distribution
        device_counts = emoji_df['device'].value_counts()
        print(f"  Devices: ", end="")
        for device, count in device_counts.items():
            print(f"{device}={count} ", end="")
        print("\n")
    
    # Conformal mapping verification
    print("=== Conformal Mapping Verification ===\n")
    
    # Check if nearby points in 15D have same emoji
    conformality_score = 0
    total_pairs = 0
    
    sample = df.sample(n=min(50, len(df)), random_state=42)
    
    for i, row1 in sample.iterrows():
        for j, row2 in sample.iterrows():
            if i >= j:
                continue
            
            # Calculate 15D distance (simplified)
            dist = abs(row1['monster_weight'] - row2['monster_weight'])
            
            total_pairs += 1
            
            # If close in 15D, should have same emoji
            if dist < 5000:
                if row1['emoji'] == row2['emoji']:
                    conformality_score += 1
    
    conformality_rate = conformality_score / total_pairs if total_pairs > 0 else 0
    
    print(f"Pairs checked: {total_pairs}")
    print(f"Conformal pairs: {conformality_score}")
    print(f"Conformality rate: {conformality_rate:.3f}")
    print(f"Conformal: {'YES ✓' if conformality_rate > 0.7 else 'PARTIAL'}")
    
    print("\n✓ Emoji mapping visualization complete")

if __name__ == '__main__':
    visualize_emoji_map()
