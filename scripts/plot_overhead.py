import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('../docs/figures', exist_ok=True)

df_timing = pd.read_csv('../results/timing.csv')
df_heap = pd.read_csv('../results/heap.csv') 

time_overhead = df_timing.groupby('run').apply(
    lambda x: x[x['mode']=='asan']['seconds'].mean() / x[x['mode']=='base']['seconds'].mean()
).reset_index(drop=True)

c1_mean = time_overhead.mean()
c1_std = time_overhead.std()

mem_overhead = df_heap['asan_rss_kb'] / df_heap['base_rss_kb']

c2_mean = mem_overhead.mean()
c2_std = mem_overhead.std()

labels = ['C1 (Time Overhead)', 'C2 (Memory Overhead)']

paper_means = [1.5, 2.0] 
paper_stds = [0, 0] 

our_means = [c1_mean, c2_mean]
our_stds = [c1_std, c2_std]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 6))

rects1 = ax.bar(x - width/2, paper_means, width, label='Paper', color='lightgray')

rects2 = ax.bar(x + width/2, our_means, width, yerr=our_stds, label='Ours (Mean ± SD)', color='skyblue', capsize=5)

ax.set_ylabel('Overhead Multiplier (Higher is worse)')
ax.set_title('Performance Overhead: Paper vs Ours')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

def autolabel(rects, is_paper=False):
    for rect in rects:
        height = rect.get_height()
        label_text = f'{height:.2f}' if is_paper else f'{height:.2f}±{our_stds[rects.index(rect)]:.2f}'
        ax.annotate(label_text,
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

autolabel(rects1, is_paper=True)
autolabel(rects2, is_paper=False)

fig.tight_layout()

plt.savefig('../docs/figures/overhead_bar.png', dpi=300)
print("图表已生成并保存至 docs/figures/overhead_bar.png")
print(f"C1 平均开销: {c1_mean:.2f}x, 标准差: {c1_std:.2f}")
print(f"C2 平均开销: {c2_mean:.2f}x, 标准差: {c2_std:.2f}")