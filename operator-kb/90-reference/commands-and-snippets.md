# Commands And Snippets

## Universal Search

```bash
rg --files
rg -a -n -i 'flag|ctf|secret|token|password|admin|debug|key'
rg -a -o '([A-Za-z0-9_]+)?CTF\{[^}]{1,200}\}|flag\{[^}]{1,200}\}'
rg -a -o 'https?://[^"'"'"' <>()]+'
rg -a -o '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'
rg -a -o '\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b|\b[a-fA-F0-9]{64}\b'
```

## Encoding

```bash
echo '68656c6c6f' | xxd -r -p
echo 'aGVsbG8=' | base64 -d
echo 'NBSWY3DP' | base32 -d
echo 'uryyb' | tr 'a-zA-Z' 'n-za-mN-ZA-M'
```

URL decode:

```bash
python3 - <<'PY'
import urllib.parse, sys
print(urllib.parse.unquote(sys.stdin.read().strip()))
PY
```

All Caesar shifts:

```python
s = "Khoor Zruog"
for k in range(26):
    out = ''.join(chr((ord(c)-65-k)%26+65) if c.isupper()
                  else chr((ord(c)-97-k)%26+97) if c.islower()
                  else c for c in s)
    print(k, out)
```

## JSON/Text

```bash
jq .
jq -r '.. | strings? // empty' data.json
jq -r '.[] | [.id,.name,.role] | @tsv' data.json
awk -F, '{print NR,$1,$NF}' data.csv
awk '{count[$1]++} END {for (x in count) print count[x],x}' log | sort -nr
```

## Web

```bash
curl -sk -i "$URL"
curl -sk "$URL/robots.txt"
ffuf -u "$URL/FUZZ" -w wordlist.txt -mc all -fs 0
for m in GET POST PUT PATCH DELETE OPTIONS TRACE; do curl -sk -X "$m" -i "$URL/path" | sed -n '1,20p'; done
```

JWT:

```bash
echo "$TOKEN" | cut -d. -f1 | base64 -d 2>/dev/null | jq .
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | jq .
```

## Forensics

```bash
find . -maxdepth 3 -type f -printf '%p\t%s bytes\n' | sort
find . -maxdepth 3 -type f -exec file -k {} \;
find . -maxdepth 3 -type f -exec sha256sum {} \;
strings -a -n 6 artifact | rg -i 'flag|ctf|secret|http|key'
binwalk -e artifact
exiftool artifact
```

PCAP:

```bash
tshark -r capture.pcap -q -z io,phs
tshark -r capture.pcap -Y 'dns.qry.name' -T fields -e dns.qry.name
tshark -r capture.pcap --export-objects http,extracts/
```

## Reverse/Pwn

```bash
file binary
checksec --file=binary
strings -a -n 5 binary | rg -i 'flag|correct|wrong|password'
ltrace -s 500 ./binary
strace -f -s 500 ./binary
ROPgadget --binary binary | rg 'pop rdi|syscall|ret'
```

Pwntools cyclic:

```bash
python3 - <<'PY'
from pwn import *
print(cyclic(300))
print(cyclic_find(0x61616168))
PY
```

