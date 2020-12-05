from collections import defaultdict

with open("input.txt") as f:
    tickets = f.read().splitlines()


def part1(tickets):
    highest = 0

    for ticket in tickets:
        row, seat = get_seat(ticket)
        seatid = row * 8 + seat
        highest = max(seatid, highest)

    return highest


def part2(tickets):
    taken = defaultdict(list)

    for ticket in tickets:
        row, seat = get_seat(ticket)
        taken[row].append(seat)

    nseats = max(len(seats) for seats in taken.values())
    rows = taken.keys()

    for row, seats in taken.items():
        if len(seats) < nseats and row not in (min(rows), max(rows)):
            seat = list(set(range(0, nseats)) - set(seats))[0]

            return row * 8 + seat


def get_seat(ticket):
    seatmap = {"L": 1, "R": 0}
    rowmap = {"F": 1, "B": 0}

    row = get_id(ticket[:-3], rowmap, 127)
    seat = get_id(ticket[-3:], seatmap, 7)

    return row, seat


def get_id(code, mapping, _range):
    low, high = (0, _range)

    for c in code:
        lower = mapping[c]
        low, high = partition(low, high, lower)

    return low


def partition(low, high, lower):
    r = (high - low + 1) // 2

    if lower:
        return low, high - r
    else:
        return low + r, high
