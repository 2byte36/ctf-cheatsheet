# External Tools

| Tool / Repo | Problem it solves | Install | Realistic CTF usage |
|---|---|---|---|
| `ffuf` | Fast web path/vhost/param fuzzing | `go install github.com/ffuf/ffuf/v2@latest` | `ffuf -u http://HOST/FUZZ -w raft-small-words.txt` |
| `sqlmap` | SQLi extraction after manual proof | `pip install sqlmap` | `sqlmap -u 'http://HOST/?id=1' --batch --dump` |
| `flask-unsign` | Flask cookie decode/sign/bruteforce | `pip install flask-unsign` | `flask-unsign --decode --cookie COOKIE` |
| `hash_extender` | Hash length extension | build from GitHub or package manager | `hash_extender -f sha256 -s SIG -d MSG -a APPEND -l 16` |
| `pwntools` | Pwn scripting and packing | `pip install pwntools` | `python3 scripts/pwn/ret2win_template.py REMOTE` |
| `ROPgadget` | ROP gadget discovery | `pip install ROPGadget` | `ROPgadget --binary chall | rg 'pop rdi'` |
| `one_gadget` | libc one-shot constraints | `gem install one_gadget` | `one_gadget libc.so.6` |
| `seccomp-tools` | Seccomp filter analysis | `gem install seccomp-tools` | `seccomp-tools dump ./chall` |
| Ghidra | Decompilation | Install from NSA GitHub release | Open binary, follow success string xrefs |
| radare2 | CLI reversing | `apt install radare2` / `brew install radare2` | `r2 -A chall`, `pdf @ main` |
| Frida | Runtime hooks | `pip install frida-tools` | Hook Android `check()` or libc `strcmp` |
| angr | Symbolic execution | `pip install angr` | Fill `scripts/reverse/angr_template.py` find/avoid addresses |
| Volatility 3 | Memory forensics | `pip install volatility3` | `vol3 -f mem windows.pslist` |
| Sleuth Kit | Disk image forensics | `apt install sleuthkit` | `fls -o OFFSET -r image.dd` |
| `tshark` | PCAP CLI analysis | `apt install tshark` | `tshark -r pcap -Y http.request` |
| `binwalk` | Embedded file discovery | `apt install binwalk` | `binwalk -e firmware.bin` |
| `exiftool` | Metadata extraction/editing | `apt install libimage-exiftool-perl` | `exiftool image.jpg` |
| `zsteg` | PNG/BMP stego | `gem install zsteg` | `zsteg -a image.png` |
| `zbarimg` | QR/barcode decode | `apt install zbar-tools` | `zbarimg qr.png` |
| SageMath | Lattices/finite fields | `apt install sagemath` | RSA Coppersmith or ECC math |
| PyCryptodome | Crypto scripting | `pip install pycryptodome` | RSA/AES helper scripts |
| `safetensors`, PyTorch | ML model inspection | `pip install torch safetensors transformers` | Inspect model weights/adapters |

Use external tools after you know what primitive you are testing. The playbooks show the manual confirmation step first.

