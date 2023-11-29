import re
from collections import namedtuple
import time

# https://adventofcode.com/2022/day/16

SAMPLE = 0

Valve = namedtuple("Valve", ["name", "flow", "tunnels"])


def parse(line) -> Valve:
    args = re.findall(
        r"Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]*)", line
    )[0]
    return Valve(args[0], int(args[1]), args[2].split(", "))


with open("input-sample.txt" if SAMPLE else "input.txt", "r") as f:
    valves = {v.name: v for v in [parse(l) for l in f.readlines()]}

dist = {v: {v: len(valves) + 1 for v in valves} for v in valves}
for v in valves:
    dist[v][v] = 0
    for v2 in valves[v].tunnels:
        dist[v][v2] = 1

for n in valves:
    for i in valves:
        for j in valves:
            dist[i][j] = min(dist[i][j], dist[i][n] + dist[n][j])

solutions = []


def explore(v, time, pressure, valves_rem):
    if valves[v].flow and time > 0:
        time -= 1
        pressure += valves[v].flow * time
    if not valves_rem or time <= 0:
        solutions.append(pressure)
        return
    for vn in valves_rem:
        vr = [x for x in valves_rem if x != vn]
        explore(vn, time - dist[v][vn], pressure, vr)


t = time.time()
explore("AA", 30, 0, [v for v in valves if valves[v].flow > 0])
t = (time.time() - t) * 1000

print(sorted(solutions, reverse=True)[0], ",", t, "ms")
