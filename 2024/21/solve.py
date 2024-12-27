"""https://adventofcode.com/2024/day/21"""

import argparse
import heapq
import itertools
import time
from collections import defaultdict
from functools import cache

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2

DIRS = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}


def neighbors(p):
    for symbol, delta in DIRS.items():
        yield (p[0] + delta[0], p[1] + delta[1]), symbol


@cache
def best_paths(grid, start, end):
    q = [(0, start, [])]  # cost, cur, path
    w, h = len(grid[0]), len(grid)

    best_cost = abs(end[1] - start[1]) + abs(end[0] - start[0])
    best_paths = []

    while q:
        c, p, path = heapq.heappop(q)
        if c >= best_cost and p != end:
            continue
        if p == end:
            best_paths.append(path + ["A"])
            continue
        for p1, d1 in neighbors(p):
            if (0 <= p1[0] < w) and (0 <= p1[1] < h) and grid[p1[1]][p1[0]] != " ":
                heapq.heappush(q, (c + 1, p1, path + [d1]))

    return best_paths


def prob_1(data: list[str]) -> int:
    grid_door = ("789", "456", "123", " 0A")
    grid_bot = (" ^A", "<v>")

    keymap_door, keymap_bot = tuple(
        {c: (x, y) for y, row in enumerate(kp) for x, c in enumerate(row)}
        for kp in (grid_door, grid_bot)
    )

    complexity = 0

    for code in data:
        totalseq = ""

        for kp_move in zip(["A"] + [x for x in code], code):
            minseq = None
            for p in best_paths(
                grid_door, keymap_door[kp_move[0]], keymap_door[kp_move[1]]
            ):
                p2 = [
                    best_paths(grid_bot, keymap_bot[pr[0]], keymap_bot[pr[1]])
                    for pr in zip(["A"] + p, p)
                ]
                p3_minseq = None
                for p2ex in itertools.product(*p2):
                    # print("  ", "".join(x for a in combo for x in a))
                    p2ex = [x for a in p2ex for x in a]
                    p3 = [
                        best_paths(grid_bot, keymap_bot[pr[0]], keymap_bot[pr[1]])
                        for pr in zip(["A"] + p2ex, p2ex)
                    ]
                    p3_seq = [
                        [x for a in p3ex for x in a] for p3ex in itertools.product(*p3)
                    ]
                    x = min(len(x) for x in p3_seq)
                    if not p3_minseq or x < len(p3_minseq):
                        p3_minseq = p3_seq[0]
                if not minseq or len(p3_minseq) < len(minseq):
                    minseq = p3_minseq
            totalseq += "".join(minseq)

        print(code, ": ", totalseq, len(totalseq))
        complexity += len(totalseq) * int(code[:-1])
    return complexity


def calc_next_level_seqs(p2_seq, grid_bot, keymap_bot):
    p3_seqs = []
    for p2ex in p2_seq:
        p3 = [
            best_paths(grid_bot, keymap_bot[pr[0]], keymap_bot[pr[1]])
            for pr in zip(["A"] + p2ex, p2ex)
        ]
        length = sum(len(x[0]) if x else 0 for x in p3)
        if not p3_seqs or length < len(p3_seqs[0]):
            p3_seqs = [[x for a in p3ex for x in a] for p3ex in itertools.product(*p3)]
    return p3_seqs


# TODO: This is all a mess
def prob_2(data: list[str]) -> int:
    grid_door = ("789", "456", "123", " 0A")
    grid_bot = (" ^A", "<v>")

    keymap_door, keymap_bot = tuple(
        {c: (x, y) for y, row in enumerate(kp) for x, c in enumerate(row)}
        for kp in (grid_door, grid_bot)
    )

    complexity = 0

    for code in data:
        totalseq = ""

        p0_seq = [
            [kp_move[0], kp_move[1]] for kp_move in zip(["A"] + [x for x in code], code)
        ]
        for s in p0_seq:
            print("".join(s))

        p1_seq = calc_next_level_seqs(p0_seq, grid_door, keymap_door)
        for s in p1_seq:
            print("".join(s))
        continue

        p1 = [
            best_paths(grid_door, keymap_door[kp_move[0]], keymap_door[kp_move[1]])
            for kp_move in zip(["A"] + [x for x in code], code)
        ]
        # p1_seq = Shortest possible valid sequences for typing the door code
        p1_seq = [[x for a in p1ex for x in a] for p1ex in itertools.product(*p1)]

        p2_seq = calc_next_level_seqs(p1_seq, grid_bot, keymap_bot)

        p3_seq = calc_next_level_seqs(p2_seq, grid_bot, keymap_bot)

        for s in p3_seq:
            print("".join(s))
        return

        for kp_move in zip(["A"] + [x for x in code], code):
            minseq = None
            for p1 in best_paths(
                grid_door, keymap_door[kp_move[0]], keymap_door[kp_move[1]]
            ):
                p2 = [
                    best_paths(grid_bot, keymap_bot[pr[0]], keymap_bot[pr[1]])
                    for pr in zip(["A"] + p1, p1)
                ]
                p2_seq = [
                    [x for a in p2ex for x in a] for p2ex in itertools.product(*p2)
                ]

                p3_minseqs = calc_next_level_seqs(p2_seq, grid_bot, keymap_bot)
                if not minseq or len(p3_minseqs[0]) < len(minseq):
                    minseq = p3_minseqs[0]
            totalseq += "".join(minseq)

        print(code, ": ", totalseq, len(totalseq))
        complexity += len(totalseq) * int(code[:-1])
    return complexity


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 21.")
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
