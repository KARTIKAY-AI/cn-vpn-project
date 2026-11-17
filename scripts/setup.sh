#!/bin/bash
# Two nodes (client, server) joined by a virtual cable

sudo ip netns del client 2>/dev/null || true
sudo ip netns del server 2>/dev/null || true

sudo ip netns add client
sudo ip netns add server

sudo ip link add veth-c type veth peer name veth-s

sudo ip link set veth-c netns client
sudo ip link set veth-s netns server

sudo ip -n client addr add 10.0.0.1/24 dev veth-c
sudo ip -n server addr add 10.0.0.2/24 dev veth-s

sudo ip -n client link set lo up
sudo ip -n server link set lo up

sudo ip -n client link set veth-c up
sudo ip -n server link set veth-s up

sudo ip netns exec client ping -c 3 10.0.0.2
