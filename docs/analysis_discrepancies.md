# Analysis of Discrepancies

Our reproduction does not match every number in the paper. Below we separate the three
claims, report our value and the paper's, and explain the difference.

## 1. Runtime overhead (C1)

| | Value |
|---|---|
| Ours | **+52%** average slowdown (1.52x) |
| Paper | **+73%** average slowdown (1.73x) |

The direction and the order of magnitude match; the gap comes from the workload mix.

1. **Workload size and mix.** We used three micro-benchmarks (`loop`, `matrix`, `sort`).
   `loop` is compute-bound and pays only +9%, which pulls our average down. SPEC CPU2006
   contains more memory-heavy code, so its average is higher.
2. **Per-benchmark spread.** Our three ratios are 1.09x, 2.04x and 1.44x (standard
   deviation 0.39x), so the average depends strongly on which kernels are included.
   The paper averages 18 programs.
3. **Platform and compiler.** Performance numbers were measured under WSL2 (Ubuntu,
   x86-64, recent clang). The paper used clang 3.x on x86-64 Linux in 2012; code
   generation and the sanitizer runtime have changed since then.

## 2. Memory overhead (C2)

| | Value |
|---|---|
| Ours, small kernels | **1.05x** |
| Ours, heap-churn workload | **3.39x** |
| Paper | **3.37x** |

This looked like a failure at first, and it is the most instructive discrepancy.

1. **RSS does not see the shadow memory.** ASan maps shadow memory for 1/8 of the address
   space, but only pages that are actually touched become resident. Our three kernels
   allocate a few megabytes, so `ru_maxrss` barely moves — the 11.6 MB baseline is
   dominated by the runtime, not by the program's data.
2. **The ratio is a property of the workload, not of ASan.** Once the workload allocates
   like a SPEC process (`heap`: three 32 MB blocks allocated, touched and freed), the
   freed blocks stay in ASan's quarantine and the shadow becomes resident. The measured
   ratio is then 3.39x, within 1% of the paper's 3.37x.
3. **Allocator and OS differences.** macOS and Linux differ in how freed pages are
   returned to the OS, which is why we report the WSL2 numbers and keep the macOS bug
   screenshots separate.

## 3. Stack memory (C3)

| Mode | VmStk |
|---|---|
| Native | 132 kB |
| ASan | 132 kB |

No change, which is consistent with the paper: ASan adds redzones around stack objects,
but they are small relative to a page, and `VmStk` is accounted in 4 kB pages. The paper
reports that only 6 of 18 benchmarks change noticeably and only 3 exceed 10%. Our probe
uses a fixed 16 × 64 byte buffer, so a 0% change is expected rather than surprising.

## Summary

| Claim | Paper | Ours | Verdict |
|---|---|---|---|
| C1 runtime | 73% | 52% | Same order of magnitude; difference explained by workload mix |
| C2 memory | 3.37x | 3.39x (heap-churn) | Reproduced once the workload allocates enough |
| C3 stack | largely unaffected | 0% change | Reproduced |
