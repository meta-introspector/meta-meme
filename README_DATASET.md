---
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

This dataset contains 2177 consultation URLs generated from the Meta-Meme formally verified system. Each URL represents a consultation with one of 9 AI muses about a specific file in the repository.

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
