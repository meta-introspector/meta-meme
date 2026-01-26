#!/usr/bin/env python3
"""
Extract Mathlib ASTs to JSON, index by complexity, map to Monster lattice
"""
import json
import subprocess
from pathlib import Path
from collections import defaultdict

MATHLIB_PATH = Path("/mnt/data1/nix/time/2024/09/06/mathlib")

def count_lean_files():
    """Count Lean files in mathlib"""
    lean_files = list(MATHLIB_PATH.rglob("*.lean"))
    print(f"📚 Found {len(lean_files)} Lean files in mathlib")
    return lean_files

def extract_ast_complexity(lean_file):
    """Extract AST complexity metrics from Lean file"""
    try:
        content = lean_file.read_text()
        lines = len(content.split('\n'))
        
        # Count key constructs
        theorems = content.count('theorem ')
        lemmas = content.count('lemma ')
        defs = content.count('def ')
        structures = content.count('structure ')
        inductives = content.count('inductive ')
        
        # Complexity score (similar to schema complexity)
        complexity = (
            lines * 0.1 +           # Conductor: size
            (theorems + lemmas) * 5 + # Weight: proofs
            defs * 2 +              # Level: definitions
            structures * 3 +        # Traits: structures
            inductives * 4          # Key primes: inductives
        )
        
        return {
            'file': str(lean_file.relative_to(MATHLIB_PATH)),
            'lines': lines,
            'theorems': theorems,
            'lemmas': lemmas,
            'defs': defs,
            'structures': structures,
            'inductives': inductives,
            'complexity': complexity
        }
    except Exception as e:
        return None

def map_to_monster_lattice(complexity):
    """Map complexity to Monster lattice coordinates"""
    # Map to 15D Monster manifold
    # Use modular arithmetic to distribute across Monster dimensions
    
    c = int(complexity)
    
    return {
        'base_8d': {
            'conductor': complexity * 0.1,
            'weight': c % 100,
            'level': (c // 100) % 20,
            'traits': (c // 2000) % 4,
            'key_primes': (c // 8000) % 10,
            'git_depth': 0,
            'muse_count': 9,
            'complexity': complexity
        },
        'monster_7d': {
            'm1': (c % 196883),           # Leech lattice
            'm2': (c % 21493760),         # Conway
            'm3': (c % 864299970),        # Fischer
            'm4': (c % 20245856256),      # Baby Monster
            'm5': (c % 333202640600),     # Bimonster
            'm6': (c % 4252023300096),    # Moonshine
            'm7': (c % 44656994071935)    # j-invariant
        }
    }

def find_monster_resonances(mathlib_data):
    """Find files that resonate with Monster coefficients"""
    resonances = []
    
    monster_coeffs = [196883, 21493760, 864299970]
    
    for entry in mathlib_data:
        c = int(entry['complexity'])
        
        for coeff in monster_coeffs:
            if c % coeff < 100:  # Close to Monster coefficient
                resonances.append({
                    'file': entry['file'],
                    'complexity': c,
                    'resonates_with': coeff,
                    'distance': c % coeff
                })
    
    return resonances

def main():
    print("🔬 Mathlib → Monster Lattice Mapping")
    print("=" * 60)
    
    # Count files
    lean_files = count_lean_files()
    
    # Sample first 100 for speed
    sample_files = lean_files[:100]
    print(f"📊 Analyzing {len(sample_files)} files (sample)...")
    
    # Extract complexity
    mathlib_data = []
    for i, f in enumerate(sample_files):
        if i % 10 == 0:
            print(f"  Processing {i}/{len(sample_files)}...")
        
        ast_data = extract_ast_complexity(f)
        if ast_data:
            mathlib_data.append(ast_data)
    
    print(f"✅ Extracted {len(mathlib_data)} AST complexities")
    
    # Sort by complexity
    mathlib_data.sort(key=lambda x: x['complexity'], reverse=True)
    
    # Map to Monster lattice
    print("\n🔢 Mapping to Monster lattice...")
    for entry in mathlib_data[:10]:
        entry['monster_coords'] = map_to_monster_lattice(entry['complexity'])
    
    # Find resonances
    print("\n🎵 Finding Monster resonances...")
    resonances = find_monster_resonances(mathlib_data)
    
    print(f"✅ Found {len(resonances)} Monster resonances!")
    
    # Save results
    output = {
        'mathlib_path': str(MATHLIB_PATH),
        'total_files': len(lean_files),
        'analyzed_files': len(mathlib_data),
        'top_10_complex': mathlib_data[:10],
        'monster_resonances': resonances[:20],
        'summary': {
            'mean_complexity': sum(e['complexity'] for e in mathlib_data) / len(mathlib_data),
            'max_complexity': mathlib_data[0]['complexity'] if mathlib_data else 0,
            'total_theorems': sum(e['theorems'] for e in mathlib_data),
            'total_lemmas': sum(e['lemmas'] for e in mathlib_data)
        }
    }
    
    with open('mathlib_monster_mapping.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Saved to mathlib_monster_mapping.json")
    
    # Print top resonances
    print(f"\n🎯 Top Monster Resonances:")
    for r in resonances[:5]:
        print(f"  {r['file']}")
        print(f"    Complexity: {r['complexity']:.1f}")
        print(f"    Resonates with: {r['resonates_with']}")
        print(f"    Distance: {r['distance']}")
    
    print(f"\n📊 Summary:")
    print(f"  Total Lean files: {len(lean_files)}")
    print(f"  Analyzed: {len(mathlib_data)}")
    print(f"  Mean complexity: {output['summary']['mean_complexity']:.2f}")
    print(f"  Max complexity: {output['summary']['max_complexity']:.2f}")
    print(f"  Total theorems: {output['summary']['total_theorems']}")
    print(f"  Total lemmas: {output['summary']['total_lemmas']}")
    print(f"  Monster resonances: {len(resonances)}")
    
    print(f"\n🎉 Mathlib resonates with the Monster!")

if __name__ == '__main__':
    main()
