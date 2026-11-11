import csv
import os
import subprocess
import sys

BENCHMARKS = ["loop", "matrix", "sort"]
WARMUP = 1
RUNS = 3

os.makedirs("results", exist_ok=True)

rows = []


def measure(binary):
    out = subprocess.check_output(
        [sys.executable, "scripts/time_run.py", binary], text=True
    ).strip()
    sec, rss = out.split(",")
    return float(sec), float(rss)


for bench in BENCHMARKS:
    asan_bin = os.path.join("build", "perf", bench)
    base_bin = os.path.join("build", "perf_base", bench + "_base")

    for _ in range(WARMUP):
        measure(base_bin)
        measure(asan_bin)

    print("--- %s ---" % bench)
    for i in range(1, RUNS + 1):
        tb, mb = measure(base_bin)
        ta, ma = measure(asan_bin)
        rows.append((bench, "base", i, tb, mb))
        rows.append((bench, "asan", i, ta, ma))
        print("  run %d: base %.4fs %.0fkB | asan %.4fs %.0fkB | %.2fx %.2fx"
              % (i, tb, mb, ta, ma, ta / tb, ma / mb))

with open(os.path.join("results", "timing.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["program", "mode", "run", "seconds", "maxrss_kb"])
    w.writerows(rows)

heap_rows = []
heap_base = os.path.join("build", "perf_base", "heap_base")
heap_asan = os.path.join("build", "perf", "heap")

if os.path.exists(heap_base) and os.path.exists(heap_asan):
    for _ in range(WARMUP):
        measure(heap_base)
        measure(heap_asan)
    print("--- heap (memory experiment) ---")
    for i in range(1, RUNS + 1):
        tb, mb = measure(heap_base)
        ta, ma = measure(heap_asan)
        heap_rows.append((i, tb, mb, ta, ma))
        print("  run %d: base %.0fkB | asan %.0fkB | %.2fx" % (i, mb, ma, ma / mb))
    with open(os.path.join("results", "heap.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["run", "base_seconds", "base_rss_kb", "asan_seconds", "asan_rss_kb"])
        w.writerows(heap_rows)


def vmstk(binary):
    out = subprocess.check_output([binary], text=True).strip()
    return out.split("=")[-1]


base_stk = vmstk(os.path.join("build", "perf_base", "stack_probe_base"))
asan_stk = vmstk(os.path.join("build", "perf", "stack_probe"))

with open(os.path.join("results", "stack.csv"), "w") as f:
    f.write("mode,vmstk_kb\n")
    f.write("base,%s\n" % base_stk)
    f.write("asan,%s\n" % asan_stk)

print("VmStk: base=%s kB asan=%s kB" % (base_stk, asan_stk))
print("raw data written to results/timing.csv, results/heap.csv, results/stack.csv")
