"""https://adventofcode.com/2024/day/24"""

import argparse
import time
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from operator import __and__ as AND, __or__ as OR, __xor__ as XOR, add as ADD
from typing import Callable

from more_itertools import set_partitions

# Input file path (default is "input.txt")
INPUT = "input.txt"

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

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, value):
        return self.name == value

    def __lt__(self, other):
        return self.name < other.name


@dataclass
class Gate:
    i1: Wire
    i2: Wire
    op: Callable[[int, int], int]
    out: Wire

    def __str__(self) -> str:
        return f"{self.i1.name} {self.op} {self.i2.name} -> {self.out.name}"


# TODO: TEST all, then start using?
class Device:
    def __init__(self, gates, wires):
        self.gates, self.wires = gates, wires
        sw = sorted(w for w in wires.values())
        self.xwires, self.ywires, self.zwires = [
            [w for w in sw if w.name[0] == ltr] for ltr in "xyz"
        ]

    def set_x(self, value):
        for i, b in enumerate(reversed(f"{value:0{len(self.xwires)}b}")):
            self.xwires[i].value = int(b)

    def set_y(self, value):
        for i, b in enumerate(reversed(f"{value:0{len(self.ywires)}b}")):
            self.ywires[i].value = int(b)

    def get_z(self):
        return sum(w.value << i for i, w in enumerate(self.zwires))


def parse(data: list[str]):
    split = data.index("")
    wires = keydefaultdict(
        lambda w: Wire(w, -1),
        {w: Wire(w, int(v)) for w, v in [line.split(": ") for line in data[:split]]},
    )
    opmap = {"A": AND, "O": OR, "X": XOR}
    return [
        Gate(wires[i1], wires[i2], opmap[op[0]], wires[out])
        for i1, op, i2, _, out in [line.split() for line in data[split + 1 :]]
    ], wires


def run(gates, wires, changed_wires):
    q = [
        g
        for g in gates
        if g.i1 in changed_wires or g.i2 in changed_wires or g.out in changed_wires
    ]
    orig_outputs = dict()
    iters = 0
    while q:
        changed_wires = set()
        for g in q:
            if (tmp := g.op(g.i1.value, g.i2.value)) != g.out.value:
                if g.out not in orig_outputs:
                    orig_outputs[g.out] = g.out.value
                g.out.value = tmp
                changed_wires.add(g.out)

        q = [g for g in gates if g.i1 in changed_wires or g.i2 in changed_wires]
        iters += 1
        # Dumb loop prevention: if we've looped more than 64 times (more than enough to recompute the whole thing,
        # assume we're created a loop
        if iters > 64:
            print("loop detected")
            return orig_outputs

    return orig_outputs


def prob_1(data: list[str]) -> int:
    gates, wires = parse(data)
    changed = [w for n, w in wires.items() if n[0] != "z"]
    run(gates, wires, changed)
    return sum(
        w.value << i
        for i, w in enumerate(sorted(w for w in wires.values() if w.name[0] == "z"))
    )


def set_input(wires: dict[Wire], ltr, value):
    inwires = sorted((w for n, w in wires.items() if n[0] == ltr), key=lambda w: w.name)
    for i, b in enumerate(reversed(f"{value:0{len(inwires)}b}")):
        inwires[i].value = int(b)


def clr_input(inputs, ltr):
    for w in [w for w in inputs if w[0] == ltr]:
        inputs[w].value = -1


def gather_candidates(gates, wires, gates_by_output, x, y):
    bag_size, op = (4, AND) if "ex" in INPUT else (8, ADD)
    candidates = []

    combos_to_try = (
        [n for pr in x for n in pr]
        for combo in combinations(gates_by_output.keys(), bag_size)
        for x in set_partitions(combo, bag_size // 2, 2, 2)
    )

    zwires = sorted(w for w in wires.values() if w.name[0] == "z")

    def get_z():
        return sum(w.value << i for i, w in enumerate(zwires))

    i = 1

    with open("candidates.txt", "w") as f:
        f.write("---\n")

    # Find all candidate swaps (those that give correct result with the preset X and Y)
    for sw in combos_to_try:
        if not i % 1000:
            print(i)
        i += 1
        sg = [gates_by_output[w] for w in sw]
        # Do the swaps
        for pr in range(0, len(sg), 2):
            sg[pr].out, sg[pr + 1].out = sg[pr + 1].out, sg[pr].out
        changed_outputs = run(gates, wires, sw)
        if get_z() == op(x, y):
            print("Found candidate:", sw)
            with open("candidates.txt", "a") as f:
                f.write(",".join(w.name for w in sw) + "\n")
            candidates.append(sw)
        # reset
        for pr in range(0, len(sg), 2):
            sg[pr].out, sg[pr + 1].out = sg[pr + 1].out, sg[pr].out
        for w, v in changed_outputs.items():
            w.value = v

    return candidates


def prob_2(data: list[str]) -> int:
    gates, wires = parse(data)

    zwires = sorted(w for w in wires.values() if w.name[0] == "z")

    def get_z():
        return sum(w.value << i for i, w in enumerate(zwires))

    bag_size, op = (4, AND) if "ex" in INPUT else (8, ADD)

    x, y = 37, 22
    set_input(wires, "x", x)
    set_input(wires, "y", y)
    run(gates, wires, [w for w in wires.values() if w.name[0] != "z"])

    gates_by_output = {g.out: g for g in gates}

    candidates = gather_candidates(gates, wires, gates_by_output, x, y)

    # Test each candidate with 100 random y's
    ywires = [w for w in wires.values() if w.name[0] == "y"]
    for sw in candidates:
        print("Testing", sw)
        sg = [gates_by_output[w] for w in sw]
        for pr in range(0, len(sg), 2):
            sg[pr].out, sg[pr + 1].out = sg[pr + 1].out, sg[pr].out
        is_bad = False
        for y in range(2 ** len(ywires)):
            set_input(wires, "y", y)
            changed_outputs = run(gates, wires, ywires)
            if get_z() != op(x, y):
                is_bad = True
                print("failed at y =", y)
                for pr in range(0, len(sg), 2):
                    sg[pr].out, sg[pr + 1].out = sg[pr + 1].out, sg[pr].out
                for w, v in changed_outputs.items():
                    w.value = v
                break
        if not is_bad:
            return ",".join(sorted([w.name for w in sw]))


def main() -> float:
    global INPUT
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 24.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    INPUT = infile

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
