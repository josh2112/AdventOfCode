#!/usr/bin/env python3

from dataclasses import dataclass
import time
import re

# https://adventofcode.com/2023/day/23

# Input file path (default is "input.txt")
INPUT = "input.ex2.txt"

# Part to solve, 1 or 2
PART = 1

path_found = []


def walk(path: list[tuple[int, int]], data: list[str], goal: tuple[int, int]):
    global path_found
    while True:
        possibilities = []
        for vec in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            loc = (path[-1][0] + vec[0], path[-1][1] + vec[1])
            nxt = data[loc[1]][loc[0]]
            if loc == goal:
                path.append(loc)
                print("Found path of", len(path) - 1, "steps")
                if not path_found or len(path) > len(path_found):
                    path_found = path
                return
            if loc not in path and (
                nxt == "."
                or (nxt == "^" and vec == (0, -1))
                or (nxt == ">" and vec == (1, 0))
                or (nxt == "v" and vec == (0, 1))
                or (nxt == "<" and vec == (-1, 0))
            ):
                possibilities.append(loc)
        if len(possibilities) > 1:
            for p in possibilities[1:]:
                walk(path + [p], data, goal)
        if possibilities:
            path.append(possibilities[0])
        if not possibilities:
            return


def walk2(path: list[tuple[int, int]], data: list[str], goal: tuple[int, int]):
    global path_found
    while True:
        possibilities = []
        for vec in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            loc = (path[-1][0] + vec[0], path[-1][1] + vec[1])
            nxt = data[loc[1]][loc[0]]
            if loc == goal:
                path.append(loc)
                print("Found path of", len(path) - 1, "steps")
                if not path_found or len(path) > len(path_found):
                    path_found = path
                return
            if loc not in path and (
                nxt
                != "#"
                # nxt == "."
                # or (nxt == "^" and vec == (0, -1))
                # or (nxt == ">" and vec == (1, 0))
                # or (nxt == "v" and vec == (0, 1))
                # or (nxt == "<" and vec == (-1, 0))
            ):
                possibilities.append(loc)
        if len(possibilities) > 1:
            for p in possibilities[1:]:
                walk2(path + [p], data, goal)
        if possibilities:
            path.append(possibilities[0])
        if not possibilities:
            return


@dataclass(frozen=True)
class State:
    pos: tuple[int, int]
    vec: int
    prev: tuple[int, int]


@dataclass(frozen=True)
class Edge:
    p1: tuple[int, int]
    p2: tuple[int, int]


# Figure out the edges. Bidirectional edges will be represented twice.
def build_graph(data: list[str]):
    edges = []
    for y, line in enumerate(data):
        for m in re.finditer(r"([\.<^>v]+)", line):
            span = (m.span(1)[0], m.span(1)[1] - 1)
            if span[0] == span[1]:
                continue
            txt = m.group(1)
            fwd = ">" in txt or "v" in txt
            rev = "<" in txt or "^" in txt
            if fwd or not rev:
                edges.append(((span[0], y), (span[1], y)))
            if rev or not fwd:
                edges.append(((span[1], y), (span[0], y)))

    for x, line in enumerate(list(map(list, zip(*data)))):
        for m in re.finditer(r"([\.<^>v]+)", "".join(line)):
            span = (m.span(1)[0], m.span(1)[1] - 1)
            if span[0] == span[1]:
                continue
            txt = m.group(1)
            fwd = ">" in txt or "v" in txt
            rev = "<" in txt or "^" in txt
            if fwd or not rev:
                edges.append(((x, span[0]), (x, span[1])))
            if rev or not fwd:
                edges.append(((x, span[1]), (x, span[0])))

    return edges


def prob_1(data: list[str]):
    build_graph(data)

    global paths_found
    path = [(1, 0), (1, 1)]
    goal = (len(data[0]) - 2, len(data) - 1)
    walk(path, data, goal)
    return len(path_found) - 1


# TODO: Runs way too slow for an answer. Maybe try building a graph containing just the decision
# points?
def prob_2(data: list[str]):
    global paths_found
    path = [(1, 0), (1, 1)]
    goal = (len(data[0]) - 2, len(data) - 1)
    walk2(path, data, goal)
    return len(path_found) - 1


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
