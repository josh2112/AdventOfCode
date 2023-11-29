def process(txt):
    v = txt.split("-")
    return range(int(v[0]), int(v[1]) + 1)


with open("input.txt", "r") as f:
    pairs = [[process(pr) for pr in l.strip().split(",")] for l in f.readlines()]


def part1():
    total = 0
    for pair in pairs:
        a, b = set(pair[0]), set(pair[1])
        if a.issubset(b) or a.issuperset(b):
            total += 1
    print(total)


def part2():
    total = 0
    for pair in pairs:
        a, b = set(pair[0]), set(pair[1])
        if len(a.intersection(b)):
            total += 1
    print(total)


part2()
