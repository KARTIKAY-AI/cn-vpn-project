#!/bin/bash
# Run from ~/cn-vpn-project with: sudo bash scripts/run_sweep.sh

OUT=results/raw
RUNS=${RUNS:-5}
RATE=${RATE:-2gbit}

mkdir -p "$OUT"

declare -A TARGET=(
    [none]=10.0.0.2
    [wireguard]=10.9.0.1
    [openvpn]=10.8.0.1
)

set_netem() {
    half=$(echo "$1" | awk '{print $1/2}')

    ip netns exec client tc qdisc replace dev veth-c root netem delay "${half}ms" loss "${2}%" rate "$RATE" limit 100000
    ip netns exec server tc qdisc replace dev veth-s root netem delay "${half}ms" rate "$RATE" limit 100000
}

measure() {
    t=${TARGET[$1]}
    tag="${1}_rtt${2}_loss${3}_run${4}"

    ip netns exec client ping -c 10 -i 0.2 -q "$t" > "$OUT/$tag.ping" || true

    for attempt in 1 2; do
        (
            sleep 2
            LC_ALL=C mpstat 1 10 | awk '/^Average:[ ]+all/ {print 100-$NF}' > "$OUT/$tag.cpu"
        ) &

        timeout 40 ip netns exec client iperf3 -c "$t" -t 10 -O 2 --json > "$OUT/$tag.tcp.json" || true

        wait

        grep -q sum_received "$OUT/$tag.tcp.json" && break

        echo "  TCP test failed, retrying ($attempt)"

        pkill iperf3
        sleep 2

        ip netns exec server iperf3 -s -D
        sleep 2
    done

    timeout 30 ip netns exec client iperf3 -c "$t" -u -b 50M -l 1200 -t 5 --json > "$OUT/$tag.udp.json" || true

    sleep 1
}

run_setting() {
    set_netem "$1" "$2"

    for r in $(seq 1 "$RUNS"); do
        for v in none wireguard openvpn; do
            echo "Running $v rtt=$1 loss=$2 run=$r"
            measure "$v" "$1" "$2" "$r"
        done
    done
}

for v in none wireguard openvpn; do
    ip netns exec client ping -c 1 -W 2 "${TARGET[$v]}" > /dev/null || {
        echo "Tunnel $v is down, run all_up.sh first"
        exit 1
    }
done

pkill iperf3
sleep 1

ip netns exec server iperf3 -s -D

for rtt in 0 10 50 100 200; do
    run_setting "$rtt" 0
done

for loss in 0.5 1 2; do
    run_setting 50 "$loss"
done

ip netns exec client tc qdisc del dev veth-c root || true
ip netns exec server tc qdisc del dev veth-s root || true

echo "Sweep finished"
