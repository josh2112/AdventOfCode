#!/usr/bin/env python3

import time
import dataclasses
from queue import PriorityQueue
from typing import Optional

# https://adventofcode.com/2023/day/17

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


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


@dataclasses.dataclass(frozen=True)
class TravelState:
    pos: tuple[int, int]
    vec: tuple[int, int]
    length: int


@dataclasses.dataclass(frozen=True)
class State:
    cost: int
    travel: TravelState
    prev: Optional["State"] = None

    def __lt__(self, other: "State"):
        return self.cost < other.cost


def print_path(data: list[str], goal_state: State, start: tuple[int, int]):
    track = []
    s = goal_state
    while s:
        track.append(s.travel.pos)
        s = s.prev
    track.append(start)

    for y in range(len(data)):
        print(
            "".join(
                f"{bg( 0,96,0)}{c}{bg()}" if (x, y) in track else c
                for x, c in enumerate(data[y])
            )
        )


def prob_1(data: list[str]):
    return solve(data, 1, 3)


def prob_2(data: list[str]):
    return solve(data, 4, 10)


def solve(data: list[str], min_straight_steps: int, max_straight_steps: int):
    xmax, ymax = len(data[0]), len(data)
    start, goal = (0, 0), (xmax - 1, ymax - 1)
    frontier = PriorityQueue()

    frontier.put(State(0, TravelState(start, (1, 0), 1)))
    frontier.put(State(0, TravelState(start, (0, 1), 1)))

    visited: set[TravelState] = set()

    goal_state = None

    while frontier:
        cur: State = frontier.get()

        if cur.travel.pos == goal and cur.travel.length >= min_straight_steps:
            goal_state = cur
            break

        if cur.travel in visited:
            continue

        visited.add(cur.travel)

        for nxt in neighbors(cur.travel.pos, xmax, ymax):
            nxt_vec = (nxt[0] - cur.travel.pos[0], nxt[1] - cur.travel.pos[1])

            if nxt_vec != (-cur.travel.vec[0], -cur.travel.vec[1]) and (
                (nxt_vec != cur.travel.vec and cur.travel.length >= min_straight_steps)
                or (
                    nxt_vec == cur.travel.vec and cur.travel.length < max_straight_steps
                )
            ):
                frontier.put(
                    State(
                        cur.cost + int(data[nxt[1]][nxt[0]]),
                        TravelState(
                            nxt,
                            nxt_vec,
                            cur.travel.length + 1 if nxt_vec == cur.travel.vec else 1,
                        ),
                        cur,
                    )
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
