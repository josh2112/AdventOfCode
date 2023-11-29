import re
from recordclass import RecordClass
import math
import itertools

# https://adventofcode.com/2022/day/16

SAMPLE = 0


class Valve(RecordClass):
    name: str
    flow: int
    tunnels: list[str]


class Solution(RecordClass):
    pressure: int
    vset1: list[str]
    vset2: list[str]


def parse(line) -> Valve:
    args = re.findall(r"Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]*)", line)[0]
    return Valve(args[0], int(args[1]), args[2].split(", "))


with open("input-sample.txt" if SAMPLE else "input.txt", "r") as f:
    valves = {v.name: v for v in [parse(l) for l in f.readlines()]}

dist = {v: {v: 9999 for v in valves} for v in valves}
nxt = {v: {v: None for v in valves} for v in valves}

for v in valves:
    dist[v][v] = 0
    nxt[v][v] = v
    for v2 in valves[v].tunnels:
        dist[v][v2] = 1
        nxt[v][v2] = v2

for k in valves:
    for i in valves:
        for j in valves:
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
                nxt[i][j] = nxt[i][k]


def path(u, v):
    if not nxt[u][v]:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


valves_with_flow = [v for v in valves if valves[v].flow > 0]

solution = None

# Calculate total pressure released by following vset (or as far as we can go) in the given time
def calc(vset, time):
    pressure = 0
    for pr in pairwise(vset):
        # print("time left:", time)
        if valves[pr[0]].flow:
            time -= 1
            pressure += valves[pr[0]].flow * time
            # print(
            #    f" - release valve {pr[0]} ({valves[pr[0]].flow}) to add {valves[pr[0]].flow} * {time} = {valves[pr[0]].flow * time}"
            # )
        # Gotta have time to get there, 1 minute to turn the valve, and at least a minute left for the pressure to matter!
        if time > dist[pr[0]][pr[1]] + 1:
            time -= dist[pr[0]][pr[1]]
        else:
            # Can't reach this valve in time enough for it to matter, end travel here
            return list(itertools.takewhile(lambda v: v != pr[1], vset)), pressure
        # print(f" - travel from {pr[0]} to {pr[1]}, dist = {dist[pr[0]][pr[1]]}. total pressure = {pressure}")
    if valves[vset[-1]].flow:
        time -= 1
        pressure += valves[vset[-1]].flow * time
        # print(
        #    f" - release valve {vset[-1]} ({valves[vset[-1]].flow}) to add {valves[vset[-1]].flow} * {time} = {valves[vset[-1]].flow * time}"
        # )
    return vset, pressure


totalperms = math.factorial(len(valves_with_flow)) // math.factorial(len(valves_with_flow) - len(valves_with_flow) // 2)
cnt = 0

# Sequences of valves that we know are too long to visit in the time alloted
invalid_paths = []

for vset1 in itertools.permutations(valves_with_flow, len(valves_with_flow) // 2):
    cnt += 1
    vset1orig = list(vset1)
    # If this set is a subset of any too-long path, forget it
    if next((i for i in invalid_paths if i in "".join(vset1orig)), None) != None:
        continue
    vset1, pressure1 = calc(["AA"] + vset1orig, 26)
    if len(vset1) < len(vset1orig):  # Path was abbreviated
        invalid_paths.append("".join(vset1orig[: len(vset1) + 1]))
    remaining = [v for v in valves_with_flow if v not in vset1]

    totalperms2 = math.factorial(len(remaining)) // math.factorial(len(remaining) - len(remaining))
    cnt2 = 0
    for vset2 in itertools.permutations(remaining, len(remaining)):
        cnt2 += 1
        vset2orig = list(vset2)
        # If this set is a subset of any too-long path, forget it
        if next((i for i in invalid_paths if i in "".join(vset2orig)), None) != None:
            continue
        vset2, pressure2 = calc(["AA"] + list(vset2orig), 26)
        if len(vset2) < len(vset2orig):  # Path was abbreviated
            invalid_paths.append("".join(vset2orig[: len(vset2) + 1]))
        if not solution or pressure1 + pressure2 > solution.pressure:
            solution = Solution(pressure1 + pressure2, vset1, vset2)

    print(f"{(cnt*100)/totalperms} %, best pressure = {solution.pressure if solution else 'N/A'}")


print(solution)
