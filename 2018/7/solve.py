"""https://adventofcode.com/2018/day/7"""

from collections import defaultdict
from dataclasses import dataclass

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


@dataclass
class Worker:
    n: str
    t: int


def prob_1(data: list[str]) -> str | int:
    return doit(data, 1)


def prob_2(data: list[str]) -> str | int:
    return doit(data, 2)


def doit(data: list[str], part: int) -> int | str:
    links = [(ln[5], ln[36]) for ln in data]

    # node -> (prev nodes, next nodes)
    nodes: defaultdict[str, tuple[set[str], set[str]]] = defaultdict(lambda: (set(), set()))
    for ln in links:
        nodes[ln[0]][1].add(ln[1])
        nodes[ln[1]][0].add(ln[0])

    NUM_WORKERS = 1 if part == 1 else (2 if len(nodes) < 10 else 5)
    TASK_TIME = 0 if len(nodes) < 10 else 60

    # Current node, time next available
    workers = [Worker("", 0) for _ in range(NUM_WORKERS)]

    frontier = set(n for n, sets in nodes.items() if not sets[0])
    path: list[str] = []
    t = 0

    while len(path) < len(nodes):
        avail_workers: list[Worker] = []

        # First, grab add any complete workers' nodes to the path and mark them as available
        for w in workers:
            if w.t <= t:
                avail_workers.append(w)
                if w.n:
                    path.append(w.n)
                    frontier |= nodes[w.n][1]
                    w.n = ""

        avail_nodes = sorted(n for n in frontier if nodes[n][0].issubset(path))

        # Assign any available nodes to any available workers
        for i in range(min(len(avail_nodes), len(avail_workers))):
            w = avail_workers[i]
            w.n = avail_nodes[i]
            w.t = t + TASK_TIME + ord(w.n) - ord("A") + 1

            frontier.remove(w.n)

        # Can we fast-forward to when the next worker is done?
        done_times = [w.t for w in workers if w.t > t]
        if not done_times:
            break
        t = min(done_times)

    return t if part == 2 else "".join(path)


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
