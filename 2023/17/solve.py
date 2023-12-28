#!/usr/bin/env python3

import time
import dataclasses
from queue import PriorityQueue

# https://adventofcode.com/2023/day/17

# Input file path (default is "input.txt")
INPUT = "input.ex2.txt"

# Part to solve, 1 or 2
PART = 1


def neighbors(pos: tuple[int, int], xmax: int, ymax: int):
    if pos[0] > 0:
        yield (pos[0] - 1, pos[1])
    if pos[0] < xmax - 1:
        yield (pos[0] + 1, pos[1])
    if pos[1] > 0:
        yield (pos[0], pos[1] - 1)
    if pos[1] < ymax - 1:
        yield (pos[0], pos[1] + 1)


def bg(r=None, g=None, b=None):
    return "\u001b[0m" if not r and not g and not b else f"\u001b[48;2;{r};{g};{b}m"


@dataclasses.dataclass
class State:
    pos: tuple[int, int]
    vec: tuple[int, int]
    length: int

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, State):
            return (
                self.pos == __value.pos
                and self.vec == __value.vec
                and self.length == __value.length
            )
        return False


@dataclasses.dataclass
class TravelState:
    cost: int
    travel: State

    def __lt__(self, other):
        return self.cost < other.cost


def prob_1(data: list[str]):
    xmax, ymax = len(data[0]), len(data)
    start, goal = (0, 0), (xmax - 1, ymax - 1)
    frontier = PriorityQueue()
    frontier.put(TravelState(0, State(start, (0, 0), 0)))

    visited: set[State] = set()

    cost_so_far: dict[tuple[int, int], int] = {start: 0}
    came_from: dict[tuple[int, int], tuple[int, int]] = {start: start}

    while frontier:
        cur: TravelState = frontier.get()

        if cur.travel.pos == goal:
            break

        if cur.travel in visited:
            continue

        visited.add(cur.travel)

        for nxt in neighbors(cur.pos, xmax, ymax):
            alt = cost_so_far[cur.pos] + int(data[nxt[1]][nxt[0]])
            if nxt not in cost_so_far or alt < cost_so_far[nxt]:
                # First: can we go this way?
                nxt_vec = (nxt[0] - cur.pos[0], nxt[1] - cur.pos[1])
                nxt_length = 0
                if cur.vec == nxt_vec:
                    # If we've already moved 3 tiles in the same direction, no go
                    if cur.length == 2:
                        continue
                    nxt_length = cur.length + 1
                else:
                    nxt_length = 1

                cost_so_far[nxt] = alt
                frontier.put(TravelState(alt, nxt, nxt_vec, nxt_length))
                came_from[nxt] = cur.pos

    track = []
    n = goal
    while n != start:
        track.append(n)
        n = came_from[n]
    track.append(start)

    for y in range(ymax):
        print(
            "".join(
                f"{bg( 0,96,0)}{c}{bg()}" if (x, y) in track else c
                for x, c in enumerate(data[y])
            )
        )

    return cost_so_far[goal]


def prob_2(data: list[str]):
    print(data)


def main():
    with open(INPUT or "input.txt", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
