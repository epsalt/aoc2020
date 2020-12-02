import re


def parse(line):
    pattern = r"^(\d+)-(\d+) ([a-z]): ([a-zA-Z]+)$"
    matches = re.search(pattern, line)

    return matches.groups()


with open("input.txt") as inputs:
    lines = [parse(line) for line in inputs]


def part1(lines):
    valid = 0

    for line in lines:
        start, end, letter, password = line
        count = password.count(letter)

        if count >= int(start) and count <= int(end):
            valid += 1

    return valid


def part2(lines):
    valid = 0

    for line in lines:
        start, end, letter, password = line
        check = sum([password[int(i) - 1] == letter for i in (start, end)])

        if check == 1:
            valid += 1

    return valid
