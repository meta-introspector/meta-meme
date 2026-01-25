#!/bin/bash
echo "🔍 Verifying all 16 Lean files..."
echo "=================================="
echo ""

files=(
  "src/DirectProof.lean"
  "src/Manifold.lean"
  "src/DocumentProver.lean"
  "src/Syscall.lean"
  "src/Mirror.lean"
  "src/Strace2Lean.lean"
  "src/Perf2Lean.lean"
  "src/Parquet2Lean.lean"
  "src/Rust2Lean.lean"
  "src/Wasm2Lean.lean"
  "src/MkBuild.lean"
  "src/URLProof.lean"
  "src/ZKWasm.lean"
  "src/metameme.lean"
  "src/metaprotocol.lean"
  "src/ProjectSnapshot.lean"
)

passed=0
failed=0

for file in "${files[@]}"; do
  echo -n "Testing $file... "
  if lean "$file" > /dev/null 2>&1; then
    echo "✅"
    ((passed++))
  else
    echo "❌"
    ((failed++))
  fi
done

echo ""
echo "Results: $passed passed, $failed failed out of ${#files[@]} files"
