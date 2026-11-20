"""Build the C1/C2 comparison chart from results/timing.csv and results/heap.csv."""
import csv
import os
import statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results")
OUT = os.path.join(ROOT, "docs", "figures")
os.makedirs(OUT, exist_ok=True)


def load_timing():
    rows = []
    with open(os.path.join(RES, "timing.csv")) as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def mean_time(rows, prog, mode):
    vals = [float(r["seconds"]) for r in rows if r["program"] == prog and r["mode"] == mode]
    return st.mean(vals)


def main():
    rows = load_timing()
    progs = sorted({r["program"] for r in rows})

    per_bench = []
    for p in progs:
        base = mean_time(rows, p, "base")
        asan = mean_time(rows, p, "asan")
        per_bench.append(asan / base)

    c1 = st.mean(per_bench)
    c1_sd = st.pstdev(per_bench)

    heap_path = os.path.join(RES, "heap.csv")
    ratios = []
    if os.path.exists(heap_path):
        with open(heap_path) as f:
            for r in csv.DictReader(f):
                ratios.append(float(r["asan_rss_kb"]) / float(r["base_rss_kb"]))
    c2 = st.mean(ratios) if ratios else float("nan")
    c2_sd = st.pstdev(ratios) if len(ratios) > 1 else 0.0

    labels = ["C1 runtime\n(slowdown multiplier)", "C2 memory\n(RSS multiplier)"]
    paper = [1.73, 3.37]
    ours = [c1, c2]
    errs = [c1_sd, c2_sd]

    x = np.arange(len(labels))
    width = 0.34

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    b1 = ax.bar(x - width / 2, paper, width, label="Paper (ATC 2012)", color="#b0b0b0")
    b2 = ax.bar(x + width / 2, ours, width, yerr=errs, capsize=5,
                label="Ours (mean ± SD)", color="#4c78a8")

    for bars, vals in ((b1, paper), (b2, ours)):
        for rect, v in zip(bars, vals):
            ax.annotate("%.2fx" % v, xy=(rect.get_x() + rect.get_width() / 2, v),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=9)

    ax.set_ylabel("Overhead multiplier (higher is worse)")
    ax.set_title("ASan overhead: paper vs our reproduction")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 4.2)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    out = os.path.join(OUT, "overhead_bar.png")
    fig.savefig(out, dpi=220)
    plt.close(fig)

    print("C1 (runtime): %.2fx ± %.2f  -> %.0f%% slowdown (paper 73%%)"
          % (c1, c1_sd, (c1 - 1) * 100))
    print("C2 (memory):  %.2fx ± %.2f  (paper 3.37x)" % (c2, c2_sd))
    print("saved", out)


if __name__ == "__main__":
    main()
