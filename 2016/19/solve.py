"""https://adventofcode.com/2016/day/19"""

import argparse
import time
from dataclasses import dataclass

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


@dataclass
class Elf:
    idx: int
    next: "Elf"


def white_elephant_adj(num_elves: int) -> int:
    elves = [Elf(i + 1, None) for i in range(num_elves)]
    elf_count = len(elves)
    for i in range(elf_count - 1):
        elves[i].next = elves[i + 1]
    elves[-1].next = elves[0]

    e = elves[0]

    while elf_count > 1:
        e.next = e.next.next
        elf_count -= 1
        e = e.next

    return e.idx


def white_elephant_2_opp(num_elves: int) -> int:
    elves = [i + 1 for i in range(num_elves)]
    elfcnt = len(elves)
    i0 = 0

    for _ in range(elfcnt - 1):
        i1 = ((elfcnt >> 1) + i0) % elfcnt
        # print(f"elf {elves[i0]} takes present(s) from elf {elves[i1]}")
        elves.remove(elves[i1])
        elfcnt -= 1
        i0 = (i0 + (1 if i1 > i0 else 0)) % elfcnt

    return elves[0]


def prob_1(data: list[str]) -> int:
    return white_elephant_adj(int(data[0]))


def prob_2(data: list[str]) -> int:
    for i in range(1, 300):
        print(f"{i}: {white_elephant_2_opp(i)}")
    # return white_elephant_2_opp(int(data[0]))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 19.")
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
