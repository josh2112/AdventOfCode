"""https://adventofcode.com/2017/day/21"""

import argparse
import time
from collections.abc import Generator
from functools import cache
from math import sqrt

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 1


ROTFLIP2_PERMS = (
    (0, 1, 2, 3),
    (0, 2, 1, 3),
    (1, 0, 3, 2),
    (1, 3, 0, 2),
    (2, 0, 3, 1),
    (2, 3, 0, 1),
    (3, 1, 2, 0),
    (3, 2, 1, 0),
)
ROTFLIP3_PERMS = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8),
    (0, 3, 6, 1, 4, 7, 2, 5, 8),
    (2, 1, 0, 5, 4, 3, 8, 7, 6),
    (2, 5, 8, 1, 4, 7, 0, 3, 6),
    (6, 3, 0, 7, 4, 1, 8, 5, 2),
    (6, 7, 8, 3, 4, 5, 0, 1, 2),
    (8, 5, 2, 7, 4, 1, 6, 3, 0),
    (8, 7, 6, 5, 4, 3, 2, 1, 0),
)


def subdivide(art: str) -> Generator[str]:
    w = int(sqrt(len(art)))

    if w == 2 or w == 3:
        yield tuple(art)
    elif not (w % 2):
        for y in range(0, w, 2):
            for x in range(0, w, 2):
                base = y * w + x
                yield tuple(
                    [
                        art[base],
                        art[base + 1],
                        art[base + w],
                        art[base + w + 1],
                    ]
                )
    elif not (w % 3):
        for y in range(0, w, 3):
            for x in range(0, w, 3):
                base = y * w + x
                yield tuple(
                    [
                        art[base],
                        art[base + 1],
                        art[base + 2],
                        art[base + w],
                        art[base + w + 1],
                        art[base + w + 2],
                        art[base + w + w],
                        art[base + w + w + 1],
                        art[base + w + w + 2],
                    ]
                )


def rotflip(art: str) -> Generator[list[str]]:
    for perm in ROTFLIP2_PERMS if len(art) == 4 else ROTFLIP3_PERMS:
        yield [art[x] for x in perm]


def combine(subart: list[str]):
    if len(subart) == 1:
        return subart[0]
    sw = int(sqrt(len(subart)))
    bw = int(sqrt(len(subart[0])))
    art = []
    for sy in range(0, len(subart), sw):
        for by in range(bw):
            for sx in range(sw):
                art += subart[sy + sx][by * bw : by * bw + bw]
    return art


def run(data: list[str], rounds: int) -> int:
    book = {k: v for k, v in (line.replace("/", "").split(" => ") for line in data)}

    @cache
    def enhance(art: str):
        for k in rotflip(art):
            if v := book.get("".join(k), None):
                return v
        print(f"** No enhancement for {art}!")

    art = ".#...####"

    for i in range(rounds):
        subart = list(subdivide(art))
        subart = [enhance(a) for a in subart]
        art = combine(subart)

    return art.count("#")


def prob_1(data: list[str]) -> int:
    return run(data, 5)


def prob_2(data: list[str]) -> int:
    return run(data, 18)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 21.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
