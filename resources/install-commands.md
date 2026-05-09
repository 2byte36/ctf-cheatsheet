# Install Commands

Use a disposable CTF VM or container where possible.

## Python

```bash
python3 -m pip install --user requests pwntools pycryptodome z3-solver angr flask-unsign volatility3 frida-tools safetensors transformers torch pillow scipy scikit-learn
```

## Web

```bash
go install github.com/ffuf/ffuf/v2@latest
python3 -m pip install --user sqlmap flask-unsign
```

## Pwn

```bash
python3 -m pip install --user pwntools ROPGadget ropper
gem install one_gadget seccomp-tools
```

## Forensics

```bash
sudo apt install -y tshark wireshark-common binwalk foremost sleuthkit exiftool zbar-tools ffmpeg sox imagemagick sqlite3 p7zip-full
gem install zsteg
```

## Reverse

```bash
sudo apt install -y gdb radare2 binutils strace ltrace apktool default-jdk
python3 -m pip install --user frida-tools angr qiling unicorn capstone lief
```

## Crypto

```bash
python3 -m pip install --user pycryptodome gmpy2 z3-solver
sudo apt install -y sagemath openssl
```

## OSINT

```bash
sudo apt install -y whois dnsutils nmap imagemagick tesseract-ocr exiftool
python3 -m pip install --user shodan pillow
```

## Notes

- Some tools are intentionally not installed by default because they are large or niche.
- Install only what a current playbook calls for during a competition.
- Prefer package manager versions for stable forensic tools, Python virtualenvs for challenge-specific libraries.

