#!/usr/bin/env python3

from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
import time
import re

# https://adventofcode.com/2023/day/23

# Input file path (default is "input.txt")
INPUT = "input.ex2.txt"

# Part to solve, 1 or 2
PART = 2

path_found = []


def walk(path: list[tuple[int, int]], data: list[str], goal: tuple[int, int]):
    global path_found
    while True:
        possibilities = []
        for vec in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            loc = (path[-1][0] + vec[0], path[-1][1] + vec[1])
            nxt = data[loc[1]][loc[0]]
            if loc == goal:
                path.append(loc)
                print("Found path of", len(path) - 1, "steps")
                if not path_found or len(path) > len(path_found):
                    path_found = path
                return
            if loc not in path and (
                nxt == "."
                or (nxt == "^" and vec == (0, -1))
                or (nxt == ">" and vec == (1, 0))
                or (nxt == "v" and vec == (0, 1))
                or (nxt == "<" and vec == (-1, 0))
            ):
                possibilities.append(loc)
        if len(possibilities) > 1:
            for p in possibilities[1:]:
                walk(path + [p], data, goal)
        if possibilities:
            path.append(possibilities[0])
        if not possibilities:
            return


def walk2(path: list[tuple[int, int]], data: list[str], goal: tuple[int, int]):
    global path_found
    while True:
        possibilities = []
        for vec in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            loc = (path[-1][0] + vec[0], path[-1][1] + vec[1])
            nxt = data[loc[1]][loc[0]]
            if loc == goal:
                path.append(loc)
                print("Found path of", len(path) - 1, "steps")
                if not path_found or len(path) > len(path_found):
                    path_found = path
                return
            if loc not in path and (
                nxt
                != "#"
                # nxt == "."
                # or (nxt == "^" and vec == (0, -1))
                # or (nxt == ">" and vec == (1, 0))
                # or (nxt == "v" and vec == (0, 1))
                # or (nxt == "<" and vec == (-1, 0))
            ):
                possibilities.append(loc)
        if len(possibilities) > 1:
            for p in possibilities[1:]:
                walk2(path + [p], data, goal)
        if possibilities:
            path.append(possibilities[0])
        if not possibilities:
            return


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    __vectors = ((0, -1), (1, 0), (0, 1), (-1, 0))

    def turn(self, cw_count: int) -> "Direction":
        return self.__class__((self.value + cw_count) % len(Direction.__members__))

    @property
    def vector(self) -> tuple[int, int]:
        return self.__class__.__vectors[self.value]

    def advance(self, coord: tuple[int, int], count: int = 1) -> tuple[int, int]:
        vec = self.vector
        return coord[0] + vec[0] * count, coord[1] + vec[1] * count

    @classmethod
    def from_line(cls, p1: tuple[int, int], p2: tuple[int, int]):
        vec = p2[0] - p1[0], p2[1] - p1[1]
        if mag := max(abs(vec[0]), abs(vec[1])):
            vec = vec[0] / mag, vec[1] / mag
        return Direction(cls.__vectors.index(vec))


def build_graph(data: list[str]):
    maze = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}

    # position -> set of neighbor node positions
    nodes: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)

    # start, direction, is_bidi
    Hallway = tuple[tuple[int, int], Direction, bool]
    # start at (1,0) moving down
    hallways: list[Hallway] = [((1, 0), Direction.DOWN, True)]

    # TODO: (1,3) should not go to (3,3)

    while hallways:
        start, direction, is_bidi = hallways.pop(0)

        # Take advantage of the fact that a node can have at most one
        # neighbor in each direction. If the (start) node has a neighbor
        # in (direction) already, skip it. For directional nodes, it's a
        # bit harder: We have to check each node to see if it has (start)
        # as a neighbor in the opposite direction
        if next(
            (n for n in nodes[start] if Direction.from_line(start, n) == direction),
            None,
        ):
            continue

        pos = start

        while True:
            # Move forward 1
            pos = direction.advance(pos)

            if pos not in maze:
                # We must be at the exit
                pos_prev = direction.advance(pos, -1)
                nodes[start].add(pos_prev)
                nodes[pos_prev].add(start)
                break

            # Enforce directionality arrow
            if (arrow := "^>v<".find(maze[pos])) != -1:
                if arrow == direction:
                    # We are going in the right way
                    is_bidi = False
                if ((arrow + 2) % 4) == direction:
                    # We are going the wrong way, stop following path
                    continue

            # Can we turn right and/or left here?
            dir_right = direction.turn(1)
            pos_right = dir_right.advance(pos)
            dir_left = direction.turn(-1)
            pos_left = dir_left.advance(pos)

            if maze[pos_left] != "#" or (maze[pos_right]) != "#":
                # Create bidirectional connection
                nodes[start].add(pos)
                if is_bidi:
                    nodes[pos].add(start)

                # Create new hallways left and/or right
                if maze[pos_left] != "#":
                    hallways.append((pos, dir_left, True))
                if maze[pos_right] != "#":
                    hallways.append((pos, dir_right, True))

                # If we can still go forward, create a new hallway
                pos_fwd = direction.advance(pos)
                if maze[pos_fwd] != "#":
                    hallways.append((pos, direction, True))

                break

    return nodes


def prob_1(data: list[str]):
    global paths_found
    path = [(1, 0), (1, 1)]
    goal = (len(data[0]) - 2, len(data) - 1)
    walk(path, data, goal)
    return len(path_found) - 1


# TODO: Runs way too slow for an answer. Maybe try building a graph containing just the decision
# points?
def prob_2(data: list[str]):
    build_graph(data)

    global paths_found
    path = [(1, 0), (1, 1)]
    goal = (len(data[0]) - 2, len(data) - 1)
    walk2(path, data, goal)
    return len(path_found) - 1


def main():
    with open(INPUT or "input.txt", mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
