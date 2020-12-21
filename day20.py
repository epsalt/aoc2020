from math import prod, sqrt
from itertools import groupby, zip_longest
import re


def get_edges(data):
    top = data[0]
    bottom = data[-1]

    left = "".join(line[0] for line in data)
    right = "".join(line[-1] for line in data)

    return top, bottom, left, right


with open("input.txt") as f:
    lines = f.read().splitlines()
    groups = [list(group) for k, group in groupby(lines, bool) if k]

    edges = {}
    tiles = {}
    for group in groups:
        name = re.search(r"\d+", group[0]).group()
        data = group[1:]

        tiles[int(name)] = data
        edges[int(name)] = get_edges(data)


def options(piece):
    for side in piece:
        yield side
        yield side[::-1]


def matches(name, tiles):
    lookup = {_name: set(options(data)) for _name, data in tiles.items()}

    for _name, opts in lookup.items():
        if bool(lookup[name] & opts):
            if _name != name:
                yield _name


def get_order(edges):
    graph = {name: list(matches(name, edges)) for name in edges.keys()}
    corners = [name for name, adj in graph.items() if len(adj) == 2]
    sidelen = sqrt(len(edges))

    start = corners[0]
    for corner in corners:
        if len(shortest(graph, start, corner)) == sidelen:
            end = corner

    puzzle = []
    placed = set()

    while True:
        row = shortest(graph, start, end)
        puzzle.append(row)
        placed.update(row)

        if len(placed) == len(edges):
            return puzzle

        start = [name for name in graph[start] if name not in placed][0]
        end = [name for name in graph[end] if name not in placed][0]


def get_image(order, tiles):
    rows = []
    for rorder in order:
        irow = []
        for x, y in zip(rorder, rorder[1:]):
            if not irow:
                xo, yo = orient(orientations(tiles[x]), tiles[y])
                irow.append(xo)
            else:
                _, yo = orient([yo], tiles[y])

            irow.append(yo)
        rows.append(concat(irow))

    img = []
    for i, j in zip(rows, rows[1:]):
        if not img:
            io, jo = orient(orientations(i), j)
            img.append(io)
        else:
            _, jo = orient([jo], j)

        img.append(jo)
    return concat(concat(img))


def concat(tiles):
    out = []
    for row in zip(*tiles):
        out.append("".join(row))

    return out


def degap(img, dim):
    out = []
    for row in grouper(img, dim):
        cols = row[1:-1]

        for col in cols:
            line = ""
            for group in grouper(col, dim):
                line += "".join(group[1:-1])

            out.append(line)

    return out


def orientations(tile):
    for _ in range(4):
        tile = ["".join(row) for row in zip(*tile[::-1])]
        yield tile

    tile = [r[::-1] for r in tile]
    for _ in range(4):
        tile = ["".join(row) for row in zip(*tile[::-1])]
        yield tile


def orient(aos, b):
    for ao in aos:
        for bo in orientations(b):
            right = "".join(line[-1] for line in ao)
            left = "".join(line[0] for line in bo)

            if left == right:
                return ao, bo


def check_monster(i, j, img):
    monster = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]

    if len(img[0]) - i < len(monster[0]):
        return False

    if len(img) - j < len(monster):
        return False

    lines = [line[i : i + len(monster[0])] for line in img[j : j + len(monster)]]

    for pair in zip(lines, monster):
        for c, mc in zip(*pair):
            if c != mc and mc != " ":
                return False

    return True


def grouper(iterable, n, fillvalue=None):
    """https://stackoverflow.com/a/434411/4501508"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def shortest(graph, start, goal):
    """http://disq.us/t/3ps3f3d"""
    explored = []
    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in explored:
            neighbours = graph[node]

            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                if neighbour == goal:
                    return new_path

            explored.append(node)


def part1(edges, tiles):
    corners = [n for n, d in edges.items() if len(list(matches(n, edges))) == 2]
    return prod(corners)


def part2(edges, tiles):
    order = get_order(edges)
    img = get_image(order, tiles)
    degapped = degap(img, 10)

    rough = 0
    for row in degapped:
        rough += sum(cell == "#" for cell in row)

    monsters = []
    for orientation in orientations(degapped):
        for j in range(len(orientation)):
            for i in range(len(orientation[0])):
                if check_monster(i, j, orientation):
                    monsters.append([i, j])

    return rough - len(monsters) * 15
