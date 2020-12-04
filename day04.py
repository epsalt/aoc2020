import re
from validators import between, validator


def part1(f):
    passports = parse_input(f)
    required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    count = 0

    for passport in passports:
        if all(key in passport for key in required):
            count += 1

    return count


def part2(f):
    passports = parse_input(f)
    count = 0

    for passport in passports:
        if validate(passport):
            count += 1

    return count


def validate(passport):
    pipeline = {
        "byr": byr,
        "iyr": iyr,
        "eyr": eyr,
        "hgt": hgt,
        "hcl": hcl,
        "ecl": ecl,
        "pid": pid,
    }

    for field, func in pipeline.items():
        val = passport.get(field)

        if val is None or not func(val):
            return False

    return True


def parse_line(line):
    pattern = r"([\S]*):([\S]*)"
    pairs = re.findall(pattern, line)

    return dict(pairs)


def parse_input(fname):
    with open(fname) as f:
        lines = f.read().splitlines()

    passport = {}
    for line in lines:
        if not line:
            yield passport
            passport = {}

        else:
            data = parse_line(line)
            passport.update(data)

    yield passport


@validator
def byr(val):
    return between(int(val), min=1920, max=2002)


@validator
def iyr(val):
    return between(int(val), min=2010, max=2020)


@validator
def eyr(val):
    return between(int(val), min=2020, max=2030)


@validator
def hgt(val):
    height, units = int(val[:-2]), val[-2:]

    if units == "cm":
        return between(height, 150, 193)

    elif units == "in":
        return between(height, 59, 76)

    else:
        return False


@validator
def hcl(val):
    pattern = r"^#(?:[0-9a-fA-F]{3}){1,2}$"

    return re.match(pattern, val)


@validator
def ecl(val):
    return val in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


@validator
def pid(val):
    return len(val) == 9 and all(c.isdigit() for c in val)
