"""https://adventofcode.com/2024/day/11"""

import argparse
import time

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    stones = data[0].split()

    for n in range(25):
        i = 0
        while i < len(stones):
            if stones[i] == "0":
                stones[i] = "1"
                i += 1
            elif not (len(stones[i]) % 2):
                v = stones[i]
                stones[i] = str(int(v[: len(v) // 2]))
                stones.insert(i + 1, str(int(v[len(v) // 2 :])))
                i += 2
            else:
                stones[i] = str(int(stones[i]) * 2024)
                i += 1

        print(f"{n+1}: {len(stones)}")
        if n < 5:
            print(" ".join(stones))

    return len(stones)


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


"""
i: num stones
1: 11
2: 15
3: 20
4: 35
5: 52
6: 78
7: 126
8: 178
9: 254
10: 415
11: 660
12: 967
13: 1406
14: 2185
15: 3411
16: 5017
17: 7689
18: 11739
19: 17556
20: 26894
21: 40984
22: 62552
23: 94101
24: 141879
25: 218956
"""


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2024 day 11.")
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
