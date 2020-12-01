with open("input.txt") as inputs:
    numbers = [int(i) for i in inputs]


def find_pair(numbers, goal):
    numberset = set(numbers)

    for number in numbers:
        friend = goal - number

        if friend in numberset:
            return number, friend


def find_triple(numbers, goal):
    for number in numbers:
        friends = set(numbers)
        friends.remove(number)

        if pair := find_pair(friends, goal=goal - number):
            return number, *pair


def part1(numbers, goal=2020):
    a, b = find_pair(numbers, goal)

    print(a, b)
    return a * b


def part2(numbers, goal=2020):
    a, b, c = find_triple(numbers, goal)

    print(a, b, c)
    return a * b * c
