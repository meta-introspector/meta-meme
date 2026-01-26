#!/usr/bin/env python3
"""Real-time perf trace to emoji bitmap converter"""

import sys
import time
import subprocess
from pathlib import Path

# Emoji to ASCII art mapping (8x8 blocks)
EMOJI_BITMAPS = {
    '⚡': [
        "  ▄▄    ",
        " ████   ",
        "  ██    ",
        " ████   ",
        "  ██    ",
        "   ██   ",
        "   ▀    ",
        "        "
    ],
    '🚀': [
        "   ▄    ",
        "  ███   ",
        " █████  ",
        "███████ ",
        " █████  ",
        "  ███   ",
        "  ▀▀▀   ",
        "        "
    ],
    '🔥': [
        "   ▄    ",
        "  ███   ",
        " █████  ",
        "███████ ",
        "███████ ",
        " █████  ",
        "  ███   ",
        "   ▀    "
    ],
    '💎': [
        "   ▄    ",
        "  ███   ",
        " █████  ",
        "███████ ",
        " █████  ",
        "  ███   ",
        "   ▀    ",
        "        "
    ],
    '🌊': [
        "        ",
        " ▄▄▄▄   ",
        "██████  ",
        "▀▀████  ",
        "  ▀▀██  ",
        "    ▀▀  ",
        "        ",
        "        "
    ],
    '🌀': [
        "  ▄▄▄   ",
        " ██▀██  ",
        "██  ██  ",
        "██ ▄██  ",
        " ████   ",
        "  ▀▀    ",
        "        ",
        "        "
    ],
    '🎯': [
        "  ▄▄▄   ",
        " █████  ",
        "███▄███ ",
        "███████ ",
        " █████  ",
        "  ▀▀▀   ",
        "        ",
        "        "
    ],
    '🧠': [
        " ▄▄▄▄▄  ",
        "███████ ",
        "███▄███ ",
        "███████ ",
        "███████ ",
        " █████  ",
        "  ▀▀▀   ",
        "        "
    ],
}

def weight_to_emoji(weight):
    """Convert Monster weight to emoji"""
    if weight < 3000:
        return '⚡'
    elif weight < 5000:
        return '🚀'
    elif weight < 7000:
        return '🔥'
    elif weight < 10000:
        return '💎'
    elif weight < 50000:
        return '🌊'
    else:
        return '🌀'

def emoji_to_bitmap(emoji):
    """Get ASCII bitmap for emoji"""
    return EMOJI_BITMAPS.get(emoji, EMOJI_BITMAPS['🔥'])

def parse_perf_line(line):
    """Parse perf stat output line"""
    parts = line.strip().split()
    if len(parts) < 2:
        return None
    
    try:
        value = int(parts[0].replace(',', ''))
        metric = ' '.join(parts[1:])
        return (metric, value)
    except:
        return None

def ingest_perf_trace(command):
    """Run command with perf and convert to emoji bitmap"""
    
    # Run with perf stat
    perf_cmd = [
        'perf', 'stat', '-e',
        'cycles,instructions,cache-misses',
        '--', *command
    ]
    
    result = subprocess.run(perf_cmd, capture_output=True, text=True)
    
    # Parse perf output
    cycles = 0
    instructions = 0
    cache_misses = 0
    
    for line in result.stderr.split('\n'):
        parsed = parse_perf_line(line)
        if not parsed:
            continue
        
        metric, value = parsed
        if 'cycles' in metric:
            cycles = value
        elif 'instructions' in metric:
            instructions = value
        elif 'cache-misses' in metric:
            cache_misses = value
    
    # Calculate Monster weight
    weight = (cycles + instructions + cache_misses) % 196883
    
    # Convert to emoji
    emoji = weight_to_emoji(weight)
    
    return {
        'cycles': cycles,
        'instructions': instructions,
        'cache_misses': cache_misses,
        'weight': weight,
        'emoji': emoji,
        'resonates': weight < 10000
    }

def render_bitmap(traces, width=10):
    """Render traces as emoji bitmap"""
    
    # Pad to full rows
    while len(traces) % width != 0:
        traces.append({'emoji': '🔥', 'weight': 0})
    
    rows = len(traces) // width
    
    # Render 8 lines per row of emojis
    for row in range(rows):
        for line in range(8):
            output = ""
            for col in range(width):
                idx = row * width + col
                if idx < len(traces):
                    emoji = traces[idx]['emoji']
                    bitmap = emoji_to_bitmap(emoji)
                    output += bitmap[line] + " "
            print(output)
        print()  # Blank line between rows

def main():
    print("=== Real-Time Perf→Emoji→Bitmap Ingestor ===\n")
    
    if len(sys.argv) < 2:
        print("Usage: perf2emoji_bitmap.py <command> [args...]")
        print("\nExample: perf2emoji_bitmap.py ./target/debug/perf_automorphic_loop")
        print("         perf2emoji_bitmap.py ls -la")
        sys.exit(1)
    
    command = sys.argv[1:]
    
    print(f"Ingesting: {' '.join(command)}")
    print(f"Running 10 iterations...\n")
    
    traces = []
    
    for i in range(10):
        print(f"Iteration {i+1}/10...", end=' ', flush=True)
        
        trace = ingest_perf_trace(command)
        traces.append(trace)
        
        emoji = trace['emoji']
        weight = trace['weight']
        resonates = '✓' if trace['resonates'] else '✗'
        
        print(f"{emoji} weight={weight:6d} {resonates}")
    
    print("\n" + "="*70)
    print("EMOJI BITMAP")
    print("="*70 + "\n")
    
    render_bitmap(traces, width=5)
    
    # Statistics
    print("="*70)
    print("STATISTICS")
    print("="*70)
    
    from collections import Counter
    emoji_counts = Counter(t['emoji'] for t in traces)
    
    print("\nEmoji Distribution:")
    for emoji, count in emoji_counts.most_common():
        pct = (count / len(traces)) * 100
        print(f"  {emoji}: {count:2d} ({pct:5.1f}%)")
    
    resonant = sum(1 for t in traces if t['resonates'])
    print(f"\nResonance: {resonant}/{len(traces)} ({resonant/len(traces)*100:.1f}%)")
    
    avg_weight = sum(t['weight'] for t in traces) / len(traces)
    print(f"Avg weight: {avg_weight:.1f}")
    
    print("\n✓ Real-time perf→emoji→bitmap complete")

if __name__ == '__main__':
    main()
