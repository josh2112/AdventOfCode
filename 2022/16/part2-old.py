import re
from recordclass import RecordClass
import time
import itertools

# https://adventofcode.com/2022/day/16

SAMPLE = 0


class Valve(RecordClass):
    name: str
    flow: int
    tunnels: list[str]


class Agent(RecordClass):
    valve: str
    time: int
    visited: list[str]


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

valves_flow = {n: v for n, v in valves.items() if v.flow > 0}

solution = None


def explore(
    agents: list[Agent],
    time,
    pressure,
    valves_open: list[str],
    valves_not_seen: set[str],
):
    global solution
    # Make a list of agents that aren't in transit to a valve
    active_agents = [a for a in agents if a.time >= time]
    agents_in_transit = [a for a in agents if a.time < time]
    # Open valves if we can
    for a in active_agents:
        if a.time > 0 and a.valve not in valves_open and valves[a.valve].flow:
            a.time -= 1
            pressure += valves[a.valve].flow * a.time
            a.visited.append(a.valve)
            valves_open.append(a.valve)

    valves_not_seen -= set(a.valve for a in agents)
    # All valves open or out of time?
    if len(valves_open) == len(valves_flow) or sum(a.time for a in agents) <= 0:
        if not solution or pressure > solution[0]:
            solution = [pressure] + agents
        return
    active_agents = [a for a in active_agents if a.time > 0]
    for vpair in itertools.combinations(sorted(valves_not_seen), len(active_agents)):
        new_agents = [
            Agent(v, a.time - dist[a.valve][v], a.visited.copy())
            for a, v in zip(active_agents, vpair)
        ] + [Agent(a.valve, a.time, a.visited.copy()) for a in agents_in_transit]
        time = max(a.time for a in new_agents)
        explore(new_agents, time, pressure, valves_open.copy(), valves_not_seen.copy())
        # return  # DEBUG
    if not valves_not_seen:
        if agents_in_transit:
            explore(
                agents,
                max(a.time for a in agents_in_transit),
                pressure,
                valves_open,
                valves_not_seen,
            )
        else:
            if not solution or pressure > solution[0]:
                solution = [pressure] + agents


t = time.time()
explore(
    [Agent("AA", 26, []), Agent("AA", 26, [])],
    26,
    0,
    [],
    set(valves_flow),
)
t = (time.time() - t) * 1000

print(solution, ",", t, "ms")
