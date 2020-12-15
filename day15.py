from collections import defaultdict, deque
from itertools import count, islice

with open("input.txt") as f:
    line = f.readline().rstrip()
    numbers = [int(x) for x in line.split(",")]


def speak(numbers):
    mem = defaultdict(deque)

    for i, n in enumerate(numbers):
        mem[n].append(i)
        yield n

    for j in count(i + 1):
        if len(mem[n]) == 1:
            n = 0
        else:
            n, _ = mem[n][1] - mem[n][0], mem[n].popleft()

        mem[n].append(j)
        yield n


def nth(gen, n):
    return next(islice(gen, n, n + 1))


def part1(numbers, n):
    return nth(speak(numbers), n - 1)


def part1(numbers, n):
    return nth(speak(numbers), n - 1)
