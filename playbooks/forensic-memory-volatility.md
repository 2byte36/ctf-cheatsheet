# Forensic Memory With Volatility

## When to suspect this

- Artifact is `.raw`, `.dmp`, `.vmem`, minidump, coredump, or memory capture.
- Prompt asks about process, command, malware, clipboard, browser secret, encryption key.
- Disk artifact is encrypted and key may be in memory.

## Fast triage checklist

- Identify OS/profile with Volatility 3.
- List processes and command lines.
- List network connections.
- Search files and dump likely artifacts.
- Search strings/YARA for flag format.
- Check clipboard, environment, browser processes, command history.
- For ransomware/encryption, search keys, IVs, config, script source.

## Manual confirmation

```bash
vol3 -f memory.dmp windows.info
vol3 -f memory.dmp windows.pslist
vol3 -f memory.dmp windows.cmdline
vol3 -f memory.dmp windows.netscan
vol3 -f memory.dmp windows.yarascan --yara-string 'flag{'
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| Volatility 3 | Main memory framework | `vol3 -f mem windows.pslist` | Process list |
| `strings` | Quick triage | `strings -a -n 6 mem | rg flag` | Direct hits |
| `yarascan` | Search patterns in memory | `vol3 ... yarascan --yara-string flag{` | Offset/process |
| `dumpfiles` | Recover file objects | `vol3 ... dumpfiles --pid PID` | Extracted file |
| GDB | Coredumps/native memory | `gdb binary core` | Runtime state |

## Payload starter pack

Windows:

```bash
vol3 -f mem windows.pstree
vol3 -f mem windows.envars
vol3 -f mem windows.filescan | rg -i 'flag|secret|\.txt|\.zip|\.kdbx'
vol3 -f mem windows.dumpfiles --virtaddr ADDR -o extracts
vol3 -f mem windows.clipboard
```

Linux/coredump:

```bash
strings -a -n 6 core | rg -i 'flag|ctf|key|secret'
gdb ./binary core
```

## Exploit skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail
MEM="${1:?memory image}"
OUT="${2:-work/memory}"
mkdir -p "$OUT"
vol3 -f "$MEM" windows.info | tee "$OUT/info.txt" || true
vol3 -f "$MEM" windows.pslist | tee "$OUT/pslist.txt" || true
vol3 -f "$MEM" windows.cmdline | tee "$OUT/cmdline.txt" || true
vol3 -f "$MEM" windows.netscan | tee "$OUT/netscan.txt" || true
vol3 -f "$MEM" windows.yarascan --yara-string 'flag{' | tee "$OUT/flag_yara.txt" || true
strings -a -n 6 "$MEM" | rg -i 'flag|ctf|secret|token|password|key' | tee "$OUT/interesting_strings.txt" || true
```

## Escalation path

- If process is suspicious, dump its memory/files.
- If browser process exists, recover cookies/history/session data.
- If encryption key is found, use it on disk/archive artifact.
- If network sockets exist, correlate with PCAP.
- If malware config appears, reconstruct C2/decrypt traffic.

## Common bypasses

- Flag split across memory regions.
- Unicode strings need UTF-16 search.
- Minidumps contain enough strings but not full process memory.
- File objects may require virtual address dumping.
- Linux memory workflows differ from Windows Volatility plugins.

## Rabbit holes

- Dumping every file before reading cmdline/process tree.
- Assuming Volatility profile failure means no memory analysis.
- Ignoring simple `strings`.
- Executing dumped suspicious binaries.

## Final solve checklist

- OS/profile/process context recorded.
- Suspicious process, file, or string source identified.
- Dumped artifacts hashed and typed.
- Flag/key recovery steps are reproducible.

