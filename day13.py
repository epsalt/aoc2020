from collections import namedtuple
from functools import reduce
from itertools import count
from math import lcm

route = namedtuple("Route", ["mult", "offset"])

with open("input.txt") as f:
    earliest, data = f.read().splitlines()
    earliest = int(earliest)

    routes = []
    for i, r in enumerate(data.split(",")):
        if r.isnumeric():
            routes.append(route(int(r), i))


def part1(earliest, routes):
    for time in count(earliest):
        for route in routes:
            if route.mult is not None and time % route.mult == 0:
                return route.mult * (time - earliest)


def combine(a, b):
    for n in count():
        t = (a.mult * n) - a.offset

        if (t - b.offset) % b.mult == 0:
            mult = lcm(a.mult, b.mult)
            off = mult - t
            return route(mult, off)


def part2(routes):
    ans = reduce(combine, routes)

    return ans.offset
