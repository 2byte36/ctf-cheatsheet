# Tools Matrix

## Universal

| Tool | Use |
|---|---|
| `rg` | Fast content/file search |
| `file` | Type and magic identification |
| `sha256sum` | Evidence integrity |
| `strings` | Quick plaintext and indicator extraction |
| `xxd` | Hex inspection and magic bytes |
| `jq` | JSON parsing |
| `sed`, `awk` | Stream extraction and quick transforms |
| CyberChef | Encoding, XOR, compression, ASN.1, quick recipes |

## Web

| Tool | Use |
|---|---|
| Browser DevTools | Storage, network, DOM, JS debugging |
| Burp/Caido | Repeater, proxy history, auth-state diffing |
| `curl` | Reproducible HTTP transcripts |
| `ffuf` | Route/vhost/parameter fuzzing |
| `sqlmap` | SQLi confirmation/extraction after manual proof |
| `flask-unsign` | Flask cookie decode/bruteforce |
| JWT tooling | Token decode/forge/testing |
| `webhook.site` | Blind callback and bot proof |

## Forensics

| Tool | Use |
|---|---|
| `exiftool` | Metadata |
| `binwalk` | Embedded files and firmware |
| `foremost`, `scalpel` | Carving |
| `tshark`, Wireshark | PCAP analysis |
| Zeek | Network logs from PCAPs |
| Sleuth Kit | Disk image filesystem recovery |
| Volatility 3 | Memory forensics |
| `sqlite3` | Browser/app artifacts |
| `zsteg`, steghide | Image stego |
| `sox`, `ffmpeg` | Audio/video transforms |
| `zbarimg` | QR/barcode decoding |

## Reverse

| Tool | Use |
|---|---|
| GDB + pwndbg/GEF | Debugging and runtime values |
| radare2/r2pipe | CLI disassembly and scripting |
| Ghidra/IDA/Binary Ninja | Decompilation |
| Frida | Dynamic instrumentation |
| angr | Symbolic execution |
| Qiling/Unicorn/Triton | Emulation and DSE |
| jadx/apktool | Android |
| dnSpy/ILSpy | .NET |
| wasm2wat/wat2wasm | WASM |
| dogbolt.org | Decompiler comparison |

## Pwn

| Tool | Use |
|---|---|
| pwntools | Exploit scripting |
| checksec | Mitigation summary |
| ROPgadget/ropper | Gadget search |
| one_gadget | libc one-shot candidates |
| seccomp-tools | Seccomp filter analysis |
| libc database | Remote libc identification |
| QEMU | Kernel/foreign-arch labs |

## Crypto

| Tool | Use |
|---|---|
| PyCryptodome | RSA/AES/hash scripting |
| SageMath | number theory, lattices, finite fields |
| Z3 | bit-vector constraints |
| RsaCtfTool | RSA weakness automation |
| OpenSSL | cert/key/ASN.1 parsing |
| hash_extender/hashpumpy | Length extension |

## OSINT

| Tool | Use |
|---|---|
| `dig`, `whois` | DNS and registration |
| crt.sh/Censys | Certificate transparency |
| Wayback CDX | Historical snapshots |
| Shodan | Host/fingerprint lookup |
| `magick`, OCR | Image crop/cleanup/text |
| Reverse image search | Geolocation and source tracing |

## Misc/AI

| Tool | Use |
|---|---|
| zbarimg/qrencode | QR/barcode |
| Tesseract/Selenium | CAPTCHA and visual automation |
| multimon-ng | Audio tones |
| NumPy/SciPy | RF/signal/math |
| PyTorch/transformers/safetensors | ML model inspection |
| Foolbox-style tooling | Adversarial examples |

