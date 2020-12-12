import re

with open("input.txt") as f:
    lines = f.read().splitlines()
    actions = [
        (action, int(n))
        for line in lines
        for action, n in re.findall(r"^([A-z])(\d+)$", line)
    ]

turns = {"L": -1, "R": 1}
directions = {"N": 0, "E": 90, "S": 180, "W": 270}
complexify = {0: (0 + 1j), 90: (1 + 0j), 180: (0 - 1j), 270: (-1 + 0j), 360: (0 + 1j)}


def rotate(loc, direction, theta):
    cw = turns[direction]

    for _ in range(theta // 90):
        loc = complex(cw * loc.imag, -cw * loc.real)

    return loc


def manhattan(loc):
    distance = abs(loc.real) + abs(loc.imag)
    return int(distance)


def part1(actions):
    ship = 0
    orientation = 90

    for move in actions:
        action, n = move

        if action in directions:
            direction = complexify[directions[action]]
            ship += direction * n

        if action in turns:
            orientation = (orientation + turns[action] * n) % 360

        if action == "F":
            direction = complexify[orientation]
            ship += direction * n

    return manhattan(ship)


def part2(actions):
    ship = 0
    waypoint = 10 + 1j

    for move in actions:
        action, n = move

        if action in directions:
            direction = complexify[directions[action]]
            waypoint += direction * n

        if action in turns:
            waypoint = rotate(waypoint, action, n)

        if action == "F":
            ship += waypoint * n

    return manhattan(ship)
