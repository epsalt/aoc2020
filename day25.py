from itertools import count


def transform(subject, loop_size):
    val = 1
    for _ in range(loop_size):
        val = val * subject
        val = val % 20201227

    return val


def get_loop(subject, public):
    val = 1
    for loop in count():
        val = val * subject
        val = val % 20201227

        if val == public:
            return loop


def part1(door, card):
    loop = get_loop(7, door)
    encryption = transform(loop, card)

    return encryption
