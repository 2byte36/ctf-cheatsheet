# Forensic PCAP DNS

## When to suspect this

- PCAP has many DNS queries, long subdomains, TXT lookups, or unusual labels.
- Prompt hints at exfiltration, tunneling, domains, resolver, or beaconing.
- `tshark` protocol hierarchy shows DNS volume disproportionate to traffic.

## Fast triage checklist

- List all queried names and TXT answers.
- Count repeated domains and label lengths.
- Extract subdomain labels before known suffix.
- Check base64/base32/hex encodings.
- Preserve query order by frame/time.
- Look for NXDOMAIN vs valid response bits.
- Check DNS tunneling tools such as dnscat2 patterns.

## Manual confirmation

```bash
tshark -r capture.pcap -Y 'dns.qry.name' -T fields -e frame.number -e frame.time_epoch -e ip.src -e dns.qry.name | tee work/dns_queries.tsv
tshark -r capture.pcap -Y 'dns.txt' -T fields -e dns.txt
awk '{print $4}' work/dns_queries.tsv | sort | uniq -c | sort -nr | head
```

Positive signal:

- Long high-entropy labels.
- Sequential labels decode as base64/hex.
- TXT records contain encoded chunks.
- Query timing/last byte encodes data.

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| `tshark` | Extract names/TXT in order | `tshark -r f -Y dns.qry.name -T fields -e dns.qry.name` | Label stream |
| `awk/sed/tr` | Strip suffix and join chunks | `sed 's/.exfil.com$//'` | Encoded blob |
| CyberChef | Decode candidate blobs | From Base64/Hex/Base32 | Plaintext/file magic |
| [forensic-pcap-http.md](forensic-pcap-http.md) | DNS points to HTTP stage | Open when URLs appear | Follow-on artifact |

## Payload starter pack

Extraction filters:

```bash
tshark -r capture.pcap -Y 'dns.qry.name' -T fields -e dns.qry.name
tshark -r capture.pcap -Y 'dns.flags.rcode == 3' -T fields -e dns.qry.name
tshark -r capture.pcap -Y 'dns.txt' -T fields -e dns.txt
```

Suffix stripping:

```bash
tshark -r capture.pcap -Y 'dns.qry.name' -T fields -e dns.qry.name \
  | sed 's/\.example\.com$//' | tr -d '\n' | base64 -d
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import base64, binascii, sys

suffix = sys.argv[1] if len(sys.argv) > 1 else ".example.com"
labels = []
for line in sys.stdin:
    q = line.strip().rstrip(".")
    if q.endswith(suffix):
        labels.append(q[:-len(suffix)].replace(".", ""))
blob = "".join(labels)
print("chars", len(blob))
for name, fn in [
    ("hex", lambda x: bytes.fromhex(x)),
    ("base64", lambda x: base64.b64decode(x + "=" * (-len(x) % 4))),
    ("base32", lambda x: base64.b32decode(x + "=" * (-len(x) % 8))),
]:
    try:
        out = fn(blob)
        print(name, out[:100])
    except (binascii.Error, ValueError):
        pass
```

## Escalation path

- If decoded bytes have magic, write to file and run `file`.
- If order matters, sort by frame number/time, not alphabetically.
- If labels include sequence numbers, parse and reorder.
- If DNS answers encode bits, extract response code/TXT/A record bytes.
- If tunnel protocol is present, use dnscat2/iodine-specific decoders.

## Common bypasses

- Base32 often used because DNS labels are case-insensitive.
- Padding removed.
- Dots split chunks.
- Label order may include counters.
- Last byte of query/response may encode data.
- Timing between packets may encode bits.

## Rabbit holes

- Sorting labels alphabetically and destroying order.
- Ignoring responses.
- Decoding full FQDN including suffix.
- Assuming all long labels are base64.

## Final solve checklist

- Query order preserved.
- Suffix/chunking logic documented.
- Decoded output identified by magic or readable text.
- Recovered flag/artifact saved.

