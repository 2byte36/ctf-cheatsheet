#!/usr/bin/env python3
"""Wiener small-d attack template for RSA CTF challenges."""

import sys
import gmpy2
from Crypto.Util.number import long_to_bytes


def contfrac(n, d):
    while d:
        q = n // d
        yield q
        n, d = d, n - q * d


def convergents(cf):
    n0, n1 = 1, 0
    d0, d1 = 0, 1
    for q in cf:
        n0, n1 = q * n0 + n1, n0
        d0, d1 = q * d0 + d1, d0
        yield n0, d0


def wiener(e, n):
    for k, d in convergents(contfrac(e, n)):
        if k == 0:
            continue
        phi_num = e * d - 1
        if phi_num % k:
            continue
        phi = phi_num // k
        s = n - phi + 1
        discr = s * s - 4 * n
        if discr >= 0:
            t = gmpy2.is_square(discr)
            if t:
                return d
    return None


if len(sys.argv) < 3:
    raise SystemExit(f"usage: {sys.argv[0]} N E [C]")

n = int(sys.argv[1], 0)
e = int(sys.argv[2], 0)
d = wiener(e, n)
print("d =", d)
if d and len(sys.argv) > 3:
    c = int(sys.argv[3], 0)
    print(long_to_bytes(pow(c, d, n)))

