"""https://adventofcode.com/2018/day/12"""

from collections import deque

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def do_gen(s: str, si: int, rules: list[tuple[str, ...]]) -> tuple[str, int]:
    if not s.startswith("....."):
        s = "....." + s
        si -= 5
    if not s.endswith("....."):
        s = s + "....."

    s2 = ["." for _ in range(len(s))]

    for i in range(len(s) - 5):
        span = "".join(s[i : i + 5])
        r = next((r for r in rules if r[0] == span), None)
        if r:
            s2[i + 2] = "#"

    return "".join(s2), si


def prob_1(data: list[str]) -> int:
    s, si = data[0][15:], 0
    rules = [tuple(ln.split(" => ")) for ln in data[2:] if ln[-1] == "#"]

    for _ in range(20):
        s, si = do_gen(s, si, rules)

    return sum(i + si for i, p in enumerate(s) if p == "#")


def prob_2(data: list[str]) -> int:
    s, si = data[0][15:], 0
    rules = [tuple(ln.split(" => ")) for ln in data[2:] if ln[-1] == "#"]

    # One of those AoC problems that's impossible to calculate but there's a
    # pattern you have to find. In this case the sums very quickly become
    # linear.

    cnt = 0
    prev_sums: deque[int] = deque(maxlen=20)

    while True:
        cnt += 1
        s, si = do_gen(s, si, rules)
        prev_sums.append(sum(i + si for i, p in enumerate(s) if p == "#"))

        # Look for 20 sums in a row that all differ by the same amount
        if len(prev_sums) == 20:
            delta = [prev_sums[i] - prev_sums[i - 1] for i in range(1, len(prev_sums))]
            if all(d == delta[0] for d in delta):
                # Project from there to 50 billion
                return prev_sums.pop() + delta[0] * (50_000_000_000 - cnt)

    return -1


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
