with open("input.txt", "r") as f:
    sacks = [l.strip() for l in f.readlines()]


def itemtype_to_score(item) -> int:
    if item >= ord("a") and item <= ord("z"):
        return item - ord("a") + 1
    else:
        return item - ord("A") + 27


def part1():
    total = 0
    for sack in sacks:
        cmps = set(sack[: len(sack) >> 1]), set(sack[len(sack) >> 1 :])
        itemtype = ord(cmps[0].intersection(cmps[1]).pop())
        if itemtype >= ord("a") and itemtype <= ord("z"):
            total += itemtype_to_score(itemtype)
        else:
            total += itemtype_to_score(itemtype)

    print(total)


def part2():
    total = 0
    for group in zip(sacks[::3], sacks[1::3], sacks[2::3]):
        itemtype = ord(set(group[0]).intersection(set(group[1])).intersection(set(group[2])).pop())
        total += itemtype_to_score(itemtype)

    print(total)


# part1()
part2()
