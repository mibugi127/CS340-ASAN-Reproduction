# Weekly Project Log

## Week 1 (Nov 1 - Nov 8, 2026)

### 1. Tasks Completed
*   **A. Environment & Build:** 
    *   Created `Dockerfile` (based on Ubuntu 22.04) and `Makefile` for automated building.
    *   Fixed path issue in `Makefile` for `stack_probe.c`.
    *   Successfully compiled all 8 experiment programs.
*   **B. Experiment Programs:** 
    *   Wrote 4 bug programs (`double_free`, `overflow`, `stack_overflow`, `use_after_free`) and 3 performance programs (`loop`, `matrix`, `sort`).
    *   **Verification:** Successfully triggered AddressSanitizer detection on the `double_free` program (caught `attempting double-free` error).
*   **C. Documentation:** 
    *   Drafted `reproduction_plan.md` defining the 3 core claims (C1: 73% runtime slowdown, C2: 3.37x memory overhead, C3: Stack memory unaffected).
    *   Completed `environment_survey.md`.
*   **D. Contribution:** Created `contribution.md` and established the weekly log system.

### 2. Troubleshooting & Lessons Learned (Critical)
During the initial verification, we encountered two major environment-specific issues:
*   **Issue 1: macOS SDK Compatibility:** `clang` failed to compile with a `tapi error: malformed file` due to the macOS 27 SDK on Apple Silicon. 
    *   *Resolution:* Removed the problematic SDK folder and forced the compiler to use the correct SDK path.
*   **Issue 2: Compiler Optimization on Bugs:** At `-O2` optimization level, Apple Clang optimized away the `free(p); free(p);` dead code, causing ASan to miss the double-free bug.
    *   *Resolution:* Added `printf` statements / `volatile` keywords to the bug programs to prevent dead code elimination. 
    *   *Insight:* This highlights a platform deviation from the original paper (which was likely tested on older x86 Linux). We plan to document this in the "Analysis of Discrepancies" section.

### 3. Next Steps for Week 2
*   Run all performance benchmarks (`perf/*.c`) 3+ times and collect `time` data.
*   Calculate Mean ± Standard Deviation for the performance overhead (Claim 1 and Claim 2).
*   Begin drafting the "Results" section of the final report.

## Week 2 (Nov 9 - Nov 15, 2026)

### 1. Tasks Completed
*   **A. Bug detection:** all four bug programs are now detected by ASan on macOS:
    double-free, heap-buffer-overflow, stack-buffer-overflow and heap-use-after-free.
    The reports are saved as screenshots in `docs/images/`.
*   **B. Baseline build:** added a `base` target to the `Makefile`; it compiles the same
    performance sources with `-O2 -g` (no sanitizer) into `build/perf_base/*_base`.
*   **C. Harness:** `scripts/run_all.sh` builds both variants, runs the bug demos,
    then calls `scripts/run_bench.py`.
*   **D. Measurement fix:** the first version of `run_bench.py` read
    `ru_maxrss` from `RUSAGE_CHILDREN`, which is a running maximum over *all*
    children, so the memory numbers were meaningless. It now measures each child in
    a separate process (`scripts/time_run.py`), discards one warm-up run, and writes
    `results/timing.csv` + `results/stack.csv`; `scripts/analyze.py` turns them into
    `results/summary.md`.

### 2. Measurements
| benchmark | native (s) | ASan (s) | slowdown | native RSS (MB) | ASan RSS (MB) | ratio |
|---|---|---|---|---|---|---|
| loop | 0.18 | 0.20 | +9% | 11.6 | 11.6 | 1.00x |
| matrix | 0.03 | 0.07 | +104% | 11.7 | 11.6 | 0.99x |
| sort | 0.11 | 0.15 | +44% | 11.6 | 13.4 | 1.16x |

*   Average slowdown: **+52%** (paper: 73%)
*   Average memory ratio on the small kernels: **1.05x** (paper: 3.37x)
*   Heap-churn experiment (3 x 32 MB): 33.4 MB -> 113.2 MB = **3.39x** (paper: 3.37x)
*   VmStk: native 132 kB, ASan 132 kB (+0.0%)

### 3. Troubleshooting
*   The first measurement run was much slower than the rest (1.70 s vs 0.07 s) because
    the binary was not yet in the page cache; the warm-up run now absorbs this.
*   On macOS `ru_maxrss` is reported in bytes, on Linux in kilobytes; `time_run.py`
    normalises both to kilobytes.
*   The shell scripts were saved with CRLF line endings, which made bash fail with
    `$'\r': command not found`. Converted to LF and added `.gitattributes` so it does
    not happen again.
*   The first version of `run_bench.py` read `ru_maxrss` from `RUSAGE_CHILDREN`, which
    is a running maximum over all children; the memory numbers it printed were
    therefore meaningless and were discarded.

### 4. Next Steps for Week 3
*   Plot runtime and memory per benchmark for the report.
*   Scale the workloads up (larger matrix and sort, a large heap allocation) to get a
    measurable memory ratio.
*   Write the "Analysis of discrepancies" section (micro-benchmarks vs SPEC,
    RSS vs virtual shadow memory, platform differences).