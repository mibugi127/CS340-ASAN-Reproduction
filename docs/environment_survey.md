# Environment Survey

## 1. Hardware
*   **CPU:** Apple Silicon (ARM64) - *replace with actual model if needed*
*   **RAM:** *e.g., 16GB*

## 2. Software
*   **Host OS:** macOS 26.6.2 (Build 25G83)
*   **Kernel Version:** Darwin 25.6.0
*   **Compiler:** Apple clang version 21.0.0 (clang-2100.1.1.101)
*   **Build Tools:** GNU Make, Docker (Ubuntu 22.04 container with LLVM/Clang)

## 3. Deviations from the Paper's Setup
*   **Original Paper Environment:** The paper likely used x86_64 architecture and an older version of Clang/LLVM on Linux.
*   **Our Setup:** We are using an ARM64 Mac system. This architecture difference might cause slight variations in the performance overhead. We will also verify our results in the Docker container (Ubuntu 22.04) to align closer with the paper's OS environment.