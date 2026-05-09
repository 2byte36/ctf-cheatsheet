#!/usr/bin/env bash
set -euo pipefail

IN="${1:?usage: carve_common.sh <file> [outdir]}"
OUT="${2:-carved}"
mkdir -p "$OUT"

echo "[*] file:"
file -k "$IN" | tee "$OUT/file.txt"

echo "[*] binwalk:"
binwalk "$IN" | tee "$OUT/binwalk.txt" || true
binwalk -e "$IN" --directory "$OUT/binwalk_extract" >/dev/null 2>&1 || true

echo "[*] foremost:"
foremost -i "$IN" -o "$OUT/foremost" >/dev/null 2>&1 || true

echo "[*] magic offsets:"
bash "$(dirname "$0")/magic_scan.sh" "$IN" | tee "$OUT/magic_offsets.txt"

echo "[*] extracted file types:"
find "$OUT" -type f -exec file {} \; || true

