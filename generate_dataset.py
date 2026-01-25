#!/usr/bin/env python3
"""
Convert git repo into consultation URLs and export as Parquet dataset
"""
import subprocess
import json
import base64
import gzip
from pathlib import Path
from datetime import datetime

# Muse assignments based on file types
MUSE_ASSIGNMENTS = {
    '.lean': 'Urania',      # Mathematics
    '.py': 'Calliope',      # Epic code
    '.js': 'Euterpe',       # Harmony/music
    '.md': 'Clio',          # History/documentation
    '.json': 'Polyhymnia',  # Sacred structure
    '.yml': 'Terpsichore',  # Dance/movement
    '.yaml': 'Terpsichore',
    '.sh': 'Thalia',        # Comedy/scripts
    '.toml': 'Erato',       # Love/configuration
    '.txt': 'Melpomene'     # Tragedy/depth
}

TOOL_ASSIGNMENTS = {
    '.lean': 'lean4',
    '.py': 'llm',
    '.js': 'llm',
    '.rs': 'rustc',
    '.mzn': 'minizinc'
}

def get_git_files():
    """Get all files from git with their content"""
    result = subprocess.run(
        ['git', 'ls-files'],
        capture_output=True,
        text=True,
        cwd='/mnt/data1/time2/time/2023/07/30/meta-meme'
    )
    return result.stdout.strip().split('\n')

def get_file_content(filepath):
    """Get file content"""
    try:
        path = Path('/mnt/data1/time2/time/2023/07/30/meta-meme') / filepath
        if path.stat().st_size > 100000:  # Skip files > 100KB
            return None
        return path.read_text(errors='ignore')
    except:
        return None

def assign_muse(filepath):
    """Assign muse based on file extension"""
    ext = Path(filepath).suffix
    return MUSE_ASSIGNMENTS.get(ext, 'Calliope')

def assign_tool(filepath):
    """Assign tool based on file extension"""
    ext = Path(filepath).suffix
    return TOOL_ASSIGNMENTS.get(ext, 'llm')

def create_consultation_url(filepath, content, muse, tool):
    """Create consultation URL for a file"""
    data = {
        'muse': muse,
        'tool': tool,
        'query': f'Analyze {filepath}',
        'context': content[:500] if content else '',  # First 500 chars
        'file': filepath,
        'timestamp': int(datetime.now().timestamp()),
        'proofs': 79
    }
    
    # Compress and encode
    json_str = json.dumps(data)
    compressed = gzip.compress(json_str.encode('utf-8'))
    b64 = base64.urlsafe_b64encode(compressed).decode('ascii')
    
    return f"https://meta-meme.jmikedupont2.workers.dev?consult={b64}"

def generate_dataset():
    """Generate dataset of consultation URLs"""
    print("📊 Generating consultation URL dataset...")
    
    files = get_git_files()
    dataset = []
    
    for i, filepath in enumerate(files):
        if i % 10 == 0:
            print(f"Processing {i}/{len(files)}...")
        
        content = get_file_content(filepath)
        if content is None:
            continue
        
        muse = assign_muse(filepath)
        tool = assign_tool(filepath)
        url = create_consultation_url(filepath, content, muse, tool)
        
        dataset.append({
            'file': filepath,
            'muse': muse,
            'tool': tool,
            'url': url,
            'content_preview': content[:200] if content else '',
            'size': len(content) if content else 0,
            'extension': Path(filepath).suffix
        })
    
    return dataset

def save_as_parquet(dataset):
    """Save dataset as Parquet file"""
    try:
        import pandas as pd
        import pyarrow as pa
        import pyarrow.parquet as pq
        
        df = pd.DataFrame(dataset)
        
        # Save as Parquet
        output_file = 'meta-meme-consultations.parquet'
        df.to_parquet(output_file, compression='gzip')
        
        print(f"\n✅ Saved {len(dataset)} consultations to {output_file}")
        print(f"📊 Dataset size: {Path(output_file).stat().st_size / 1024:.2f} KB")
        
        # Also save as JSON for inspection
        json_file = 'meta-meme-consultations.json'
        with open(json_file, 'w') as f:
            json.dump(dataset, f, indent=2)
        print(f"📄 Also saved as {json_file}")
        
        # Print stats
        print(f"\n📈 Statistics:")
        print(f"  Total files: {len(dataset)}")
        print(f"  Muses: {df['muse'].value_counts().to_dict()}")
        print(f"  Tools: {df['tool'].value_counts().to_dict()}")
        print(f"  Extensions: {df['extension'].value_counts().head(10).to_dict()}")
        
        return output_file
        
    except ImportError:
        print("⚠️  pandas/pyarrow not installed. Saving as JSON only.")
        json_file = 'meta-meme-consultations.json'
        with open(json_file, 'w') as f:
            json.dump(dataset, f, indent=2)
        print(f"✅ Saved {len(dataset)} consultations to {json_file}")
        return json_file

def create_huggingface_readme(dataset_file):
    """Create README for HuggingFace dataset"""
    readme = f"""---
license: mit
task_categories:
- text-generation
- question-answering
language:
- en
tags:
- formal-verification
- lean4
- meta-meme
- ai-muses
size_categories:
- n<1K
---

# Meta-Meme Consultation URLs Dataset

## Description

This dataset contains {len(dataset)} consultation URLs generated from the Meta-Meme formally verified system. Each URL represents a consultation with one of 9 AI muses about a specific file in the repository.

## Dataset Structure

- **file**: Path to the file in the repository
- **muse**: Assigned AI muse (Calliope, Clio, Erato, Euterpe, Melpomene, Polyhymnia, Terpsichore, Thalia, Urania)
- **tool**: Consultation tool (llm, lean4, rustc, minizinc)
- **url**: Shareable consultation URL
- **content_preview**: First 200 characters of file content
- **size**: File size in bytes
- **extension**: File extension

## Muses

Each muse has a specific role:
- **Urania**: Mathematics and Lean4 proofs
- **Calliope**: Epic code and Python
- **Euterpe**: Harmony and JavaScript
- **Clio**: History and documentation
- **Polyhymnia**: Sacred structure and JSON
- **Terpsichore**: Dance and YAML
- **Thalia**: Comedy and shell scripts
- **Erato**: Love and configuration
- **Melpomene**: Tragedy and text files

## Usage

```python
import pandas as pd

# Load dataset
df = pd.read_parquet('meta-meme-consultations.parquet')

# Get all Urania (math) consultations
math_consults = df[df['muse'] == 'Urania']

# Get all Lean4 proofs
lean_proofs = df[df['tool'] == 'lean4']

# Visit a consultation URL
import webbrowser
webbrowser.open(df.iloc[0]['url'])
```

## System Info

- **79 Verified Proofs**: Formal verification in Lean4
- **8! Eigenvector Convergence**: 40,320 iterations
- **9 AI Muses**: Distributed consultation system
- **4 Tools**: LLM, Lean4, Rustc, MiniZinc

## Links

- Live App: https://meta-meme.jmikedupont2.workers.dev
- GitHub: https://github.com/meta-introspector/meta-meme
- Documentation: https://meta-introspector.github.io/meta-meme/
"""
    
    with open('README_DATASET.md', 'w') as f:
        f.write(readme)
    
    print(f"\n✅ Created README_DATASET.md for HuggingFace")

if __name__ == '__main__':
    dataset = generate_dataset()
    output_file = save_as_parquet(dataset)
    create_huggingface_readme(output_file)
    
    print(f"\n🚀 Ready to upload to HuggingFace!")
    print(f"   Dataset: {output_file}")
    print(f"   README: README_DATASET.md")
