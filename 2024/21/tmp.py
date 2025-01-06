import heapq
import itertools
from functools import cache

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


def dfs(paths, depth):
    def calc(path, shortest, depth):
        if depth == 0:
            return sum(len(shortest[pr]) for pr in zip(["A"] + path, path))
        else:
            return sum(
                calc(shortest[pr], shortest, depth - 1)
                for pr in zip(["A"] + path, path)
            )

    # Precompute best path between all pairs of keys

    # move pair (a,b) => (shortest_path, cost_at_level_2)
    shortest, l2_cost = dict(), dict()

    for pr in itertools.combinations([k for k in keymap_bot if k != " "], r=2):
        l1_paths = best_paths(grid_bot, *[keymap_bot[k] for k in pr])
        for l1_path in l1_paths:
            l2_paths = []
            for pr2 in zip(["A"] + l1_path, l1_path):
                l2_paths += [best_paths(grid_bot, *[keymap_bot[k] for k in pr2])]
            minlen = sum(min([len(seq) for seq in group]) for group in l2_paths)
            if pr not in l2_cost or minlen < l2_cost[pr]:
                shortest[pr], l2_cost[pr] = l1_path, minlen

    shortest.update({(pr[1], pr[0]): p for pr, p in shortest.items()})
    shortest.update({(k, k): ["A"] for k in keymap_bot.keys()})

    for p in paths:
        print("".join(c for c in p), calc(p, shortest, depth))


def bfs(paths, depth):
    for i in range(depth):
        next_paths = []
        for p in paths:
            next_p = []
            for pr in zip(["A"] + p, p):
                next_p += [best_paths(grid_bot, *[keymap_bot[k] for k in pr])]
            next_paths += [
                [c for part in seq for c in part] for seq in itertools.product(*next_p)
            ]

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
# pr = ("3", "7")

depth = 10


paths = best_paths(grid_door, *[keymap_door[k] for k in pr])

# paths = bfs(paths, depth)
paths = dfs(paths, depth)


print(f"length {len(paths[0])} to go 3 -> 7 from depth {depth}")


# print("\n".join("".join(c for c in path) for path in paths))
