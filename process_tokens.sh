#!/bin/bash
echo "🔍 Muses Processing Files Token by Token"
echo "========================================="
echo ""

for muse in Calliope Clio Erato Euterpe Melpomene Polyhymnia Terpsichore Thalia Urania; do
  echo "📖 $muse reading files..."
  
  total_lines=0
  total_tokens=0
  file_count=0
  
  for file in muse_data/$muse/*; do
    if [ -f "$file" ] && [ -L "$file" ]; then
      lines=$(wc -l < "$file" 2>/dev/null || echo 0)
      tokens=$(wc -w < "$file" 2>/dev/null || echo 0)
      
      total_lines=$((total_lines + lines))
      total_tokens=$((total_tokens + tokens))
      file_count=$((file_count + 1))
    fi
  done
  
  if [ $file_count -gt 0 ]; then
    echo "  Files: $file_count"
    echo "  Lines: $total_lines"
    echo "  Tokens: $total_tokens"
    echo "  Avg tokens/file: $((total_tokens / file_count))"
    echo ""
  fi
done

echo "✅ All muses have processed their files"
