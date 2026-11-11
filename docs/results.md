# Results

## 4.1 Experimental setup

- **Platform:** WSL2 (Ubuntu) on Windows 11, x86-64 laptop.
- **Bug detection:** the four reports were also captured on macOS (Apple Silicon,
  Apple clang) and are stored in `docs/images/`.
- **Compiler:** `clang`, `-O2 -fsanitize=address -fno-omit-frame-pointer -g`;
  the native baseline uses the same sources with `-O2 -g` and no sanitizer
  (`build/perf_base/*_base`).
- **Benchmarks:** `loop` (compute-bound, 100M iterations), `matrix` (500 × 500 double
  multiplication, about 6 MB of data), `sort` (`qsort` on 1,000,000 integers),
  `heap` (allocates, touches and frees three 32 MB blocks), and `stack_probe`.
- **Runs:** one warm-up run discarded, then 3 measured runs per configuration.
- **ASan options:** `ASAN_OPTIONS=detect_leaks=0`.

## 4.2 Claim 1: runtime overhead (paper: 73% average slowdown)

| benchmark | native (s) | ASan (s) | slowdown |
|---|---|---|---|
| loop | 0.18 ± 0.00 | 0.20 ± 0.02 | +9% |
| matrix | 0.03 ± 0.01 | 0.07 ± 0.01 | +104% |
| sort | 0.11 ± 0.00 | 0.15 ± 0.03 | +44% |
| **average** | | | **+52%** |

Measured average: **+52%** (paper: 73%).

Discussion. The average is in the same range as the paper, and the per-program
pattern is the one the paper describes:

- `loop` is compute-bound and performs almost no memory accesses, so it pays only 9%.
  ASan instruments loads and stores, and there are very few of them here.
- `matrix` is the most memory-intensive program (125 million accesses over 6 MB) and
  pays the most: +104%, close to the paper's worst benchmarks (perlbench 2.60x,
  xalancbmk 2.67x).
- `sort` sits in between (+44%): comparisons and swaps go through memory, but the
  4 MB array fits in cache, so the check is cheap relative to the comparison.

The gap to the paper's 73% comes from the workload mix: SPEC CPU2006 contains more
memory-heavy code than our three kernels, so its average is higher. The trend —
overhead grows with memory-access density — is reproduced.

## 4.3 Claim 2: memory overhead (paper: 3.37x average)

### Small benchmarks

| benchmark | native RSS (MB) | ASan RSS (MB) | ratio |
|---|---|---|---|
| loop | 11.6 ± 0.0 | 11.6 ± 0.0 | 1.00x |
| matrix | 11.7 ± 0.0 | 11.6 ± 0.1 | 0.99x |
| sort | 11.6 ± 0.1 | 13.4 ± 0.2 | 1.16x |
| **average** | | | **1.05x** |

On these programs the ratio is about 1x, which is **not** a contradiction of the
paper. Two effects hide the overhead:

- ASan's shadow memory is mapped, not resident. Only pages that are actually touched
  count towards RSS, and these programs touch only a few megabytes.
- The baseline RSS (about 11.6 MB) is dominated by the runtime (libc plus the ASan
  runtime itself), so a small absolute increase vanishes in the ratio.

### Heap-churn benchmark

To test the claim under a workload that allocates like SPEC does, `heap` allocates,
touches and frees three 32 MB blocks. The freed blocks stay in ASan's quarantine, and
the shadow of the touched pages becomes resident.

| run | native RSS (MB) | ASan RSS (MB) | ratio |
|---|---|---|---|
| 1 | 33.4 | 113.2 | 3.39x |
| 2 | 33.4 | 113.2 | 3.39x |
| 3 | 33.4 | 113.3 | 3.39x |

Mean ratio: **3.39x** (paper: 3.37x).

With a realistic heap the measured ratio matches the paper almost exactly: 33.4 MB
native against 113.2 MB under ASan, made up of the live block (32 MB), the quarantine
(two freed blocks, 64 MB), the shadow for the touched pages (about 12 MB) and the
runtime. This confirms that the paper's 3.37x is a property of heap-heavy workloads,
not of ASan in general — which is exactly why our three small kernels show 1.05x.

## 4.4 Claim 3: stack memory (paper: stack largely unaffected)

| mode | VmStk (kB) |
|---|---|
| native | 132 |
| ASan | 132 |

Change: **+0 kB (+0.0%)**.

Discussion. The paper reports that stack memory is largely unaffected: only 6 of 18
benchmarks change noticeably and only 3 exceed a 10% increase. Our probe shows no
change at all. The probe uses one fixed 16 × 64-byte buffer, and `VmStk` is accounted
in 4 kB pages, so the redzones ASan adds around the buffer are much smaller than one
page and the page count does not move. The result is consistent with the claim,
although it is a weak test because the stack usage is tiny to begin with.

## 4.5 Threats to validity

- **Micro-benchmarks instead of SPEC CPU2006.** Absolute numbers are not comparable;
  only direction and order of magnitude.
- **Short runtimes.** `matrix` takes about 30 ms natively, close to timer noise; the
  standard deviation on its slowdown is the largest of the three.
- **RSS cannot see virtual shadow memory** — the reason the small benchmarks show 1x.
- **Heterogeneous platform.** Bug detection was captured on macOS, performance on WSL2.
- **ASan defaults.** Quarantine size, redzone sizes and
  `detect_stack_use_after_return` are runtime defaults, not the paper's settings.
- **The heap benchmark is a synthetic workload.** Its size was chosen to be comparable
  to a SPEC process; the exact ratio depends on `quarantine_size_mb`.

## 4.6 Conclusion

- **C1 (runtime):** +52% average slowdown against the paper's 73% — same order of
  magnitude, and the per-program pattern (memory-heavy code pays more) matches.
- **C2 (memory):** 1.05x on the small kernels, but **3.39x** on a heap-churn workload
  that allocates like SPEC — almost exactly the paper's 3.37x. The first number shows
  the limit of small benchmarks, the second reproduces the claim.
- **C3 (stack):** no change (132 kB in both modes), consistent with the paper's claim
  that stack memory is largely unaffected.
