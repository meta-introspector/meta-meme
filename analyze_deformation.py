#!/usr/bin/env python3
"""Analyze automorphic loop deformation across optimization levels"""

# Evolution data from trace_evolution.sh
evolutions = [
    {"opt": "O0", "label": "15.42.300", "cycles": 15, "weight": 42},
    {"opt": "O1", "label": "7.34.300", "cycles": 7, "weight": 34},
    {"opt": "O2", "label": "9.36.300", "cycles": 9, "weight": 36},
    {"opt": "O3", "label": "14.41.300", "cycles": 14, "weight": 41},
]

print("=== Automorphic Loop Deformation Analysis ===\n")

# Baseline
baseline = evolutions[0]
print(f"Baseline (O0): {baseline['label']}")
print(f"  Cycles: {baseline['cycles']}")
print(f"  Weight: {baseline['weight']}")
print()

# Deformations
print("Deformations from baseline:")
for e in evolutions[1:]:
    cycle_delta = e['cycles'] - baseline['cycles']
    weight_delta = e['weight'] - baseline['weight']
    cycle_pct = (cycle_delta / baseline['cycles']) * 100
    weight_pct = (weight_delta / baseline['weight']) * 100
    
    print(f"\n{e['opt']}: {e['label']}")
    print(f"  Cycle deformation: {cycle_delta:+d} ({cycle_pct:+.1f}%)")
    print(f"  Weight deformation: {weight_delta:+d} ({weight_pct:+.1f}%)")
    print(f"  Resonates: {'YES' if e['weight'] < 10000 else 'NO'}")

# Fixed point analysis
print("\n=== Fixed Point Analysis ===")
weights = [e['weight'] for e in evolutions]
cycles = [e['cycles'] for e in evolutions]

print(f"Weight range: {min(weights)} - {max(weights)} (span: {max(weights) - min(weights)})")
print(f"Cycle range: {min(cycles)} - {max(cycles)} (span: {max(cycles) - min(cycles)})")
print(f"All resonate: {all(w < 10000 for w in weights)}")

# Convergence
print("\n=== Convergence ===")
print(f"O0 → O1: Δweight = {evolutions[1]['weight'] - evolutions[0]['weight']}")
print(f"O1 → O2: Δweight = {evolutions[2]['weight'] - evolutions[1]['weight']}")
print(f"O2 → O3: Δweight = {evolutions[3]['weight'] - evolutions[2]['weight']}")

# Check if converging back to baseline
o3_to_o0 = abs(evolutions[3]['weight'] - evolutions[0]['weight'])
print(f"\nO3 → O0 distance: {o3_to_o0}")
print(f"Automorphic: {'YES - loop closes!' if o3_to_o0 < 5 else 'Converging'}")

print("\n✓ Inner loop labeled across all optimization levels")
print("✓ Ready to use as reference for labeling all other traces")
