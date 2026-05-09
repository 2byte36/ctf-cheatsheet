# Wordlists

## Web Paths

| Resource | Problem solved | Install / get | CTF usage |
|---|---|---|---|
| SecLists `Discovery/Web-Content` | Hidden routes, backups, admin panels | `git clone https://github.com/danielmiessler/SecLists` | `ffuf -u http://HOST/FUZZ -w SecLists/Discovery/Web-Content/raft-small-words.txt` |
| SecLists `Fuzzing` | Parameter and payload fuzzing | Same SecLists clone | `ffuf -u 'http://HOST/item?FUZZ=1' -w SecLists/Discovery/Web-Content/burp-parameter-names.txt` |
| `common.txt` / raft small | Fast first pass | SecLists | Use before huge lists to avoid wasting time |

## LFI Files

Start with these before large lists:

```text
/etc/passwd
/etc/hosts
/proc/self/environ
/proc/self/cmdline
/proc/self/fd/0
/app/app.py
/app/config.py
/var/www/html/index.php
/flag
/flag.txt
/app/flag.txt
```

Usage:

```bash
python3 scripts/web/lfi_wordlist_probe.py --url 'http://HOST/view?file=INJECT'
```

## Passwords And Secrets

| Resource | Problem solved | Install / get | CTF usage |
|---|---|---|---|
| `rockyou.txt` | Weak web/JWT/zip/steg passwords | Kali: `/usr/share/wordlists/rockyou.txt.gz` | `flask-unsign --unsign --cookie COOKIE --wordlist rockyou.txt` |
| SecLists `Passwords/Common-Credentials` | App default creds | SecLists | Try only when login brute force is intended and rate safe |
| `jwt.secrets.list` | JWT weak HMAC secrets | SecLists or jwt_tool wordlists | `hashcat -m 16500 token jwt.secrets.list` |

## DNS/Subdomains

| Resource | Problem solved | Install / get | CTF usage |
|---|---|---|---|
| SecLists `DNS/subdomains-top1million-5000.txt` | Fast vhost/subdomain pass | SecLists | `ffuf -H 'Host: FUZZ.domain' -u http://IP/ -w list` |
| Custom names | CTF-specific internal hosts | Build from source/Docker | Try `admin`, `api`, `internal`, `backend`, service names |

## Rule

Use the smallest wordlist that can falsify the hypothesis. Huge lists are for confirmed fuzzable surfaces, not initial triage.

