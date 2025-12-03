"""https://adventofcode.com/2025/day/3"""

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def max_joltage(bank: str, count: int) -> int:
    # Pick highest digit in the window between last digit chosen (or start) and first len(bank)-count+1 chars
    # Repeat 'till full
    result = []
    a, b = 0, len(bank) - count + 1
    while len(result) < count:
        result.append(max(bank[a:b]))
        i = bank[a:b].index(result[-1]) + a
        a = i + 1
        b += 1
    return int("".join(result))


def prob_1(data: list[str]) -> int:
    return sum(max_joltage(bank, 2) for bank in data)


def prob_2(data: list[str]) -> int:
    return sum(max_joltage(bank, 12) for bank in data)


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
