#!/bin/bash
echo "📚 Complete File Distribution Among Muses"
echo "=========================================="
echo ""

# Create muse directories
for muse in Calliope Clio Erato Euterpe Melpomene Polyhymnia Terpsichore Thalia Urania; do
  mkdir -p muse_data/$muse
done

# Find all files and distribute
find . -type f \( -name "*.md" -o -name "*.lean" -o -name "*.rs" -o -name "*.ts" -o -name "*.sh" -o -name "*.json" \) | while read file; do
  content=$(cat "$file" 2>/dev/null | tr '[:upper:]' '[:lower:]')
  
  # Assign based on keywords
  if echo "$content" | grep -qE "language|grammar|syntax|parser"; then
    muse="Calliope"
  elif echo "$content" | grep -qE "data|storage|persistence|document|history"; then
    muse="Clio"
  elif echo "$content" | grep -qE "visual|graph|chart|diagram|svg"; then
    muse="Erato"
  elif echo "$content" | grep -qE "interface|ui|ux|design|web"; then
    muse="Euterpe"
  elif echo "$content" | grep -qE "error|exception|fail|bug|crash"; then
    muse="Melpomene"
  elif echo "$content" | grep -qE "algorithm|proof|theorem|lean|verify"; then
    muse="Polyhymnia"
  elif echo "$content" | grep -qE "flow|pipeline|orchestrate|workflow"; then
    muse="Terpsichore"
  elif echo "$content" | grep -qE "test|debug|assert|check|validate"; then
    muse="Thalia"
  elif echo "$content" | grep -qE "architecture|system|structure|scale"; then
    muse="Urania"
  else
    muse="Polyhymnia"  # Default
  fi
  
  # Create symlink
  ln -sf "$(realpath "$file")" "muse_data/$muse/" 2>/dev/null
done

# Count files per muse
echo "📊 Distribution Results:"
for muse in Calliope Clio Erato Euterpe Melpomene Polyhymnia Terpsichore Thalia Urania; do
  count=$(find muse_data/$muse -type l | wc -l)
  echo "  $muse: $count files"
done

echo ""
echo "✅ All files distributed to muse_data/ directories"
