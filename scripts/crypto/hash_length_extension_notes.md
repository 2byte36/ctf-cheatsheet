# Hash Length Extension Notes

Use when a challenge signs data as:

```python
hashlib.sha1(secret + message).hexdigest()
hashlib.sha256(secret + message).hexdigest()
hashlib.md5(secret + message).hexdigest()
```

Do not use for HMAC or `hash(message + secret)`.

## CLI with hash_extender

```bash
hash_extender \
  -f sha256 \
  -s SIGNATURE_HEX \
  -d 'user=guest' \
  -a '&admin=true' \
  -l 16
```

Try secret lengths:

```bash
for k in $(seq 1 64); do
  hash_extender -f sha256 -s SIGNATURE_HEX -d 'user=guest' -a '&admin=true' -l "$k"
done
```

## What To Verify

- Exact original message bytes.
- Whether the server hashes raw bytes or URL-decoded bytes.
- Whether glue padding must be URL-encoded.
- Whether duplicate parameters use first-wins or last-wins.

