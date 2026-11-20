# Results Tables

All numbers are mean ± standard deviation over three measured runs, after one discarded
warm-up run per configuration.

## 1. C1 runtime and C2 memory on the small kernels

| Benchmark | Native time (s) | ASan time (s) | Slowdown | Native RSS (MB) | ASan RSS (MB) | Memory ratio |
|---|---|---|---|---|---|---|
| loop | 0.18 ± 0.01 | 0.20 ± 0.01 | +9% | 11.6 ± 0.0 | 11.6 ± 0.0 | 1.00x |
| matrix | 0.03 ± 0.00 | 0.07 ± 0.01 | +104% | 11.7 ± 0.1 | 11.6 ± 0.1 | 0.99x |
| sort | 0.11 ± 0.01 | 0.15 ± 0.02 | +44% | 11.6 ± 0.1 | 13.4 ± 0.2 | 1.16x |
| **Average** | | | **+52%** | | | **1.05x** |

## 2. C2 on a heap-churn workload

`heap` allocates, touches and frees three 32 MB blocks, so the freed memory stays in
ASan's quarantine and the shadow of the touched pages becomes resident.

| Run | Native RSS (MB) | ASan RSS (MB) | Ratio |
|---|---|---|---|
| 1 | 33.4 | 113.2 | 3.39x |
| 2 | 33.4 | 113.2 | 3.39x |
| 3 | 33.4 | 113.3 | 3.39x |
| **Mean** | 33.4 | 113.2 | **3.39x** |

## 3. C3 stack memory

| Mode | VmStk | Change |
|---|---|---|
| Native | 132 kB | — |
| ASan | 132 kB | +0.0% |

## 4. Summary against the paper

| Claim | Paper | Ours | Note |
|---|---|---|---|
| C1 runtime | 73% | +52% | Micro-benchmarks; `loop` is compute-bound and dilutes the average |
| C2 memory | 3.37x | 3.39x | Measured on the heap-churn workload |
| C3 stack | largely unaffected | 0% | Consistent |
