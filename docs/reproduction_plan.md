# Reproduction Plan: AddressSanitizer (ATC 2012)

## 1. Claims Under Test
Based on the paper "AddressSanitizer: A Fast Address Sanity Checker" (ATC 2012), we plan to reproduce the following 3 claims:

*   **Claim 1 (Runtime Overhead):** ASAN incurs an average slowdown of 73% compared to uninstrumented code. *(Ref: Paper Figure 2)*
*   **Claim 2 (Memory Overhead):** ASAN incurs an average memory increase of 3.37x. *(Ref: Paper Table 1)*
*   **Claim 3 (Stack Memory Impact):** Stack memory usage is largely unaffected by ASAN. Out of 18 benchmarks, only 6 show obvious changes, and only 3 exceed a 10% increase. *(Ref: Paper Table 2)*

## 2. Experimental Setup & Workloads
*   **Benchmarks:** We will use standard benchmarks (e.g., SPEC CPU2006 or similar micro-benchmarks) to evaluate the overhead.
*   **Metrics:**
    *   Execution time (in seconds) for runtime overhead.
    *   Peak memory usage (RSS) for memory overhead.
    *   Stack memory usage.
*   **Runs:** Each experiment will be run at least 3 times to calculate Mean ± Standard Deviation.

## 3. Extension Plan
*   **Question:** How does ASAN performance overhead change with newer compiler optimizations (e.g., `-O3` instead of `-O2`)?
*   **Design:** Run the same benchmarks with `-O3 -fsanitize=address` and compare the overhead against `-O3` uninstrumented code.