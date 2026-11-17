#!/bin/bash
# OpenVPN tunnel (UDP, AES-256-GCM). Run from ~/cn-vpn-project
set -e
D=$PWD/vpn/openvpn
mkdir -p "$D"
umask 077

sudo pkill openvpn 2>/dev/null || true
sleep 1

if [ ! -f "$D/server.crt" ]; then
    for n in server client; do
        openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -days 30 -subj "/CN=$n" -keyout "$D/$n.key" -out "$D/$n.crt" 2>/dev/null
    done
fi

SFP=$(openssl x509 -in "$D/server.crt" -noout -fingerprint -sha256 | cut -d= -f2)
CFP=$(openssl x509 -in "$D/client.crt" -noout -fingerprint -sha256 | cut -d= -f2)

cat > "$D/server.conf" << EOF
dev tun
proto udp
local 10.0.0.2
port 1194
server 10.8.0.0 255.255.255.0
topology subnet
dh none
cert $D/server.crt
key $D/server.key
peer-fingerprint $CFP
data-ciphers AES-256-GCM
keepalive 10 60
verb 3
EOF

cat > "$D/client.conf" << EOF
client
dev tun
proto udp
remote 10.0.0.2 1194
nobind
cert $D/client.crt
key $D/client.key
peer-fingerprint $SFP
data-ciphers AES-256-GCM
verb 3
EOF

sudo ip netns exec server openvpn --config "$D/server.conf" --daemon --log /tmp/ovpn-server.log
sleep 2

sudo ip netns exec client openvpn --config "$D/client.conf" --daemon --log /tmp/ovpn-client.log
sleep 6

sudo ip netns exec client ping -c 3 10.8.0.1
