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
                if target and target[: len(out)] != out:
                    return out
            case 6:  # bdv
                regs[1] = regs[0] // pow(2, cmb(op))
            case 7:  # cdv
                regs[2] = regs[0] // pow(2, cmb(op))
        ip += 2

    return out


def prob_1(data: list[str]) -> int:
    regs, prog = parse(data)
    return ",".join(str(v) for v in run(regs, prog))


def prob_2(data: list[str]) -> int:
    regs_orig, prog = parse(data)
    a, out = pow(8, 15) - 1, []

    while out != prog:
        a += 1_000
        regs = regs_orig.copy()
        regs[0] = a
        out = run(regs, prog, prog)

        if out[0] == prog[0]:
            print(a, out)

    return a


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
