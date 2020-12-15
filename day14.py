from collections import deque
import re

with open("input.txt") as f:
    program = []

    for line in f.read().splitlines():
        if mask := re.search(r"^mask = (.*)$", line):
            program.append(("mask", mask.group(1)))

        if mem := re.search(r"^mem\[(\d*)\] = (\d*)$", line):
            program.append(("mem", [int(g) for g in mem.groups()]))


def bitmask(val, mask):
    string = "{0:b}".format(val).zfill(len(mask))
    masked = [v if m == "X" else m for v, m in zip(string, mask)]

    return int("".join(masked), base=2)


def decode(address, mask):
    string = "{0:b}".format(address).zfill(len(mask))

    masked = []
    for a, m in zip(string, mask):
        if m == "0":
            masked.append(a)
        elif m == "1":
            masked.append(m)
        else:
            masked.append("X")

    return floating(masked)


def floating(masked):
    addresses = [0]

    for i in range(len(masked))[::-1]:
        m = masked.pop(0)
        new = [n + 2 ** i for n in addresses]

        if m == "X":
            addresses += new
        elif m == "1":
            addresses = new

    return addresses


def part1(program):
    memory = {}

    for line in program:
        instruction, payload = line

        if instruction == "mask":
            mask = payload

        if instruction == "mem":
            loc, val = payload
            memory[loc] = bitmask(val, mask)

    return sum(memory.values())


def part2(program):
    memory = {}

    for line in program:
        instruction, payload = line

        if instruction == "mask":
            mask = payload

        if instruction == "mem":
            loc, val = payload
            locs = decode(loc, mask)

            for l in locs:
                memory[l] = val

    return sum(memory.values())
