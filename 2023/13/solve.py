"""https://adventofcode.com/2023/day/13"""

import argparse
import time
import itertools

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def find_reflection(data: list[str], is_prob2: bool):
    for pr in itertools.pairwise(range(len(data))):
        x0, x1 = pr
        diffs = []
        while x0 >= 0 and x1 < len(data):
            diffs.append(sum(0 if p[0] == p[1] else 1 for p in zip(data[x0], data[x1])))
            if diffs[-1] > 1:
                diffs = []
                break
            x0 -= 1
            x1 += 1
        if not is_prob2 and diffs and sum(diffs) == 0:
            return pr[0] + 1
        if is_prob2 and diffs and sum(diffs) == 1:
            return pr[0] + 1
    return 0


def find_reflections(data: list[str], is_prob2: bool):
    vert = find_reflection(data, is_prob2)
    horiz = find_reflection(list(map(list, zip(*data))), is_prob2)  # type: ignore
    return vert * 100 + horiz


def parse(data: list[str]):
    seps = [-1] + [i for i, d in enumerate(data) if not d] + [len(data)]
    return [data[pr[0] + 1 : pr[1]] for pr in itertools.pairwise(seps)]


def prob_1(data: list[str]):
    return sum(find_reflections(b, False) for b in parse(data))


def prob_2(data: list[str]):
    return sum(find_reflections(b, True) for b in parse(data))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 13.")
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
