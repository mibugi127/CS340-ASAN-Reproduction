# CS340‑ASAN‑Reproduction
> Course: CS340 Operating Systems, Academic Year 2026‑2027
> Paper: AddressSanitizer: A Fast Address Sanity Checker
> Paper link: https://www.usenix.org/system/files/conference/atc12/atc12‑final39.pdf
> Official documentation：https://clang.llvm.org/docs/AddressSanitizer.html

## Group Members
| Student ID | Full Name | GitHub Username |
|------------|-----------|----------------|
| 1240016877 | 黄旻烨 | @mibugi127 |
| 1240021797 | 刘莆 | @liupu006 |
| 1240017218 | 黄锦晨 | @LeoH321 |
| 1240036451 | 谭蕊 | @TANRUI94 |

## Project Overview
This project aims to reproduce core performance and bug‑detection claims from the AddressSanitizer ATC 2012 paper.
We test several key bug‑detection cases and evaluate runtime overhead described in the original publication.

## Repository Information
- Starting code / reference: LLVM‑Clang AddressSanitizer implementation
- Recorded original commit: **To be filled**
- List of modified files: **To be filled**

## Environment Requirements
> This project can be built on macOS / Linux.
> For grading reproducibility, please pin your toolchain versions and record hardware in `docs/environment_survey.md`.

### Dependencies
- `clang` (with AddressSanitizer support)
- `gcc` (optional)
- `make` / `cmake`
- Git

Suggested tested versions (fill in after your environment survey):
- Operating System: **To be filled**
- Kernel Version: **To be filled**
- Clang version: **To be filled**
- Hardware info: **To be filled**

> Note: Deviations from the original paper’s experimental setup are documented in `docs/environment_survey.md` and the final report PDF.

## Build & Run Instructions

### 1. Clone this repository
```bash
git clone git@github.com:mibugi127/CS340‑ASAN‑Reproduction.git
cd CS340‑ASAN‑Reproduction