"""https://adventofcode.com/2025/day/5"""

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def read_ranges(data: list[str]) -> list[range]:
    ranges = sorted(
        [range(int(a), int(b) + 1) for a, b in [r.split("-") for r in data]],
        key=lambda r: r.start,
    )
    # Join contiguous ranges
    joined = [ranges[0]]
    for r1 in ranges[1:]:
        r0 = joined[-1]
        if r1.start <= r0.stop:
            # Ensure r1 is not fully inside r0 before updating it!
            if r1.stop > r0.stop:
                joined[-1] = range(r0.start, r1.stop)
        else:
            joined.append(r1)

    return joined


def prob_1(data: list[str]) -> int:
    sep = data.index("")
    ranges = read_ranges(data[:sep])
    return sum(
        1 for i in [int(i) for i in data[sep + 1 :]] if any(i in r for r in ranges)
    )


def prob_2(data: list[str]) -> int:
    return sum(len(r) for r in read_ranges(data[: data.index("")]))


def main() -> float:
    return solve(__file__, PART, INPUT, prob_1, prob_2)


if __name__ == "__main__":
    main()
