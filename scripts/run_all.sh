#!/usr/bin/env bash
set -e

mkdir -p results
make
make base

echo "== bug demos =="
for b in build/bugs/*; do
    echo "--- $b"
    "$b" 2>&1 | head -5 || true
done

echo "== perf benchmarks (ASan vs Base) =="
for b in build/perf/*; do
    [ -f "$b" ] || continue
    name=$(basename "$b")
    base_bin="build/perf_base/${name}_base"
    
    echo "--- $name (ASan) ---"
    /usr/bin/time -f "%e s, %M KB" "$b" > /dev/null || true
    
    if [ -f "$base_bin" ]; then
        echo "--- $name (Base) ---"
        /usr/bin/time -f "%e s, %M KB" "$base_bin" > /dev/null || true
    fi
done