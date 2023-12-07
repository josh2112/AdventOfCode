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


# for x in each possible hold-down-button length:
# dist = (race.time - x) * x
# 0 = - x^2 + (race.time * x) - dist
# quadratic equation with a = -1, b = race.time, c = -dist


def solve_quad(a: float, b: float, c: float):
    discr = math.sqrt(b * b - 4 * a * c)
    return ((-b + discr) / (2 * a), (-b - discr) / (2 * a))


def solve_races(races: list[Race]):
    num_ways = []
    for race in races:
        crossings = solve_quad(-1, race.time, -race.dist)
        num_ways.append(
            (crossings[1] - 1 if crossings[1] == int(crossings[1]) else math.floor(crossings[1]))
            - (crossings[0] + 1 if crossings[0] == int(crossings[0]) else math.ceil(crossings[0]))
            + 1
        )
    return int(math.prod(num_ways))


def prob_1(data: list[str]):
    data2 = [line.split()[1:] for line in data]
    return solve_races(Race(int(data2[0][i]), int(data2[1][i])) for i in range(len(data2[0])))


def prob_2(data: list[str]):
    t, d = [int(line.split(":")[1].replace(" ", "")) for line in data]
    return solve_races([Race(t, d)])


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
