import heapq
from functools import cache
from itertools import product

DIRS = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}


def neighbors(p):
    for symbol, delta in DIRS.items():
        yield (p[0] + delta[0], p[1] + delta[1]), symbol


@cache
def best_paths(grid, start: tuple[int, int], end: tuple[int, int]):
    q = [(0, start, [])]  # cost, cur, path
    w, h = len(grid[0]), len(grid)

    best_cost = abs(end[1] - start[1]) + abs(end[0] - start[0])
    best_paths = []

    while q:
        c, p, path = heapq.heappop(q)
        if c >= best_cost and p != end:
            continue
        if p == end:
            best_paths.append(path + ["A"])
            continue
        for p1, d1 in neighbors(p):
            if (0 <= p1[0] < w) and (0 <= p1[1] < h) and grid[p1[1]][p1[0]] != " ":
                heapq.heappush(q, (c + 1, p1, path + [d1]))

    return best_paths


# def dfs(paths,depth):
#    for p in paths:


def bfs(paths, depth):
    for i in range(depth):
        next_paths = []
        for p in paths:
            next_p = []
            for pr in zip(["A"] + p, p):
                next_p += [best_paths(grid_bot, *[keymap_bot[k] for k in pr])]
            # next_paths += [
            #    [c for part in seq for c in part] for seq in product(*next_p)
            # ]
            minlen = sum(min([len(seq) for seq in group]) for group in next_p)
            print(f"shortest path for {''.join(p)} = {minlen}")
            next_paths += next_p

        min_len = min(len(seq) for seq in next_paths)
        paths = [p for p in next_paths if len(p) == min_len]
        # print(f"length {len(paths[0])} to go 3 -> 7 from depth {depth}")

    return paths


grid_door = ("789", "456", "123", " 0A")
grid_bot = (" ^A", "<v>")

keymap_door, keymap_bot = tuple(
    {c: (x, y) for y, row in enumerate(kp) for x, c in enumerate(row)}
    for kp in (grid_door, grid_bot)
)


# This will be A->3 , 3->7, ... x->A in the end
pr = ("3", "7")

depth = 3

paths = best_paths(grid_door, *[keymap_door[k] for k in pr])

paths = bfs(paths, depth)
# paths = dfs(paths, depth)


print(f"length {len(paths[0])} to go 3 -> 7 from depth {depth}")


# print("\n".join("".join(c for c in path) for path in paths))
