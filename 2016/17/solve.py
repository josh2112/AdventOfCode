"""https://adventofcode.com/2016/day/17"""

import argparse
import time
from hashlib import md5
import heapq

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2

DIRS = [(b"U", (0, -1)), (b"D", (0, 1)), (b"L", (-1, 0)), (b"R", (1, 0))]


def neighbors(p0, valid, bounds):
    for i in [i for i in range(4) if valid[i]]:
        if (
            (p1 := (p0[0] + DIRS[i][1][0], p0[1] + DIRS[i][1][1]))
            and 0 <= p1[0] < bounds[0]
            and 0 <= p1[1] < bounds[1]
        ):
            yield DIRS[i][0], p1


def valid_dirs(d: bytes) -> tuple[bool, bool, bool, bool]:
    h0, h1 = md5(d).digest()[:2]
    return h0 >= 0xB0, (h0 & 0xF) >= 0xB, h1 >= 0xB0, (h1 & 0xF) >= 0xB


def solve(start, end, bounds, passcode: str, do_longest: bool = False):
    print(f"Passcode: {passcode}")

    # steps, pos, passcode
    q = [(0, start, passcode.encode())]

    longest_path = 0

    while q:
        c0, p0, pc0 = heapq.heappop(q)

        if p0 == end:
            if do_longest:
                longest_path = max(c0, longest_path)
                continue
            else:
                return pc0[len(passcode.encode()) :].decode()

        for k, p1 in neighbors(p0, valid_dirs(pc0), bounds):
            heapq.heappush(q, (c0 + 1, p1, pc0 + k))

    return longest_path


def prob_1(data: list[str]) -> int:
    return solve((0, 0), (3, 3), (4, 4), data[0])


def prob_2(data: list[str]) -> int:
    return solve((0, 0), (3, 3), (4, 4), data[0], do_longest=True)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 17.")
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
