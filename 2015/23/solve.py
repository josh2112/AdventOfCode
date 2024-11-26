"""https://adventofcode.com/2015/day/23"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def parse(data: list[str]) -> tuple:
    for line in data:
        yield [
            int(t) if t[0] == "-" or t[0] == "+" else t
            for t in line.replace(",", "").split()
        ]


def run(prog, reg, ip):
    while ip >= 0 and ip < len(prog):
        oldip = ip
        instr = prog[ip]

        if instr[0][0] == "h":
            reg[instr[1]] /= 2
        elif instr[0][0] == "t":
            reg[instr[1]] *= 3
        elif instr[0][0] == "i":
            reg[instr[1]] += 1
        elif instr[0][2] == "p":
            ip += instr[1]
        elif instr[0][2] == "e":
            ip += instr[2] if not (reg[instr[1]] % 2) else 0
        elif instr[0][2] == "o":
            ip += instr[2] if reg[instr[1]] == 1 else 0
        else:
            raise f"Can't execute instruction {instr}!"

        print(f"{oldip+1}: {instr}   a={reg['a']}, b={reg['b']}")

        if oldip == ip:
            ip += 1

    return int(reg["b"])


def prob_1(data: list[str]) -> int:
    prog = list(parse(data))
    return run(prog, {"a": 0, "b": 0}, 0)


def prob_2(data: list[str]) -> int:
    prog = list(parse(data))
    return run(prog, {"a": 1, "b": 0}, 0)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 23.")
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
