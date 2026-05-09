#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./chall", checksec=False)
HOST, PORT = "HOST", 1337


def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(elf.path)


io = start()
io.recvuntil(b"> ")
io.sendline(b"test")
io.interactive()

