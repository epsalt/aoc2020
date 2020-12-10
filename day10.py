from collections import Counter

with open("input.txt") as f:
    numbers = [int(n) for n in f.readlines()]
    adapters = [0] + sorted(numbers) + [max(numbers) + 3]


def differences(adapters):
    for x, y in zip(adapters, adapters[1:]):
        yield y - x


def steps(n):
    if n in (0, 1):
        return 1
    elif n == 2:
        return 2
    else:
        return steps(n - 3) + steps(n - 2) + steps(n - 1)


def part1(adapters):
    counts = Counter(differences(adapters))

    return counts[1] * counts[3]


def part2(adapters):
    todo = []
    count = 1

    for adapter, diff in zip(adapters, differences(adapters)):
        todo.append(adapter)

        if diff == 3:
            count *= steps(len(todo) - 1)
            todo = []

    return count
