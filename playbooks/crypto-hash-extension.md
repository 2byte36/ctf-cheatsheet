# Crypto Hash Length Extension

## When to suspect this

- MAC looks like `md5(secret || message)`, `sha1(secret || message)`, or `sha256(secret || message)`.
- Server gives `message` and digest, then verifies modified message.
- Source uses raw hash instead of HMAC.
- Challenge asks to append `admin=true`, `role=admin`, or extra command.

## Fast triage checklist

- Identify hash algorithm and digest length.
- Confirm construction is `secret || message`, not `message || secret`.
- Confirm not HMAC.
- Determine original message bytes exactly.
- Brute-force secret length range.
- Append extension and URL-encode glue padding if needed.
- Verify against oracle.

## Manual confirmation

```bash
python3 - <<'PY'
import hashlib
print(len(bytes.fromhex("DIGEST")))
PY
```

Vulnerable source shape:

```python
hashlib.sha256(secret + msg).hexdigest()
```

Not vulnerable:

```python
hmac.new(secret, msg, hashlib.sha256).hexdigest()
hashlib.sha256(msg + secret).hexdigest()
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/crypto/hash_length_extension_notes.md](../scripts/crypto/hash_length_extension_notes.md) | Implementation notes | Open notes | Correct tool/flow |
| hash_extender | CLI length extension | `hash_extender -d MSG -s SIG -a '&admin=1' -f sha256 -l 16` | New sig/message |
| hashpumpy | Python/CLI helper | `hashpump -s SIG -d MSG -a APPEND -k 16` | Forged pair |
| Burp Repeater | Oracle verification | Replace msg/sig | Accepted admin |

## Payload starter pack

Extensions:

```text
&admin=true
&role=admin
;cat /flag
,"admin":true
```

Algorithms:

```text
MD5 digest: 32 hex chars
SHA1 digest: 40 hex chars
SHA256 digest: 64 hex chars
```

## Exploit skeleton

```bash
# Try secret lengths 1..64 with hash_extender.
for k in $(seq 1 64); do
  hash_extender -f sha256 -s SIGNATURE_HEX -d 'user=guest' -a '&admin=true' -l "$k"
done
```

Python oracle loop placeholder:

```python
#!/usr/bin/env python3
import requests, subprocess, re

URL = "http://HOST/check"
SIG = "SIGNATURE_HEX"
MSG = "user=guest"
APPEND = "&admin=true"

for k in range(1,65):
    out = subprocess.check_output([
        "hash_extender", "-f", "sha256", "-s", SIG, "-d", MSG, "-a", APPEND, "-l", str(k)
    ], text=True)
    sig = re.search(r"New signature: ([0-9a-f]+)", out).group(1)
    msg = re.search(r"New string: (.+)", out).group(1)
    r = requests.get(URL, params={"sig": sig, "msg": msg}, timeout=10)
    if "admin" in r.text or "flag" in r.text:
        print(k, sig, msg, r.text[:500])
        break
```

## Escalation path

- If accepted, append admin/command parameter and retrieve flag.
- If not accepted, verify exact message encoding and parameter parser.
- Try different secret lengths and algorithms.
- Check whether server URL-decodes before hashing.
- If HMAC, pivot to weak secret brute or logic bug.

## Common bypasses

- URL-encode `\x80` glue padding.
- Parameter parser last-wins: append duplicate parameter.
- Base64 wrapper around message.
- JSON needs valid syntax after padding only if parser sees decoded bytes differently.
- Secret length may be known from source but not remote; brute it.

## Rabbit holes

- Trying length extension against HMAC.
- Hashing displayed URL-encoded message instead of raw bytes.
- Forgetting `message || secret` is not vulnerable.
- Assuming one secret length.

## Final solve checklist

- Vulnerable construction confirmed.
- Forged signature/message accepted by oracle.
- Appended data triggers privilege/flag behavior.
- Exact encoded final request is saved.

