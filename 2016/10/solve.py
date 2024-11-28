"""https://adventofcode.com/2016/day/10"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


# TODO: This is all wrong. A bot instruction is not followed until the bot contains
# 2 chips. Need to either
# 1) execute the instruction set over and over in a loop until all instructions are used, or
# 2) index each instruction to its bot, and trigger it to be executed once the bot gains 2 chips
def prob_1(data: list[str]) -> int:
    bots, outputs = {}, {}
    for line in [ln for ln in data if ln[0] == "v"]:
        tk = line.split()
        bot, value = int(tk[-1]), int(tk[1])
        bots.setdefault(bot, []).append(value)
    for line in [ln for ln in data if ln[0] == "b"]:
        tk = line.split()
        bot, low, low_is_output, high, high_is_output = (
            int(tk[1]),
            int(tk[6]),
            tk[5][0] == "o",
            int(tk[-1]),
            tk[-2][0] == "o",
        )
        if bots.setdefault(bot, []) == []:
            continue
        if sorted(bots[bot]) == [17, 61]:  # example: [2, 5]
            return bot
        (outputs if low_is_output else bots).setdefault(low, []).append(min(bots[bot]))
        (outputs if high_is_output else bots).setdefault(high, []).append(
            max(bots[bot])
        )
        bots[bot].clear()

    print("outputs =", outputs)
    print("bots =", bots)
    return 0


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


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
