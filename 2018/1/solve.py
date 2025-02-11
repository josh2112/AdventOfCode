"""https://adventofcode.com/2018/day/1"""

from aoclib.runner import solve

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    return sum(int(line) for line in data)


def prob_2(data: list[str]) -> int:
    freqs = [int(line) for line in data]
    seen = set()
    freq = 0
    while True:
        for f in freqs:
            freq += f
            if freq in seen:
                return freq
            seen.add(freq)


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
