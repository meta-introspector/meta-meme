#!/usr/bin/env bash
# Complete witness of plocate reading database
# Captures: instructions, registers, memory, bits

set -e

WITNESS_DIR="/mnt/data1/time2/time/2023/07/30/meta-meme/plocate_witness"
mkdir -p "$WITNESS_DIR"

echo "🔬 Creating complete plocate witness"
echo "===================================="

# 1. Find plocate database
PLOCATE_DB=$(locate -d /var/lib/plocate/plocate.db --statistics 2>&1 | grep "Database" | awk '{print $2}' || echo "/var/lib/plocate/plocate.db")
echo "📊 Database: $PLOCATE_DB"
ls -lh "$PLOCATE_DB" 2>/dev/null || echo "Database not found, will use locate command"

# 2. Analyze database file bit-level
echo ""
echo "📁 Bit-level analysis of database..."
if [ -f "$PLOCATE_DB" ]; then
    # File size
    stat "$PLOCATE_DB" > "$WITNESS_DIR/db_stat.txt"
    
    # First 1KB hex dump
    xxd -l 1024 "$PLOCATE_DB" > "$WITNESS_DIR/db_header_hex.txt"
    
    # Entropy analysis (compression potential)
    head -c 1048576 "$PLOCATE_DB" | gzip -c | wc -c > "$WITNESS_DIR/db_entropy.txt"
    ORIG_SIZE=$(head -c 1048576 "$PLOCATE_DB" | wc -c)
    COMP_SIZE=$(cat "$WITNESS_DIR/db_entropy.txt")
    RATIO=$(echo "scale=4; $COMP_SIZE / $ORIG_SIZE" | bc)
    echo "  Original: $ORIG_SIZE bytes"
    echo "  Compressed: $COMP_SIZE bytes"
    echo "  Ratio: $RATIO (lower = more compressible)"
fi

# 3. Perf record with full register capture
echo ""
echo "🎯 Recording plocate execution with full instrumentation..."
perf record -e cycles,instructions,cache-references,cache-misses \
    --call-graph dwarf \
    --sample-cpu \
    --sample-regs-user=AX,BX,CX,DX,SI,DI,BP,SP,IP,FLAGS,R8,R9,R10,R11,R12,R13,R14,R15 \
    -o "$WITNESS_DIR/plocate.perf.data" \
    -- locate --database "$PLOCATE_DB" "*.rs" 2>&1 | head -100 > "$WITNESS_DIR/locate_output.txt"

echo "  Captured: $WITNESS_DIR/plocate.perf.data"

# 4. Extract instruction trace
echo ""
echo "📜 Extracting instruction trace..."
perf script -i "$WITNESS_DIR/plocate.perf.data" > "$WITNESS_DIR/instruction_trace.txt"
echo "  Instructions: $(wc -l < "$WITNESS_DIR/instruction_trace.txt")"

# 5. Analyze register states
echo ""
echo "🔢 Analyzing register states..."
perf script -i "$WITNESS_DIR/plocate.perf.data" -F ip,sym,regs | head -1000 > "$WITNESS_DIR/register_states.txt"

# 6. Call graph
echo ""
echo "📊 Generating call graph..."
perf report -i "$WITNESS_DIR/plocate.perf.data" --stdio --no-children > "$WITNESS_DIR/call_graph.txt"

# 7. Cache analysis
echo ""
echo "💾 Cache analysis..."
perf stat -e cache-references,cache-misses,L1-dcache-loads,L1-dcache-load-misses \
    locate --database "$PLOCATE_DB" "*.rs" 2>&1 | head -100 > /dev/null 2> "$WITNESS_DIR/cache_stats.txt"

# 8. Disassemble plocate binary
echo ""
echo "⚙️  Disassembling plocate..."
which plocate > "$WITNESS_DIR/plocate_path.txt" || which locate > "$WITNESS_DIR/plocate_path.txt"
PLOCATE_BIN=$(cat "$WITNESS_DIR/plocate_path.txt")
objdump -d "$PLOCATE_BIN" > "$WITNESS_DIR/plocate_disasm.txt" 2>/dev/null || echo "Could not disassemble"

# 9. Summary
echo ""
echo "✅ Witness complete!"
echo ""
echo "Generated files:"
ls -lh "$WITNESS_DIR"/ | tail -n +2

# 10. Quick analysis
echo ""
echo "📈 Quick analysis:"
echo "  Total instructions: $(grep -c "cycles" "$WITNESS_DIR/instruction_trace.txt" || echo "N/A")"
echo "  Unique functions: $(grep -o "in [^ ]*" "$WITNESS_DIR/call_graph.txt" | sort -u | wc -l || echo "N/A")"
echo "  Cache miss rate: $(grep "cache-misses" "$WITNESS_DIR/cache_stats.txt" | head -1 || echo "N/A")"

echo ""
echo "🎯 Next: Analyze with Rust to create bit model"
