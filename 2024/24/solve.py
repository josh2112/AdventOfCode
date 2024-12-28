"""https://adventofcode.com/2024/day/24"""

import argparse
import time
from collections import defaultdict
from itertools import combinations


# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def run(gates, inputs):
    unknown = set(g[3] for g in gates if inputs[g[3]] < 0)

    while unknown:
        for g in gates:
            if (
                inputs[g[3]] < 0
                and (a := inputs[g[0]]) >= 0
                and (b := inputs[g[1]]) >= 0
            ):
                inputs[g[3]] = (
                    a & b if g[2][0] == "A" else (a | b if g[2][0] == "O" else a ^ b)
                )
                unknown.remove(g[3])

    return get_output(inputs, "z")


def parse(data: list[str]):
    split = data.index("")
    return [
        (i1, i2, op, o)
        for i1, op, i2, _, o in [line.split() for line in data[split + 1 :]]
    ], defaultdict(
        lambda: -1,
        {w: int(v) for w, v in [line.split(": ") for line in data[:split]]},
    )


def prob_1(data: list[str]) -> int:
    return run(*parse(data))


def set_input(inputs, ltr, value):
    wires = sorted(w for w in inputs if w[0] == ltr)
    for i, b in enumerate(reversed(f"{value:0{len(wires)}b}")):
        inputs[wires[i]] = int(b)


def get_output(inputs, ltr):
    return sum(
        inputs[z] << i for i, z in enumerate(sorted(w for w in inputs if w[0] == ltr))
    )


def clr_input(inputs, ltr):
    for w in [w for w in inputs if w[0] == ltr]:
        inputs[w] = -1


def prob_2(data: list[str]) -> int:
    gates, inputs = parse(data)

    for x, y in combinations(range(0, 10), 2):
        set_input(inputs, "x", x)
        set_input(inputs, "y", y)
        z = run(gates, inputs)
        print(f"{x} + {y} = {z}  {'' if z == x+y else 'BAD'}")

    return 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 24.")
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
