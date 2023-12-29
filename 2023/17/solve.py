#!/usr/bin/env python3

import time
from dataclasses import dataclass, field
from heapq import heappush, heappop
from typing import Optional

# https://adventofcode.com/2023/day/17

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


@dataclass(frozen=True)
class TravelState:
    pos: tuple[int, int]
    vec: int
    length: int


@dataclass(frozen=True, order=True)
class State:
    cost: int
    travel: TravelState = field(compare=False)
    prev: Optional["State"] = field(default=None, compare=False)


def print_path(data: list[str], goal_state: State, start: tuple[int, int]):
    track = []
    s = goal_state
    while s:
        track.append(s.travel.pos)
        s = s.prev
    track.append(start)

    def bg(r=None, g=None, b=None):
        return "\u001b[0m" if not r and not g and not b else f"\u001b[48;2;{r};{g};{b}m"

    for y in range(len(data)):
        print(
            "".join(
                f"{bg( 0,96,0)}{c}{bg()}" if (x, y) in track else c
                for x, c in enumerate(data[y])
            )
        )


UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
VEC = ((0, -1), (1, 0), (0, 1), (-1, 0))


def prob_1(data: list[str]):
    return solve(data, 1, 3)


def prob_2(data: list[str]):
    return solve(data, 4, 10)


def solve(data: list[str], min_straight_steps: int, max_straight_steps: int):
    xmax, ymax = len(data[0]), len(data)
    start, goal = (0, 0), (xmax - 1, ymax - 1)

    frontier: list[State] = [
        State(0, TravelState(start, RIGHT, 1)),
        State(0, TravelState(start, DOWN, 1)),
    ]

    visited: set[TravelState] = set()

    goal_state = None

    while frontier:
        cur: State = heappop(frontier)

        if cur.travel.pos == goal and cur.travel.length >= min_straight_steps:
            goal_state = cur
            break

        if cur.travel in visited:
            continue

        visited.add(cur.travel)

        # Can we turn?
        if min_straight_steps <= cur.travel.length <= max_straight_steps:
            for d in (-1, 1):
                nxt_dir = (cur.travel.vec + d) % len(VEC)
                vec = VEC[nxt_dir]
                nxt = (cur.travel.pos[0] + vec[0], cur.travel.pos[1] + vec[1])
                if 0 <= nxt[0] < xmax and 0 <= nxt[1] < ymax:
                    heappush(
                        frontier,
                        State(
                            cur.cost + int(data[nxt[1]][nxt[0]]),
                            TravelState(nxt, nxt_dir, 1),
                            cur,
                        ),
                    )

        # Can we go straight?
        if cur.travel.length < max_straight_steps:
            vec = VEC[cur.travel.vec]
            nxt = (cur.travel.pos[0] + vec[0], cur.travel.pos[1] + vec[1])
            if 0 <= nxt[0] < xmax and 0 <= nxt[1] < ymax:
                heappush(
                    frontier,
                    State(
                        cur.cost + int(data[nxt[1]][nxt[0]]),
                        TravelState(nxt, cur.travel.vec, cur.travel.length + 1),
                        cur,
                    ),
                )

    if goal_state:
        # print_path(data, goal_state, start)
        return goal_state.cost


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
