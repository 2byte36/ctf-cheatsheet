# Forensic PCAP HTTP

## When to suspect this

- Provided file is `.pcap`/`.pcapng` and challenge hints at web traffic, upload, download, credentials, or exfiltration.
- Wireshark shows HTTP, web forms, file transfers, API calls, or unusual response bodies.
- Prompt mentions browser, web server logs, malware download, or stolen file.

## Fast triage checklist

- Run `capinfos` and protocol hierarchy.
- List HTTP requests and hosts.
- Export HTTP objects.
- Follow interesting TCP streams.
- Search for flags, credentials, tokens, filenames.
- Check uploads as well as downloads.
- Reassemble split archives or chunks.
- Check compression and content encodings.

## Manual confirmation

```bash
capinfos capture.pcap
tshark -r capture.pcap -q -z io,phs
tshark -r capture.pcap -Y 'http.request' -T fields -e frame.number -e ip.src -e http.host -e http.request.method -e http.request.uri
tshark -r capture.pcap --export-objects http,extracts/
find extracts -type f -exec file {} \;
```

Positive signal:

- Exported objects contain files, archives, scripts, or flag text.
- HTTP POST includes credentials or uploaded data.
- TCP stream contains readable response/request body.

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/forensics/pcap_http_extract.sh](../scripts/forensics/pcap_http_extract.sh) | First HTTP extraction pass | `bash scripts/forensics/pcap_http_extract.sh capture.pcap extracts` | Objects and request list |
| `tshark` | CLI PCAP extraction | `tshark -r file -Y http.request` | HTTP metadata |
| Wireshark | Manual stream follow/export | Follow TCP Stream | Full request/response |
| `binwalk`, `file` | Inspect exported objects | `file extracts/*` | Hidden file types |

## Payload starter pack

Not exploit payloads; extraction filters:

```bash
tshark -r capture.pcap -Y 'http.request.method == "POST"' -T fields -e frame.number -e http.file_data
tshark -r capture.pcap -Y 'http contains "flag"'
tshark -r capture.pcap -Y 'http.authorization or http.cookie'
tshark -r capture.pcap -q -z follow,tcp,ascii,0
```

## Exploit skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail
PCAP="${1:-capture.pcap}"
OUT="${2:-extracts}"
mkdir -p "$OUT"
tshark -r "$PCAP" -Y 'http.request' -T fields \
  -e frame.number -e ip.src -e http.host -e http.request.method -e http.request.uri \
  | tee "$OUT/http_requests.tsv"
tshark -r "$PCAP" --export-objects "http,$OUT" >/dev/null 2>&1 || true
find "$OUT" -type f -exec file {} \;
rg -a -n -i 'flag|ctf|secret|token|password|key' "$OUT" || true
```

## Escalation path

- If object extracted, inspect magic and metadata.
- If credentials found, use only if challenge expects reconstruction, not live unauthorized reuse.
- If archive split across transfers, sort by time/URI and concatenate.
- If TLS exists, look for keylog files, private keys, or memory dump with master secrets.
- If malware/C2 traffic, pivot to malware protocol extraction.

## Common bypasses

- HTTP chunks/gzip need decompression.
- Files may be uploaded in multipart POST, not exported as responses.
- Objects may have wrong extension.
- Multiple TCP streams can contain file chunks.
- Proxy/cache responses may duplicate or truncate content.

## Rabbit holes

- Following random streams before protocol hierarchy.
- Ignoring POST bodies.
- Assuming Wireshark export catches all objects.
- Missing compressed or base64 bodies.

## Final solve checklist

- PCAP overview and HTTP request list saved.
- All exported objects identified with `file`.
- Interesting strings searched.
- Recovered artifact/flag provenance is documented.

