"""https://adventofcode.com/2017/day/17"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    stepsize = int(data[0])
    buf, i = [0], 0

    for v in range(1, 2018):
        i = (i + stepsize + 1) % len(buf)
        buf.insert(i, v)

    return buf[(i + 1) % len(buf)]


def prob_2(data: list[str]) -> int:
    stepsize = int(data[0])
    buf, i = [0], 0
    i_zero = 0
    tgt = 0

    # Possible approach: We don't care about the contents of the list, we only care about
    # the value after the 0. And that value resets to the current iteration every time an insert
    # is made at its index. So can we store just the length of the list, the index of the post-0
    # value, and the current value of it?

    for v in range(1, 5_000_001):
        i = (i + stepsize + 1) % len(buf)
        buf.insert(i, v)
        if i_zero >= i:
            i_zero += 1
        # print([buf[x % len(buf)] for x in range(i_zero - 1, i_zero + 2)])
        if not v % 10_000 and buf[(i_zero + 1) % len(buf)] != tgt:
            tgt = buf[(i_zero + 1) % len(buf)]
            print(tgt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solves AoC 2017 day 17.")
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
