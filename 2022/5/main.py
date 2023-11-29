def parse_stacks(layout):
    stacks = [[] for _ in range(len(range(1, len(layout[0]), 4)))]

    for line in layout:
        letters = [line[i] for i in range(1, len(line), 4)]
        for i in range(len(letters)):
            if letters[i].isalpha():
                stacks[i].append(letters[i])

    return stacks


def print_stacks(stacks):
    out = []
    for y in range(1, max([len(s) for s in stacks]) + 1):
        out.append("".join([(f" {s[-y]} " if y <= len(s) else "   ") for s in stacks]))
    print("\n".join(reversed(out)))


def parse_moves(moves):
    for m in moves:
        parts = [int(v) for v in m.split()[1::2]]
        yield (parts[0], parts[1] - 1, parts[2] - 1)


with open("input.txt", "r") as f:
    lines = [l for l in f.readlines()]

sep = lines.index("\n")
stacks = parse_stacks(lines[: sep - 1])
moves = list(parse_moves(lines[sep + 1 :]))


def part1():
    for m in moves:
        tomove = reversed(stacks[m[1]][: m[0]])
        stacks[m[2]] = list(tomove) + stacks[m[2]]
        stacks[m[1]] = stacks[m[1]][m[0] :]

    print_stacks(stacks)


def part2():
    for m in moves:
        tomove = stacks[m[1]][: m[0]]
        stacks[m[2]] = list(tomove) + stacks[m[2]]
        stacks[m[1]] = stacks[m[1]][m[0] :]

    print_stacks(stacks)


# part1()
part2()
