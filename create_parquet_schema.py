#!/usr/bin/env python3
"""
Create central parquet schema index (like Postgres information_schema)
For each parquet: file path, columns, schema, creator process
Exclude test files
"""
import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
import json
import subprocess

# Key parquet locations (exclude tests)
PARQUET_DIRS = [
    Path.home() / ".local/share/toolchain-analysis",
    Path.home() / "nix-controller/data",
    Path.home() / "meta-introspector",
    Path("/mnt/data1/time2/time/2023/07/30/meta-meme")
]

EXCLUDE_PATTERNS = ['test', 'pyarrow/tests', 'pandas/tests', '.venv', 'site-packages']

def should_exclude(path_str):
    """Check if path should be excluded"""
    return any(pattern in path_str for pattern in EXCLUDE_PATTERNS)

def get_parquet_schema(file_path):
    """Extract schema from parquet file"""
    try:
        table = pq.read_table(file_path)
        return {
            'columns': table.column_names,
            'schema': str(table.schema),
            'num_rows': table.num_rows,
            'num_columns': len(table.column_names)
        }
    except Exception as e:
        return {'error': str(e)}

def find_creator_process(file_path):
    """Try to determine what created this parquet"""
    path_str = str(file_path)
    
    if 'toolchain-analysis' in path_str:
        return 'toolchain-analysis'
    elif 'nix-controller' in path_str:
        if 'rust_lattice' in path_str:
            return 'rust-lattice-analyzer'
        elif 'markov' in path_str:
            return 'markov-model-builder'
        return 'nix-controller'
    elif 'meta-introspector' in path_str:
        if 'perf' in path_str:
            return 'performance-profiler'
        elif 'nix_build' in path_str:
            return 'nix-build-logger'
        return 'meta-introspector'
    elif 'meta-meme' in path_str:
        return 'meta-meme-generator'
    return 'unknown'

def scan_parquet_files():
    """Scan all parquet files and build schema index"""
    schemas = []
    
    for base_dir in PARQUET_DIRS:
        if not base_dir.exists():
            continue
        
        print(f"📂 Scanning {base_dir}...")
        
        for pq_file in base_dir.rglob("*.parquet"):
            path_str = str(pq_file)
            
            if should_exclude(path_str):
                continue
            
            print(f"  📄 {pq_file.name}")
            
            schema_info = get_parquet_schema(pq_file)
            
            if 'error' not in schema_info:
                schemas.append({
                    'file_path': path_str,
                    'file_name': pq_file.name,
                    'file_size': pq_file.stat().st_size,
                    'columns': schema_info['columns'],
                    'num_rows': schema_info['num_rows'],
                    'num_columns': schema_info['num_columns'],
                    'creator_process': find_creator_process(pq_file),
                    'schema': schema_info['schema']
                })
    
    return schemas

def create_schema_index(schemas):
    """Create schema index like Postgres information_schema"""
    
    # Main index
    df = pd.DataFrame([{
        'file_path': s['file_path'],
        'file_name': s['file_name'],
        'file_size_mb': s['file_size'] / (1024*1024),
        'num_rows': s['num_rows'],
        'num_columns': s['num_columns'],
        'creator_process': s['creator_process']
    } for s in schemas])
    
    # Column catalog (like information_schema.columns)
    columns_catalog = []
    for s in schemas:
        for i, col in enumerate(s['columns']):
            columns_catalog.append({
                'file_path': s['file_path'],
                'file_name': s['file_name'],
                'column_name': col,
                'ordinal_position': i + 1,
                'creator_process': s['creator_process']
            })
    
    df_columns = pd.DataFrame(columns_catalog)
    
    return df, df_columns, schemas

def main():
    print("🗄️  Parquet Schema Index (like Postgres information_schema)")
    print("=" * 60)
    
    # Scan files
    schemas = scan_parquet_files()
    print(f"\n✅ Found {len(schemas)} parquet files (excluding tests)")
    
    # Create index
    df_files, df_columns, full_schemas = create_schema_index(schemas)
    
    # Save as parquet (parquet-of-parquet!)
    df_files.to_parquet('parquet_schema_index.parquet')
    df_columns.to_parquet('parquet_columns_catalog.parquet')
    
    print(f"✅ Saved parquet_schema_index.parquet")
    print(f"✅ Saved parquet_columns_catalog.parquet")
    
    # Save full schemas as JSON
    with open('parquet_schemas.json', 'w') as f:
        json.dump(full_schemas, f, indent=2, default=str)
    print(f"✅ Saved parquet_schemas.json")
    
    # Stats
    print(f"\n📊 Statistics:")
    print(f"  Total files: {len(df_files)}")
    print(f"  Total size: {df_files['file_size_mb'].sum():.2f} MB")
    print(f"  Total rows: {df_files['num_rows'].sum():,}")
    print(f"  Total columns: {len(df_columns)}")
    
    print(f"\n  By creator process:")
    for proc, count in df_files['creator_process'].value_counts().items():
        rows = df_files[df_files['creator_process'] == proc]['num_rows'].sum()
        print(f"    {proc}: {count} files, {rows:,} rows")
    
    print(f"\n  Top 10 largest files:")
    for _, row in df_files.nlargest(10, 'file_size_mb').iterrows():
        print(f"    {row['file_name']}: {row['file_size_mb']:.2f} MB ({row['num_rows']:,} rows)")

if __name__ == '__main__':
    main()
