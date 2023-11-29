import functools, math

USE_SAMPLE = 0
PART = 2

with open("input-sample.txt" if USE_SAMPLE else "input.txt", "r") as f:
    lines = f.readlines()
    pairs = [(eval(a), eval(b)) for a, b in zip(lines[0::3], lines[1::3])]


def cmp(l, r):
    if isinstance(l, list) and isinstance(r, list):
        for i in range(max(len(l), len(r))):
            if i == len(l):
                return -1
            elif i == len(r):
                return 1
            d = cmp(l[i], r[i])
            if d != 0:
                return d
        return 0
    elif isinstance(l, int) and isinstance(r, int):
        return (l - r) / max(abs(l - r), 1)
    else:
        return cmp([l], r) if isinstance(l, int) else cmp(l, [r])


def part1():
    correct = []

    for i in range(len(pairs)):
        if cmp(*pairs[i]) < 0:
            correct.append(i + 1)

    print(sum(correct))


def part2():
    pkts = [[[2]], [[6]]] + [p for pr in pairs for p in pr]
    # print("\n".join(f"{p}" for p in pkts))
    pkts = list(sorted(pkts, key=functools.cmp_to_key(cmp)))
    print("\n".join(f"{p}" for p in pkts))

    indices = pkts.index([[2]]) + 1, pkts.index([[6]]) + 1
    print("----\n", math.prod(indices))


part1() if PART == 1 else part2()
