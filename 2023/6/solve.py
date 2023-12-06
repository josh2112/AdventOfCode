#!/usr/bin/env python3

from dataclasses import dataclass
import math
import time

# https://adventofcode.com/2023/day/6

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


@dataclass
class Race:
    time: int
    dist: int


def prob_1(data: list[str]):
    data2 = [line.split()[1:] for line in data]
    races = [Race(int(data2[0][i]), int(data2[1][i])) for i in range(len(data2[0]))]
    num_ways = []
    for race in races:
        i0, i1 = -1, -1
        for t in range(1, race.time):
            dist = (race.time - t) * t
            if dist > race.dist:
                i0 = t
                break
        for t in range(race.time - 1, 1, -1):
            dist = (race.time - t) * t
            if dist > race.dist:
                i1 = t
                break
        num_ways.append(i1 - i0 + 1)
    return math.prod(num_ways)


def prob_2(data: list[str]):
    time, dist = [int(line.split(":")[1].replace(" ", "")) for line in data]
    i0, i1 = -1, -1
    for t in range(1, time):
        d = (time - t) * t
        if d > dist:
            i0 = t
            break
    for t in range(time - 1, 1, -1):
        d = (time - t) * t
        if d > dist:
            i1 = t
            break
    return i1 - i0 + 1


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
