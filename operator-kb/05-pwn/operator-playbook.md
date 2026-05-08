# Pwn Operator Playbook

## Mindset

Pwn is primitive engineering:

```text
bug -> crash/control -> leak -> base calculation -> write/control -> shell or ORW -> flag
```

Use the exposed service. Local Docker/source are analysis aids, not shortcuts to secrets.

## Initial Triage

```bash
file vuln
checksec --file=vuln
readelf -h vuln
readelf -s vuln | rg 'win|system|puts|read|write|printf'
strings -a -n 5 vuln | rg -i 'flag|sh|bin|win|puts|printf|scanf|gets'
ldd ./vuln 2>/dev/null || true
```

Offset:

```bash
python3 - <<'PY'
from pwn import *
print(cyclic(300).decode())
PY
```

Gadgets:

```bash
ROPgadget --binary vuln | rg 'pop rdi|pop rsi|pop rdx|syscall|ret'
ropper -f vuln --search 'pop rdi; ret'
```

## Mitigation-Driven Strategy

| Protection | Strategy |
|---|---|
| No PIE | fixed binary addresses, ret2win, GOT/PLT |
| PIE | leak binary pointer or partial same-page overwrite |
| NX | ROP, ret2libc, SROP, ORW |
| No NX | shellcode if bad chars/size allow |
| Canary | leak, brute force on forking service, avoid stack, partial overwrite |
| Partial RELRO | GOT overwrite |
| Full RELRO | hooks if available, return addr, vtable, heap/FSOP |
| Seccomp | ORW, allowed syscalls, x32/RETF tricks, SROP |

## Common Vulnerability Families

- Stack overflow: `gets`, `scanf("%s")`, unchecked `read`, parser length mismatch.
- Format string: `%p` leaks, `%s` reads, `%n/%hn/%hhn` writes.
- Heap: UAF, double free, tcache poisoning, null byte overflow, unsafe unlink, custom allocators.
- Integer: truncation, sign extension, negative indexes, loop counter wrap.
- Race: threads, sleep/usleep, global state, userfaultfd/kernel race.
- Sandbox: seccomp, custom VM, bytecode validator, restricted shell.
- Kernel: stack/heap overflow, UAF, modprobe_path/core_pattern, kROP, SMEP/SMAP/KPTI.

## Minimal Pwntools Skeleton

```python
from pwn import *

context.binary = elf = ELF('./vuln')
HOST, PORT = 'host', 31337

def start():
    return remote(HOST, PORT) if args.REMOTE else process(elf.path)

io = start()
offset = 72
rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]

payload = flat(
    b'A' * offset,
    ret,
    elf.sym['win'],
)

io.sendlineafter(b'> ', payload)
io.interactive()
```

## Exploit Patterns

### Ret2libc

1. Leak libc function from GOT.
2. Return to main/vuln.
3. Calculate libc base.
4. Call `system("/bin/sh")` or ORW.

### ORW

```text
open("/flag", 0) -> read(fd, buf, n) -> write(1, buf, n)
```

Do not hardcode fd `3` if Docker/socat may shift descriptors. Capture `open()` return from `rax`.

### Format String

```bash
python3 - <<'PY'
print(' '.join(f'%{i}$p' for i in range(1,50)))
PY
```

Look for canary, PIE, libc, stack pointers. Use writes only after offset and target are proven.

### Heap

Map:

```text
struct layout -> allocation size -> index table -> create/free/edit/show -> leak/write primitive
```

Check tcache behavior, safe-linking, unsorted bin leaks, stdout/FILE targets, hooks availability, `environ` stack leak, and exit/atexit/TLS destructors.

## Niche/Specialized Tactics

- ret2csu for 3-argument calls.
- SROP and RETF/x32 seccomp bypasses.
- DynELF when libc unknown.
- Exotic x86 gadgets: BEXTR/XLAT/STOSB/PEXT.
- Bad-character ROP encoding.
- FSOP/House of Apple/House of Orange.
- Kernel KASLR/FGKASLR, KPTI, SMEP/SMAP bypass.
- Blind shellcode via timing when `write` is blocked.
- Windows SEH/CFG/IAT, ARM/Thumb/ARM64 gadgets, m68k/DOS shellcode.
- Data-interpretation pwn: Chip-8, BF JIT, Game of Life shellcode, neural net output as function pointer.

## Rabbit Holes

- Starting with heap when ret2win exists.
- Ignoring `checksec`.
- Hardcoding local libc against remote.
- Forgetting stack alignment before `system`.
- Assuming fd numbers.
- Failing to preserve canary bytes.
- Treating source/config flags as solve inputs.
- Not confirming the bug is exploitation, not reverse engineering.

## Source Deep Dives

- Main workflow: [ctf-pwn/SKILL.md](../../ctf-pwn/SKILL.md)
- Stack basics: [overflow-basics.md](../../ctf-pwn/overflow-basics.md)
- ROP/shellcode: [rop-and-shellcode.md](../../ctf-pwn/rop-and-shellcode.md), [rop-advanced.md](../../ctf-pwn/rop-advanced.md)
- Format strings: [format-string.md](../../ctf-pwn/format-string.md)
- Heap/FSOP: [heap-techniques.md](../../ctf-pwn/heap-techniques.md), [heap-fsop.md](../../ctf-pwn/heap-fsop.md)
- Kernel: [kernel.md](../../ctf-pwn/kernel.md), [kernel-bypass.md](../../ctf-pwn/kernel-bypass.md)
- Sandbox: [sandbox-escape.md](../../ctf-pwn/sandbox-escape.md)
- Advanced: [advanced-exploits.md](../../ctf-pwn/advanced-exploits.md)

