"""https://adventofcode.com/2016/day/23"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

INC, DEC, CPY, JNZ, TGL = range(5)
INSTRS = ["inc", "dec", "cpy", "jnz", "tgl"]


def run(data: list[str], reg: dict[str, int], ic: int) -> int:
    prog = [(line + " .").split() for line in data]
    for instr in prog:
        instr[0] = INSTRS.index(instr[0])

    while ic < len(prog) - 1:
        ic += 1

        instr, x, y, *_ = prog[ic]

        if instr == TGL:  # tgl
            d = ic + reg[x] if x in reg else int(x)
            if d < 0 or d >= len(prog):
                continue
            elif prog[d][0] == CPY:
                prog[d][0] = JNZ
            elif prog[d][0] == JNZ:
                prog[d][0] = CPY
            elif prog[d][0] == INC:
                prog[d][0] = DEC
            elif prog[d][0] in (DEC, TGL):
                prog[d][0] = INC

        elif instr == CPY and y in reg:
            reg[y] = reg[x] if x in reg else int(x)

        elif instr in (INC, DEC):
            reg[x] += 1 * (1 if instr == INC else -1)

        elif instr == JNZ and (reg[x] if x in reg else int(x)) != 0:
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
