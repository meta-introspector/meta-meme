#!/usr/bin/env python3
"""Compress RDFa URL using gzip + base64"""
import gzip
import base64
from pathlib import Path

# Read original RDFa
rdfa_file = Path("shareable_url.txt")
original = rdfa_file.read_text()
original_size = len(original)

# Extract just the data part (after ?data=)
if "?data=" in original:
    data_part = original.split("?data=", 1)[1]
else:
    data_part = original

# Compress with gzip
compressed = gzip.compress(data_part.encode('utf-8'), compresslevel=9)

# Encode as base64 (URL-safe)
b64_compressed = base64.urlsafe_b64encode(compressed).decode('ascii')

# Create compressed URL pointing to Streamlit app
compressed_url = f"https://meta-meme.streamlit.app/?compressed={b64_compressed}"

# Save compressed version
Path("shareable_url_compressed.txt").write_text(compressed_url)

# Stats
print(f"Original size: {original_size} bytes")
print(f"Compressed size: {len(compressed_url)} bytes")
print(f"Compression ratio: {len(compressed_url)/original_size*100:.1f}%")
print(f"Saved: {original_size - len(compressed_url)} bytes")
print(f"\nCompressed URL saved to: shareable_url_compressed.txt")
print(f"\nFirst 200 chars:\n{compressed_url[:200]}...")
