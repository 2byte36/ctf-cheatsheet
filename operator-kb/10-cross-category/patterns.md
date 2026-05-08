# Cross-Category Patterns

These patterns repeat across CTF categories. Recognizing them early is often faster than recognizing the nominal category.

## Parser Mismatches

Core idea: one component validates data differently than the component that consumes it.

| Surface | Examples |
|---|---|
| Web URL parsing | proxy vs framework, `parse_url` vs curl, browser normalization, multi-slash paths |
| File uploads | extension vs magic bytes, MIME sniffing, image library vs web server |
| Archives | ZIP symlink traversal, tar filenames, duplicate entries, path normalization |
| XML/Office/SVG | DOCX XXE, SVG converter XXE, XML deserialization |
| SQL/filter | keyword splitting, encoding, comments, charset confusion |
| Binary parsers | unchecked length fields, signed/unsigned coordinates, DNS compression pointers |
| Crypto serialization | base64 decoder leniency vs parameter parser |

Operator question:

```text
What validates this data, and what later consumes it?
```

## Oracles And Side Channels

An oracle is any observable response correlated with hidden state.

| Oracle | Categories |
|---|---|
| Boolean response | SQLi, crypto equality, jail comparisons |
| Timing | blind SQLi, ReDoS, PBKDF2, binary prefix checks |
| Error type | parser bugs, padding oracle, AST/jail filters |
| Output length | compression, web responses, exfil channels |
| Crash/no crash | pwn, reverse, fuzzing |
| Instruction count | reverse side channel |
| Network callback | SSRF, XXE, XSS bot, DNS exfil |
| Visual difference | stego frames, image XOR, CAPTCHA/games |

Workflow:

```text
stabilize baseline -> vary one bit/byte/field -> measure -> automate extraction
```

## Polyglots And File-Format Abuse

Polyglots are common when upload, parser, or forensics boundaries exist.

Examples:

- PNG/ZIP, PNG/PHP, JPEG/HTML, WAV upload bypass, DOCX/XXE, SVG/XXE, PDF hidden objects, Office ZIP.
- Web upload to RCE.
- Forensics overlay carving.
- Pwn parser overflow inside valid PCAP/image/archive.

Manual checks:

```bash
file -k sample
xxd -l 256 sample
binwalk sample
strings -a -n 6 sample | head
```

## Encoding And Serialization Boundaries

Before exploitation, strip or understand:

- Base64/Base64URL/Base32/hex/URL encoding
- UTF-16 endian issues, fullwidth/unicode normalization
- JSON/XML/YAML/PHP serialize/pickle/Java serialization
- JWT/JWE/JWK/JWKS
- ASN.1/PEM/DER
- Compression: gzip, zlib, xz, brotli
- Pickle opcodes, PHP serialized length fields, Java gadget chains

Repeated lesson: if a payload is transformed before reaching the sink, pre-encode the exploit so the sink sees the intended bytes.

## Covert Channels

| Carrier | Examples |
|---|---|
| DNS | labels, TXT, timing, NSEC walking, tunnels |
| ICMP/TCP | payload bytes, flags, lengths, intervals, checksums |
| HTTP | headers, response sizes, cache behavior, TRACE |
| Images | LSB, palette, chunks, thumbnails, frame diffs |
| Audio/RF | spectrogram, DTMF, SSTV, frequency bins, IQ symbols |
| Keyboard/peripheral | HID reports, LED Morse, mouse deltas, MIDI |
| Terminal/text | ANSI escapes, whitespace, homoglyphs |

## Source And History Leaks

Sources repeat across Web, OSINT, Forensics, and Misc:

- `.git`, `.bzr`, reflog, fsck, deleted repos.
- Source maps, JS bundles, backup files.
- GitHub issues/comments/commits/wikis.
- Browser history/local storage/cookies.
- CTFd API and challenge attachments.
- CI/CD variables and build logs.

## Multi-Stage Chain Patterns

- Web source leak -> secret/key -> session forge -> admin endpoint.
- XSS -> bot exfil -> internal page -> flag.
- SSRF -> internal service -> protocol smuggling -> SQL/file read.
- Forensics PCAP -> recovered binary -> reverse config -> decrypt C2.
- Reverse transform -> crypto weakness -> flag.
- Pwn leak -> libc base -> ORW under seccomp.
- OSINT domain -> exposed Git -> credentials -> web login.
- AI/ML prompt injection -> tool call -> file/API exfil.

## Cross-Category Triage Questions

- Is this really the category label, or only the wrapper?
- What parser consumes my input last?
- Is there an oracle?
- Is the data encoded, compressed, serialized, or encrypted?
- Can I prove a one-step primitive before chaining?
- Does the exploit survive remote parity?
- Is the flag in a file, memory, database, browser, model output, blockchain state, or public record?

