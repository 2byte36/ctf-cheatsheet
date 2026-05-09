# Forensic File Carving

## When to suspect this

- File magic and extension disagree.
- `binwalk` finds embedded files.
- Image/PDF/archive has extra data after EOF.
- Prompt hints at hidden files, nested dolls, corrupt archive, appended content.
- `strings` shows `PK`, `%PDF`, `flag`, or encoded data inside another file.

## Fast triage checklist

- Run `file -k`, `xxd`, `binwalk`.
- Search for common magic bytes.
- Locate EOF markers and compare file size.
- Try safe extraction with `7z`, `binwalk -e`, `foremost`.
- If corrupt, inspect header fields and CRC/size values.
- Identify nested files recursively.
- Preserve original and carve into `carved/`.

## Manual confirmation

```bash
file -k artifact
xxd -l 256 artifact
binwalk artifact
rg -a -n 'PK\x03\x04|%PDF|flag|CTF' artifact
```

Carve by offset:

```bash
dd if=artifact of=carved/blob.bin bs=1 skip=OFFSET status=none
file carved/blob.bin
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/forensics/magic_scan.sh](../scripts/forensics/magic_scan.sh) | Find magic offsets | `bash scripts/forensics/magic_scan.sh artifact` | Offset list |
| [scripts/forensics/carve_common.sh](../scripts/forensics/carve_common.sh) | Carve common embedded files | `bash scripts/forensics/carve_common.sh artifact carved` | Extracted blobs |
| `binwalk` | Embedded file scan | `binwalk -e artifact` | Recognized signatures |
| `foremost` | Bulk carving | `foremost -i artifact -o carved` | Recovered files |
| `7z` | Archive listing/extraction | `7z l artifact` | Valid entries |

## Payload starter pack

Magic searches:

```bash
xxd -p artifact | tr -d '\n' | rg -o -b '504b0304|25504446|89504e47|ffd8ff|1f8b08|7f454c46'
binwalk artifact
strings -a -td artifact | rg -i 'PK|PDF|flag|ctf|base64'
```

EOF markers:

```text
PNG IEND: 49 45 4e 44 ae 42 60 82
JPEG EOI: ff d9
PDF EOF: %%EOF
ZIP EOCD: 50 4b 05 06
```

## Exploit skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail
IN="${1:?artifact}"
OUT="${2:-carved}"
mkdir -p "$OUT"
file -k "$IN" | tee "$OUT/file.txt"
binwalk "$IN" | tee "$OUT/binwalk.txt"
binwalk -e "$IN" --directory "$OUT/binwalk_extract" || true
foremost -i "$IN" -o "$OUT/foremost" || true
find "$OUT" -type f -exec file {} \;
rg -a -n -i 'flag|ctf|secret|password' "$OUT" || true
```

## Escalation path

- If embedded archive is passworded, search metadata/strings for password.
- If headers are corrupt, repair magic, sizes, CRC, central directory.
- If nested, recurse with inventory each layer.
- If file is encrypted, look for known plaintext or key in companion artifacts.

## Common bypasses

- Null byte interleaving anti-carving.
- Byte-reversed ZIP/DOCX.
- Duplicate tar/zip entries.
- Wrong file extension.
- Appended data after valid EOF.
- Split files across HTTP streams or disk sectors.

## Rabbit holes

- Running carving tools without noting offsets.
- Deleting intermediate files.
- Ignoring metadata/comments.
- Treating every high-entropy blob as encryption.

## Final solve checklist

- Original hash preserved.
- Carved offsets and commands recorded.
- Extracted files identified with `file`.
- Nested extraction stopped only after no new signals remain.

