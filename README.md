2026-11-17
Fedora release 45 (Forty Five)
7.3.3-300.fc45.x86_64
iperf 3.22 (cJSON 1.7.15)
wireguard-tools v1.0.20260223 - https://git.zx2c4.com/wireguard-tools/
OpenVPN 2.7.9 x86_64-redhat-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] [DCO]
VM: 4 CPUs, 8 GB RAM, 50 GB disk, NAT
Baseline (no VPN, no netem): 22.5 Gbit/s, ping avg 0.069 ms
netem works: delay split across both sides, loss on client side
WireGuard: throughput not measured, ping avg 2.064 ms (MTU 1420 default)
OpenVPN: UDP, AES-256-GCM, default MTU. 2.44 Gbit/s, ping avg 0.169 ms
Link capped at 2 Gbit/s with netem rate to keep the VM stable
Experiment settings: 3 paths (none, WireGuard, OpenVPN), 5 runs each, interleaved.
Delay sweep: round trip 0/10/50/100/200 ms (half per direction via netem), no loss.
Loss sweep: 0.5/1/2 percent on client to server direction only, round trip 50 ms.
TCP: iperf3 10 s, first 2 s omitted. UDP: 50 Mbit/s, 1200 byte datagrams, 5 s. Ping: 10 probes.
CPU: whole-VM busy percent from mpstat during the TCP test (covers both endpoints).
OpenVPN: UDP, AES-256-GCM, default MTU. WireGuard: default MTU 1420.
