"""https://adventofcode.com/2016/day/25"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

INC, DEC, CPY, JNZ, OUT = range(5)
INSTRS = ["inc", "dec", "cpy", "jnz", "out"]


def parse(data: list[str]):
    prog = [(line + " .").split() for line in data]

    for instr in prog:
        instr[0] = INSTRS.index(instr[0])
        instr[1] = instr[1] if str.isalpha(instr[1]) else int(instr[1])
        instr[2] = (
            instr[2] if str.isalpha(instr[2]) or instr[2] == "." else int(instr[2])
        )

    return prog


def run(prog: list, reg: dict[str, int], start: int = 0) -> int:
    ic = start - 1

    while ic < len(prog) - 1:
        ic += 1

        if ic == 0:  # First 8 lines are essentially d = a + 2541
            reg["d"] = reg["a"] + 2541
            ic = 8

        if ic == 11:
            reg["c"] = 1 if reg["a"] % 2 else 2
            reg["b"] = 0
            reg["a"] = reg["a"] // 2
            ic = 20

        if ic == 20:
            reg["b"] = 2 - reg["c"]
            reg["c"] = 0
            ic = 27

        instr, x, y, *_ = prog[ic]

        if instr == CPY and y in reg:
            reg[y] = reg[x] if x in reg else x

        elif instr in (INC, DEC):
            reg[x] += 1 if instr == INC else -1

        elif instr == JNZ and (reg[x] if x in reg else x) != 0:
            ic += (reg[y] if y in reg else y) - 1

        elif instr == OUT:
            yield reg[x] if x in reg else x


def target():
    i = 0
    while True:
        yield i % 2
        i += 1


def prob_1(data: list[str]) -> int:
    prog = parse(data)

    # Spent 6 hours looking for the wrong sequence (1,0,1,0...)
    # Answer pops up surprisingly early when looking for the correct sequence (0,1,0,1...)

    a = 0

    while True:
        src = run(prog, {"a": a, "b": 0, "c": 0, "d": 0})
        tgt = target()

        if all(next(src) == next(tgt) for _ in range(100_000)):
            return a

        a += 1


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 25.")
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
