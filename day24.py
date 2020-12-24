from collections import defaultdict


def parse(line):
    moves = []
    curr = ""
    options = ["e", "se", "sw", "w", "nw", "ne"]

    for c in line:
        curr += c
        if curr in options:
            moves.append(curr)
            curr = ""

    return moves


with open("input.txt") as f:
    paths = []
    for line in f.read().splitlines():
        paths.append(parse(line))


moves = {
    "e": (1, -1, 0),
    "se": (0, -1, 1),
    "sw": (-1, 0, 1),
    "w": (-1, 1, 0),
    "nw": (0, +1, -1),
    "ne": (1, 0, -1),
}


def get_tiles(paths):
    tiles = defaultdict(lambda: False)

    for path in paths:
        loc = (0, 0, 0)
        for step in path:
            loc = tuple(sum(x) for x in zip(loc, moves[step]))

        tiles[loc] = not tiles[loc]

    return dict(tiles)


def get_neighbours(tile):
    for loc in moves.values():
        yield tuple(sum(x) for x in zip(tile, loc))


def part1(paths):
    tiles = get_tiles(paths)

    return sum(tiles.values())


def part2(paths, n):
    tiles = get_tiles(paths)

    for i in range(n):
        _next = {}
        neighbours = {}
        for tile in tiles.keys():
            for neighbour in get_neighbours(tile):
                if not tiles.get(neighbour):
                    neighbours[neighbour] = False

        tiles.update(neighbours)

        for tile, state in tiles.items():
            adj = sum(tiles.get(neighbour, False) for neighbour in get_neighbours(tile))

            if state and (adj == 0 or adj > 2):
                _next[tile] = not (state)
            elif state:
                _next[tile] = state

            if not state and adj == 2:
                _next[tile] = not (state)
            elif not state:
                _next[tile] = state

        tiles = _next

    return sum(tiles.values())
