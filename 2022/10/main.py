with open("input.txt", "r") as f:
    cmds = [l.split() for l in f.readlines()]


def calc():
    cur = 1
    v = []

    for cmd in cmds:
        if cmd[0] == "noop":
            v += [cur]
        else:
            v += [cur, cur]
            cur += int(cmd[1])
    return v + [cur]


def part1():
    v = calc()
    print(sum((i + 1) * v[i] for i in range(19, 220, 40)))


def part2():
    v = calc()
    crt = ["." for _ in range(len(v))]
    for i in range(len(v)):
        if abs((i % 40) - v[i]) <= 1:
            crt[i % 240] = "#"

    lines = ["".join(crt[i : i + 40]) for i in range(0, 241, 40)]
    print("\n".join(lines))


# part1()
part2()
