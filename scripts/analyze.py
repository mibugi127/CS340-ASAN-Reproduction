import csv
import os
import statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "results")


def read_timing():
    rows = []
    with open(os.path.join(RES, "timing.csv")) as f:
        for r in csv.DictReader(f):
            rows.append({
                "program": r["program"],
                "mode": r["mode"],
                "seconds": float(r["seconds"]),
                "rss": float(r["maxrss_kb"]),
            })
    return rows


def agg(rows, prog, mode):
    t = [r["seconds"] for r in rows if r["program"] == prog and r["mode"] == mode]
    m = [r["rss"] for r in rows if r["program"] == prog and r["mode"] == mode]
    return (st.mean(t), st.pstdev(t) if len(t) > 1 else 0.0,
            st.mean(m), st.pstdev(m) if len(m) > 1 else 0.0)


def main():
    rows = read_timing()
    progs = sorted({r["program"] for r in rows})

    lines = ["# Week 2 results", "",
             "Wall time and peak RSS, averaged over the runs in `results/timing.csv`.", "",
             "| program | time native (s) | time ASan (s) | slowdown | memory native (MB) | memory ASan (MB) | memory ratio |",
             "|---|---|---|---|---|---|---|"]

    slowdowns, memratios = [], []
    for p in progs:
        tb, sb, mb, smb = agg(rows, p, "base")
        ta, sa, ma, sma = agg(rows, p, "asan")
        slow = (ta / tb - 1.0) * 100.0 if tb > 0 else float("nan")
        ratio = ma / mb if mb > 0 else float("nan")
        slowdowns.append(slow)
        memratios.append(ratio)
        lines.append(
            "| %s | %.2f ± %.2f | %.2f ± %.2f | %+.0f%% | %.1f ± %.1f | %.1f ± %.1f | %.2fx |"
            % (p, tb, sb, ta, sa, slow, mb / 1024, smb / 1024, ma / 1024, sma / 1024, ratio)
        )

    lines += ["",
              "**Average slowdown: %+.0f%%** (paper: 73%%)." % st.mean(slowdowns),
              "**Average memory ratio: %.2fx** (paper: 3.37x)." % st.mean(memratios),
              ""]

    heap_path = os.path.join(RES, "heap.csv")
    if os.path.exists(heap_path):
        with open(heap_path) as f:
            hr = list(csv.DictReader(f))
        if hr:
            base = [float(r["base_rss_kb"]) for r in hr]
            asan = [float(r["asan_rss_kb"]) for r in hr]
            lines += ["## Heap-churn experiment (Claim 2)", "",
                      "`heap` allocates, touches and frees three 32 MB blocks, so a large",
                      "part of the freed memory stays in ASan's quarantine and the shadow",
                      "for the touched pages becomes resident.", "",
                      "| run | native RSS (MB) | ASan RSS (MB) | ratio |",
                      "|---|---|---|---|"]
            for i, (b, a) in enumerate(zip(base, asan), 1):
                lines.append("| %d | %.1f | %.1f | %.2fx |" % (i, b / 1024, a / 1024, a / b))
            lines += ["",
                      "Mean ratio: **%.2fx** (paper: 3.37x)."
                      % (st.mean(asan) / st.mean(base)), ""]

    stack_path = os.path.join(RES, "stack.csv")
    if os.path.exists(stack_path):
        with open(stack_path) as f:
            stack = {r["mode"]: float(r["vmstk_kb"]) for r in csv.DictReader(f)}
        if "base" in stack and "asan" in stack:
            delta = stack["asan"] - stack["base"]
            lines += ["## Stack memory (VmStk)", "",
                      "| mode | VmStk (kB) |", "|---|---|",
                      "| native | %.0f |" % stack["base"],
                      "| ASan | %.0f |" % stack["asan"], "",
                      "Change: %+.0f kB (%+.1f%%)." % (delta, delta / stack["base"] * 100.0), ""]

    lines += ["## Notes", "",
              "- ASan binaries run with `ASAN_OPTIONS=detect_leaks=0`.",
              "- One warm-up run per configuration is discarded before the measured runs.",
              "- These are micro-benchmarks, not SPEC CPU2006: absolute numbers are not comparable,",
              "  only the direction and the order of magnitude.",
              ""]

    out = os.path.join(RES, "summary.md")
    with open(out, "w") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
