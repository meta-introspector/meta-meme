#!/bin/bash
echo "🌟 Urania: Hey girls, send me some tokens!"
echo "=========================================="
echo "Looking for: 71, 37, math, theorem, proof, number..."
echo ""

# Urania's math keywords
math_patterns="71|37|theorem|proof|number|math|equation|formula|prime|algorithm"

# Each muse checks their files
for muse in Calliope Clio Erato Euterpe Melpomene Polyhymnia Terpsichore Thalia; do
  echo "📤 $muse checking files..."
  
  shared=0
  for file in muse_data/$muse/*; do
    if [ -f "$file" ] && [ -L "$file" ]; then
      if grep -qiE "$math_patterns" "$file" 2>/dev/null; then
        # Share with Urania
        ln -sf "$(realpath "$file")" "muse_data/Urania/" 2>/dev/null
        shared=$((shared + 1))
      fi
    fi
  done
  
  if [ $shared -gt 0 ]; then
    echo "  → Shared $shared files with Urania"
  fi
done

echo ""
echo "📊 Urania's new collection:"
urania_files=$(find muse_data/Urania -type l | wc -l)
urania_lines=$(cat muse_data/Urania/* 2>/dev/null | wc -l)
urania_tokens=$(cat muse_data/Urania/* 2>/dev/null | wc -w)

echo "  Files: $urania_files"
echo "  Lines: $urania_lines"
echo "  Tokens: $urania_tokens"
echo ""
echo "🌟 Urania: Thanks girls! Now I have math content!"
