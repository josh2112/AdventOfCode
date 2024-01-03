#!/usr/bin/env python3

from collections import defaultdict
from itertools import pairwise
import time

from aoclib.direction import Direction, XYPos

# https://adventofcode.com/2023/day/23

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 2

Nodes = dict[int, dict[int, int]]
Nodes2 = dict[XYPos, dict[XYPos, int]]


def build_graph(data: list[str]) -> Nodes2:
    # look up by (x,y) instead of [y][x]
    maze = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}

    # position -> neighbor node positions with values = path lengths
    nodes: Nodes2 = defaultdict(dict)

    # start, direction, is_bidi
    Hallway = tuple[XYPos, Direction, bool]
    # start at (1,0) moving down
    hallways: list[Hallway] = [((1, 0), Direction.DOWN, True)]

    while hallways:
        start, direction, is_bidi = hallways.pop(0)

        # Take advantage of the fact that a node can have at most one
        # neighbor in each direction. If the (start) node has a neighbor
        # in (direction) already, skip it.
        if any(Direction.from_line(start, n) == direction for n in nodes[start]):
            continue

        pos = start

        while True:
            # Move forward 1
            pos = direction.advance(pos)

            if pos not in maze:
                # We must be at the exit
                pos_prev = direction.advance(pos, -1)
                length = abs(start[0] - pos_prev[0]) + abs(start[1] - pos_prev[1])
                nodes[start][pos_prev] = length
                nodes[pos_prev][start] = length
                break

            # Enforce directionality arrow
            if (arrow := "^>v<".find(maze[pos])) != -1:
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

            if can_go_right or can_go_left:
                # Create bidirectional connection
                length = abs(start[0] - pos[0]) + abs(start[1] - pos[1])
                nodes[start][pos] = length
                if is_bidi:
                    nodes[pos][start] = length

                # Create new hallways left and/or right
                if can_go_right:
                    hallways.append((pos, dir_right, True))
                if can_go_left:
                    hallways.append((pos, dir_left, True))

                # Start a new hallway forward if we can
                if maze[direction.advance(pos)] != "#":
                    hallways.append((pos, direction, True))

                break

    return nodes


# Build a condensed version of the graph, condensing long hallways with no exits.
# Only use for part 2 (breaks the directionality arrows!)
def build_graph_2(data: list[str]) -> Nodes2:
    def xy2int(xy: tuple[int, int]) -> int:
        return (xy[0] << 8) + xy[1]

    def int2xy(i: int) -> tuple[int, int]:
        return i >> 8, i & 0xFF

    # look up by (x,y) instead of [y][x]
    maze = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}

    # position -> neighbor node positions with values = path lengths
    nodes: Nodes2 = defaultdict(dict)

    # start, direction
    Path = tuple[XYPos, Direction]
    # start at (1,0) moving down
    paths: list[Path] = [((1, 0), Direction.DOWN)]

    while paths:
        start, direction = paths.pop(0)

        # Take advantage of the fact that a node can have at most one
        # neighbor in each direction. If the (start) node has a neighbor
        # in (direction) already, skip it.
        # if any(Direction.from_line(start, n) == direction for n in nodes[start]):
        #    continue

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

            # Can we turn right and/or left here?
            dir_right = direction.turn(1)
            can_go_right = maze[dir_right.advance(pos)] != "#"
            dir_left = direction.turn(-1)
            can_go_left = maze[dir_left.advance(pos)] != "#"
            can_go_forward = (newpos := direction.advance(pos)) in maze and maze[
                newpos
            ] != "#"

            num_choices = sum(
                1 for d in (can_go_left, can_go_right, can_go_forward) if d
            )

            if num_choices == 1:
                # There's only one way to advance. Change direction if needed, then keep going
                if can_go_right:
                    direction = dir_right
                elif can_go_left:
                    direction = dir_left
            else:
                # Dead-end or junction point

                if pos in nodes[start]:
                    # We've already seen this node; stop!
                    break

                # Create bidirectional connection
                nodes[start][pos] = length
                nodes[pos][start] = length

                # Create new hallways left, right and/or straight
                if can_go_right:
                    paths.append((pos, dir_right))
                if can_go_left:
                    paths.append((pos, dir_left))
                if can_go_forward:
                    paths.append((pos, direction))
                break

    return nodes


def walk(nodes: Nodes2, start: XYPos, goal: XYPos) -> int:
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
                elif n not in path:
                    possibilities.append(n)
            if not possibilities:
                break
            for n in possibilities[1:]:
                paths.append(path + [n])
            path.append(possibilities[0])

    return max_steps


def longest_path(data: list[str]):
    nodes = build_graph_2(data) if PART == 2 else build_graph(data)

    for n in nodes.keys():
        nodes[n] = dict(sorted(nodes[n].items(), key=lambda kv: kv[1], reverse=True))

    start = (1, 0)
    goal = (len(data[0]) - 2, len(data) - 1)
    # Optimization: If we hit the node directly above the exit, we must take the exit,
    # otherwise we'll block our path to it. So make the goal the penultimate node, and
    # just add the last-hop size later.
    penultimate = next(iter(nodes[goal]))
    print(f"* Add {nodes[penultimate][goal]} for last leg!")

    max_steps = walk(nodes, start, penultimate)
    return max_steps + nodes[penultimate][goal]


def prob_1(data: list[str]):
    return longest_path(data)


def prob_2(data: list[str]):
    return longest_path(data)


def main():
    from os.path import join, dirname

    inp = join(dirname(__file__), INPUT or "input.txt")
    with open(inp, mode="r", encoding="utf-8") as f:
        data = [line.strip() for line in f.readlines()]

    start = time.perf_counter()
    result = prob_1(data) if PART == 1 else prob_2(data)
    elapsed = time.perf_counter() - start

    print(f"Problem {PART}: {result}")
    print(f"Time: {elapsed} s")


if __name__ == "__main__":
    main()
