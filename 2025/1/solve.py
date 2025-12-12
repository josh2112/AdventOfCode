"""https://adventofcode.com/2025/day/1"""

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def prob_1(data: list[str]) -> int:
    d, c = 50, 0
    for ln in data:
        inc = int(ln[1:])
        d = (d + inc) if ln[0] == "R" else (d - inc)
        if not d % 100:
            c += 1
    return c


def prob_2(data: list[str]) -> int:
    d, c, from_zero = 50, 0, False
    for ln in data:
        inc = int(ln[1:])
        c += inc // 100
        inc %= 100
        d = (d + inc) if ln[0] == "R" else (d - inc)
        if not (from_zero or 0 < d < 100):
            c += 1
        d %= 100
        from_zero = not d
    return c


def main() -> float:
    return solve(__file__, PART, INPUT, prob_1, prob_2)


if __name__ == "__main__":
    main()
