#!/bin/bash
# Trace evolution: Compile with increasing optimization and trace deformation

set -e

echo "=== Perf Trace Evolution: O0 → O3 → GPU ==="
echo

# O0: Baseline (already built)
echo "1. O0 (zero optimization) - Baseline"
cargo build --bin perf_automorphic_loop 2>/dev/null
./target/debug/perf_automorphic_loop | grep "LMFDB Label"
echo

# O1: Basic optimization
echo "2. O1 (basic optimization)"
cargo build --bin perf_automorphic_loop --release --config 'profile.release.opt-level=1' 2>/dev/null
./target/release/perf_automorphic_loop | grep "LMFDB Label"
echo

# O2: More optimization
echo "3. O2 (more optimization)"
cargo build --bin perf_automorphic_loop --release --config 'profile.release.opt-level=2' 2>/dev/null
./target/release/perf_automorphic_loop | grep "LMFDB Label"
echo

# O3: Full optimization
echo "4. O3 (full optimization)"
cargo build --bin perf_automorphic_loop --release 2>/dev/null
./target/release/perf_automorphic_loop | grep "LMFDB Label"
echo

echo "✓ Evolution complete - labels show deformation of automorphic loop"
echo
echo "Next: Compare labels to measure optimization deformation"
