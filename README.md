# CS340-ASAN-Reproduction
> Course: CS340 Operating Systems, Academic Year 2026-2027
> Paper: AddressSanitizer: A Fast Address Sanity Checker
> Paper link: https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf
> Official documentation: https://clang.llvm.org/docs/AddressSanitizer.html

## Group Members
| Student ID | Full Name | GitHub Username |
|------------|-----------|----------------|
| 1240016877 | 黄旻烨 | @mibugi127 |
| 1240021797 | 刘莆 | @liupu006 |
| 1240017218 | 黄锦晨 | @LeoH321 |
| 1240036451 | 谭蕊| @TANRUI94 |

## Project Overview
This project reproduces core performance and bug-detection claims from the
AddressSanitizer ATC 2012 paper.

## Claims Under Test (Based on Plan B)
*According to the requirements, each claim is strictly linked to a table or figure in the paper.*

- **Claim 1 (C1 - Runtime Performance):** ASAN incurs an average runtime slowdown of 73%
  compared to uninstrumented code. *(Ref: Paper Figure 2)*
- **Claim 2 (C2 - Memory Overhead):** ASAN incurs an average memory increase of 3.37x.
  *(Ref: Paper Table 1)*
- **Claim 3 (C3 - Stack Performance):** Stack memory usage is largely unaffected by ASAN;
  out of 18 benchmarks only 6 show obvious changes and only 3 exceed a 10% increase.
  *(Ref: Paper Table 2)*

## Repository Information
- Starting code / reference: LLVM/Clang AddressSanitizer implementation (stock `-fsanitize=address`)
- Recorded original commit: N/A (using stock compiler instrumentation)
- List of modified files: `Makefile`, `scripts/`, `experiments/perf/heap.c`

## Artifacts and Screenshots
- **Final report:** `docs/report.pdf` (6 pages) and its editable source `docs/report.docx`.
- **Bug detection screenshots:** four ASan reports in `docs/images/`
  (double-free, heap overflow, stack overflow, use-after-free).
- **Comparison chart:** `docs/figures/overhead_bar.png` (paper vs ours, C1 and C2).
- **Results tables:** `docs/results_tables.md`.
- **Full results section:** `docs/results.md`.
- **Analysis of discrepancies:** `docs/analysis_discrepancies.md`.

## Environment Requirements

### Tested environments
| Purpose | System | Compiler |
|---|---|---|
| Bug detection screenshots | macOS 26.6.2, Apple Silicon (arm64) | Apple clang 21.0.0 |
| Performance measurements | WSL2, Ubuntu 26.04, x86-64 | Ubuntu clang 21.1.8 |

### Dependencies
- `clang` with AddressSanitizer support
- `make`
- `python3` (for the measurement and plotting scripts)
- `matplotlib` (plot script only)
- Git

## Build & Run Instructions

### 1. Clone the repository
```bash
git clone git@github.com:mibugi127/CS340-ASAN-Reproduction.git
cd CS340-ASAN-Reproduction
```

### 2. Build the ASan binaries
```bash
make
```
This produces `build/bugs/*` and `build/perf/*` (compiled with
`-O2 -fsanitize=address -fno-omit-frame-pointer -g`).

### 3. Build the native baseline
```bash
make base
```
This produces `build/perf_base/*_base` (same sources with `-O2 -g`, no sanitizer).

### 4. Run a bug demo
```bash
./build/bugs/overflow
```
Expected output: an `ERROR: AddressSanitizer: heap-buffer-overflow` report, exit code 1.

### 5. Collect the performance data
```bash
bash scripts/run_all.sh
```
The script runs the bug demos, then measures `loop`, `matrix`, `sort` and `heap`
(one warm-up run discarded, three measured runs each), and writes:

```
results/timing.csv
results/heap.csv
results/stack.csv
results/summary.md
```

Set `REPEATS=5` to change the number of measured runs.

### 6. Regenerate the comparison chart
```bash
python3 scripts/plot_overhead.py
```
Writes `docs/figures/overhead_bar.png`.

### 7. Docker (optional)
```bash
docker build -t asan-repro .
docker run -it --rm asan-repro
```

## Results at a Glance
| Claim | Paper | Ours | Status |
|---|---|---|---|
| C1 runtime | 73% | +52% | Same order of magnitude |
| C2 memory | 3.37x | 3.39x (heap-churn) | Reproduced |
| C3 stack | largely unaffected | 0% change | Reproduced |

See `docs/analysis_discrepancies.md` for why C1 is lower than the paper's value.
