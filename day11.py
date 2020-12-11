from hashlib import md5

with open("input.txt") as f:
    lines = [list(line) for line in f.read().splitlines()]


class Seating:
    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.directions = (
            (1, 0),
            (1, 1),
            (1, -1),
            (0, 1),
            (0, -1),
            (-1, 0),
            (-1, 1),
            (-1, -1),
        )

    def adjacent(self, x, y):
        for d in self.directions:
            yield self[x + d[0], y + d[1]]

    def sight(self, x, y):
        for direction in self.directions:
            dx, dy = direction
            yield self._sightline(x, y, dx, dy)

    def next(self, x, y, fn, n):
        occupied = sum(seat == "#" for seat in fn(x, y))

        if self[x, y] == ".":
            return "."
        elif occupied >= n:
            return "L"
        elif occupied == 0:
            return "#"
        else:
            return self[x, y]

    def step(self, fn, n):
        self.lines = [
            [self.next(x, y, fn, n) for x in range(self.width)]
            for y in range(len(self))
        ]

    def _sightline(self, x, y, dx, dy):
        while True:
            x += dx
            y += dy
            seat = self[x, y]

            if seat == ".":
                pass
            elif not seat or seat == "L":
                return "L"
            elif seat == "#":
                return "#"

    def _string(self):
        return "".join(["".join(line) for line in self.lines])

    @property
    def occupied(self):
        return sum(seat == "#" for seat in self._string())

    @property
    def hash(self):
        return md5(self._string().encode("utf-8")).hexdigest()

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, pos):
        x, y = pos

        if y < 0 or y >= len(self):
            return None

        if x < 0 or x >= self.width:
            return None

        return self.lines[y][x]

    def __str__(self):
        return "\n".join(["".join(line) for line in self.lines])


def part1(lines):
    seating = Seating(lines)
    last = seating.hash

    while True:
        seating.step(seating.adjacent, 4)
        new = seating.hash

        if new == last:
            return seating.occupied
        else:
            last = new


def part2(lines):
    seating = Seating(lines)
    last = seating.hash

    while True:
        seating.step(seating.sight, 5)
        new = seating.hash

        if new == last:
            return seating.occupied
        else:
            last = new
