# Coverage Audit

## Current Concrete Playbooks

### Web

| Covered type | Playbook | Script/template |
|---|---|---|
| SQL injection | [web-sqli.md](playbooks/web-sqli.md) | manual `curl`, `sqlmap` guidance |
| Boolean/time blind SQLi | [web-blind-sqli.md](playbooks/web-blind-sqli.md) | [blind_sqli_boolean.py](scripts/web/blind_sqli_boolean.py), [blind_sqli_time.py](scripts/web/blind_sqli_time.py) |
| Command injection | [web-command-injection.md](playbooks/web-command-injection.md) | [command_injection_probe.py](scripts/web/command_injection_probe.py) |
| LFI/path traversal | [web-lfi-path-traversal.md](playbooks/web-lfi-path-traversal.md) | [lfi_wordlist_probe.py](scripts/web/lfi_wordlist_probe.py) |
| SSRF | [web-ssrf.md](playbooks/web-ssrf.md) | [ssrf_probe.py](scripts/web/ssrf_probe.py) |
| SSTI | [web-ssti.md](playbooks/web-ssti.md) | manual probes / tplmap guidance |
| XSS admin bot | [web-xss-admin-bot.md](playbooks/web-xss-admin-bot.md) | [xss_exfil_template.html](scripts/web/xss_exfil_template.html) |
| File upload abuse | [web-file-upload.md](playbooks/web-file-upload.md) | upload skeleton in playbook |
| JWT/session | [web-jwt-session.md](playbooks/web-jwt-session.md) | [jwt_decode.py](scripts/web/jwt_decode.py), [flask_cookie_check.py](scripts/web/flask_cookie_check.py) |
| Prototype pollution | [web-prototype-pollution.md](playbooks/web-prototype-pollution.md) | JSON payload skeleton |
| GraphQL | [web-graphql.md](playbooks/web-graphql.md) | GraphQL Python skeleton |

### Forensics

| Covered type | Playbook | Script/template |
|---|---|---|
| PCAP HTTP | [forensic-pcap-http.md](playbooks/forensic-pcap-http.md) | [pcap_http_extract.sh](scripts/forensics/pcap_http_extract.sh) |
| PCAP DNS | [forensic-pcap-dns.md](playbooks/forensic-pcap-dns.md) | DNS decoder skeleton in playbook |
| File carving | [forensic-file-carving.md](playbooks/forensic-file-carving.md) | [magic_scan.sh](scripts/forensics/magic_scan.sh), [carve_common.sh](scripts/forensics/carve_common.sh) |
| Image stego | [forensic-steg-image.md](playbooks/forensic-steg-image.md) | LSB extractor skeleton |
| Memory/Volatility | [forensic-memory-volatility.md](playbooks/forensic-memory-volatility.md) | Volatility shell skeleton |
| Windows artifacts | [forensic-windows-artifacts.md](playbooks/forensic-windows-artifacts.md) | [timeline_sort.py](scripts/forensics/timeline_sort.py) |

### Reverse

| Covered type | Playbook | Script/template |
|---|---|---|
| Flag checker | [reverse-flag-checker.md](playbooks/reverse-flag-checker.md) | [strings_ranker.py](scripts/reverse/strings_ranker.py), [xor_bruteforce.py](scripts/reverse/xor_bruteforce.py) |
| Python bytecode | [reverse-python-pyc.md](playbooks/reverse-python-pyc.md) | marshal/dis skeleton |
| Android APK | [reverse-android-apk.md](playbooks/reverse-android-apk.md) | APK triage shell skeleton |
| angr symbolic execution | referenced in reverse playbook | [angr_template.py](scripts/reverse/angr_template.py) |

### Pwn

| Covered type | Playbook | Script/template |
|---|---|---|
| ret2win | [pwn-ret2win.md](playbooks/pwn-ret2win.md) | [ret2win_template.py](scripts/pwn/ret2win_template.py) |
| ret2libc | [pwn-ret2libc.md](playbooks/pwn-ret2libc.md) | [ret2libc_template.py](scripts/pwn/ret2libc_template.py) |
| Format string | [pwn-format-string.md](playbooks/pwn-format-string.md) | [fmtstr_template.py](scripts/pwn/fmtstr_template.py) |
| Generic pwntools remote | referenced by pwn playbook | [pwntools_remote_template.py](scripts/pwn/pwntools_remote_template.py) |

### Crypto

| Covered type | Playbook | Script/template |
|---|---|---|
| RSA common checks | [crypto-rsa.md](playbooks/crypto-rsa.md) | [rsa_common_checks.py](scripts/crypto/rsa_common_checks.py), [rsa_wiener_template.py](scripts/crypto/rsa_wiener_template.py) |
| XOR | [crypto-xor.md](playbooks/crypto-xor.md) | [xor_known_plaintext.py](scripts/crypto/xor_known_plaintext.py), [xor_bruteforce.py](scripts/reverse/xor_bruteforce.py) |
| Hash length extension | [crypto-hash-extension.md](playbooks/crypto-hash-extension.md) | [hash_length_extension_notes.md](scripts/crypto/hash_length_extension_notes.md) |

