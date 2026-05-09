#!/usr/bin/env python3
"""Recover XOR key bytes from known plaintext prefix or crib."""

import argparse
from pathlib import Path


def load(s):
    p = Path(s)
    if p.exists():
        return p.read_bytes()
    return bytes.fromhex(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ct", required=True, help="ciphertext hex or file")
    ap.add_argument("--known", required=True, help="known plaintext string")
    ap.add_argument("--offset", type=int, default=0)
    args = ap.parse_args()
    ct = load(args.ct)
    known = args.known.encode()
    key = bytes(ct[args.offset + i] ^ known[i] for i in range(len(known)))
    print("key-bytes:", key)
    print("key-hex:", key.hex())
    trial = bytes(ct[i] ^ key[(i - args.offset) % len(key)] for i in range(len(ct)))
    print("trial:", trial[:500])


if __name__ == "__main__":
    main()

