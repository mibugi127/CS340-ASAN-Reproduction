import subprocess
import time
import resource
import os

# 要测试的性能程序
benchmarks = ["loop", "matrix", "sort"]

# 准备 results 文件夹
os.makedirs("results", exist_ok=True)

with open("results/log_perf_3runs.txt", "w") as log_file:
    def log(msg):
        print(msg)
        log_file.write(msg + "\n")

    log("=== C1 & C2 Benchmark Results (3 Runs) ===\n")

    for bench in benchmarks:
        asan_bin = f"./build/perf/{bench}"
        base_bin = f"./build/perf_base/{bench}_base"

        log(f"--- Benchmark: {bench} ---")

        for i in range(1, 4):
            start = time.time()
            subprocess.run([base_bin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            base_time = time.time() - start
            base_mem = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / (1024 * 1024)

            start = time.time()
            subprocess.run([asan_bin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            asan_time = time.time() - start
            asan_mem = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / (1024 * 1024)

            log(f"Run {i}:")
            log(f"  [Base] Time: {base_time:.3f}s | Mem: {base_mem:.2f} MB")
            log(f"  [ASan] Time: {asan_time:.3f}s | Mem: {asan_mem:.2f} MB")
            log(f"  --> Slowdown: {asan_time/base_time:.2f}x | Mem Overhead: {asan_mem/base_mem:.2f}x\n")

print("数据已成功保存到 results/log_perf_3runs.txt")