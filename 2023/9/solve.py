#!/usr/bin/env python3

import time

# https://adventofcode.com/2023/day/9

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


def predict(data: list[str]):
    result = [0, 0]
    for line in data:
        nums = [[int(i) for i in line.split()]]
        while any(n != 0 for n in nums[-1]):
            # diff pairs
            nums.append(
                [nums[-1][i] - nums[-1][i - 1] for i in range(1, len(nums[-1]))]
            )
        nums[-1].insert(0, 0)
        nums[-1].append(0)
        for i in range(len(nums) - 2, -1, -1):
            nums[i].insert(0, nums[i][0] - nums[i + 1][0])
            nums[i].append(nums[i][-1] + nums[i + 1][-1])
        result[0] += nums[0][0]
        result[1] += nums[0][-1]
    return result


def prob_1(data: list[str]):
    return predict(data)[-1]


def prob_2(data: list[str]):
    return predict(data)[0]


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
