#!/usr/bin/env bash
# Simplified plocate witness without sudo
set -e

WITNESS_DIR="/mnt/data1/time2/time/2023/07/30/meta-meme/plocate_witness"
mkdir -p "$WITNESS_DIR"

echo "🔬 Creating plocate witness (no sudo)"
echo "====================================="

# 1. Run locate and capture output
echo "📊 Running locate..."
time locate "*.rs" 2>&1 | head -10000 > "$WITNESS_DIR/locate_output.txt"
TOTAL_FILES=$(wc -l < "$WITNESS_DIR/locate_output.txt")
echo "  Found: $TOTAL_FILES files"

# 2. Analyze file sizes
echo ""
echo "📏 Analyzing file sizes..."
while IFS= read -r file; do
    if [ -f "$file" ]; then
        stat -c "%s %n" "$file" 2>/dev/null
    fi
done < "$WITNESS_DIR/locate_output.txt" | head -1000 > "$WITNESS_DIR/file_sizes.txt"

# 3. Calculate size distribution
echo "  Size distribution:"
awk '{print $1}' "$WITNESS_DIR/file_sizes.txt" | sort -n | \
    awk 'BEGIN{min=999999999; max=0; sum=0; count=0}
         {if($1<min)min=$1; if($1>max)max=$1; sum+=$1; count++}
         END{print "    Min: "min" bytes\n    Max: "max" bytes\n    Mean: "int(sum/count)" bytes\n    Total: "count" files"}'

# 4. Compression analysis
echo ""
echo "🗜️  Compression analysis (sample)..."
head -100 "$WITNESS_DIR/file_sizes.txt" | while read size file; do
    if [ -f "$file" ] && [ "$size" -lt 1000000 ]; then
        ORIG=$size
        COMP=$(gzip -c "$file" 2>/dev/null | wc -c)
        RATIO=$(echo "scale=4; $COMP / $ORIG" | bc 2>/dev/null || echo "0")
        echo "$RATIO $ORIG $file"
    fi
done | sort -n | head -20 > "$WITNESS_DIR/compression_ratios.txt"

echo "  Top 10 most compressible:"
head -10 "$WITNESS_DIR/compression_ratios.txt" | awk '{printf "    %.4f  %10d  %s\n", $1, $2, $3}'

# 5. Monster resonance by file size
echo ""
echo "🎵 Monster resonance analysis..."
awk '{print $1}' "$WITNESS_DIR/file_sizes.txt" | \
    awk '{
        size = $1
        weight = size % 196883
        conductor = int(size / 1000000)
        if (weight < 10000) {
            resonant++
            print size, weight, conductor
        }
        total++
    }
    END {
        print "# Total:", total > "/dev/stderr"
        print "# Resonant:", resonant > "/dev/stderr"
        print "# Rate:", resonant/total > "/dev/stderr"
    }' > "$WITNESS_DIR/resonant_files.txt" 2> "$WITNESS_DIR/resonance_stats.txt"

cat "$WITNESS_DIR/resonance_stats.txt"

echo ""
echo "✅ Witness captured!"
echo ""
echo "Files:"
ls -lh "$WITNESS_DIR"/ | tail -n +2
