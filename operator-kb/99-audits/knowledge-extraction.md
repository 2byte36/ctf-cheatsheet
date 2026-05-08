# Knowledge Extraction

This file records the distinct skills, workflows, tools, heuristics, and operational patterns discovered from the local CTF notes. It intentionally treats the repository layout as source material, not as the final taxonomy.

## Source Coverage

| Source | Extracted Knowledge Families |
|---|---|
| `ctf-web/` | HTTP recon, auth/session/JWT/JWE, SQLi/NoSQLi/LDAP/XPath, SSTI, SSRF, LFI/path traversal, XXE/XML, command/code injection, deserialization, upload/polyglot, client-side/admin bot/CSP/XS-Leaks, Node/prototype pollution, OAuth/SAML/CORS/CI/CD, Web3, CVE matching. |
| `ctf-forensic/` | Evidence triage, found.md logging, disk/memory/VM/container/cloud forensics, Windows/Linux artifacts, PCAP/TLS/DNS/SMB/USB, steganography, media/signal/hardware, malware-style config and C2 extraction, safe static analysis. |
| `ctf-reverse/` | Static/dynamic triage, decompiler comparison, GDB/r2/Ghidra/Frida/angr/Qiling/Unicorn, anti-debug/anti-VM/anti-DBI, custom VMs, packed binaries, byte transforms, side channels, platform/language-specific reversing, symbolic solving. |
| `ctf-pwn/` | Service-only exploitation, `checksec`-driven strategy, stack/ROP/shellcode, format strings, heap/tcache/FSOP, seccomp, ret2dlresolve, sandbox escape, kernel pwn, Windows/ARM/embedded exploitation, advanced edge primitives. |
| `ctf-misc/` | Encodings, QR/barcodes, jails, bash restrictions, games/VMs, oracle automation, Z3, RF/SDR, DNS tricks, CTFd automation, Linux privesc, puzzle-specific math and recurrence solving. |
| `ctf-osint/` | Geolocation, reverse image search, metadata/OCR, social/usernames, DNS/WHOIS/Wayback/cert transparency, GitHub mining, Telegram/FEC/Tor/Shodan, platform false-positive handling. |
| `ctf-ai-ml/` | Model file inspection, weight perturbation, LoRA merging, inversion, extraction, membership inference, adversarial examples/patches, poisoning/backdoors, prompt injection, token smuggling, tool-use attacks. |

## Extracted Workflows

### Universal

- Workspace inventory and hash/filetype preservation.
- Evidence-driven hypothesis loop.
- Remote parity and exposed-interface solve discipline.
- Smallest proof first: leak, write, oracle, bypass, control, or decode.
- Tool escalation only after manual classification.
- Timeboxing and pivot decision-making.

### Web

- First-pass HTTP map: headers, HTML, JS, routes, methods, content types.
- Source-available Docker mode: map topology without using setup secrets.
- Bot hosting ladder: webhook capture -> static hosted page -> dynamic VPS only when needed.
- Parser mismatch hunting: URL parsers, proxies, sanitizers, file type sniffers, XML parsers, browser normalization.
- Chain building: hidden route -> auth bypass -> file read; XSS -> admin action; SSRF -> internal service; SQLi -> write primitive -> SSTI/upload.

### Forensics

- Artifact inventory -> targeted parser -> extraction -> correlation.
- Remote Q&A loop with per-question evidence logging.
- Read-only recovery and deterministic carving.
- Timeline correlation by timestamp, path, username, PID, flow, hash, and domain.
- Safe static malware analysis and config/protocol reconstruction.

### Reverse

- Quick wins: strings, ltrace/strace, compare breakpoints.
- Follow input to final decision instead of reversing the entire binary.
- Runtime oracle extraction: dump computed values, hook comparisons, count instructions, patch branches.
- Deobfuscation: unpack, simplify MBA, trace VM dispatch, recover bytecode.
- Solver construction: invert transforms, symbolic execution, Z3, meet-in-the-middle.

### Pwn

- Protection-driven exploit planning.
- Crash/control offset -> leak -> base calculation -> write/control -> flag.
- Ret2win before ret2libc before full ROP.
- Heap menu mapping: allocation sizes, indexes, UAF/double-free/show/edit.
- ORW and seccomp-aware syscall strategy.
- Kernel workflow: QEMU/initramfs, symbols, heap sprays, mitigation bypass, privesc trigger.

### Crypto

- Primitive and parameter identification before attack.
- Encoding/compression stripping before cryptanalysis.
- Oracle classification: padding, signing, equality, timing, comparison.
- Bad-parameter checks: RSA gcd/small e/close primes/small d, reused nonces, repeated IV/nonce, weak RNG.
- Exact verifier scripts before exploit scripts.

### OSINT

- Entity extraction before search.
- Crop-specific reverse image search.
- Metadata/OCR/visual clue preservation.
- Archive and historical identity tracking.
- Corroboration before submission.

### Misc

- Constraint mapping for jails and games.
- Alphabet/syntax/eval-context enumeration.
- Encoding chain validation one layer at a time.
- Interactive oracle scripting after manual protocol capture.
- RF/signal visualization before demodulation.

### AI/ML

- Model artifact inspection by format.
- Weight diffing and adapter merging.
- Gradient-based input recovery and adversarial generation.
- Query-boundary model extraction.
- LLM prompt/tool boundary testing.

## Tool-Specific Knowledge Extracted

- HTTP: `curl`, Burp/Caido, `ffuf`, `jq`, `sqlmap`, `flask-unsign`, JWT tooling.
- Forensics: `file`, `sha256sum`, `exiftool`, `binwalk`, `foremost`, `tshark`, Wireshark, Zeek, Sleuth Kit, Volatility 3, `sqlite3`, `zsteg`, `sox`, `ffmpeg`.
- Reverse: GDB/pwndbg/GEF, radare2/r2pipe, Ghidra, Frida, angr, Qiling, Unicorn, Triton, IDA/Binary Ninja, jadx/apktool, dnSpy/ILSpy.
- Pwn: pwntools, checksec, ROPgadget, ropper, one_gadget, seccomp-tools, libc databases, QEMU.
- Crypto/math: PyCryptodome, SageMath, Z3, RsaCtfTool, hash_extender/hashpumpy, OpenSSL ASN.1 tools.
- OSINT: `dig`, `whois`, Shodan, Censys, Wayback CDX, crt.sh, exiftool, OCR, reverse image search.
- Misc: zbarimg, qrencode, Tesseract, Selenium, multimon-ng, SDR tooling, dnslib, CTFd APIs.
- AI/ML: PyTorch, transformers, safetensors, scikit-learn, Pillow, Foolbox-style adversarial tooling.

