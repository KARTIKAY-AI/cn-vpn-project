import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('results/dataset.csv')

print('Rows:', len(df))
print('Missing values per column:')
print(df.isna().sum())

# Derived metrics compared with the no-VPN baseline
# at the same network setting
keys = ['rtt_ms', 'loss_pct']

base = df[df.vpn == 'none'].groupby(keys)[
    ['throughput_mbps', 'latency_ms']
].mean()

base.columns = ['base_mbps', 'base_lat_ms']

df = df.join(base, on=keys)

df['overhead_pct'] = 100 * (
    1 - df.throughput_mbps / df.base_mbps
)

df['added_latency_ms'] = df.latency_ms - df.base_lat_ms

df['mbps_per_cpu'] = df.throughput_mbps / df.cpu_pct

df.to_csv('results/dataset_features.csv', index=False)

# Summary statistics per setting
summary = df.groupby(['vpn', 'rtt_ms', 'loss_pct']).agg(
    runs=('run', 'count'),
    thr_mean=('throughput_mbps', 'mean'),
    thr_std=('throughput_mbps', 'std'),
    lat_mean=('latency_ms', 'mean'),
    jitter_mean=('jitter_ms', 'mean'),
    cpu_mean=('cpu_pct', 'mean'),
    overhead_mean=('overhead_pct', 'mean')
)

summary['cv_pct'] = 100 * summary.thr_std / summary.thr_mean

summary = summary.round(2)

summary.to_csv('results/summary.csv')

print(summary.to_string())
print()

print('Noisy settings (spread above 20 percent of the mean):')
print(
    summary[summary.cv_pct > 20][
        ['thr_mean', 'thr_std', 'cv_pct']
    ].to_string()
)

# Box plot: run-to-run spread per VPN at RTT 50 ms, no loss
sub = df[(df.rtt_ms == 50) & (df.loss_pct == 0)]

sub.boxplot(
    column='throughput_mbps',
    by='vpn',
    figsize=(6, 4.5)
)

plt.suptitle('')
plt.title('Throughput per path (round trip 50 ms, no loss)')
plt.ylabel('Mbit/s')

plt.savefig(
    'graphs/eda_boxplot.png',
    dpi=150,
    bbox_inches='tight'
)

plt.close()

# Correlation heatmap
cols = [
    'rtt_ms',
    'loss_pct',
    'throughput_mbps',
    'latency_ms',
    'jitter_ms',
    'cpu_pct'
]

corr = df[cols].corr()

fig, ax = plt.subplots(figsize=(6.5, 5.5))

im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)

ax.set_xticks(range(len(cols)))
ax.set_xticklabels(cols, rotation=45, ha='right')

ax.set_yticks(range(len(cols)))
ax.set_yticklabels(cols)

for i in range(len(cols)):
    for j in range(len(cols)):
        ax.text(
            j,
            i,
            f'{corr.iloc[i, j]:.2f}',
            ha='center',
            va='center',
            fontsize=8
        )

fig.colorbar(im)

ax.set_title('Correlation of measured variables')

fig.savefig(
    'graphs/eda_heatmap.png',
    dpi=150,
    bbox_inches='tight'
)

plt.close()

print('\nEDA completed successfully.')
print('Generated:')
print('- results/dataset_features.csv')
print('- results/summary.csv')
print('- graphs/eda_boxplot.png')
print('- graphs/eda_heatmap.png')

