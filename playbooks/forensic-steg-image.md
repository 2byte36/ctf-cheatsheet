# Forensic Image Steganography

## When to suspect this

- Challenge gives PNG/JPEG/GIF/BMP with visual clue or "stego" hint.
- Metadata, dimensions, palette, chunks, thumbnails, or frames look unusual.
- Image appears normal but file size is large.
- `binwalk` or `strings` finds hidden data.
- Prompt hints at colors, layers, pixels, palette, QR, or noise.

## Fast triage checklist

- Run `file`, `exiftool`, `binwalk`, `strings`.
- Check dimensions and color mode.
- Inspect channels and bitplanes.
- Check post-EOF data and chunks.
- For GIF/APNG/video, extract frames and diff/accumulate.
- For JPEG, inspect thumbnails, comments, DCT/steg tools.
- Try `zsteg` on PNG/BMP.
- Search for QR/barcode after transforms.

## Manual confirmation

```bash
file image.png
exiftool image.png
binwalk image.png
strings -a -n 6 image.png | rg -i 'flag|ctf|password|PK|base64'
zsteg image.png
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| `zsteg` | PNG/BMP LSB/bitplane | `zsteg -a image.png` | Hidden text/data |
| `exiftool` | Metadata/comments/thumbnails | `exiftool image.jpg` | Comment/password/GPS |
| `binwalk` | Embedded files | `binwalk -e image.png` | Extracted object |
| ImageMagick | Channel/frame operations | `magick img.png -separate out_%d.png` | Visible hidden layer |
| `zbarimg` | QR/barcode after extraction | `zbarimg qr.png` | Decoded text |

## Payload starter pack

Analysis commands:

```bash
magick image.png -separate work/channel_%d.png
magick image.png -alpha extract work/alpha.png
magick image.gif work/frame_%04d.png
compare -compose src frame1.png frame2.png work/diff.png
zbarimg -S*.enable work/*.png
```

Python LSB quick check:

```python
from PIL import Image
img = Image.open("image.png").convert("RGB")
bits = []
for r,g,b in img.getdata():
    bits.extend([r&1,g&1,b&1])
data = bytes(int("".join(map(str,bits[i:i+8])),2) for i in range(0,len(bits)-7,8))
print(data[:200])
```

## Exploit skeleton

```python
#!/usr/bin/env python3
from PIL import Image
import sys

path = sys.argv[1]
img = Image.open(path).convert("RGB")
for channel, idx in [("r",0),("g",1),("b",2)]:
    bits = [(px[idx] & 1) for px in img.getdata()]
    data = bytes(int("".join(str(x) for x in bits[i:i+8]), 2) for i in range(0, len(bits)-7, 8))
    print(f"== {channel} LSB ==")
    print(data[:300])
```

## Escalation path

- If metadata reveals password, try steghide/DeepSound/archive password.
- If bitplanes show QR, crop/threshold and decode.
- If chunks/palette are suspicious, extract chunk data or palette LSBs.
- If frames differ, XOR/diff/average/accumulate frames.
- If image is scrambled, try dimensions, row/column permutations, seed-based shuffle.

## Common bypasses

- LSB only in one channel or near-black pixels.
- Palette entry bits instead of pixel bits.
- Alpha channel data.
- Resized/nearest-neighbor survivor pixels.
- JPEG thumbnails/comments/slack space.
- Frame order or differential data.
- QR split into tiles.

## Rabbit holes

- Running stego tools only once with defaults.
- Ignoring metadata because "EXIF is too easy".
- Not visualizing bitplanes.
- Assuming PNG methods work on JPEG DCT stego.
- Forgetting password may be in prompt/title.

## Final solve checklist

- Metadata, strings, chunks, and bitplanes checked.
- Any extracted data is identified with `file`.
- If QR/barcode appears, final image is saved.
- The extraction process is reproducible.

