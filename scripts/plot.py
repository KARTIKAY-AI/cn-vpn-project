import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('results/dataset_features.csv')

COLORS = {
    'none': 'gray',
    'wireguard': 'tab:blue',
    'openvpn': 'tab:orange'
}

def sweep(x, fixed, metric, ylabel, title, fname):
    plt.figure(figsize=(7, 4.5))

    for vpn, g in df.query(fixed).groupby('vpn'):
        s = g.groupby(x)[metric].agg(['mean', 'std']).reset_index()

        plt.errorbar(
            s[x],
            s['mean'],
            yerr=s['std'],
            marker='o',
            capsize=3,
            label=vpn,
            color=COLORS[vpn]
        )

    plt.xlabel(
        'Round trip added by netem (ms)'
        if x == 'rtt_ms'
        else 'Packet loss (%)'
    )

    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(alpha=0.3)

    plt.savefig(
        f'graphs/{fname}.png',
        dpi=150,
        bbox_inches='tight'
    )

    plt.close()


D = 'loss_pct == 0'
L = 'rtt_ms == 50'

sweep(
    'rtt_ms', D,
    'throughput_mbps',
    'Throughput (Mbit/s)',
    'Throughput vs delay',
    'throughput_vs_delay'
)

sweep(
    'loss_pct', L,
    'throughput_mbps',
    'Throughput (Mbit/s)',
    'Throughput vs packet loss (round trip 50 ms)',
    'throughput_vs_loss'
)

sweep(
    'rtt_ms', D,
    'latency_ms',
    'Ping latency (ms)',
    'Latency vs delay',
    'latency_vs_delay'
)

sweep(
    'rtt_ms', D,
    'jitter_ms',
    'Jitter (ms)',
    'Jitter vs delay',
    'jitter_vs_delay'
)

sweep(
    'rtt_ms', D,
    'cpu_pct',
    'CPU busy (%)',
    'CPU use vs delay',
    'cpu_vs_delay'
)

print('All graphs generated successfully.')

