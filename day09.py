from itertools import combinations


with open("input.txt") as f:
    numbers = [int(n) for n in f.readlines()]


def part1(numbers, lag):
    for i, n in enumerate(numbers[lag:]):
        prev = numbers[i: i + lag]
        combos = list(combinations(prev, 2))
        choices = [a + b for combo in combos for a, b in combos]

        if n not in choices:
            return n


def part2(numbers, key):
    cache = {}
    total = 0

    for i in range(len(numbers)):
        total += numbers[i]

        if total - key in cache:
            start, end = cache[total - key] + 1, i

            return max(numbers[start:end]) + min(numbers[start:end])

        cache[total] = i
