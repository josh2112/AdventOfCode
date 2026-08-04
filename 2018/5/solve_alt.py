"""https://adventofcode.com/2018/day/5"""

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def react(polymer: str):
    d, i = [ord(c) for c in polymer], 0
    total, start = 0, 0

    while i < len(d) - 1:
        if abs(d[i] - d[i + 1]) == 32:
            j = i + 1
            while abs(d[i] - d[j]) == 32 and i > 0 and j < len(d) - 1:
                i, j = i - 1, j + 1
            if j == len(d) - 1:
                break
            else:
                total += i - start
                i, j = j + 1, j + 2
        else:
            i += 1
    return len(d)


def prob_1(data: list[str]) -> int:
    return react(data[0])


def prob_2(data: list[str]) -> int:
    min_len = len(data[0])
    for i in range(ord("a"), ord("z") + 1):
        polymer = [c for c in data[0] if ord(c) not in (i, i - 32)]
        length = react(polymer)
        print(f"{chr(i)}: count={len(data[0]) - len(polymer)}, length={length}")
        min_len = min(min_len, length)
    return min_len


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
