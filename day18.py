import pyparsing as pp

with open("input.txt") as f:
    expressions = f.read().splitlines()


opn = {
    "+": lambda a, b: int(a) + int(b),
    "*": lambda a, b: int(a) * int(b),
}


def parse1(expression):
    arith = pp.infixNotation(
        pp.Word(pp.nums),
        [(pp.oneOf("+ *"), 2, pp.opAssoc.LEFT)],
    )

    return arith.parseString(expression).asList()


def parse2(expression):
    arith = pp.infixNotation(
        pp.Word(pp.nums),
        [(pp.Literal("+"), 2, pp.opAssoc.LEFT), (pp.Literal("*"), 2, pp.opAssoc.LEFT)],
    )

    return arith.parseString(expression).asList()


def evaluate(parsed):
    parsed.reverse()
    total = parsed.pop()

    if isinstance(total, list):
        total = evaluate(total)

    while parsed:
        op = parsed.pop()
        n = parsed.pop()

        if isinstance(n, list):
            n = evaluate(n)

        total = opn[op](total, n)

    return total


def part1(expressions):
    parsed = [parse1(expression) for expression in expressions]

    return sum(evaluate(p) for p in parsed)


def part2(expressions):
    parsed = [parse2(expression) for expression in expressions]

    return sum(evaluate(p) for p in parsed)
