#!/usr/bin/env bash
set -euo pipefail

PCAP="${1:?usage: pcap_http_extract.sh <capture.pcap> [outdir]}"
OUT="${2:-extracts_http}"
mkdir -p "$OUT"

capinfos "$PCAP" | tee "$OUT/capinfos.txt" || true
tshark -r "$PCAP" -q -z io,phs | tee "$OUT/protocol_hierarchy.txt" || true
tshark -r "$PCAP" -Y 'http.request' -T fields \
  -e frame.number -e frame.time_epoch -e ip.src -e http.host -e http.request.method -e http.request.uri \
  | tee "$OUT/http_requests.tsv" || true
tshark -r "$PCAP" --export-objects "http,$OUT/objects" >/dev/null 2>&1 || true
find "$OUT" -type f -exec file {} \; | tee "$OUT/filetypes.txt" || true
rg -a -n -i 'flag|ctf|secret|token|password|key' "$OUT" || true

