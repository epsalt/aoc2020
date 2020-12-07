import re


def build_graph(input_file):
    graph = {}
    
    with open("input.txt") as f:
        for line in f.read().splitlines():
            parent = re.findall(r"^(.*) bags contain", line)[0]
            children = [
                {'n': int(n), 'color': color}
                for n, color
                in re.findall(r"(\d) (.*?) bags?", line)
            ]
            graph[parent] = children

    return graph


def contains(rules, parent, target):
    if not rules[parent]:
        return False

    for child in rules[parent]:
        if child['color'] == target or contains(rules, child['color'], target):
            return True

    return False


def bag_count(rules, parent):
    count = 1

    if not rules[parent]:
        return count

    for child in rules[parent]:
        for _ in range(child['n']):
            count += bag_count(rules, child['color'])

    return count


def part1(input_file, goal='shiny gold'):
    rules = build_graph(input_file)
    count = 0

    for color in rules.keys():
        if contains(rules, color, goal):
            count += 1

    return count


def part2(input_file, goal='shiny gold'):
    rules = build_graph(input_file)

    return bag_count(rules, goal) - 1
