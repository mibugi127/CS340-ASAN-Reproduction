#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

export ASAN_OPTIONS=detect_leaks=0

echo "======================================"
echo "🚀 Starting Automated ASan Benchmark & Detection Tests"
echo "======================================"

echo "🧹 Cleaning old files and compiling ASan & Baseline versions..."
make clean
make
make base

echo "🐛 Running Bug Detection Tests..."
mkdir -p results/logs
for b in build/bugs/*; do
    echo "Running $b..." >> results/logs/bug_test_summary.txt
    "$b" > /dev/null 2>> results/logs/bug_test_summary.txt || true
done
echo "✅ Bug detection finished. Logs saved to results/logs/bug_test_summary.txt"

echo "⏱️ Running performance benchmarks (C1 & C2)..."
python3 scripts/run_bench.py

echo "📊 Processing data, generating CSV and Markdown tables..."
python3 scripts/analyze.py

echo "======================================"
echo "🎉 All tests completed! Check the results/ folder for data."
echo "======================================"