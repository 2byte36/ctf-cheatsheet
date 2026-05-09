#!/usr/bin/env python3
"""Quick RSA checks for CTF inputs."""

import argparse
from math import gcd
import gmpy2
from Crypto.Util.number import long_to_bytes, inverse


def parse_int(x):
    return int(x, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", required=True, type=parse_int)
    ap.add_argument("--e", required=True, type=parse_int)
    ap.add_argument("--c", type=parse_int)
    ap.add_argument("--p", type=parse_int)
    ap.add_argument("--q", type=parse_int)
    args = ap.parse_args()

    print(f"n bits: {args.n.bit_length()}")
    print(f"e: {args.e}")

    if args.c is not None:
        root, exact = gmpy2.iroot(args.c, args.e)
        print(f"small-e exact root: {exact}")
        if exact:
            print(long_to_bytes(int(root)))

    if args.p and args.q:
        phi = (args.p - 1) * (args.q - 1)
        d = inverse(args.e, phi)
        print(f"d: {d}")
        if args.c is not None:
            print(long_to_bytes(pow(args.c, d, args.n)))


if __name__ == "__main__":
    main()

