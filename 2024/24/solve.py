"""https://adventofcode.com/2024/day/24"""

import argparse
import time
from collections import defaultdict
from dataclasses import dataclass, field
from operator import __and__, __or__, __xor__
from typing import Callable

# Part to solve, 1 or 2
PART = 1

OPMAP = {"AND": __and__, "OR": __or__, "XOR": __xor__}


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
    value: int = field(hash=False)

    def __lt__(self, other):
        return self.name < other.name


@dataclass
class Gate:
    i1: Wire
    i2: Wire
    op: Callable[[int, int], int]
    opname: str
    out: Wire

    def inputs_from(self, gates) -> bool:
        return any(g.out in (self.i1, self.i2) for g in gates)

    def outputs_to(self, gates) -> bool:
        return all(self.out in (g.i1, g.i2) for g in gates)

    def run(self) -> bool:
        self.out.value = self.op(self.i1.value, self.i2.value)


class Circuit:
    @classmethod
    def parse(cls, data: list[str]):
        split = data.index("")
        wires = keydefaultdict(
            lambda w: Wire(w, -1),
            {
                w: Wire(w, int(v))
                for w, v in [line.split(": ") for line in data[:split]]
            },
        )
        return Circuit(
            [
                Gate(wires[i1], wires[i2], OPMAP[op], op, wires[out])
                for i1, op, i2, _, out in [line.split() for line in data[split + 1 :]]
            ],
            wires,
        )

    def __init__(self, gates, wires):
        self.gates, self.wires = gates, wires
        sw = sorted(w for w in wires.values())
        self.xwires, self.ywires, self.zwires = [
            [w for w in sw if w.name[0] == ltr] for ltr in "xyz"
        ]

    def get_z(self):
        return sum(w.value << i for i, w in enumerate(self.zwires))


def prob_1(data: list[str]) -> int:
    c = Circuit.parse(data)

    q = [g for g in c.gates if g.i1.value >= 0 and g.i2.value >= 0]

    while q:
        for g in q:
            g.run()

        outputs = [g.out for g in q]
        q = [
            nxt
            for nxt in c.gates
            if (nxt.i1 in outputs or nxt.i2 in outputs)
            and nxt.i1.value >= 0
            and nxt.i2.value >= 0
        ]

    return c.get_z()


def verify_adder(ci, wx, wy, co, wz, l1_gates: list[Gate], l2_gates: list[Gate]):
    # L1 AND: output should be input of L2 OR
    if not l1_gates[0].outputs_to([l2_gates[1]]):
        yield l1_gates[0]
    # L1 XOR: output should be input of L2 AND and OR
    if not l1_gates[1].outputs_to([l2_gates[0], l2_gates[-1]]):
        yield l1_gates[1]
    # L2 AND: output should be L2 OR:
    if not l2_gates[0].outputs_to([l2_gates[1]]):
        yield l2_gates[0]
    # L2 OR should not be wz (to catch 1 edge case)
    if l2_gates[1].out == wz:
        yield l2_gates[1]
    # L2 XOR outputs to wz
    if l2_gates[2].out != wz:
        yield l2_gates[2]


def prob_2(data: list[str]) -> int:
    c = Circuit.parse(data)

    wx, wy, wz = c.xwires[0], c.ywires[0], c.zwires[0]
    gates = sorted(
        (g for g in c.gates if g.i1 in (wx, wy) or g.i2 in (wx, wy)),
        key=lambda g: g.opname,
    )
    co = gates[0].out  # First gate should be AND, its output is the carry-out

    bad_gates = []

    for i, wx in enumerate(c.xwires[1:]):
        wy, wz = c.ywires[i + 1], c.zwires[i + 1]
        l1_gates = sorted(
            (g for g in c.gates if g.i1 in (wx, wy) or g.i2 in (wx, wy)),
            key=lambda g: g.opname,
        )

        l2_gates = sorted(
            (g for g in c.gates if g.inputs_from(l1_gates)),
            key=lambda g: g.opname,
        )
        if len(l2_gates) < 3:
            l2_gates += [g for g in c.gates if g.inputs_from(l2_gates)]
            l2_gates = sorted(
                (
                    g
                    for g in l2_gates
                    if g.out.name in set(g.out.name for g in l2_gates)
                ),
                key=lambda g: g.opname,
            )

        ci, co = co, l2_gates[1].out  # This should be OR?

        bad_gates += verify_adder(ci, wx, wy, co, wz, l1_gates, l2_gates)

    return ",".join(sorted(g.out.name for g in bad_gates))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 24.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    args = parser.parse_args()
    part, infile = args.part, "input.txt"

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
