"""https://adventofcode.com/2023/day/14"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def roll_west(data: list[list[str]]):
    for line in data:
        stop_point = 0
        for x, c in enumerate(line):
            if c == "O":
                if stop_point < x:
                    line[stop_point] = "O"
                    line[x] = "."
                stop_point += 1
            elif c == "#":
                stop_point = x + 1


def roll_east(data: list[list[str]]):
    for line in data:
        stop_point = len(line) - 1
        for x in range(len(line) - 1, -1, -1):
            if line[x] == "O":
                if stop_point > x:
                    line[stop_point] = "O"
                    line[x] = "."
                stop_point -= 1
            elif line[x] == "#":
                stop_point = x - 1


def prob_1(data: list[str]):
    # 1) transpose so that west is north
    d = list(map(list, zip(*data)))
    roll_west(d)
    # 2) transpose back
    d = list(map(list, zip(*d)))
    load = 0
    for y, line in enumerate(d):
        load += sum(len(data) - y for c in line if c == "O")
    return load


def cycle(d: list[list[str]]):
    # north
    d = list(map(list, zip(*d)))
    roll_west(d)
    d = list(map(list, zip(*d)))

    roll_west(d)

    # south
    d = list(map(list, zip(*d)))
    roll_east(d)
    d = list(map(list, zip(*d)))

    roll_east(d)
    return d


def difference(d: list[list[str]], d2: list[list[str]]):
    return sum(
        sum(0 if d[y][x] == d2[y][x] else 1 for x in range(len(d[0])))
        for y in range(len(d))
    )


def load(d: list[list[str]]):
    ld = 0
    for y, line in enumerate(d):
        ld += sum(len(d) - y for c in line if c == "O")
    return ld


def find_cycle(arr: list) -> tuple[int, int]:
    for width in range(2, len(arr) // 2):
        for i in range(0, len(arr) - 2, 2):
            if arr[i : i + width] == arr[i + width : i + width * 2]:
                return i, width
    return 0, 0


def predict_from_cycle(arr: list, index: int, offset: int, width: int):
    return arr[((index - offset) % width) + offset]


def prob_2(data: list[str]):
    d = list(map(list, data))
    loads = [load(d)]
    for _ in range(200):
        d = cycle(d)
        loads.append(load(d))
    offset, width = find_cycle(loads)
    return predict_from_cycle(loads, 1000000000, offset, width) if width > 0 else 0


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 14.")
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
