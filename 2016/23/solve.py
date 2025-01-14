"""https://adventofcode.com/2016/day/23"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def run(data: list[str], reg: dict[str, int], ic: int) -> int:
    prog = [(line + " .").split() for line in data]

    while ic < len(prog) - 1:
        ic += 1

        instr, x, y, *_ = prog[ic]

        if instr == "tgl":  # tgl
            d = ic + reg[x] if x in reg else int(x)
            if d < 0 or d >= len(prog):
                continue
            elif prog[d][0] == "cpy":  # cpy
                prog[d][0] = "jnz"
            elif prog[d][0] == "jnz":  # jnz
                prog[d][0] = "cpy"
            elif prog[d][0] == "inc":  # inc
                prog[d][0] = "dec"
            elif prog[d][0] in ("dec", "tgl"):
                prog[d][0] = "inc"

        elif instr[0] == "c" and y in reg:  # cpy
            reg[y] = reg[x] if x in reg else int(x)

        elif instr[2] == "c":  # inc/dec
            reg[x] += 1 * (1 if instr[0] == "i" else -1)

        elif instr[0] == "j" and (reg[x] if x in reg else int(x)) != 0:  # jnz
            ic += reg[y] if y in reg else int(y) - 1

    return reg["a"]


def prob_1(data: list[str]) -> int:
    return run(data, {"a": 7, "b": 0, "c": 0, "d": 0}, -1)


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 23.")
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
