"""https://adventofcode.com/2024/day/17"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def parse(data: list[str]) -> int:
    return [int(line.split(": ")[1]) for line in data[: data.index("")]], [
        int(v) for v in data[data.index("") + 1].split(": ")[1].split(",")
    ]


def run(regs, prog, target=None):
    def cmb(op):
        return op if op < 4 else regs[op - 4]

    ip, out = 0, []
    while 0 <= ip < len(prog) - 1:
        op = prog[ip + 1]
        match prog[ip]:
            case 0:  # adv
                regs[0] //= pow(2, cmb(op))
            case 1:  # bxl
                regs[1] ^= op
            case 2:  # bst
                regs[1] = cmb(op) % 8
            case 3:  # jnz
                if regs[0] != 0:
                    ip = op - 2
            case 4:  # bxc
                regs[1] ^= regs[2]
            case 5:  # out
                out.append(cmb(op) % 8)
            case 6:  # bdv
                regs[1] = regs[0] // pow(2, cmb(op))
            case 7:  # cdv
                regs[2] = regs[0] // pow(2, cmb(op))
        ip += 2

    return out


def prob_1(data: list[str]) -> int:
    return ",".join(str(v) for v in run(*parse(data)))


def prob_2(data: list[str]) -> int:
    (_, b, c), prog = parse(data)

    q = [[]]

    while True:
        octets = q.pop(0)
        A = 0
        for v in octets:
            A = (A + v) << 3

        if len(octets) == len(prog):
            return A >> 3

        tgt = prog[-len(octets) - 1 :]
        poss = [i for i in range(8) if tgt == run({0: A + i, 1: b, 2: c}, prog)]
        for p in poss:
            q.append(octets + [p])


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 17.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
