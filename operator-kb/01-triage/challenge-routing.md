# Challenge Routing

## First Five Minutes

```bash
pwd
find . -maxdepth 3 -type f -printf '%p\t%s bytes\n' | sort
find . -maxdepth 3 -type f -exec file -k {} \;
rg -a -n -i 'flag|ctf|secret|token|password|admin|debug|TODO|FIXME' .
```

If there is a remote endpoint:

```bash
curl -sI "$URL" 2>/dev/null
nc -vz HOST PORT
```

## Routing Table

| Observable | Route | First Proof To Seek |
|---|---|---|
| URL, cookies, admin bot, API, Docker web app | [Web](../02-web/operator-playbook.md) | Input crosses into DB/template/path/URL/browser/auth boundary |
| PCAP, disk image, memory dump, logs, Office/PDF/media | [Forensics](../03-forensics/operator-playbook.md) | Artifact source, timeline, carved object, decoded channel |
| Native binary validates a flag/password | [Reverse](../04-reverse/operator-playbook.md) | Final comparison or validation transform |
| ELF/libc plus `nc`, crash, vulnerable source | [Pwn](../05-pwn/operator-playbook.md) | Control of IP, leak, write, shell/ORW path |
| Ciphertexts, moduli, signatures, RNG, oracle | [Crypto](../06-crypto/operator-playbook.md) | Primitive, bad parameter, oracle type |
| Real-world clue, image, username, domain, coordinates | [OSINT](../07-osint/operator-playbook.md) | Entity extraction and independent corroboration |
| Jail, weird encoding, game, VM, QR, RF, DNS oddity | [Misc](../08-misc-specialized/operator-playbook.md) | Rule set, allowed alphabet, format, oracle |
| Model weights, prompts, ML API, classifier | [AI/ML](../09-ai-ml/operator-playbook.md) | Model artifact, query surface, gradient/decision oracle |

## Challenge-Type Heuristics

### Web

- Login + role fields -> authz, JWT/session, IDOR, mass assignment.
- URL fetcher/export/PDF -> SSRF, file read, internal service, parser mismatch.
- Report/admin bot -> XSS, CSRF, CSP bypass, XS-Leak.
- Upload -> polyglot, extension/content-type mismatch, parser RCE, XXE.
- GraphQL -> introspection, batching, resolver authz.

### Forensics

- Valid file plus extra bytes -> overlays, post-EOF carving.
- PCAP with long DNS labels -> DNS exfil/covert channel.
- Memory dump -> process list, command lines, network sockets, dumped files, YARA strings.
- Disk image -> partition table, deleted files, snapshots, filesystem metadata.
- Media -> metadata, LSB, spectrogram, frame differential, hidden thumbnails.

### Reverse

- Success/failure strings -> xrefs to final branch.
- `strcmp`/`memcmp` -> dump runtime args.
- Heavy dispatch loop -> VM/bytecode.
- `ptrace`, timing, `/proc` -> anti-debug.
- Many byte constraints -> Z3/angr/side channel.

### Pwn

- `gets`, `%s`, unchecked `read` -> stack overflow.
- `printf(user)` -> format string.
- menu create/free/edit/show -> heap UAF/double free/poisoning.
- seccomp -> ORW or allowed syscall chain.
- kernel module/QEMU/initramfs -> kernel pwn.

### Crypto

- `n,e,c` -> RSA.
- repeated ECDSA/DSA `r` -> nonce reuse.
- repeated 16-byte blocks -> ECB.
- same nonce in CTR/stream -> two-time pad.
- `hash(secret||msg)` -> length extension.
- timestamp seed -> PRNG recovery.

### OSINT

- Image with signs/landmarks -> crop-specific reverse search and map verification.
- Username -> multi-platform correlation, old IDs, archives.
- Domain -> DNS, WHOIS, cert transparency, Wayback.
- 40 hex -> SHA1 or Tor fingerprint. 64 hex -> SHA256.

### Misc

- Restricted input -> jail enumeration.
- Repeated decoding -> encoding chain.
- Interactive compare service -> oracle extraction.
- SDR/IQ -> sample format, constellation, timing recovery.
- Game state cookie -> checkpoint/restore and state manipulation.

