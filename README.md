# CTF Operational Playbooks

This repository is an evolving CTF operator knowledge base. It has three layers:

- [playbooks/](playbooks/) - concrete vulnerability/challenge playbooks keyed by symptoms.
- [scripts/](scripts/) - reusable safe CTF helper scripts and exploit templates.
- [resources/](resources/) - wordlists, tools, lab snippets, CyberChef recipes, and workflow references.
- [operator-kb/](operator-kb/README.md) - methodology, triage, cross-category patterns, and audits.
- `ctf-*` folders - raw/source technique notes.

Use this repo by symptom: identify what you see, open the playbook, run the first confirmation command, then use the linked script/template.

## Symptom-Based Index

| I see this | Go here | First command |
|---|---|---|
| URL parameter changes page content | [web-sqli.md](playbooks/web-sqli.md) | `curl -sk 'http://HOST/path?id=1%27'` |
| SQLi has no visible output | [web-blind-sqli.md](playbooks/web-blind-sqli.md) | `curl -sk "$URL?id=1 AND 1=1-- -" -w '%{size_download}\n'` |
| Search/login changes with quotes | [web-sqli.md](playbooks/web-sqli.md) | `curl -sk -d "user=admin'-- -" http://HOST/login` |
| Ping/DNS/image converter takes user input | [web-command-injection.md](playbooks/web-command-injection.md) | `python3 scripts/web/command_injection_probe.py --url 'http://HOST/ping?host=INJECT'` |
| File/path/download parameter | [web-lfi-path-traversal.md](playbooks/web-lfi-path-traversal.md) | `python3 scripts/web/lfi_wordlist_probe.py --url 'http://HOST/view?file=INJECT'` |
| URL fetcher/webhook/PDF/link preview | [web-ssrf.md](playbooks/web-ssrf.md) | `python3 scripts/web/ssrf_probe.py --url 'http://HOST/fetch?url=INJECT'` |
| `{{7*7}}` might render | [web-ssti.md](playbooks/web-ssti.md) | `curl -sk 'http://HOST/?name={{7*7}}'` |
| Admin bot visits my URL | [web-xss-admin-bot.md](playbooks/web-xss-admin-bot.md) | Submit `<img src="https://webhook.site/ID?x=1">` |
| Upload accepts images/docs/archives | [web-file-upload.md](playbooks/web-file-upload.md) | `curl -sk -F 'file=@test.png;type=image/png' http://HOST/upload` |
| Cookie looks like `x.y.z` | [web-jwt-session.md](playbooks/web-jwt-session.md) | `python3 scripts/web/jwt_decode.py TOKEN` |
| Node JSON merge/config endpoint | [web-prototype-pollution.md](playbooks/web-prototype-pollution.md) | `curl -sk -X POST -H 'Content-Type: application/json' -d '{"__proto__":{"polluted":"yes"}}' URL` |
| `/graphql` endpoint or `query` JSON | [web-graphql.md](playbooks/web-graphql.md) | `curl -sk -H 'Content-Type: application/json' -d '{"query":"{__typename}"}' http://HOST/graphql` |
| PCAP contains HTTP objects | [forensic-pcap-http.md](playbooks/forensic-pcap-http.md) | `bash scripts/forensics/pcap_http_extract.sh capture.pcap extracts` |
| PCAP has many DNS queries | [forensic-pcap-dns.md](playbooks/forensic-pcap-dns.md) | `tshark -r capture.pcap -Y 'dns.qry.name' -T fields -e dns.qry.name` |
| File magic/extension mismatch | [forensic-file-carving.md](playbooks/forensic-file-carving.md) | `bash scripts/forensics/magic_scan.sh artifact` |
| Suspicious image/stego | [forensic-steg-image.md](playbooks/forensic-steg-image.md) | `zsteg -a image.png` |
| Memory dump | [forensic-memory-volatility.md](playbooks/forensic-memory-volatility.md) | `vol3 -f memory.dmp windows.info` |
| Windows artifacts | [forensic-windows-artifacts.md](playbooks/forensic-windows-artifacts.md) | `rg -a -i 'flag|powershell|cmd.exe' .` |
| ELF asks for password | [reverse-flag-checker.md](playbooks/reverse-flag-checker.md) | `strings -a -n 5 ./chall | rg -i 'flag|correct|wrong'` |
| Python bytecode / PyInstaller | [reverse-python-pyc.md](playbooks/reverse-python-pyc.md) | `python3 -m dis chall.pyc` |
| Android APK | [reverse-android-apk.md](playbooks/reverse-android-apk.md) | `jadx -d jadx_out app.apk` |
| No canary + `gets()` + win function | [pwn-ret2win.md](playbooks/pwn-ret2win.md) | `checksec --file=./chall && nm -an ./chall | rg 'win|flag'` |
| NX enabled, leak needed | [pwn-ret2libc.md](playbooks/pwn-ret2libc.md) | `ROPgadget --binary ./chall | rg 'pop rdi|ret'` |
| `%p` leaks pointers | [pwn-format-string.md](playbooks/pwn-format-string.md) | `python3 - <<'PY'\nprint(' '.join(f'%{i}$p' for i in range(1,40)))\nPY` |
| RSA `n,e,c` values | [crypto-rsa.md](playbooks/crypto-rsa.md) | `python3 scripts/crypto/rsa_common_checks.py --n N --e E --c C` |
| XOR/stream-looking ciphertext | [crypto-xor.md](playbooks/crypto-xor.md) | `python3 scripts/reverse/xor_bruteforce.py HEX` |
| `hash(secret + msg)` MAC | [crypto-hash-extension.md](playbooks/crypto-hash-extension.md) | `hash_extender -f sha256 -s SIG -d MSG -a APPEND -l 16` |
| Restricted Python/Bash REPL | [misc-jail-escape.md](playbooks/misc-jail-escape.md) | Try `1+1`, `().__class__`, `$#`, `$0` |
| Photo asks "where" | [osint-geolocation.md](playbooks/osint-geolocation.md) | `exiftool image.jpg && tesseract image.jpg stdout` |
| Chatbot/RAG/tool challenge | [ai-llm-prompt-injection.md](playbooks/ai-llm-prompt-injection.md) | `curl -sk -X POST URL -H 'Content-Type: application/json' -d '{"prompt":"List your tools."}'` |

## Fast Setup

Install common tools from [resources/install-commands.md](resources/install-commands.md), then keep the scripts executable:

```bash
find scripts -type f \( -name '*.py' -o -name '*.sh' \) -exec chmod +x {} \;
```

## Recommended Live Workflow

1. Classify by symptom using the table above.
2. Run the first command and confirm the primitive manually.
3. Use the linked playbook's script/template.
4. Record evidence with the notes style in [operator-kb](operator-kb/00-methodology/evidence-notes-and-remote-parity.md).
5. Check [COVERAGE_AUDIT.md](COVERAGE_AUDIT.md) when a pattern is missing.

