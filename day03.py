from functools import reduce


class Terrain:
    def __init__(self, lines):
        self.rows = lines
        self.width = len(self.rows[0])

    def __getitem__(self, pos):
        x, y = pos
        row = self.rows[y]

        return row[x % self.width]

    def __len__(self):
        return len(self.rows)


def taboggan(hill, slopes):
    for (dx, dy) in slopes:
        trees = 0
        for y in range(0, len(hill), dy):
            x = y * dx // dy

            if hill[x, y] == '#':
                trees += 1

        yield trees


with open("input.txt") as f:
    lines = f.read().splitlines()
    hill = Terrain(lines)


def part1(hill):
    slopes = [(3, 1)]
    runs = list(taboggan(hill, slopes))

    print(runs)
    return reduce((lambda x, y: x * y), runs)


def part2(hill):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    runs = list(taboggan(hill, slopes))

    print(runs)
    return reduce((lambda x, y: x * y), runs)
