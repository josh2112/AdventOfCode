#!/usr/bin/env python3
import re
import math

# https://adventofcode.com/2023/day/3

# Input file path, or None for the default, "input.txt"
INPUT = "input.txt"

# Daily problem to solve, 1 or 2
PROBLEM = 2


def prob_1(data: list[str]):
    def process(m: re.Match[str], y: int):
        x0, x1 = m.start(), m.end() - 1
        xmax = len(data[y]) - 1
        # check left, right
        if x0 > 0 and data[y][x0 - 1] != ".":
            return True
        elif x1 < xmax and data[y][x1 + 1] != ".":
            return True
        # check top, bottom rows
        if y > 0:
            for x in range(max(x0 - 1, 0), min(x1 + 1, xmax) + 1):
                if data[y - 1][x] != ".":
                    return True
        if y < len(data) - 1:
            for x in range(max(x0 - 1, 0), min(x1 + 1, xmax) + 1):
                if data[y + 1][x] != ".":
                    return True

    nums = []
    for y in range(len(data)):
        nums.extend(m.group() for m in re.finditer(r"\d+", data[y]) if process(m, y))
    return sum(int(n) for n in nums)


def prob_2(data: list[str]):
    def process_star(x: int, y: int) -> int:
        # Find all the numbers on the 3 surrounding rows
        # Take the ones whose start/end overlap [x-1...x+1]
        # If there are exactly 2, multiply and return
        adjacent_nums = [
            int(m.group())
            for row in range(max(y - 1, 0), min(y + 1, len(data) - 1) + 1)
            for m in re.finditer(r"\d+", data[row])
            if m.start() <= x + 1 and m.end() >= x
        ]
        return math.prod(adjacent_nums) if len(adjacent_nums) == 2 else 0

    return sum(
        process_star(m.start(), y)
        for y in range(len(data))
        for m in re.finditer(r"\*", data[y])
    )


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    print(f"Problem {PROBLEM}")
    print(prob_1(data) if PROBLEM == 1 else prob_2(data))


if __name__ == "__main__":
    main()
