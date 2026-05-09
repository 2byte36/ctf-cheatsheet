#!/usr/bin/env python3
"""Single-byte XOR brute force for hex or raw files."""

import argparse
import string
from pathlib import Path


def load(arg):
    p = Path(arg)
    if p.exists():
        return p.read_bytes()
    return bytes.fromhex(arg)


def score(buf):
    good = bytes(string.printable, "ascii")
    return sum(b in good for b in buf) - sum(b < 9 for b in buf) * 5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data", help="hex string or file path")
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()
    data = load(args.data)
    cands = []
    for k in range(256):
        pt = bytes(b ^ k for b in data)
        cands.append((score(pt), k, pt))
    for s, k, pt in sorted(cands, reverse=True)[:args.top]:
        print(f"key=0x{k:02x} score={s} {pt[:200]!r}")


if __name__ == "__main__":
    main()

