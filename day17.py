from collections import namedtuple
from itertools import product

cube = namedtuple("Cube", ["x", "y", "z"])
hypercube = namedtuple("Hypercube", ["x", "y", "z", "w"])

with open("input.txt") as f:
    cubes = []
    for y, line in enumerate(f.read().splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                cubes.append(cube(x, y, 0))


def neighbours(shape):
    combos = product(range(-1, 2), repeat=len(shape._fields))

    out = set()
    for combo in combos:
        neighbour = shape._make(map(sum, zip(shape, combo)))
        if neighbour != shape:
            out.add(neighbour)

    return out


def count(shapes, cycles):
    active = set(shapes)

    for _ in range(cycles):
        next_active = set()

        for a in active:
            if len(active & neighbours(a)) in [2, 3]:
                next_active.add(a)

        inactive = set(c for a in active for c in neighbours(a)) - active
        for i in inactive:
            if len(active & neighbours(i)) == 3:
                next_active.add(i)

        active = next_active

    return len(active)


def part1(cubes, cycles):
    return count(cubes, cycles)


def part2(cubes, cycles):
    hypercubes = [hypercube(*cube, 0) for cube in cubes]

    return count(hypercubes, cycles)
