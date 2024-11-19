"""https://adventofcode.com/2015/day/7"""

import argparse
import time
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


@dataclass
class Input:
    i1: str | int
    i2: str | int
    op: str


def parse(data: list[str]) -> dict[str, Input]:
    """Returns dict of inputs, keyed by their output wire"""
    circuit: dict[str, Input] = {}

    def iora(v):
        return int(v) if v.isdecimal() else v

    for ln in data:
        tk = ln.split()
        out = tk[-1]
        if len(tk) == 5:  # AND, OR, LSHIFT, RSHIFT (w1,w2|i,)
            i2 = int(tk[2]) if tk[1][1] == "S" else iora(tk[2])
            circuit[out] = Input(iora(tk[0]), i2, tk[1][0])
        elif len(tk) == 4:  # NOT (w,0, "NOT")
            circuit[out] = Input(tk[1], 0, tk[0][0])
        else:  # hardcoded value or single wire (w|i,0, "H")
            circuit[out] = Input(iora(tk[0]), 0, "H")
    return circuit


def solve(circuit: dict[str, Input]) -> dict[str, int]:
    # Pull out hardcoded values
    solved = {
        w: inp.i1
        for w, inp in circuit.items()
        if inp.op == "H" and isinstance(inp.i1, int)
    }

    def isknown(v: int | str) -> bool:
        return isinstance(v, int) or v in solved

    def val(v: int | str) -> int:
        return v if isinstance(v, int) else solved[v]

    for k in solved:
        del circuit[k]
    while len(circuit):
        to_solve = [
            w for w, inp in circuit.items() if isknown(inp.i1) and isknown(inp.i2)
        ]
        if not to_solve:
            break
        for w in to_solve:
            inp = circuit[w]
            v1, v2 = val(inp.i1), val(inp.i2)
            if inp.op == "H":
                solved[w] = v1
            elif inp.op == "N":
                solved[w] = ~v1
            elif inp.op == "A":
                solved[w] = v1 & v2
            elif inp.op == "O":
                solved[w] = v1 | v2
            elif inp.op == "L":
                solved[w] = v1 << v2
            elif inp.op == "R":
                solved[w] = v1 >> v2
            del circuit[w]
    for k in solved:
        solved[k] = solved[k] % 65536
    return solved


def prob_1(data: list[str]) -> int:
    return solve(parse(data))["a"]


def prob_2(data: list[str]) -> int:
    a = prob_1(data)
    circuit = parse(data)
    circuit["b"] = Input(a, 0, "H")
    return solve(circuit)["a"]


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2015 day 7.")
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
