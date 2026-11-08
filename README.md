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
This project aims to reproduce core performance and bug-detection claims from the AddressSanitizer ATC 2012 paper.

## Claims Under Test (Based on Plan B)
*According to the requirements, each claim is strictly linked to a table or figure in the paper.*

- **Claim 1 (C1 - Runtime Performance):** ASAN incurs an average runtime slowdown of 73% compared to uninstrumented code. *(Ref: Paper Figure 2)*
- **Claim 2 (C2 - Memory Overhead):** ASAN incurs an average memory increase of 3.37x. *(Ref: Paper Table 1)*
- **Claim 3 (C3 - Stack Performance):** Stack memory usage is largely unaffected by ASAN. Out of 18 benchmarks, only 6 show obvious changes, and only 3 exceed a 10% increase. *(Ref: Paper Table 2)*

## Repository Information
- Starting code / reference: LLVM/Clang AddressSanitizer implementation (stock `-fsanitize=address`)
- Recorded original commit: **To be filled** (if modified)
- List of modified files: **To be filled**

## Environment Requirements
> This project can be built on macOS / Linux.

### Dependencies
- `clang` (with AddressSanitizer support)
- `gcc` (optional)
- `make` / `cmake`
- Git
- Docker (Optional, for cross-platform consistency)

### Tested Environment
- Operating System: macOS 26.6.2 (Build 25G83)
- Kernel Version: Darwin 25.6.0
- Clang version: Apple clang version 21.0.0 (clang-2100.1.1.101)
- Hardware info: Apple Silicon (arm64 architecture) 

## Build & Run Instructions

### 1. Clone this repository
```bash
git clone git@github.com:mibugi127/CS340-ASAN-Reproduction.git
cd CS340-ASAN-Reproduction