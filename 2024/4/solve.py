"""https://adventofcode.com/2024/day/4"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def find_xmas(data: list[str], x: int, y: int, dx: int, dy: int):
    return (
        data[x + dx][y + dy] == "M"
        and data[x + dx * 2][y + dy * 2] == "A"
        and data[x + dx * 3][y + dy * 3] == "S"
    )


def find_x_mas(data: list[str], x: int, y: int):
    return (
        (data[x - 1][y - 1] == "M" and data[x + 1][y + 1] == "S")
        or (data[x - 1][y - 1] == "S" and data[x + 1][y + 1] == "M")
    ) and (
        (data[x - 1][y + 1] == "M" and data[x + 1][y - 1] == "S")
        or (data[x - 1][y + 1] == "S" and data[x + 1][y - 1] == "M")
    )


def prob_1(data: list[str]) -> int:
    data = (
        ["." * (len(data[0]) + 2)]
        + ["." + line + "." for line in data]
        + ["." * (len(data[0]) + 2)]
    )
    count = 0
    for y in range(1, len(data[0]) - 1):
        for x in range(1, len(data) - 1):
            if data[x][y] != "X":
                continue
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if find_xmas(data, x, y, dx, dy):
                        count += 1
    return count


def prob_2(data: list[str]) -> int:
    count = 0
    for y in range(1, len(data[0]) - 1):
        for x in range(1, len(data) - 1):
            if data[x][y] == "A" and find_x_mas(data, x, y):
                count += 1
    return count


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 4.")
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
