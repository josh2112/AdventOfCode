#!/usr/bin/env python3

from collections import defaultdict
from itertools import pairwise
import time

from aoclib.direction import Direction, XYPos

# https://adventofcode.com/2023/day/23

# Input file path (default is "input.txt")
INPUT = "input.ex.txt"

# Part to solve, 1 or 2
PART = 2


def build_graph(data: list[str], ignore_directional: bool):
    # look up by (x,y) instead of [y][x]
    maze = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}

    # position -> neighbor node positions with values = path lengths
    nodes: dict[XYPos, dict[XYPos, int]] = defaultdict(dict)

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
            if not ignore_directional and (arrow := "^>v<".find(maze[pos])) != -1:
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


max_steps = 0


def walk(path: list[XYPos], nodes: dict[XYPos, dict[XYPos, int]], goal: XYPos):
    global max_steps
    while True:
        possibilities = []
        for n in nodes[path[-1]]:
            if n == goal:
                path.append(n)
                steps = sum(nodes[n1][n2] for n1, n2 in pairwise(path))
                if steps > max_steps:
                    print("Found path of", steps, "steps")
                    max_steps = max(steps, max_steps)
                return
            if n not in path:
                possibilities.append(n)
        if len(possibilities) > 1:
            for p in possibilities[1:]:
                walk(path + [p], nodes, goal)
        if possibilities:
            path.append(possibilities[0])
        if not possibilities:
            return


def collapse_non_branches_1(nodes: dict[XYPos, dict[XYPos, int]]):
    already_processed = []
    # Try to find long segments with no branches and collapse them
    n = next((n for n in nodes if len(nodes[n]) == 2), None)
    while n:
        # Find the ends of the chain
        s, e = n, n
        length = 0
        to_remove = set([n])
        while len(nodes[tmp := list(nodes[s])[0]]) == 2:
            length += nodes[s][tmp]
            to_remove.add(tmp)
            s = tmp
        while len(nodes[tmp := list(nodes[e])[1]]) == 2:
            length += nodes[e][tmp]
            to_remove.add(tmp)
            e = tmp
        if s != e:
            del nodes[s][next(n for n in nodes[s] if n in to_remove)]
            del nodes[e][next(n for n in nodes[e] if n in to_remove)]
            nodes[s][e] = length
            nodes[e][s] = length

            for n in [n for n in to_remove if n not in [s, e]]:
                del nodes[n]

            already_processed.append(s)
        already_processed.append(e)

        n = next(
            (n for n in nodes if n not in already_processed and len(nodes[n]) == 2),
            None,
        )
        pass


def collapse_non_branches_2(nodes: dict[XYPos, dict[XYPos, int]]):
    # Try to find long segments with no branches and collapse them
    n = next((n for n in nodes if len(nodes[n]) == 2), None)
    while n:
        # Find the ends of the chain
        s, e = n, n
        length = 0
        to_remove = set([n])
        while len(nodes[s]) == 2:
            tmp = list(nodes[s])[0]
            length += nodes[s][tmp]
            to_remove.add(tmp)
            s = tmp
        while len(nodes[e]) == 2:
            tmp = list(nodes[e])[1]
            length += nodes[e][tmp]
            to_remove.add(tmp)
            e = tmp
        # s = (1,1), e = (4,1)
        del nodes[s][next(n for n in nodes[s] if n in to_remove)]
        del nodes[e][next(n for n in nodes[e] if n in to_remove)]
        nodes[s][e] = length
        nodes[e][s] = length

        for n in [n for n in to_remove if n not in [s, e]]:
            del nodes[n]

        n = next((n for n in nodes if len(nodes[n]) == 2), None)
        pass


def longest_path(data: list[str], ignore_directionals: bool):
    nodes = build_graph(data, ignore_directionals)
    collapse_non_branches_1(nodes)

    for n in nodes.keys():
        nodes[n] = dict(sorted(nodes[n].items(), key=lambda kv: kv[1], reverse=True))

    path = [(1, 0), (1, 1)]
    goal = (len(data[0]) - 2, len(data) - 1)
    # Optimization: If we hit the node directly above the exit, we must take the exit,
    # otherwise we'll block our path to it. So make the goal the penultimate node, and
    # just add the last-hop size later.
    penultimate = next(iter(nodes[goal]))
    print(f"* Add {nodes[penultimate][goal]} for last leg!")
    walk(path, nodes, penultimate)
    return max_steps + nodes[penultimate][goal]


def prob_1(data: list[str]):
    return longest_path(data, False)


# TODO: It's bigger than 6226...
def prob_2(data: list[str]):
    return longest_path(data, True)


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
