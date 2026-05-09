# Forensic Windows Artifacts

## When to suspect this

- Provided artifacts include `Windows`, `Users`, `NTUSER.DAT`, `SYSTEM`, `SAM`, `.evtx`, `$MFT`, `$Recycle.Bin`, Prefetch, LNK, Jump Lists.
- Prompt asks about user activity, login time, deleted files, commands, RDP, malware execution, browser history.

## Fast triage checklist

- Identify users and profiles.
- Parse event logs and timeline.
- Check PowerShell history and command artifacts.
- Inspect browser history/downloads.
- Check Recycle Bin and deleted file metadata.
- Inspect registry hives for users, run keys, USB, typed paths.
- Check MFT/USN for file creation/deletion.
- Search for flag/secret strings across artifacts.

## Manual confirmation

```bash
find . -type f -iname '*.evtx' -o -iname 'NTUSER.DAT' -o -iname 'SYSTEM' -o -iname 'SAM'
strings -a -n 6 ./* 2>/dev/null | rg -i 'flag|ctf|powershell|cmd.exe|download|secret'
```

Browser:

```bash
sqlite3 History "select datetime(last_visit_time/1000000-11644473600,'unixepoch'),url,title from urls order by last_visit_time desc limit 30;"
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| Eric Zimmerman's tools | Windows artifact parsing | `MFTECmd`, `EvtxECmd`, `RegistryExplorer` | Timelines |
| `evtx_dump`/`python-evtx` | EVTX on Linux | `evtx_dump Security.evtx` | Event records |
| `sqlite3` | Browser DBs | query Chrome/Firefox history | URLs/downloads |
| `ripgrep/strings` | Fast artifact search | `rg -a -i flag .` | Direct clue |
| Timeline sorter | Mixed CSV/time events | `python3 scripts/forensics/timeline_sort.py events.tsv` | Ordered events |

## Payload starter pack

Event IDs to check:

```text
4624 login
4625 failed login
4634 logoff
4688 process creation
4697 service install
7045 service created
1149 RDP authentication
4104 PowerShell script block
```

Common paths:

```text
Users/<user>/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt
Users/<user>/Downloads
Users/<user>/AppData/Local/Google/Chrome/User Data/Default/History
$Recycle.Bin
Windows/System32/winevt/Logs
```

## Exploit skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
OUT="${2:-work/windows}"
mkdir -p "$OUT"
find "$ROOT" -type f | tee "$OUT/files.txt"
rg -a -n -i 'flag|ctf|secret|token|password|powershell|cmd\.exe|download' "$ROOT" | tee "$OUT/interesting.txt" || true
find "$ROOT" -type f -iname 'ConsoleHost_history.txt' -exec sh -c 'echo "== $1 =="; sed -n "1,200p" "$1"' _ {} \; | tee "$OUT/powershell_history.txt" || true
```

## Escalation path

- If timeline is needed, normalize all timestamps to UTC/local challenge timezone.
- If deleted file is referenced, recover via `$MFT`, `$Recycle.Bin`, USN, disk carving.
- If command executed malware, pivot to static malware analysis.
- If browser downloaded archive, recover and inspect it.
- If SAM/SYSTEM present, extract local hashes only if challenge asks.

## Common bypasses

- PowerShell history may contain exact commands.
- Browser downloads DB often links to file path and URL.
- Recycle Bin stores original path metadata.
- NTFS ADS can hide flag.
- Defender logs may reveal quarantined path.
- Prefetch/LNK/Jump Lists reveal execution even when file is gone.

## Rabbit holes

- Parsing every artifact before asking the exact question.
- Ignoring timezone.
- Treating registry binary blobs as unreadable instead of using tools.
- Missing user-specific hives.

## Final solve checklist

- User, timestamp, path, and artifact source are recorded.
- Answer/flag is backed by at least one parsed artifact.
- Timezone assumptions are stated.
- Recovery path is reproducible.

