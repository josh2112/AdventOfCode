"""https://adventofcode.com/2016/day/10"""

import argparse
import time
import math

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def run(data: list[str], chip_search=None):
    bots, outputs = {}, {}

    # Fill bots from the input bins first
    for line in [ln for ln in data if ln[0] == "v"]:
        tk = line.split()
        bot, value = int(tk[-1]), int(tk[1])
        bots.setdefault(bot, []).append(value)

    # Parse instructions
    # bot -> (low, low_is_output, high, high_is_output)
    instrs_by_bot = {}
    for line in [ln for ln in data if ln[0] == "b"]:
        tk = line.split()
        instrs_by_bot[int(tk[1])] = (
            int(tk[6]),
            tk[5][0] == "o",
            int(tk[-1]),
            tk[-2][0] == "o",
        )

    # Start with the instructions for any bots with 2 values
    q = [(b, instrs_by_bot[b]) for b in bots if len(bots[b]) == 2]
    while q:
        bot, (low, low_is_output, high, high_is_output) = q.pop(0)

        if sorted(bots[bot]) == chip_search:
            return bot

        (outputs if low_is_output else bots).setdefault(low, []).append(min(bots[bot]))
        (outputs if high_is_output else bots).setdefault(high, []).append(
            max(bots[bot])
        )
        bots[bot].clear()
        del instrs_by_bot[bot]

        # Queue up the instructions for any other bots which now have 2 values
        if not low_is_output and len(bots[low]) == 2:
            q.append((low, instrs_by_bot[low]))
        if not high_is_output and len(bots[high]) == 2:
            q.append((high, instrs_by_bot[high]))

    return outputs


def prob_1(data: list[str]) -> int:
    return run(data, [17, 61])  # example: [2, 5]


def prob_2(data: list[str]) -> int:
    outputs = run(data)
    return math.prod(outputs[i][0] for i in range(3))


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2016 day 10.")
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
