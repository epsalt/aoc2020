from itertools import count


class Console:
    def __init__(self, program):
        self.instructions = list(self._parse(program))
        self.line = 0
        self.accumulator = 0

    def step(self):
        op, n = self.instructions[self.line]
        op(n)

    def acc(self, n):
        self.accumulator += n
        self.line += 1

    def jmp(self, n):
        self.line += n

    def nop(self, n):
        self.line += 1

    def patch(self, line):
        op, n = self.instructions[line]

        if op == self.nop:
            op = self.jmp

        elif op == self.jmp:
            op = self.nop

        self.instructions[line] = op, n

    def _parse(self, program):
        with open(program) as f:
            lines = f.read().splitlines()
            for line in lines:
                op, n = line.split()
                yield (getattr(self, op), int(n))

    def __len__(self):
        return len(self.instructions)


def loops(console):
    seen = set()

    while True:
        if console.line in seen:
            return True

        if console.line > len(console) - 1:
            return False

        seen.add(console.line)
        console.step()


def part1(input_file):
    console = Console(input_file)
    loops(console)

    return console.accumulator


def part2(input_file):
    for line in count():
        console = Console(input_file)
        op, n = console.instructions[line]
        console.patch(line)

        if not loops(console):
            return console.accumulator
