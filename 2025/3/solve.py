"""https://adventofcode.com/2025/day/3"""

from aoclib.runner import solve
import heapq

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def max_joltage(bank: str, cnt: int) -> int:
    indices = []
    sublists = [(0, len(bank))]

    while len(indices) < cnt:
        # Find all indices of the highest number in the rightmost sublist
        a, b = heapq.heappop_max(sublists)
        m = max(bank[a:b])
        found = [i for i in range(a, b) if bank[i] == m]
        # Add as many as needed to fill the result
        indices.extend(found[: cnt - len(indices)])

        # Split list at indices and queue all non-empty sublists
        for i in found + [b]:
            if i > a:
                heapq.heappush_max(sublists, (a, i))
            a = i + 1

    return int("".join(bank[i] for i in sorted(indices)))


def prob_1(data: list[str]) -> int:
    return sum(max_joltage(bank, 2) for bank in data)


def prob_2(data: list[str]) -> int:
    return sum(max_joltage(bank, 12) for bank in data)


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
