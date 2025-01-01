"""https://adventofcode.com/2024/day/24"""

import argparse
import time
from dataclasses import dataclass
from typing import Callable
from collections import defaultdict
from operator import __and__ as AND, __or__ as OR, __xor__ as XOR


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

    def __str__(self) -> str:
        return self.name


@dataclass
class Gate:
    i1: Wire
    i2: Wire
    op: Callable[[int, int], int]
    out: Wire

    def __str__(self) -> str:
        return f"{self.i1.name} {self.op} {self.i2.name} -> {self.out.name}"


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
        opmap = {"A": AND, "O": OR, "X": XOR}
        return Circuit(
            [
                Gate(wires[i1], wires[i2], opmap[op[0]], wires[out])
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


def prob_1(data: list[str]) -> int:
    pass


def prob_2(data: list[str]) -> int:
    c = Circuit.parse(data)

    c.wires["x01"]


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
