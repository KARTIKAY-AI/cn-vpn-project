#!/bin/bash
# Rebuilds nodes, both VPNs and the iperf3 server
set -e
cd ~/cn-vpn-project
sudo pkill openvpn 2>/dev/null || true
sudo pkill iperf3 2>/dev/null || true
bash scripts/setup.sh
bash scripts/wg_up.sh
bash scripts/ovpn_up.sh
sudo ip netns exec server iperf3 -s -D
echo Lab ready
