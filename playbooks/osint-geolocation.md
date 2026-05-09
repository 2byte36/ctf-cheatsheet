# OSINT Image Geolocation

## When to suspect this

- Prompt asks for place, coordinates, street, building, city, or country.
- Artifact is a photo/screenshot/video frame with signs, roads, shops, terrain, architecture, or weather.
- EXIF GPS may be present or stripped.
- Challenge title hints at travel, map, street view, route, landmark, or "where".

## Fast triage checklist

- Preserve original image.
- Run metadata and OCR.
- List visible hard clues: language, road signs, business names, phone numbers, plates, transit logos.
- Crop distinctive regions and reverse-search separately.
- Identify country/region from driving side, road markings, scripts, infrastructure.
- Verify candidate using map/street-view/user photos.
- Record coordinates in required format.

## Manual confirmation

```bash
exiftool image.jpg
identify -verbose image.jpg | head -60
tesseract image.jpg stdout
magick image.jpg -crop 800x400+X+Y work/crop.jpg
magick image.jpg -flop work/flipped.jpg
```

Positive signal:

- Exact business/sign text search returns candidate.
- Street View or map photos match camera angle.
- Multiple independent clues agree.

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| `exiftool` | Metadata/GPS/device | `exiftool image.jpg` | GPS/time/device |
| Tesseract | OCR signs/text | `tesseract image.jpg stdout` | Searchable text |
| ImageMagick | Crop/flip/enhance | `magick image.jpg -crop ... crop.jpg` | Better reverse search |
| Google Lens/Yandex/Baidu | Reverse image/crop search | Upload cropped sign/facade | Candidate location |
| Overpass Turbo | Search map features | Query amenity/name in region | Candidate points |

## Payload starter pack

Search queries:

```text
"exact visible phrase"
"business name" "city clue"
"road number" "town name"
"phone prefix" "shop name"
site:maps.google.com "landmark name"
```

Visual clues:

```text
Driving side
Road sign shape/color
Lane markings
Utility poles
License plate color/shape
Script/language
Terrain/coastline/mountains
```

## Exploit skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail
IMG="${1:?image}"
OUT="${2:-work/osint}"
mkdir -p "$OUT"
exiftool "$IMG" | tee "$OUT/exif.txt"
identify -verbose "$IMG" | head -100 | tee "$OUT/identify.txt"
tesseract "$IMG" stdout | tee "$OUT/ocr.txt" || true
magick "$IMG" -resize 1600x "$OUT/resized.jpg"
magick "$IMG" -flop "$OUT/flipped.jpg"
```

## Escalation path

- If EXIF GPS exists, verify visually; do not submit blindly.
- If text exists, search exact phrase in quotes.
- If landmark/business found, verify with street-view/user photos.
- If no text, use infrastructure/terrain to narrow region.
- If candidate set remains large, use Overpass queries for combined features.

## Common bypasses

- Social platforms strip EXIF, but thumbnails or filenames may remain.
- Reflected text must be flipped.
- Reposted images may rank higher than original.
- Cropped region search often beats full image search.
- Google/Yandex/Baidu differ by region.

## Rabbit holes

- Trusting first reverse-search result.
- Submitting coordinates without visual confirmation.
- Treating language as country proof.
- Ignoring shadows/weather only when they can constrain time/place.

## Final solve checklist

- Hard clues are listed.
- Candidate is verified by visual match.
- Coordinates/name match requested format.
- Source links/screenshots are recorded in notes.

