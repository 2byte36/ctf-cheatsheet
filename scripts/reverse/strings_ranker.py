#!/usr/bin/env python3
"""Rank strings from a binary by CTF relevance."""

import argparse
import subprocess

KEYWORDS = ["flag", "ctf", "correct", "wrong", "password", "secret", "key", "admin", "debug", "/bin/sh"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("binary")
    args = ap.parse_args()
    out = subprocess.check_output(["strings", "-a", "-n", "4", args.binary], text=True, errors="replace")
    rows = []
    for s in out.splitlines():
        low = s.lower()
        score = sum(10 for k in KEYWORDS if k in low)
        score += min(len(s), 80) / 80
        if score >= 10:
            rows.append((score, s))
    for score, s in sorted(rows, reverse=True):
        print(f"{score:05.1f} {s}")


if __name__ == "__main__":
    main()

