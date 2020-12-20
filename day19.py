from itertools import count, groupby

with open("input.txt") as f:
    lines = f.read().splitlines()
    rule_lines, messages = [list(group) for k, group in groupby(lines, bool) if k]

    rules = {}
    for rl in rule_lines:
        k, v = rl.replace('"', "").split(": ")
        rules[k] = [i.strip().split(" ") for i in v.split("|")]


def generate(n, rules, messages=[""]):
    if n not in rules:
        return [message + n for message in messages]

    choices = rules[n]

    new = []
    for sequence in choices:
        temp = messages

        for i in sequence:
            temp = generate(i, rules, temp)

        new.extend(temp)

    return new


def trim(message, patterns):
    pattern_len = len(patterns[0])

    for c in count():
        if any(message.startswith(pattern) for pattern in patterns):
            message = message[pattern_len:]
        else:
            return message, c


def part1(rules, messages):
    choices = generate("0", rules)

    return sum(message in choices for message in messages)


def part2(rules, messages):
    """
    0: 8 11
    8: 42 | 42 8
    11: 42 31 | 42 11 31

    - Message consists entirely of 42 and 31
    - Starts with repeated 42
    - Ends with repeated 31
    - Number of 42 > number of 31

    All OK:
    42 42 31
    42 42 42 31
    42 42 42 31 31
    42 42 42 42 31 31 31
    42 42 42 42 42 42 31

    Not OK:
    31
    42
    42 42
    31 31
    42 42 31 31
    """

    ok = 0
    for message in messages:
        counts = {}

        for n, looper in ((n, generate(n, rules)) for n in ("42", "31")):
            message, counts[n] = trim(message, looper)

        if not message and all(counts.values()) and counts["42"] > counts["31"]:
            ok += 1

    return ok
