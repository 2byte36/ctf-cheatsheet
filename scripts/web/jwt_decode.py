#!/usr/bin/env python3
"""Decode JWT header and payload without verifying the signature."""

import argparse
import base64
import json


def b64url_decode(part):
    part += "=" * (-len(part) % 4)
    return base64.urlsafe_b64decode(part.encode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("token")
    args = ap.parse_args()
    parts = args.token.split(".")
    if len(parts) < 2:
        raise SystemExit("Not enough JWT parts")
    for name, part in [("header", parts[0]), ("payload", parts[1])]:
        raw = b64url_decode(part)
        print(f"== {name} ==")
        try:
            print(json.dumps(json.loads(raw), indent=2, sort_keys=True))
        except json.JSONDecodeError:
            print(raw)
    if len(parts) > 2:
        print("== signature bytes ==")
        print(b64url_decode(parts[2]).hex())


if __name__ == "__main__":
    main()

