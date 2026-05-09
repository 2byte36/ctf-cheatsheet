# Misc And Specialized Operator Playbook

## Operational Playbook Router

| If you see | Open playbook | First action |
|---|---|---|
| restricted Python/Bash REPL | [Jail Escape](../../playbooks/misc-jail-escape.md) | Try `1+1`, `().__class__`, `$#`, `$0` |
| unknown encoding chain | Use [payloads/decoders](../90-reference/payloads-magic-and-decoders.md) | `file mystery && xxd -l 256 mystery` |
| QR/barcode | Use this playbook and resources | `zbarimg -S*.enable image.png` |
| DNS oddity | [PCAP DNS](../../playbooks/forensic-pcap-dns.md) or DNS notes | `dig -t txt target` |

## Mindset

Misc is not a dumping ground. It is where the core task is format recognition, constraints, jails, games, protocols, or unusual tooling rather than one of the main exploit categories.

Start by classifying the rule system.

## Routing

| Shape | Workflow |
|---|---|
| Encoding chain | identify charset, decode one layer, inspect, repeat |
| QR/barcode | decode, repair, reassemble, infer structure |
| Python/Bash jail | enumerate allowed chars/syntax/context, build primitives |
| Game/VM | model state transitions, find oracle, automate |
| Esoteric language | identify interpreter, translate/instrument |
| RF/SDR/IQ | identify sample format, visualize, sync/demodulate |
| DNS oddity | TXT/AXFR/NSEC/IXFR/tunnel/rebinding |
| Linux privesc | SUID/caps/sudo/cron/services/internal network |
| CTFd ops | API navigation, file download, flag submit, scoreboard |

## First Checks

```bash
file mystery
xxd -l 256 mystery
strings -a -n 5 mystery | head -100
binwalk mystery
exiftool mystery 2>/dev/null
```

## Encodings

| Symptom | Candidate |
|---|---|
| `A-Za-z0-9+/=` | Base64 |
| `A-Z2-7=` | Base32 |
| even hex chars | Hex, but prioritize over base64 when ambiguous |
| `%xx` | URL encoding |
| CJK mojibake | UTF-16 endian reversal or base65536 |
| float list | IEEE-754 raw bytes |
| decimal digit nibbles | BCD |
| dots/dashes | Morse |
| weird spaces/tabs | Whitespace/esolang/stego |

## Jail Workflow

Python:

```text
Map errors -> allowed syntax -> blocked names/chars -> available builtins -> object graph -> file read or command primitive.
```

Bash:

```text
Map allowed chars -> detect eval "$input" vs eval $input -> build digits/strings -> spawn shell/read file/internal service.
```

Useful primitives:

- `().__class__.__mro__[1].__subclasses__()`
- `exec(compile(..., '', 'exec'))`
- hex/octal/Unicode escapes
- `$#`, `$$`, `$0`, ANSI-C `$'\ooo'`
- `HISTFILE=/flag /bin/bash`
- `bash -v /flag`
- `/dev/tcp/host/port`

## Games, VMs, And Oracles

- Save cookies/checkpoints before guesses.
- Use binary search when comparison output exists.
- Model finite-state transitions.
- Use Z3 for symbolic constraints.
- Use graph search for mazes/puzzles.
- Use De Bruijn sequences for substring coverage.
- For custom VMs, write a disassembler before a full emulator.

## RF/SDR

Start with sample type:

| Format | Load |
|---|---|
| `cf32` | `np.complex64` |
| `cs16` | int16 I/Q pairs |
| `cu8` | unsigned 8-bit RTL-SDR |

Look for:

- constellation clusters
- carrier offset
- symbol timing
- framing/preamble
- bit order and whitening/scrambling

## Platform Privesc

Quick checks:

```bash
id
sudo -l
find / -perm -4000 -type f 2>/dev/null
find / -executable -type f -exec getcap {} \; 2>/dev/null
ps auxww
cat /proc/*/cmdline 2>/dev/null | tr '\0' ' ' | rg -i 'flag|socat|readflag|backup|cron'
```

Preserve CTF ethics: use only intended challenge surfaces and avoid destructive actions.

## Source Deep Dives

- Main workflow: [ctf-misc/SKILL.md](../../ctf-misc/SKILL.md)
- Encodings/QR: [encodings.md](../../ctf-misc/encodings.md), [encodings-advanced.md](../../ctf-misc/encodings-advanced.md)
- Python jails: [pyjails.md](../../ctf-misc/pyjails.md)
- Bash jails: [bashjails.md](../../ctf-misc/bashjails.md)
- Games/VMs: [games-and-vms.md](../../ctf-misc/games-and-vms.md)
- DNS: [dns.md](../../ctf-misc/dns.md)
- RF/SDR: [rf-sdr.md](../../ctf-misc/rf-sdr.md)
- Linux privesc: [linux-privesc.md](../../ctf-misc/linux-privesc.md)
- CTFd ops: [ctfd-navigation.md](../../ctf-misc/ctfd-navigation.md)
