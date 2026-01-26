#!/usr/bin/env python3
"""
Order parquet schemas by complexity (LMFDB-inspired)
conductor: file size, row count
weight: column count, data types
level: nesting depth, relationships
traits: git tracking, creator process
key primes: unique columns, primary keys
"""
import pandas as pd
import json

def calculate_complexity(schema):
    """Calculate complexity score for a parquet file"""
    
    # Conductor: size and scale
    conductor = (
        schema.get('file_size_mb', 0) * 0.1 +  # Size weight
        schema.get('num_rows', 0) / 1000000     # Row count (millions)
    )
    
    # Weight: dimensionality
    weight = schema.get('num_columns', 0)
    
    # Level: depth (inferred from column names)
    columns = schema.get('columns', [])
    level = sum(1 for c in columns if '.' in c or '_' in c)  # Nested/compound columns
    
    # Traits: metadata richness
    traits = (
        (1 if schema.get('git_repo') else 0) +
        (1 if schema.get('git_commit') else 0) +
        (1 if schema.get('creator_process') != 'unknown' else 0)
    )
    
    # Key primes: unique identifiers
    key_primes = sum(1 for c in columns if any(k in c.lower() for k in ['id', 'key', 'hash', 'uuid']))
    
    # Total complexity
    complexity = conductor + weight * 2 + level * 3 + traits + key_primes * 5
    
    return {
        'complexity': complexity,
        'conductor': conductor,
        'weight': weight,
        'level': level,
        'traits': traits,
        'key_primes': key_primes
    }

def main():
    print("📊 Ordering Parquet Schemas by Complexity (LMFDB-inspired)")
    print("=" * 60)
    
    # Load schemas
    with open('parquet_schemas.json') as f:
        schemas = json.load(f)
    
    print(f"Loaded {len(schemas)} schemas")
    
    # Calculate complexity for each
    for schema in schemas:
        complexity_metrics = calculate_complexity(schema)
        schema.update(complexity_metrics)
    
    # Sort by complexity
    schemas_sorted = sorted(schemas, key=lambda s: s['complexity'], reverse=True)
    
    # Create ordered DataFrame
    df = pd.DataFrame([{
        'file_name': s['file_name'],
        'complexity': s['complexity'],
        'conductor': s['conductor'],
        'weight': s['weight'],
        'level': s['level'],
        'traits': s['traits'],
        'key_primes': s['key_primes'],
        'num_rows': s['num_rows'],
        'num_columns': s['num_columns'],
        'file_size_mb': s['file_size_mb'],
        'creator_process': s['creator_process']
    } for s in schemas_sorted])
    
    # Save ordered schema
    df.to_parquet('parquet_schema_ordered.parquet')
    print(f"✅ Saved parquet_schema_ordered.parquet")
    
    # Save full ordered schemas
    with open('parquet_schemas_ordered.json', 'w') as f:
        json.dump(schemas_sorted, f, indent=2)
    print(f"✅ Saved parquet_schemas_ordered.json")
    
    # Print top 20 most complex
    print(f"\n🔝 Top 20 Most Complex Schemas:")
    print(f"{'File':<40} {'Complexity':>10} {'Conductor':>10} {'Weight':>7} {'Level':>6} {'Traits':>7} {'Primes':>7}")
    print("-" * 100)
    
    for _, row in df.head(20).iterrows():
        print(f"{row['file_name']:<40} {row['complexity']:>10.1f} {row['conductor']:>10.1f} "
              f"{row['weight']:>7} {row['level']:>6} {row['traits']:>7} {row['key_primes']:>7}")
    
    # Print statistics
    print(f"\n📈 Complexity Distribution:")
    print(f"  Mean complexity: {df['complexity'].mean():.2f}")
    print(f"  Median complexity: {df['complexity'].median():.2f}")
    print(f"  Max complexity: {df['complexity'].max():.2f}")
    print(f"  Min complexity: {df['complexity'].min():.2f}")
    
    print(f"\n  By creator process:")
    for proc, group in df.groupby('creator_process'):
        avg_complexity = group['complexity'].mean()
        print(f"    {proc}: {len(group)} files, avg complexity {avg_complexity:.2f}")

if __name__ == '__main__':
    main()
