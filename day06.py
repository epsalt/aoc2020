def parse_input(fname):
    with open(fname) as f:
        lines = f.read().splitlines()

    group = []
    for line in lines:
        if not line:
            yield group
            group = []

        else:
            group.append(line)

    yield group


def part1(fname):
    groups = parse_input(fname)
    count = 0

    for group in groups:
        responses = (response for person in group for response in person)
        count += len(set(responses))

    return count


def part2(fname):
    groups = parse_input(fname)
    count = 0

    for group in groups:
        questions = set(response for person in group for response in person)

        for question in questions:
            if all(question in person for person in group):
                count += 1

    return count
