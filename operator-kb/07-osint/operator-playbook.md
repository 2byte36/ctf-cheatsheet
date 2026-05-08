# OSINT Operator Playbook

## Mindset

OSINT is clue preservation and corroboration. Extract entities first, search second, verify before submitting. A first search result is a lead, not proof.

## Workflow

1. Preserve prompt, files, screenshots, and URLs.
2. Extract metadata, OCR, strings, visible text, usernames, domains, coordinates, timestamps.
3. Split clues into hard facts and guesses.
4. Search exact phrases and distinctive crops.
5. Corroborate with map/archive/platform evidence.

```bash
exiftool image.jpg
identify -verbose image.jpg | head -60
strings -a -n 5 artifact | tee work/strings.txt
rg -o 'https?://[^ ]+' work/strings.txt
rg -o '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' work/strings.txt
```

## Domain Routing

| Challenge Shape | Workflow |
|---|---|
| Image geolocation | OCR/signs -> crop reverse search -> map/street-view verification |
| Username/persona | cross-platform lookup -> historical IDs -> archives -> false-positive filtering |
| Domain/infrastructure | DNS/WHOIS/certs/Wayback/Shodan/Censys |
| Social post | numeric IDs/snowflakes -> timestamp -> replies/archives/APIs |
| GitHub/repo | commits, branches, issues, PRs, comments, gists, leaked secrets |
| Coordinates | EXIF GPS, MGRS, Plus Codes, What3Words, visual verification |
| Hash/fingerprint | identify by length and exact-search |

## Commands

DNS and infra:

```bash
dig target.com
dig -t txt target.com
dig -t mx target.com
dig -t ns target.com
dig axfr @ns1.target.com target.com
whois target.com
curl -s 'https://crt.sh/?q=%25.example.com&output=json' | jq -r '.[].name_value' | sort -u
```

Wayback:

```bash
curl -s 'https://web.archive.org/cdx?url=example.com/*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200' | jq .
```

Git:

```bash
git log --all --oneline --decorate
git grep -n -i 'flag\|secret\|token\|password' $(git rev-list --all)
git show COMMIT
```

Image processing:

```bash
magick image.jpg -crop 800x400+X+Y work/crop.jpg
magick image.jpg -flop work/flipped.jpg
tesseract image.jpg stdout
```

## Specialized Tactics

- Crop-specific Google Lens/Yandex/Baidu search for signs, logos, facades, and road clues.
- Reflected/mirrored text flipping.
- Twitter/X and Discord snowflake timestamp decoding.
- Persistent Twitter/X numeric user IDs after renames.
- Tumblr headers and avatar paths.
- BlueSky public API search.
- Tor relay fingerprint lookups.
- Shodan SSH fingerprint search.
- Google Docs/Sheets export endpoints.
- Overpass Turbo spatial queries.
- Google Street View panorama matching.
- Platform false-positive filtering for common usernames.

## Rabbit Holes

- Trusting reposts as original source.
- Submitting coordinates without visual match.
- Treating common username matches as proof.
- Searching broad terms instead of exact text.
- Ignoring archive dates.
- Assuming EXIF exists after social upload.

## Source Deep Dives

- Main workflow: [ctf-osint/SKILL.md](../../ctf-osint/SKILL.md)
- Geolocation/media: [geolocation-and-media.md](../../ctf-osint/geolocation-and-media.md)
- Social media: [social-media.md](../../ctf-osint/social-media.md)
- Web/DNS/archive: [web-and-dns.md](../../ctf-osint/web-and-dns.md)

