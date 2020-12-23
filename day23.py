class LinkedListNode:
    def __init__(self, val, n=None):
        self.val = val
        self.n = n

    def __repr__(self):
        return "{}".format(self.val)

def make_linked_list(puzzle):
    nodes = [LinkedListNode(n) for n in puzzle]
    for node, next_node in zip(nodes, nodes[1:]):
        node.n = next_node
    nodes[-1].n = nodes[0]

    return nodes

def play(nodes, d, rounds):
    current = nodes[0]
    highest = max(d)
    lowest = min(d)

    for _ in range(rounds):
        pickup = [current.n, current.n.n, current.n.n.n]
        current.n = pickup[-1].n

        dest_val = current.val - 1
        while True:
            if dest_val in (pc.val for pc in pickup):
                pass
            elif dest_val in d:
                break

            if dest_val < lowest:
                dest_val = highest
            else:
                dest_val -= 1

        dest = d[dest_val]
        pickup[-1].n = dest.n
        dest.n = pickup[0]
        current = current.n

    return nodes

def part1(puzzle_string, rounds=10):
    puzzle = [int(c) for c in puzzle_string]

    nodes = make_linked_list(puzzle)
    d = {node.val: node for node in nodes}
    nodes = play(nodes, d, rounds)

    cup = d[1]
    solution = ""
    for i in range(len(puzzle) - 1):
        cup = cup.n
        solution += str(cup.val)

    return solution

def part2(puzzle_string, rounds=10**7):
    puzzle = [int(c) for c in puzzle_string]
    puzzle += list(range(max(puzzle) + 1, 10**6 + 1))

    nodes = make_linked_list(puzzle)
    d = {node.val: node for node in nodes}
    nodes = play(nodes, d, rounds)

    return d[1].n.val * d[1].n.n.val