### Misc, OSINT, AI/ML

| Covered type | Playbook | Script/template |
|---|---|---|
| Python/Bash jail escape | [misc-jail-escape.md](playbooks/misc-jail-escape.md) | pwntools REPL skeleton |
| Image geolocation | [osint-geolocation.md](playbooks/osint-geolocation.md) | image/OCR shell skeleton |
| LLM prompt/tool injection | [ai-llm-prompt-injection.md](playbooks/ai-llm-prompt-injection.md) | chat API Python skeleton |

## Scripts Currently Present

```text
scripts/
  web/
    blind_sqli_boolean.py
    blind_sqli_time.py
    command_injection_probe.py
    flask_cookie_check.py
    jwt_decode.py
    lfi_wordlist_probe.py
    ssrf_probe.py
    xss_exfil_template.html
  forensics/
    carve_common.sh
    extract_strings_interesting.sh
    magic_scan.sh
    pcap_http_extract.sh
    timeline_sort.py
  reverse/
    angr_template.py
    strings_ranker.py
    xor_bruteforce.py
  pwn/
    fmtstr_template.py
    pwntools_remote_template.py
    ret2libc_template.py
    ret2win_template.py
  crypto/
    hash_length_extension_notes.md
    rsa_common_checks.py
    rsa_wiener_template.py
    xor_known_plaintext.py
```

## Missing Playbooks To Add Later

High priority:

- `web-xxe.md`
- `web-deserialization.md`
- `web-oauth-saml-cors.md`
- `web-nosqli.md`
- `web-cache-poisoning-request-smuggling.md`
- `web-web3-smart-contract.md`
- `forensic-disk-image.md`
- `forensic-linux-artifacts.md`
- `forensic-audio-spectrogram.md`
- `reverse-custom-vm.md`
- `reverse-packed-binary.md`
- `reverse-wasm.md`
- `pwn-heap-uaf-tcache.md`
- `pwn-shellcode-orw-seccomp.md`
- `pwn-kernel.md`
- `crypto-aes-modes.md`
- `crypto-ecdsa-nonce.md`
- `crypto-padding-oracle.md`
- `crypto-lattice-small-roots.md`
- `misc-encoding-chain.md`
- `misc-qr-repair.md`
- `misc-rf-sdr.md`
- `osint-username-social.md`
- `osint-domain-dns-archive.md`
- `ai-model-inversion.md`
- `ai-adversarial-example.md`

## Scripts Still Missing

- `scripts/web/xxe_oob_template.py`
- `scripts/web/graphql_introspection.py`
- `scripts/web/upload_polyglot_builder.py`
- `scripts/forensics/dns_label_decoder.py`
- `scripts/forensics/png_chunk_dump.py`
- `scripts/forensics/lsb_extract.py`
- `scripts/forensics/volatility_triage.sh`
- `scripts/reverse/gdb_cmp_dump.gdb`
- `scripts/reverse/pyc_disassemble.py`
- `scripts/reverse/vm_trace_diff.py`
- `scripts/pwn/orw_rop_template.py`
- `scripts/pwn/heap_menu_template.py`
- `scripts/crypto/aes_cbc_bitflip.py`
- `scripts/crypto/ecdsa_nonce_reuse.py`
- `scripts/crypto/padding_oracle_template.py`
- `scripts/misc/jail_char_probe.py`
- `scripts/osint/image_triage.sh`
- `scripts/ai/prompt_probe.py`

## Sections That Are Still Too Shallow

- Crypto is operational for RSA/XOR/hash extension but lacks AES/ECC/lattice/oracle depth.
- Pwn lacks heap, seccomp/ORW, kernel, and Windows-specific operational playbooks.
- Reverse lacks custom VM, packed binary, WASM, and anti-debug playbooks.
- Forensics lacks disk image, Linux artifacts, audio/video, and RF-specific playbooks.
- Web lacks XXE, deserialization, OAuth/SAML, NoSQLi, request smuggling, and Web3 playbooks.
- OSINT has geolocation only; username/domain/archive workflows need concrete playbooks.
- AI/ML has LLM only; model inversion/adversarial examples need concrete playbooks.

## Suggested Next Expansion Priority

1. Add `web-xxe.md`, `web-deserialization.md`, `web-nosqli.md`, and `web-oauth-saml-cors.md`.
2. Add `pwn-heap-uaf-tcache.md` and `pwn-shellcode-orw-seccomp.md` with templates.
3. Add `forensic-disk-image.md`, `forensic-linux-artifacts.md`, and `forensic-audio-spectrogram.md`.
4. Add `crypto-aes-modes.md`, `crypto-ecdsa-nonce.md`, and `crypto-padding-oracle.md`.
5. Add `reverse-custom-vm.md`, `reverse-packed-binary.md`, and `reverse-wasm.md`.
6. Add OSINT username/domain playbooks.
7. Add AI model inversion/adversarial examples playbooks.

