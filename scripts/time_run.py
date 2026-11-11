import resource
import subprocess
import sys
import time

cmd = sys.argv[1:]
if not cmd:
    sys.exit("usage: time_run.py <program> [args...]")

t0 = time.perf_counter()
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
elapsed = time.perf_counter() - t0

ru = resource.getrusage(resource.RUSAGE_CHILDREN)
rss = ru.ru_maxrss
if sys.platform == "darwin":
    rss = rss / 1024.0
print("%.4f,%.0f" % (elapsed, rss))
