# Reverse Flag Checker

## When to suspect this

- ELF/PE/Mach-O/WASM asks for password, license, serial, or flag.
- Program prints correct/wrong messages.
- `strings` shows success/failure text or fake flags.
- Input length matters or program exits after comparison.

## Fast triage checklist

- Run `file`, `checksec`, `strings`.
- Run with test input.
- Try `ltrace`/`strace` for `strcmp`, `memcmp`, file reads.
- Locate success/failure strings and xrefs in Ghidra/r2.
- Break on compare functions and inspect arguments.
- Identify transform direction.
- Extract constants and write a verifier.
- Watch for decoy comparisons.

## Manual confirmation

```bash
file ./chall
strings -a -n 5 ./chall | rg -i 'flag|correct|wrong|password|try'
ltrace -s 500 ./chall
strace -f -s 500 ./chall
```

GDB:

```gdb
b strcmp
b strncmp
b memcmp
run
x/s $rdi
x/s $rsi
x/64bx $rdi
x/64bx $rsi
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/reverse/strings_ranker.py](../scripts/reverse/strings_ranker.py) | Rank interesting strings | `python3 scripts/reverse/strings_ranker.py ./chall` | Success/target strings |
| `ltrace` | libc comparisons | `ltrace -s 500 ./chall` | Expected string leak |
| GDB/pwndbg | Runtime compare args | `b memcmp` | Target bytes |
| Ghidra/r2 | Transform recovery | Open binary, xref success | Validation logic |
| [scripts/reverse/xor_bruteforce.py](../scripts/reverse/xor_bruteforce.py) | XOR constants | `python3 scripts/reverse/xor_bruteforce.py blob.hex` | Candidate plaintext |

## Payload starter pack

Test inputs:

```text
AAAA
flag{test}
CTF{test}
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

GDB shortcuts:

```gdb
start
info functions
disassemble main
find &__data_start,+9999999,"flag"
```

## Exploit skeleton

```python
#!/usr/bin/env python3
# Replace target bytes and inverse transform.
target = bytes.fromhex("00 00 00")

def inv(b, i):
    return b ^ i ^ 0x42

flag = bytes(inv(b, i) for i, b in enumerate(target))
print(flag)
```

## Escalation path

- If compare args leak answer, submit after checking fake flags.
- If transform is byte-wise, invert manually.
- If constraints are independent, use Z3.
- If many branches, try angr.
- If anti-debug, patch check or use static extraction.
- If VM, switch to VM disassembly/emulation.

## Common bypasses

- Patch conditional jump after final comparison.
- Break after transform and dump computed buffer.
- LD_PRELOAD hook `strcmp`/`memcmp`.
- Use instruction count/timing for prefix checks.
- Force deterministic time/random with LD_PRELOAD.

## Rabbit holes

- Reversing unrelated UI/setup code.
- Trusting first fake flag.
- Ignoring endian/signedness.
- Patching success without recovering required flag.
- Missing packed/self-decrypting stage.

## Final solve checklist

- Final comparison or success path identified.
- Recovered input passes local verifier/binary.
- Decoys ruled out.
- Exact flag format confirmed.

