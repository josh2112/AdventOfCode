"""https://adventofcode.com/2018/day/2"""

from collections import Counter
from itertools import combinations

from aoclib.runner import solve

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1


def prob_1(data: list[str]) -> int:
    n2, n3 = 0, 0
    for line in data:
        counts = Counter(line).values()
        n2 += 1 if 2 in counts else 0
        n3 += 1 if 3 in counts else 0
    return n2 * n3


def prob_2(data: list[str]) -> int:
    for a, b in combinations(data, r=2):
        if sum(diff := [1 if a[i] != b[i] else 0 for i in range(len(a))]) == 1:
            return "".join(a[i] for i in range(len(a)) if diff[i] == 0)


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
