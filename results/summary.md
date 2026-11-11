# Week 2 results

Wall time and peak RSS, averaged over the runs in `results/timing.csv`.

| program | time native (s) | time ASan (s) | slowdown | memory native (MB) | memory ASan (MB) | memory ratio |
|---|---|---|---|---|---|---|
| loop | 0.18 ± 0.00 | 0.20 ± 0.02 | +9% | 11.6 ± 0.0 | 11.6 ± 0.0 | 1.00x |
| matrix | 0.03 ± 0.01 | 0.07 ± 0.01 | +104% | 11.7 ± 0.0 | 11.6 ± 0.1 | 0.99x |
| sort | 0.11 ± 0.00 | 0.15 ± 0.03 | +44% | 11.6 ± 0.1 | 13.4 ± 0.2 | 1.16x |

**Average slowdown: +52%** (paper: 73%).
**Average memory ratio: 1.05x** (paper: 3.37x).

## Heap-churn experiment (Claim 2)

`heap` allocates and frees 4 x 32 MB, so a large part of the freed
memory stays in ASan's quarantine and the shadow for the touched
pages becomes resident.

| run | native RSS (MB) | ASan RSS (MB) | ratio |
|---|---|---|---|
| 1 | 33.4 | 113.2 | 3.39x |
| 2 | 33.4 | 113.2 | 3.39x |
| 3 | 33.4 | 113.3 | 3.39x |

Mean ratio: **3.39x** (paper: 3.37x).

## Stack memory (VmStk)

| mode | VmStk (kB) |
|---|---|
| native | 132 |
| ASan | 132 |

Change: +0 kB (+0.0%).

## Notes

- ASan binaries run with `ASAN_OPTIONS=detect_leaks=0`.
- One warm-up run per configuration is discarded before the measured runs.
- These are micro-benchmarks, not SPEC CPU2006: absolute numbers are not comparable,
  only the direction and the order of magnitude.
