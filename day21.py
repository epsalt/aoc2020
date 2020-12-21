from collections import defaultdict

with open("input.txt") as f:
    data = []
    for line in f.read().splitlines():
        i, a = line.split(" (")
        ingredients = i.split(" ")
        allergens = a[9:-1].split(", ")
        data.append((ingredients, allergens))


def get_allergies(data):
    ad = defaultdict(list)
    all_allergens = set()

    for ingredients, allergens in data:
        for allergen in allergens:
            all_allergens.add(allergen)
            ad[allergen].append(ingredients)

    possible = {a: set.intersection(*[set(il) for il in ils]) for a, ils in ad.items()}

    certain = {}
    while len(certain) < len(all_allergens):
        for allergen, ingredients in possible.items():
            diff = set(ingredients) - set(certain.values())

            if len(diff) == 1:
                certain[allergen] = diff.pop()

    return certain


def part1(data):
    certain = get_allergies(data)

    count = 0
    for ings, _ in data:
        for i in ings:
            if i not in certain.values():
                count += 1

    return count


def part2(data):
    certain = get_allergies(data)
    return ",".join(certain[key] for key in sorted(certain.keys()))
