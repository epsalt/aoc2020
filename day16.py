from collections import defaultdict
from itertools import groupby
from math import prod
import re

with open("input.txt") as f:
    lines = f.read().splitlines()
    r, t, n = [list(group) for k, group in groupby(lines, bool) if k]

    rules = {}
    for rule in r:
        name = re.match(r"(.*):", rule).group(1)
        ranges = [[int(a) for a in b] for b in re.findall(r"\W(\d+)-(\d+)", rule)]

        rules[name] = ranges

    mine = [int(n) for n in t[1].split(",")]
    nearby = [[int(n) for n in t.split(",")] for t in n[1:]]


def bad(ticket, rules):
    ranges = [r for rs in rules.values() for r in rs]

    for n in ticket:
        if not any(n in range(i, j + 1) for i, j in ranges):
            return True

    return False


def possible_fields(ticket, rules):
    d = defaultdict(list)

    for i, n in enumerate(ticket):
        for name, ranges in rules.items():
            for start, end in ranges:
                if n in range(start, end + 1):
                    d[i].append(name)

    return d


def part1(rules, nearby):
    numbers = [n for ticket in nearby for n in ticket]
    ranges = [r for rs in rules.values() for r in rs]

    return sum(n for n in numbers if not any(n in range(i, j + 1) for i, j in ranges))


def part2(mine, rules, nearby):
    ok = [t for t in nearby if not bad(t, rules)]
    decoder = {}

    possibilities = defaultdict(list)
    for ticket in ok:
        for n, f in possible_fields(ticket, rules).items():
            possibilities[n].append(set(f))

    found = set()
    for _ in range(len(rules)):
        for i, fields in possibilities.items():
            choices = set.intersection(*map(set, fields)) - found

            if len(choices) == 1:
                decoder[i] = choices.pop()
                found = set(decoder.values())

    return prod(n for i, n in enumerate(mine) if decoder[i].startswith("departure"))
