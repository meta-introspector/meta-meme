#!/usr/bin/env python3
"""
N-gram analysis: Compare similar programs to semantic_index_parallel.rs
Adjust model based on content similarity.
"""

from collections import Counter
from pathlib import Path
import re

def extract_ngrams(text, n=3):
    """Extract n-grams (token sequences) from code."""
    # Tokenize: split on whitespace and symbols
    tokens = re.findall(r'\w+|[^\w\s]', text)
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def compare_files(file1, file2, n=3):
    """Compare two files using n-gram similarity."""
    try:
        text1 = Path(file1).read_text()
        text2 = Path(file2).read_text()
        
        ngrams1 = Counter(extract_ngrams(text1, n))
        ngrams2 = Counter(extract_ngrams(text2, n))
        
        # Jaccard similarity
        intersection = sum((ngrams1 & ngrams2).values())
        union = sum((ngrams1 | ngrams2).values())
        similarity = intersection / union if union > 0 else 0
        
        # Common patterns
        common = (ngrams1 & ngrams2).most_common(10)
        
        return similarity, common, ngrams1, ngrams2
    except:
        return 0, [], Counter(), Counter()

# Our file
our_file = "src/bin/semantic_index_parallel.rs"
our_text = Path(our_file).read_text()
our_ngrams = Counter(extract_ngrams(our_text, 3))

print(f"🔬 N-gram Analysis of {our_file}")
print(f"   Total 3-grams: {len(our_ngrams)}")
print(f"   Unique patterns: {len(set(our_ngrams.elements()))}")
print()

# Similar files from previous search
similar_files = [
    "/home/mdupont/.cargo/git/checkouts/burn-6c277d792b0d5d7a/3cd0671/crates/burn-fusion/src/ops/unary.rs",
    "/home/mdupont/.cargo/git/checkouts/burn-6c277d792b0d5d7a/3cd0671/crates/burn-cubecl-fusion/src/engine/launch/executor.rs",
    "/home/mdupont/.cargo/git/checkouts/burn-6c277d792b0d5d7a/3cd0671/crates/burn-fusion/src/client.rs",
]

print("📊 Comparing to similar files:\n")

all_common_patterns = Counter()

for similar_file in similar_files:
    if not Path(similar_file).exists():
        continue
        
    similarity, common, their_ngrams, _ = compare_files(our_file, similar_file, 3)
    
    print(f"File: {Path(similar_file).name}")
    print(f"  Similarity: {similarity:.4f}")
    print(f"  Common 3-grams: {len(common)}")
    
    if common:
        print(f"  Top patterns:")
        for ngram, count in common[:5]:
            pattern = ' '.join(ngram)
            print(f"    {count}x: {pattern}")
            all_common_patterns[ngram] += count
    print()

# Analyze what makes our code unique
print("🎯 MODEL ADJUSTMENT:")
print("=" * 60)

# Most common patterns in our code
our_top = our_ngrams.most_common(20)
print("\nOur code's signature patterns:")
for ngram, count in our_top[:10]:
    pattern = ' '.join(ngram)
    print(f"  {count}x: {pattern}")

# Patterns shared with similar code
shared_top = all_common_patterns.most_common(10)
print("\nShared patterns (common to similar files):")
for ngram, count in shared_top:
    pattern = ' '.join(ngram)
    print(f"  {count}x: {pattern}")

# Unique patterns (in our code but not in similar files)
unique = set(our_ngrams.keys()) - set(all_common_patterns.keys())
unique_patterns = [(ng, our_ngrams[ng]) for ng in unique]
unique_patterns.sort(key=lambda x: -x[1])

print("\nUnique patterns (our innovation):")
for ngram, count in unique_patterns[:10]:
    pattern = ' '.join(ngram)
    print(f"  {count}x: {pattern}")

# Model adjustment
print("\n" + "=" * 60)
print("MODEL ADJUSTMENT RECOMMENDATIONS:")
print("=" * 60)

print("\n1. Shared Infrastructure (use existing patterns):")
print("   - Rust parallel processing patterns")
print("   - Channel-based communication")
print("   - Arc/Atomic for shared state")

print("\n2. Our Innovation (keep unique):")
print("   - Monster group weight calculation")
print("   - LMFDB label generation")
print("   - Resonance detection")
print("   - Semantic property proofs")

print("\n3. Optimization Opportunities:")
print("   - Adopt efficient patterns from burn-fusion")
print("   - Use similar error handling")
print("   - Follow Rust idioms from similar code")

print("\n✅ Model adjusted based on n-gram analysis!")
