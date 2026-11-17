#!/bin/bash
# WireGuard tunnel between client and server nodes. Run from ~/cn-vpn-project
set -e

D=$PWD/vpn/wireguard
mkdir -p "$D"
umask 077

[ -f "$D/server.key" ] || wg genkey | tee "$D/server.key" | wg pubkey > "$D/server.pub"
[ -f "$D/client.key" ] || wg genkey | tee "$D/client.key" | wg pubkey > "$D/client.pub"

sudo ip -n server link del wg0 2>/dev/null || true
sudo ip -n client link del wg0 2>/dev/null || true

sudo ip -n server link add wg0 type wireguard

sudo ip netns exec server wg set wg0 listen-port 51820 private-key "$D/server.key" peer "$(cat "$D/client.pub")" allowed-ips 10.9.0.2/32

sudo ip -n server addr add 10.9.0.1/24 dev wg0
sudo ip -n server link set wg0 up

sudo ip -n client link add wg0 type wireguard

sudo ip netns exec client wg set wg0 private-key "$D/client.key" peer "$(cat "$D/server.pub")" allowed-ips 10.9.0.1/32 endpoint 10.0.0.2:51820

sudo ip -n client addr add 10.9.0.2/24 dev wg0
sudo ip -n client link set wg0 up
sudo ip netns exec client ping -c 3 10.9.0.1
