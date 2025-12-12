"""https://adventofcode.com/2025/day/4"""

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def hashify(data: list[str]):
    return {
        (x, y) for y, line in enumerate(data) for x, c in enumerate(line) if c == "@"
    }


def prob_1(data: list[str]) -> int:
    rolls = hashify(data)
    kernel = {(x, y) for y in (-1, 0, 1) for x in (-1, 0, 1)}.difference({(0, 0)})
    return sum(
        1 for x, y in rolls if sum((x + dx, y + dy) in rolls for dx, dy in kernel) < 4
    )


def prob_2(data: list[str]) -> int:
    rolls = hashify(data)
    kernel = {(x, y) for y in (-1, 0, 1) for x in (-1, 0, 1)}.difference({(0, 0)})
    # Precompute neighbors for speed
    neighbors = {
        (x, y): [(x + dx, y + dy) for dx, dy in kernel if (x + dx, y + dy) in rolls]
        for x, y in rolls
    }

    num_removed = 0
    while True:
        to_remove = {
            (x, y)
            for x, y in rolls
            if sum(1 for n in neighbors[(x, y)] if n in rolls) < 4
        }
        num_removed += len(to_remove)
        rolls.difference_update(to_remove)
        if not to_remove:
            return num_removed


def main() -> float:
    return solve(__file__, PART, INPUT, prob_1, prob_2)


if __name__ == "__main__":
    main()
