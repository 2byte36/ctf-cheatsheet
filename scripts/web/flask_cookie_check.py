#!/usr/bin/env python3
"""Small Flask signed-cookie helper.

Requires Flask/itsdangerous installed. Use flask-unsign for wordlist attacks;
this helper decodes or signs when a secret is already known.
"""

import argparse
from flask.sessions import SecureCookieSessionInterface
from flask import Flask


def serializer(secret):
    app = Flask(__name__)
    app.secret_key = secret
    return SecureCookieSessionInterface().get_signing_serializer(app)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cookie", required=True)
    ap.add_argument("--secret", required=True)
    ap.add_argument("--set", action="append", default=[], help="Set key=value before re-signing")
    args = ap.parse_args()

    s = serializer(args.secret)
    data = s.loads(args.cookie)
    print("decoded:", dict(data))
    for item in args.set:
        k, v = item.split("=", 1)
        if v.lower() == "true":
            v = True
        elif v.lower() == "false":
            v = False
        data[k] = v
    if args.set:
        print("signed:", s.dumps(dict(data)))


if __name__ == "__main__":
    main()

