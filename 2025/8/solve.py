"""https://adventofcode.com/2025/day/8"""

from itertools import combinations
from math import prod

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1

# TODO: Optimize... mean times right now are about 800 and 1080 ms


def _setup(data: list[str]):
    # Store pairs of boxes keyed on distances (a bit of a cheat since my input does not contain duplicate
    # distance values, may not hold true for other inputs)
    dists_by_pair = {
        (pr[1][0] - pr[0][0]) ** 2
        + (pr[1][1] - pr[0][1]) ** 2
        + (pr[1][2] - pr[0][2]) ** 2: pr
        for pr in combinations([tuple(map(int, line.split(","))) for line in data], 2)
    }
    return dists_by_pair, sorted(dists_by_pair.keys())


def prob_1(data: list[str]) -> int:
    dists_by_pair, ordered_dists = _setup(data)

    num_cnx = 10 if len(data) < 100 else 1000

    # Grab the X closest pairs
    edges = [dists_by_pair[ordered_dists[i]] for i in range(num_cnx)]

    # Join the edges into circuits
    circuits = []
    while edges:
        e = edges.pop(0)
        c = {e[0], e[1]}
        while e := next((e for e in edges if e[0] in c or e[1] in c), None):
            edges.remove(e)
            c.add(e[0])
            c.add(e[1])
        circuits.append(c)

    return prod(sorted((len(c) for c in circuits), reverse=True)[:3])


def prob_2(data: list[str]) -> int:
    dists_by_pair, ordered_dists = _setup(data)

    circuits: list[set] = []

    # Take each pair (sorted by distance) and either create new circuit or join into existing circuit
    for e in [dists_by_pair[d] for d in ordered_dists]:
        c0 = next((c for c in circuits if e[0] in c), None)
        c1 = next((c for c in circuits if e[1] in c), None)
        # Does this edge span 2 circuits?
        if c0 and c1 and c0 != c1:
            # Join them
            c0.update(c1)
            circuits.remove(c1)
        # Is this edge not yet in a circuit?
        elif not c0 and not c1:
            circuits.append({e[0], e[1]})
            continue  # Skip length test at bottom
        # Otherwise, append to a circuit
        elif c0:
            c0.add(e[1])
        elif c1:
            c1.add(e[0])

        # Are all boxes in one circuit?
        if len(circuits[0]) == len(data):
            return e[0][0] * e[1][0]


def main() -> float:
    return solve(__file__, PART, INPUT, prob_1, prob_2)


if __name__ == "__main__":
    main()
