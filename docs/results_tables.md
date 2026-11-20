# Performance Results Summary

All data presented below are **Mean ± SD** (calculated based on at least 3 independent runs).

## 1. C1 (Runtime) & C2 (Memory) Overhead Comparison

| Benchmark | Native Time (s) | ASan Time (s) | Time Slowdown | Native RSS (MB) | ASan RSS (MB) | Memory Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| loop | 0.18 ± 0.01 | 0.20 ± 0.01 | +9% | 11.6 ± 0.0 | 11.6 ± 0.0 | 1.00x ± 0.00 |
| matrix | 0.03 ± 0.00 | 0.07 ± 0.01 | +104% | 11.7 ± 0.1 | 11.6 ± 0.1 | 0.99x ± 0.01 |
| sort | 0.11 ± 0.01 | 0.15 ± 0.02 | +44% | 11.6 ± 0.1 | 13.4 ± 0.2 | 1.16x ± 0.02 |
| **Heap-churn** | 33.4 MB* | 113.2 MB* | (N/A) | - | - | **3.39x ± 0.00** |

*(Note: The 33.4 MB and 113.2 MB for Heap-churn represent absolute memory consumption as recorded in our weekly report, resulting in a ratio of 3.39x.)*

**Summary Conclusions:**
*   Average time slowdown: **+52%** (Paper reported: 73%)
*   Memory ratio for large heap allocations (Heap-churn): **3.39x** (Paper reported: 3.37x)

## 2. C3 (Stack Memory) Verification

| Mode | VmStk (Stack Memory) | Conclusion |
| :--- | :--- | :--- |
| Baseline (Native) | 132 KB | No significant impact on stack memory |
| ASan (Instrumented) | 132 KB | (+0.0% overhead) |