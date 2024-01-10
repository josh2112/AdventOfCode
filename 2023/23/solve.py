"""https://adventofcode.com/2023/day/23"""

import argparse
from collections import defaultdict
from enum import IntEnum
from itertools import pairwise
import time

# I'm too dumb to relative import from a lower level...
# from aoclib.direction import Direction, XYPos

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2


XYPos = tuple[int, int]

VECTORS = ((0, -1), (1, 0), (0, 1), (-1, 0))

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def turn(self, cw_count: int) -> "Direction":
        return self.__class__((self.value + cw_count) % len(Direction.__members__))  # type: ignore

    @property
    def vector(self) -> XYPos:
        return VECTORS[self.value]

    def advance(self, coord: XYPos, count: int = 1) -> XYPos:
        vec = self.vector
        return coord[0] + vec[0] * count, coord[1] + vec[1] * count


Nodes = dict[XYPos, dict[XYPos, int]]


def build_graph(data: list[str], ignore_directionals: bool) -> Nodes:
    # If we're ignoring directional arrows, we can condense long branchless hallways
    condense_non_branch_paths = ignore_directionals

    # look up by (x,y) instead of [y][x]
    maze = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}

    # position -> neighbor node positions with values = path lengths
    nodes: Nodes = defaultdict(dict)

    # start, direction, is_bidi
    Path = tuple[XYPos, Direction, bool]
    # start at (1,0) moving down
    paths: list[Path] = [((1, 0), Direction.DOWN, True)]

    while paths:
        start, direction, is_bidi = paths.pop(0)

        pos = start
        length = 0

        while True:
            # Move forward 1
            pos = direction.advance(pos)
            length += 1

            if pos not in maze:
                # We must be at the exit
                pos_prev = direction.advance(pos, -1)
                length = abs(start[0] - pos_prev[0]) + abs(start[1] - pos_prev[1])
                nodes[start][pos_prev] = length
                nodes[pos_prev][start] = length
                break

            # Enforce directionality arrow
            if not ignore_directionals and (arrow := "^>v<".find(maze[pos])) != -1:
                if arrow == direction:
                    # Now we know it's one-way
                    is_bidi = False
                if ((arrow + 2) % 4) == direction:
                    # We are going the wrong way, stop following path
                    break

            # Can we turn right and/or left here?
            dir_right = direction.turn(1)
            can_go_right = maze[dir_right.advance(pos)] != "#"
            dir_left = direction.turn(-1)
            can_go_left = maze[dir_left.advance(pos)] != "#"
            can_go_forward = (newpos := direction.advance(pos)) in maze and maze[
                newpos
            ] != "#"

            has_branch = (
                sum(1 for d in (can_go_left, can_go_right, can_go_forward) if d) != 1
            )

            if condense_non_branch_paths and not has_branch:
                # There's only one way to advance. Change direction if needed, then keep going
                if can_go_right:
                    direction = dir_right
                elif can_go_left:
                    direction = dir_left
            elif (
                (condense_non_branch_paths and has_branch)
                or can_go_right
                or can_go_left
            ):
                if pos in nodes[start]:
                    # We've already seen this node; stop!
                    break

                # Create bidirectional connection
                nodes[start][pos] = length
                if is_bidi:
                    nodes[pos][start] = length

                # Create new hallways left, right and/or straight
                if can_go_right:
                    paths.append((pos, dir_right, True))
                if can_go_left:
                    paths.append((pos, dir_left, True))
                if can_go_forward:
                    paths.append((pos, direction, True))
                break

    return nodes


def walk(nodes: Nodes, start: XYPos, goal: XYPos) -> int:
    time_start = time.perf_counter()
    max_steps = 0
    paths: list[list[XYPos]] = [[start]]

    while paths:
        path = paths.pop(0)

        while True:
            possibilities = []
            for n in nodes[path[-1]]:
                if n == goal:
                    steps = sum(nodes[n1][n2] for n1, n2 in pairwise(path + [n]))
                    if steps > max_steps:
                        print(
                            f"{time.perf_counter()-time_start}: Found path of {steps} steps"
                        )
                        max_steps = steps
                        # TODO: The longest path is found quickly, but we keep churning through
                        # possibilities. Short-circuiting to avoid that.
                        if max_steps >= 6230:
                            return max_steps
                elif n not in path:
                    possibilities.append(n)
            if not possibilities:
                break
            for n in possibilities[1:]:
                paths.append(path + [n])
            path.append(possibilities[0])

    return max_steps


def longest_path(data: list[str], ignore_directionals: bool):
    nodes = build_graph(data, ignore_directionals)

    for n in nodes.keys():
        nodes[n] = dict(sorted(nodes[n].items(), key=lambda kv: kv[1], reverse=True))

    start = (1, 0)
    goal = (len(data[0]) - 2, len(data) - 1)
    return walk(nodes, start, goal)


def prob_1(data: list[str]):
    return longest_path(data, ignore_directionals=False)


def prob_2(data: list[str]):
    return longest_path(data, ignore_directionals=True)


def main() -> float:
    parser = argparse.ArgumentParser(description="Solves AoC 2023 day 23.")
    parser.add_argument("-p", "--part", choices=("1", "2", "all"), default=str(PART))
    parser.add_argument("-i", "--input", default=INPUT)
    args = parser.parse_args()
    part, infile = args.part, args.input

    with open(infile, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    if part in ("1", "all"):
        print(f"Part 1: {prob_1(data)}")
    if part in ("2", "all"):
        print(f"Part 2: {prob_2(data)}")

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed} s")

    return elapsed


if __name__ == "__main__":
    main()
