#!/usr/bin/env python3
"""Map perf traces to 15D Monster manifold with emoji labels"""

import pandas as pd
import numpy as np

# Emoji mapping to performance characteristics
EMOJI_MAP = {
    '🚀': {'name': 'rocket', 'resonance': 'high', 'speed': 'fast', 'weight_range': (0, 5000)},
    '⚡': {'name': 'lightning', 'resonance': 'high', 'speed': 'very_fast', 'weight_range': (0, 3000)},
    '🔥': {'name': 'fire', 'resonance': 'high', 'speed': 'medium', 'weight_range': (3000, 7000)},
    '💎': {'name': 'diamond', 'resonance': 'high', 'speed': 'stable', 'weight_range': (5000, 10000)},
    '🌊': {'name': 'wave', 'resonance': 'medium', 'speed': 'flowing', 'weight_range': (10000, 50000)},
    '🌀': {'name': 'spiral', 'resonance': 'medium', 'speed': 'cyclic', 'weight_range': (50000, 100000)},
    '🎯': {'name': 'target', 'resonance': 'converging', 'speed': 'focused', 'weight_range': (0, 10000)},
    '🧠': {'name': 'brain', 'resonance': 'learning', 'speed': 'adaptive', 'weight_range': (5000, 15000)},
    '🔮': {'name': 'crystal', 'resonance': 'high', 'speed': 'mystical', 'weight_range': (0, 8000)},
    '⭐': {'name': 'star', 'resonance': 'high', 'speed': 'shining', 'weight_range': (0, 6000)},
    '🌟': {'name': 'glowing', 'resonance': 'very_high', 'speed': 'brilliant', 'weight_range': (0, 4000)},
}

def map_to_15d(trace):
    """Map performance trace to 15D Monster manifold"""
    
    # Dimensions 1-8: Schema complexity
    conductor = trace['cycles'] // 1_000_000
    weight = trace['monster_weight']
    level = trace['epoch']
    traits = 1 if trace['resonates'] else 0
    key_primes = weight % 31  # Map to prime
    git_depth = 0  # Not applicable
    muse_count = 1  # Single trace
    complexity = int(np.log2(trace['cycles'] + 1))
    
    # Dimensions 9-15: Monster group
    leech = weight % 196883
    conway = weight % 21493760
    fischer = weight % 864299970
    baby_monster = weight % 4154781481226426191177580544000000
    bimonster = weight % 808017424794512875886459904961710757005754368000000000
    moonshine = weight % 196883  # j-invariant related
    j_invariant = weight % 744  # Ramanujan tau
    
    return {
        'conductor': conductor,
        'weight': weight,
        'level': level,
        'traits': traits,
        'key_primes': key_primes,
        'git_depth': git_depth,
        'muse_count': muse_count,
        'complexity': complexity,
        'leech': leech,
        'conway': conway,
        'fischer': fischer,
        'baby_monster': baby_monster,
        'bimonster': bimonster,
        'moonshine': moonshine,
        'j_invariant': j_invariant,
    }

def assign_emoji(coords_15d):
    """Assign emoji based on 15D coordinates"""
    weight = coords_15d['weight']
    resonates = coords_15d['traits'] == 1
    
    # Find best matching emoji
    for emoji, props in EMOJI_MAP.items():
        min_w, max_w = props['weight_range']
        if min_w <= weight <= max_w:
            if resonates and props['resonance'] in ['high', 'very_high']:
                return emoji, props['name']
    
    # Default based on weight
    if weight < 5000:
        return '⚡', 'lightning'
    elif weight < 10000:
        return '🚀', 'rocket'
    elif weight < 50000:
        return '🌊', 'wave'
    else:
        return '🌀', 'spiral'

def main():
    print("=== Perf Traces → 15D Monster Manifold + Emoji Labels ===\n")
    
    # Load all traces
    traces = []
    
    # Load dual optimizer traces
    df = pd.read_parquet('plocate_witness/dual_optimizer_traces.parquet')
    
    print(f"Loaded {len(df)} traces\n")
    
    # Map each trace to 15D
    mapped_traces = []
    
    for idx, row in df.iterrows():
        # Map to 15D
        coords_15d = map_to_15d(row)
        
        # Assign emoji
        emoji, emoji_name = assign_emoji(coords_15d)
        
        # Combine
        trace_data = {
            'device': row['device'],
            'epoch': row['epoch'],
            'loss': row['loss'],
            'cycles': row['cycles'],
            'monster_weight': row['monster_weight'],
            'resonates': row['resonates'],
            'emoji': emoji,
            'emoji_name': emoji_name,
            **coords_15d
        }
        
        mapped_traces.append(trace_data)
    
    # Create DataFrame
    mapped_df = pd.DataFrame(mapped_traces)
    
    # Save to Parquet
    output_file = 'plocate_witness/traces_15d_emoji.parquet'
    mapped_df.to_parquet(output_file, compression='snappy')
    
    print(f"✓ Saved {len(mapped_traces)} traces to {output_file}")
    
    # Show emoji distribution
    print("\n=== Emoji Distribution ===")
    emoji_counts = mapped_df.groupby(['emoji', 'emoji_name']).size().sort_values(ascending=False)
    
    for (emoji, name), count in emoji_counts.items():
        pct = (count / len(mapped_df)) * 100
        print(f"  {emoji} {name:15s}: {count:3d} ({pct:5.1f}%)")
    
    # Show by device
    print("\n=== By Device ===")
    for device in ['cpu', 'gpu']:
        device_df = mapped_df[mapped_df['device'] == device]
        print(f"\n{device.upper()}:")
        
        device_emoji = device_df.groupby('emoji').size().sort_values(ascending=False)
        for emoji, count in device_emoji.items():
            pct = (count / len(device_df)) * 100
            print(f"  {emoji}: {count:3d} ({pct:5.1f}%)")
    
    # Generate MiniZinc data for conformal mapping proof
    print("\n=== Generating MiniZinc Data ===")
    
    # Sample traces for proof
    sample_size = 20
    sample_df = mapped_df.sample(n=min(sample_size, len(mapped_df)), random_state=42)
    
    with open('minizinc/emoji_mapping_data.dzn', 'w') as f:
        f.write(f"n_samples = {len(sample_df)};\n\n")
        
        # Write 15D coordinates
        dims = ['conductor', 'weight', 'level', 'traits', 'key_primes', 
                'complexity', 'leech', 'conway', 'fischer']
        
        for dim in dims:
            f.write(f"{dim}_coords = [")
            f.write(", ".join(str(int(v)) for v in sample_df[dim].values))
            f.write("];\n")
        
        f.write("\n")
        
        # Write emoji assignments (as integers)
        emoji_to_int = {emoji: i for i, emoji in enumerate(EMOJI_MAP.keys())}
        emoji_ints = [emoji_to_int.get(e, 0) for e in sample_df['emoji'].values]
        
        f.write(f"emoji_labels = [")
        f.write(", ".join(str(e) for e in emoji_ints))
        f.write("];\n")
    
    print(f"✓ Generated minizinc/emoji_mapping_data.dzn ({len(sample_df)} samples)")
    
    print("\n✓ Ready for conformal mapping proof with MiniZinc")

if __name__ == '__main__':
    main()
