"""https://adventofcode.com/2025/day/11"""

from aoclib.runner import solve
from dataclasses import dataclass, field
from string import Template

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def prob_1(data: list[str]) -> int:
    nodes = {line.split(":")[0]: line.split()[1:] for line in data}

    def hop(n: str):
        return 1 if n == "out" else sum(hop(c) for c in nodes[n])

    return hop("you")


def prob_2(data: list[str]) -> int:
    nodes = {line.split(":")[0]: line.split()[1:] for line in data}

    # Count paths svr -> fft, fft -> dac, dac -> out and multiply
    # But this will be too slow -- fft occurs early in the tree, we will crash out going down paths that can't
    # possibly lead to fft. Go backwards? But we'll have the opposite problem going from dac to out.
    # Need to limit the search depth -- hardcode maximum depth from a to b by manual inspection of the graph?
    # How to find it programatically?

    def hop(n: str, dest: str, hops: int, maxhops: int):
        if hops == maxhops:
            return 0
        hops += 1
        return (
            1
            if n == dest
            else sum(hop(c, dest, hops, maxhops) for c in nodes.get(n, []))
        )

    print(
        hop(
            "svr",
            "fft",
            -1,
            10,
        )
    )
    print(
        hop(
            "fft",
            "dac",
            -1,
            19,
        )
    )
    print(
        hop(
            "dac",
            "out",
            -1,
            9,
        )
    )

    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
