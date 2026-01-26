#!/usr/bin/env python3
"""
HuggingFace Dataset Validator
Validates and syncs all meta-meme datasets
"""
from datasets import load_dataset
import pandas as pd

DATASETS = [
    "introspector/meta-meme",  # Consultation URLs
]

def validate_dataset(repo_id):
    """Validate HuggingFace dataset"""
    print(f"📦 Validating {repo_id}...")
    
    try:
        ds = load_dataset(repo_id, split='train')
        
        print(f"  ✅ Valid dataset")
        print(f"  Rows: {len(ds)}")
        print(f"  Columns: {ds.column_names}")
        print(f"  Features: {ds.features}")
        
        # Check for required columns
        required = ['file', 'muse', 'tool', 'url']
        missing = [c for c in required if c not in ds.column_names]
        if missing:
            print(f"  ⚠️  Missing columns: {missing}")
        else:
            print(f"  ✅ All required columns present")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def sync_to_parquet(repo_id, output_file):
    """Sync HuggingFace dataset to local parquet"""
    print(f"🔄 Syncing {repo_id} to {output_file}...")
    
    try:
        ds = load_dataset(repo_id, split='train')
        df = ds.to_pandas()
        df.to_parquet(output_file)
        print(f"  ✅ Synced {len(df)} rows to {output_file}")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("🔍 HuggingFace Dataset Validator")
    print("=" * 50)
    
    results = {}
    
    for repo_id in DATASETS:
        valid = validate_dataset(repo_id)
        results[repo_id] = valid
        
        if valid:
            output = f"{repo_id.split('/')[-1]}_synced.parquet"
            sync_to_parquet(repo_id, output)
        
        print()
    
    print("📊 Summary:")
    for repo_id, valid in results.items():
        status = "✅" if valid else "❌"
        print(f"  {status} {repo_id}")
    
    total = len(results)
    valid_count = sum(results.values())
    print(f"\n  Total: {valid_count}/{total} valid")

if __name__ == '__main__':
    main()
