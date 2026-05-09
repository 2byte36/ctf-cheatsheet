#!/usr/bin/env bash
set -euo pipefail

FILE="${1:?usage: magic_scan.sh <file>}"

python3 - "$FILE" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = path.read_bytes()
magics = {
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"\xff\xd8\xff": "JPEG",
    b"GIF8": "GIF",
    b"%PDF": "PDF",
    b"PK\x03\x04": "ZIP/DOCX/APK/JAR",
    b"\x1f\x8b\x08": "gzip",
    b"BZh": "bzip2",
    b"\xfd7zXZ\x00": "xz",
    b"\x7fELF": "ELF",
    b"MZ": "PE",
    b"Rar!": "RAR",
    b"7z\xbc\xaf\x27\x1c": "7z",
    b"SQLite format 3": "SQLite",
}
for magic, name in magics.items():
    start = 0
    while True:
        off = data.find(magic, start)
        if off == -1:
            break
        print(f"0x{off:x}\t{off}\t{name}")
        start = off + 1
PY

