#!/usr/bin/env python3
"""Minimal angr flag-checker template.

Fill FIND_ADDR/AVOID_ADDR after locating success/failure branches.
"""

import angr
import claripy

BINARY = "./chall"
FLAG_LEN = 32
FIND_ADDR = 0x401234
AVOID_ADDR = 0x401111

proj = angr.Project(BINARY, auto_load_libs=False)
flag = claripy.BVS("flag", FLAG_LEN * 8)
state = proj.factory.full_init_state(args=[BINARY], stdin=flag)

for b in flag.chop(8):
    state.solver.add(b >= 0x20, b <= 0x7e)

simgr = proj.factory.simulation_manager(state)
simgr.explore(find=FIND_ADDR, avoid=AVOID_ADDR)

if simgr.found:
    found = simgr.found[0]
    print(found.solver.eval(flag, cast_to=bytes))
else:
    print("no solution")

