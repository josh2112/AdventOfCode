"""https://adventofcode.com/2024/day/24"""

import argparse
import time
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from operator import __and__ as AND
from operator import add as ADD

from more_itertools import set_partitions

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
    changed_outputs = []
    iters = 0
    while q:
        changed_names = set()
        for g in q:
            a, b = g.i1.value, g.i2.value
            tmp = a & b if g.op[0] == "A" else (a | b if g.op[0] == "O" else a ^ b)
            if tmp != g.out.value:
                changed_outputs.append((g.out, g.out.value))
                g.out.value = tmp
                changed_names.add(g.out.name)

        q = [
            g for g in gates if g.i1.name in changed_names or g.i2.name in changed_names
        ]
        iters += 1
        # Dumb loop prevention: if we've looped more than 64 times (more than enough to recompute the whole thing,
        # assume we're created a loop
        if iters > 64:
            return -1, changed_outputs

    return get_output(wires, "z"), changed_outputs


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
    return run(gates, wires, changed)[0]


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


def prob_2(data: list[str]) -> int:
    gates, wires = parse(data)

    # Example:
    # bag_size, op = 4, AND

    # Real input:
    bag_size, op = 8, ADD

    x, y = 37, 22
    set_input(wires, "x", x)
    set_input(wires, "y", y)
    run(gates, wires, [n for n in wires.keys() if n[0] != "z"])

    outputs = [g.out.name for g in gates]

    candidates = []

    print("generating combos...")
    combos_to_try = (
        [w for pr in x for w in pr]
        for combo in combinations(outputs, bag_size)
        for x in set_partitions(combo, bag_size // 2, 2, 2)
    )

    i = 1

    # Find all candidate swaps (those that give correct result with the preset X and Y)
    for sw in combos_to_try:
        if not i % 1000:
            print(i)
        i += 1
        sg = {g.out.name: g for g in gates if g.out.name in sw}
        # Do the swaps
        for pr in range(0, len(sw), 2):
            sg[sw[pr]].out, sg[sw[pr + 1]].out = sg[sw[pr + 1]].out, sg[sw[pr]].out
        z, changed_outputs = run(gates, wires, sw)
        if z == op(x, y):
            print("Found candidate:", sw)
            candidates.append(sw)
        # reset
        for pr in range(0, len(sw), 2):
            sg[sw[pr]].out, sg[sw[pr + 1]].out = sg[sw[pr + 1]].out, sg[sw[pr]].out
        for w, v in changed_outputs:
            w.value = v

    # Test each candidate with 100 random y's
    ywires = [w for w in wires if w[0] == "y"]
    for sw in candidates:
        print("Testing", sw)
        sg = {g.out.name: g for g in gates if g.out.name in sw}
        for pr in range(0, len(sw), 2):
            sg[sw[pr]].out, sg[sw[pr + 1]].out = sg[sw[pr + 1]].out, sg[sw[pr]].out
        is_bad = False
        for y in range(2 ** len(ywires)):
            set_input(wires, "y", y)
            z, changed_outputs = run(gates, wires, ywires)
            if z != op(x, y):
                is_bad = True
                print("failed at y =", y)
                for pr in range(0, len(sw), 2):
                    sg[sw[pr]].out, sg[sw[pr + 1]].out = (
                        sg[sw[pr + 1]].out,
                        sg[sw[pr]].out,
                    )
                for w, v in changed_outputs:
                    w.value = v
                break
        if not is_bad:
            return ",".join(sorted(sw))


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
