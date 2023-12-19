#!/usr/bin/env python3

import functools
import re
import time
import math
import typing
from dataclasses import dataclass

# https://adventofcode.com/2023/day/19

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


@dataclass
class Part:
    vals: dict[str, int]


@dataclass
class Rule:
    var: str
    op: str
    value: int
    dest: str

    # Checks the appropriate part value against this rule
    def matches(self, part: Part):
        return (
            part.vals[self.var] < self.value
            if self.op == "<"
            else part.vals[self.var] > self.value
        )

    def __repr__(self) -> str:
        return f"{self.var} {self.op} {self.value} : {self.dest}"

    # Convert the rule to a range. e.g. a > 4 with range(0,10) => range(5,10)
    def to_range(self, rng: range):
        if self.op == "<":
            return range(rng.start, self.value)
        if self.op == "<=":
            return range(rng.start, self.value + 1)
        if self.op == ">=":
            return range(self.value, rng.stop)
        return range(self.value + 1, rng.stop)


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    fallback: str

    @staticmethod
    def parse(line: str):
        m = typing.cast(re.Match[str], re.match(r"(\w+){(.*),(\w+)}", line))
        rules = [
            Rule(m[1], m[2], int(m[3]), m[4])
            for m in re.finditer(r"(\w+)([<>])(\d+):(\w+)", m[2])
        ]
        return Workflow(m[1], rules, m[3])


def parse(data: list[str]) -> tuple[dict[str, Workflow], list[Part]]:
    sep = data.index("")
    wfs = [Workflow.parse(line) for line in data[:sep]]
    return {w.name: w for w in wfs}, [
        Part({m[1]: int(m[2]) for m in re.finditer(r"(\w+)=(\d+)", line)})
        for line in data[sep + 1 :]
    ]


# Intersects 2 ranges, e.g. range(0,5) & range(3,9) => range(3,5)
def range_intersect(x: range, y: range) -> range:
    return range(max(x[0], y[0]), min(x[-1], y[-1]) + 1)


class PathsToA:
    def __init__(self, workflows: dict[str, Workflow]):
        self.paths: list[list[Rule]] = []
        self.ranges: list[dict[str, range]] = []
        self.workflows = workflows

    # Starting with the "in" workflow, finds all the series of rules to follow that will
    # get us to "A".
    def build_paths(self):
        self._build_path(self.workflows["in"], [])

    def _build_path(self, wf: Workflow, path: list[Rule]):
        for r in wf.rules:
            if r.dest == "A":
                self.paths.append(path + [r])
            elif r.dest != "R":
                self._build_path(self.workflows[r.dest], path + [r])
            # invert the rule...
            path = path + [Rule(r.var, "<=" if r.op == ">" else ">=", r.value, "")]
        if wf.fallback == "A":
            self.paths.append(path)
        elif wf.fallback != "R":
            self._build_path(self.workflows[wf.fallback], path)

    # Given a range, figures out the valid ranges for each variable for each path.
    def build_ranges(self, rng: range):
        for p in self.paths:
            ranges: dict[str, range] = {}
            for var in "xmas":
                ranges[var] = functools.reduce(
                    range_intersect, [r.to_range(rng) for r in p if r.var == var], rng
                )
            self.ranges.append(ranges)


def prob_1(data: list[str]):
    workflows, parts = parse(data)

    accepted: list[Part] = []
    for p in parts:
        wf = "in"
        while wf not in ("A", "R"):
            wf = next(
                (r.dest for r in workflows[wf].rules if r.matches(p)),
                workflows[wf].fallback,
            )
        if wf == "A":
            accepted.append(p)
    return sum(sum(p.vals.values()) for p in accepted)


def prob_2(data: list[str]):
    workflows, _ = parse(data)
    builder = PathsToA(workflows)

    rng = range(1, 10 + 1) if ".ex2." in INPUT else range(1, 4000 + 1)

    builder.build_paths()
    # print("\n".join(str(p) for p in builder.paths))
    builder.build_ranges(rng)
    # print("\n".join(str(r) for r in builder.ranges))

    return sum(math.prod(len(r) for r in spec.values()) for spec in builder.ranges)


def main():
    with open(INPUT or "input.txt", mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
