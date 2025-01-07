"""https://adventofcode.com/2022/day/16"""

import argparse
import re
import time
from dataclasses import dataclass, field
from sys import maxsize

# Input file path (default is "input.txt")
INPUT, TIME = "input.txt", 30
# INPUT, TIME = "input.ex.txt", 30
# INPUT, TIME = "input.ex2.txt", 8

# Part to solve, 1 or 2
PART = 2


@dataclass(frozen=True)
class Valve:
    name: str
    rate: int = field(compare=False)
    neighbors: list[str] = field(compare=False)


def parse(data: list[str]):
    for line in data:
        name, rate, neighbors = re.match(
            r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]*)",
            line,
        ).groups()
        yield Valve(name, int(rate), neighbors.split(", "))


def dist_graph(valves):
    dist = {v: {v: maxsize for v in valves.values()} for v in valves.values()}
    for v in valves.values():
        dist[v][v] = 0
        for n in v.neighbors:
            dist[v][valves[n]] = 1

    for n in valves.values():
        for i in valves.values():
            for j in valves.values():
                dist[i][j] = min(dist[i][j], dist[i][n] + dist[n][j])

    return dist


def prob_1(data: list[str], time: int) -> int:
    valves = {v.name: v for v in parse(data)}
    dist = dist_graph(valves)

    def explore(v0, t0, pressure, valves_remaining):
        if not valves_remaining or t0 < 2:
            return pressure
        best = 0
        for v1 in valves_remaining:
            t1 = t0 - dist[v0][v1] - 1
            best = max(
                best,
                explore(v1, t1, pressure + v1.rate * t1, valves_remaining - {v1}),
            )
        return best

    return explore(valves["AA"], time, 0, {v for v in valves.values() if v.rate > 0})


@dataclass
class ValveNode:
    valve: Valve
    prev: "ValveNode | None"


def prob_2(data: list[str], total_time: int) -> int:
    valves = {v.name: v for v in parse(data)}
    dist = dist_graph(valves)
    total_time -= 4

    # I don't think we can take a recursive approach because the elephant and
    # human will be activating different valves at different times. So...
    # - Build a list of possible paths for the human, using no more than half the available valves
    # - For each human path, build a list of possible paths for the elephant, using the leftover valves
    # - For each human/elephant path combo, calculate total pressure released keeping the biggest

    nonzero_valves = {v for v in valves.values() if v.rate > 0}

    h_paths = []

    def build_paths(
        vn0: ValveNode,
        t0: int,
        valves_remaining: set[Valve],
        paths_list=None,
        size_limit: int | None = None,
        length: int = 0,
    ):
        # The valves we can get to before running out of time
        v1set = [v1 for v1 in valves_remaining if dist[vn0.valve][v1] + 1 < t0]
        if not v1set or (size_limit and length == size_limit):
            # If limited by time or size, build & return the path
            path = []
            ptr = vn0
            while ptr:
                path.append(ptr.valve)
                ptr = ptr.prev
            paths_list.append([p for p in reversed(path)])
            return

        # Peel off a new path for each of the remaining nodes
        for v1 in v1set:
            vn1 = ValveNode(v1, vn0)
            build_paths(
                vn1,
                t0 - dist[vn0.valve][v1] - 1,
                valves_remaining - {v1},
                paths_list,
                size_limit,
                length + 1,
            )

    def calc_path_pressure(path: list[Valve]) -> int:
        """Returns total pressure released by taking this path"""
        t, p = total_time, 0
        for a, b in zip(path, path[1:]):
            t -= dist[a][b] + 1
            p += b.rate * t
        return p

    # Build possible human paths, using no more than half the valves
    build_paths(
        ValveNode(valves["AA"], None),
        total_time,
        nonzero_valves,
        h_paths,
        len(nonzero_valves) / 2,
    )

    best = 0

    for h_path in h_paths:
        h_pressure = calc_path_pressure(h_path)
        # Build possible elephant paths using remaining nonzero valves
        e_paths = []
        build_paths(
            ValveNode(valves["AA"], None),
            total_time,
            nonzero_valves - set(h_path),
            e_paths,
        )
        e_max_pressure = max(
            (calc_path_pressure(e_path) for e_path in e_paths), default=0
        )
        if h_pressure + e_max_pressure > best:
            best = h_pressure + e_max_pressure
            e_path = next(x for x in e_paths if calc_path_pressure(x) == e_max_pressure)
            print(
                f"New best: {best}: {' '.join( v.name for v in h_path)}, {' '.join( v.name for v in e_path)}"
            )

    return best


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2022 day 16.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    parser.add_argument("-t", "--time", default=TIME)
    args = parser.parse_args()
    part, infile, total_time = args.part, args.input, args.time

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data, total_time)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data, total_time)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
