# Reverse Engineering Operator Playbook

## Mindset

Reverse engineering CTFs usually hide a validation relation. Recover that relation. You do not need to understand every function.

Shortest path:

```text
strings -> runtime calls -> input path -> final branch -> transform/constraints -> solver or patch
```

## Initial Triage

```bash
file binary
sha256sum binary
checksec --file=binary 2>/dev/null || true
strings -a -n 5 binary | rg -i 'flag|ctf|correct|wrong|password|usage|secret'
readelf -h binary
readelf -s binary | head
```

Dynamic quick wins:

```bash
chmod +x ./binary
echo AAAA | ./binary
ltrace -s 500 ./binary 2>&1 | tee logs/ltrace.txt
strace -f -s 500 ./binary 2>&1 | tee logs/strace.txt
```

Comparison dumping:

```gdb
b strcmp
b strncmp
b memcmp
run
x/s $rdi
x/s $rsi
x/32bx $rdi
x/32bx $rsi
```

## Routing By Binary Shape

| Shape | Likely Workflow |
|---|---|
| Plain ELF with strings | xrefs, compare breakpoints, invert transform |
| Stripped optimized binary | follow input, identify loops/constants, use decompiler plus assembly |
| Packed/self-modifying | unpack, dump memory, patch anti-debug, trace stages |
| Custom VM | identify bytecode, dispatch, handlers, write disassembler/emulator |
| Many byte constraints | Z3/angr, side channel, symbolic execution |
| Foreign arch/firmware | QEMU, Unicorn/Qiling, binwalk, architecture docs |
| Python/.NET/Java/APK/WASM | format-specific decompiler and runtime hooks |
| Game/mobile/engine | extract assets, scripts, metadata, runtime patch |

## Common Patterns

- XOR/repeating key/known plaintext from `flag{`.
- Position transforms: `input[i] ^ i`, rotate, add/sub with index.
- Table/S-box/keystream generation.
- Hex/base64/string comparison after decoding.
- Decoy comparisons before final check.
- Anti-debug: `ptrace`, `/proc`, timing, signals, exceptions.
- Anti-disassembly: junk bytes, opaque predicates, overlapping instructions.
- Side channels: timing, instruction count, crash/coredump, output length, branch count.
- VM obfuscation: dispatch loop, handler table, bytecode stream, custom stack/registers.

## Solver Snippets

Z3 byte skeleton:

```python
from z3 import *
n = 32
xs = [BitVec(f'x{i}', 8) for i in range(n)]
s = Solver()
for x in xs:
    s.add(x >= 0x20, x <= 0x7e)
# add recovered constraints
print(s.check())
m = s.model()
print(bytes(m[x].as_long() for x in xs))
```

XOR brute:

```python
data = bytes.fromhex("...")
for k in range(256):
    out = bytes(b ^ k for b in data)
    if b"flag{" in out or b"CTF{" in out:
        print(k, out)
```

## Tool Selection

| Tool | Use |
|---|---|
| GDB/pwndbg/GEF | Runtime values, breakpoints, patch testing |
| Ghidra/IDA/Binary Ninja | Decompile validation path |
| radare2/r2pipe | CLI reversing, scripting, VM tracing |
| Frida | Hook functions, bypass mobile/anti-debug, inspect memory |
| angr | Path-to-success symbolic execution |
| Qiling/Unicorn/Triton | Emulation and dynamic symbolic execution |
| Dogbolt | Compare decompilers when output is confusing |
| jadx/apktool/dnSpy/ILSpy/wasm2wat | Platform-specific decompilation |

## Niche/Specialized Tactics

- LD_PRELOAD key extraction and time freezing.
- Instruction-count and memcmp side channels.
- VM trace diffing instead of full disassembly.
- GDB scripted constraint extraction.
- BPF/seccomp filter reversing via JIT.
- Bootloader/MBR, firmware, SGX, RISC-V, ARM64, MIPS, Game Boy, automotive CAN.
- TensorFlow/DNN inversion and ML artifacts found through binaries.
- OpenType ligature and font-based hidden messages.

## Rabbit Holes

- Reversing everything instead of the final check.
- Trusting decompiler output without assembly validation.
- Missing comparison direction.
- Losing endian/width/signedness.
- Fighting anti-debug dynamically when static extraction is enough.
- Ignoring side-channel oracles.
- Stopping at a patched success branch when the challenge requires the actual flag.

## Source Deep Dives

- Main workflow: [ctf-reverse/SKILL.md](../../ctf-reverse/SKILL.md)
- Tools: [tools.md](../../ctf-reverse/tools.md), [tools-dynamic.md](../../ctf-reverse/tools-dynamic.md), [tools-emulation.md](../../ctf-reverse/tools-emulation.md)
- Anti-analysis: [anti-analysis.md](../../ctf-reverse/anti-analysis.md)
- Patterns: [patterns.md](../../ctf-reverse/patterns.md), [patterns-ctf.md](../../ctf-reverse/patterns-ctf.md)
- Languages/platforms: [languages.md](../../ctf-reverse/languages.md), [languages-platforms.md](../../ctf-reverse/languages-platforms.md), [platforms.md](../../ctf-reverse/platforms.md)

