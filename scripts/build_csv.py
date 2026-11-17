import json
import glob
import os
import pandas as pd

rows = []

for path in sorted(glob.glob('results/raw/*.tcp.json')):
    tag = os.path.basename(path).replace('.tcp.json', '')
    p = tag.split('_')

    row = {
        'vpn': p[0],
        'rtt_ms': float(p[1][3:]),
        'loss_pct': float(p[2][4:]),
        'run': int(p[3][3:])
    }

    try:
        with open(path) as f:
            d = json.load(f)
        row['throughput_mbps'] = d['end']['sum_received']['bits_per_second'] / 1e6
        row['retransmits'] = d['end']['sum_sent']['retransmits']
    except Exception:
        row['throughput_mbps'] = None
        row['retransmits'] = None

    try:
        with open(f'results/raw/{tag}.udp.json') as f:
            d = json.load(f)
        row['jitter_ms'] = d['end']['sum']['jitter_ms']
        row['udp_loss_pct'] = d['end']['sum']['lost_percent']
    except Exception:
        row['jitter_ms'] = None
        row['udp_loss_pct'] = None

    try:
        with open(f'results/raw/{tag}.ping') as f:
            txt = f.read()
        line = [l for l in txt.splitlines() if 'min/avg/max' in l][0]
        row['latency_ms'] = float(line.split('=')[1].split('/')[1])
    except Exception:
        row['latency_ms'] = None

    try:
        with open(f'results/raw/{tag}.cpu') as f:
            row['cpu_pct'] = float(f.read().strip())
    except Exception:
        row['cpu_pct'] = None

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv('results/dataset.csv', index=False)

print("Dataset shape:", df.shape)
print(df.head())
