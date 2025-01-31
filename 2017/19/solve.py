"""https://adventofcode.com/2017/day/19"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 1


def traverse(data: list[str], part2: bool = False) -> int:
    path, steps = [], 0
    p, d = (data[0].index("|"), 0), (0, 1)

    def get(p):
        try:
            return p1 if (p1 := data[p[1]][p[0]]) != " " else None
        except:  # noqa: E722
            return None

    while p := (p[0] + d[0], p[1] + d[1]):
        steps += 1
        match get(p):
            case c if c and str.isalpha(c):
                path.append(c)
            case "+":
                d = next(
                    d1
                    for d1 in ((0, 1), (1, 0), (0, -1), (-1, 0))
                    if d1 != (-d[0], -d[1]) and get((p[0] + d1[0], p[1] + d1[1]))
                )
            case None:
                break

    return steps if part2 else "".join(path)


def prob_1(data: list[str]) -> int:
    return traverse(data)


def prob_2(data: list[str]) -> int:
    return traverse(data, part2=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 19.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()

    with open(args.input, mode="r", encoding="utf-8") as f:
        data = [line[:-1] for line in f.readlines()]

    start = time.perf_counter()
    if args.part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if args.part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    print(f"Time: {time.perf_counter() - start} s")
