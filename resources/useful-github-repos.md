# Useful GitHub Repositories

| Repo | Problem it solves | Setup | CTF usage |
|---|---|---|---|
| `danielmiessler/SecLists` | Wordlists for web, DNS, passwords | `git clone https://github.com/danielmiessler/SecLists` | `ffuf -w SecLists/Discovery/Web-Content/raft-small-words.txt` |
| `sqlmapproject/sqlmap` | SQLi automation | `pip install sqlmap` or clone repo | Extract DB after manual SQLi proof |
| `Paradoxis/Flask-Unsign` | Flask cookie attacks | `pip install flask-unsign` | Decode/bruteforce/resign Flask cookies |
| `ticarpi/jwt_tool` | JWT testing | Clone and run `python3 jwt_tool.py` | Test alg confusion, kid, jku |
| `Gallopsled/pwntools` | Pwn scripting | `pip install pwntools` | Build local/remote exploit scripts |
| `JonathanSalwan/ROPgadget` | Gadget search | `pip install ROPGadget` | Find `pop rdi; ret` |
| `zardus/ctf-tools` | Broad CTF tooling references | Clone selectively | Discover niche tool names |
| `volatilityfoundation/volatility3` | Memory forensics | `pip install volatility3` | Process/network/file scans |
| `ReFirmLabs/binwalk` | Firmware/embedded extraction | package manager or clone | Extract hidden files/firmware |
| `extremecoders-re/pyinstxtractor` | PyInstaller extraction | Download script | Extract Python bytecode |
| `zrax/pycdc` | Python bytecode decompile | Build with CMake | Decompile newer `.pyc` |
| `RsaCtfTool/RsaCtfTool` | RSA attack automation | Clone and install requirements | Quick RSA weakness scan |
| `sherlly/PCRT` | CTF crypto helper references | Clone as reference | RSA/crypto method lookup |
| `radareorg/radare2` | CLI reverse engineering | package manager/build | Scriptable disassembly |
| `angr/angr` | Symbolic execution | `pip install angr` | Solve path-to-success binaries |

Do not clone huge repos during a live CTF unless they directly support your current hypothesis.

