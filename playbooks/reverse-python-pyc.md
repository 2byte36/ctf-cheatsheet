# Reverse Python PYC

## When to suspect this

- Artifact is `.pyc`, `__pycache__`, PyInstaller executable, marshal blob, or Python bytecode.
- `file` mentions Python byte-compiled.
- Strings show `PyInstaller`, `PYZ`, `marshal`, code object names.
- Challenge logic is Python but source is missing/obfuscated.

## Fast triage checklist

- Identify Python version from magic bytes.
- Try decompilers.
- If decompile fails, use `dis`.
- Extract PyInstaller with pyinstxtractor.
- Check for opcode remapping or PyArmor.
- Search constants, strings, code object names.
- Reconstruct validation logic or run isolated deobfuscated functions if safe.

## Manual confirmation

```bash
file chall.pyc
xxd -l 16 chall.pyc
strings -a -n 5 chall.pyc | head
python3 -m dis chall.pyc 2>/dev/null | sed -n '1,120p'
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| `uncompyle6` | Older pyc decompile | `uncompyle6 chall.pyc` | Python source |
| `pycdc` | Newer bytecode fallback | `pycdc chall.pyc` | Decompiled source |
| `dis` | Decompiler fails | `python3 -m dis chall.pyc` | Bytecode |
| pyinstxtractor | PyInstaller exe | `python3 pyinstxtractor.py chall` | PYZ/extracted pyc |
| `marshal` scripts | Raw code objects | `marshal.load(open(...,'rb'))` | Code object |

## Payload starter pack

Disassemble code object:

```python
import marshal, dis
with open("blob.pyc","rb") as f:
    f.read(16)
    co = marshal.load(f)
dis.dis(co)
print(co.co_consts)
```

Search constants:

```bash
strings -a -n 4 chall.pyc | rg -i 'flag|ctf|key|xor|correct|wrong'
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import marshal, dis, types, sys

path = sys.argv[1]
with open(path, "rb") as f:
    header = f.read(16)
    code = marshal.load(f)

def walk(co, depth=0):
    print("  "*depth + f"code {co.co_name} consts={len(co.co_consts)}")
    dis.dis(co)
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            walk(c, depth+1)
        elif isinstance(c, (bytes, str, int)):
            print("  "*(depth+1), repr(c))

walk(code)
```

## Escalation path

- If decompiled source is clear, solve like normal Python.
- If bytecode only, reconstruct stack operations around compare.
- If opcode remapped, infer mapping from known patterns/imports.
- If PyArmor, inspect bootloader/decryption traces statically.
- If PyInstaller, extract all modules and search recursively.

## Common bypasses

- Wrong Python version breaks decompile; try multiple tools.
- Header length differs by version.
- Constants may hold encrypted flag.
- Marshal blobs can be nested in strings/resources.
- PyInstaller extracted pyc may need header repair.

## Rabbit holes

- Running untrusted extracted code.
- Assuming decompiler output is semantically perfect.
- Ignoring nested code objects.
- Missing Python version magic mismatch.

## Final solve checklist

- Python version/source format identified.
- Validation logic reconstructed or constants extracted.
- Recovered flag verified against logic.
- No suspicious code executed blindly.

