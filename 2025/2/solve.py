"""https://adventofcode.com/2025/day/2"""

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def sequences(length: int, max_digits: int, rpt_count: int | None = None):
    # Generate sequences of [length] digits repeating until [max_digits] count.
    # Number of repeats is limited to rpt_count if given.
    m = 1
    for _ in (
        range(rpt_count, rpt_count + 1)
        if rpt_count
        else range(max_digits // length - 1)
    ):
        # For length=1 this gives us 11, 111, 1111, etc. For length=2 we get 101, 10101, 10101, etc.
        m = m * (10**length) + 1
        # Multiply m by every length-digit number
        yield from (i * m for i in range(10 ** (length - 1), 10**length))


def _solve(data: str, rpt_count: int | None = None) -> int:
    # Ranges are inclusive - increment the upper values
    ranges = [
        range(*map(sum, zip(map(int, r.split("-")), [0, 1]))) for r in data.split(",")
    ]
    max_digits = len(str(max(max(r) for r in ranges)))

    # Use set to exclude duplicates
    return sum(
        set(
            [
                x
                for i in range(1, max_digits // 2 + 1)
                for x in sequences(i, max_digits, rpt_count=rpt_count)
                if any(x in r for r in ranges)
            ]
        )
    )


def prob_1(data: list[str]) -> int:
    return _solve(data[0], rpt_count=2)


def prob_2(data: list[str]) -> int:
    return _solve(data[0])


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
