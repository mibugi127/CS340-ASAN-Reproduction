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