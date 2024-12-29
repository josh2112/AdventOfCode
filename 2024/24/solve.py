"""https://adventofcode.com/2024/day/24"""

import argparse
import time
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
import random

# Input file path (default is "input.txt")
INPUT = "input.ex3.txt"

# Part to solve, 1 or 2
PART = 2


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


@dataclass
class Wire:
    name: str
    value: int


@dataclass
class Gate:
    i1: Wire
    i2: Wire
    op: str
    out: Wire

    def __str__(self) -> str:
        return f"{self.i1.name} {self.op} {self.i2.name} -> {self.out.name}"


def run(gates, wires, changed_names):
    q = [g for g in gates if any(w.name in changed_names for w in (g.i1, g.i2, g.out))]
    while q:
        changed_names = set()
        for g in q:
            a, b = g.i1.value, g.i2.value
            g.out.value = (
                a & b if g.op[0] == "A" else (a | b if g.op[0] == "O" else a ^ b)
            )
            changed_names.add(g.out.name)

        q = [
            g for g in gates if g.i1.name in changed_names or g.i2.name in changed_names
        ]

    return get_output(wires, "z")


def parse(data: list[str]):
    split = data.index("")
    wires = keydefaultdict(
        lambda w: Wire(w, -1),
        {w: Wire(w, int(v)) for w, v in [line.split(": ") for line in data[:split]]},
    )
    return [
        Gate(wires[i1], wires[i2], op, wires[out])
        for i1, op, i2, _, out in [line.split() for line in data[split + 1 :]]
    ], wires


def prob_1(data: list[str]) -> int:
    gates, wires = parse(data)
    changed = [n for n in wires.keys() if n[0] != "z"]
    return run(gates, wires, changed)


def set_input(wires: dict[Wire], ltr, value):
    inwires = sorted((w for n, w in wires.items() if n[0] == ltr), key=lambda w: w.name)
    for i, b in enumerate(reversed(f"{value:0{len(inwires)}b}")):
        inwires[i].value = int(b)


def get_output(wires, ltr):
    return sum(
        wires[z].value << i
        for i, z in enumerate(sorted((n for n in wires if n[0] == ltr)))
    )


def clr_input(inputs, ltr):
    for w in [w for w in inputs if w[0] == ltr]:
        inputs[w].value = -1


def do_example(gates, wires):
    x, y = 37, 22
    set_input(wires, "x", x)
    set_input(wires, "y", y)
    z = run(gates, wires, [n for n in wires.keys() if n[0] != "z"])

    sw_prev = []

    outputs = sorted(g.out.name for g in gates)

    candidates = []

    # Find all candiate swaps (those that give correct result with the preset X and Y)
    for sw in combinations(outputs, 4):
        sg = {g.out.name: g for g in gates if g.out.name in sw}
        a, b, c, d = sw
        for sw in [(a, b, c, d), (a, c, b, d), (a, d, b, c)]:
            a, b, c, d = sw
            sg[a].out, sg[b].out = sg[b].out, sg[a].out
            sg[c].out, sg[d].out = sg[d].out, sg[c].out
            z = run(gates, wires, set(sw).union(set(sw_prev)))
            if z == x & y:
                candidates.append(sw)
            # reset
            sg[a].out, sg[b].out = sg[b].out, sg[a].out
            sg[c].out, sg[d].out = sg[d].out, sg[c].out
            sw_prev = sw

    # Reset
    run(gates, wires, sw_prev)

    # Test each candidate with 100 random y's
    ywires = [w for w in wires if w[0] == "y"]
    for sw in candidates:
        print("Testing", sw)
        sg = {g.out.name: g for g in gates if g.out.name in sw}
        a, b, c, d = sw
        sg[a].out, sg[b].out = sg[b].out, sg[a].out
        sg[c].out, sg[d].out = sg[d].out, sg[c].out
        run(gates, wires, sw)
        is_bad = False
        for y in range(2 ** len(ywires)):
            set_input(wires, "y", y)
            z = run(gates, wires, ywires)
            if z != x & y:
                is_bad = True
                print("failed at y =", y)
                break
        if not is_bad:
            return sw


def prob_2(data: list[str]) -> int:
    gates, wires = parse(data)

    return do_example(gates, wires)

    # 0 + 31 = 31
    # 0 + 32 = 64  BAD
    # but also... ?
    # 31 + 0 = 31
    # 32 + 0 = 64  BAD

    for y, x in combinations(range(100), 2):
        set_input(wires, "x", x)
        set_input(wires, "y", y)
        z = run(gates, wires, [n for n in wires.keys() if n[0] != "z"])
        print(f"{x} & {y} = {z}  {'' if z == x&y else 'BAD'}")

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
