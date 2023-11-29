import re
import itertools

SAMPLE = 1

ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3

with open("input-sample.txt" if SAMPLE else "input.txt", "r") as f:
    # [0] bp num
    # [1] ore robot cost (ore)
    # [2] clay robot cost (ore)
    # [3,4] obsidian robot cost (ore,clay)
    # [5,6] geode robot cost (ore,obsidian)
    blueprints = [
        [int(v) for v in line]
        for line in re.findall(
            r"Blueprint (\d+):\s+Each ore robot costs (\d+) ore\.\s+Each clay robot costs (\d+) ore\.\s+Each obsidian robot costs (\d+) ore and (\d+) clay\.\s+Each geode robot costs (\d+) ore and (\d+) obsidian\.",
            f.read(),
        )
    ]


def run(b, bot_limits, t):
    bots = [1, 0, 0, 0]
    res = [0, 0, 0, 0]

    for t in range(t):
        # Can we build anything?
        existing_bots = bots.copy()
        if bots[GEODE] < bot_limits[GEODE] and res[ORE] >= b[5] and res[OBSIDIAN] >= b[6]:
            res[ORE] -= b[5]
            res[OBSIDIAN] -= b[6]
            bots[GEODE] += 1
        if bots[OBSIDIAN] < bot_limits[OBSIDIAN] and res[ORE] >= b[3] and res[CLAY] >= b[4]:
            res[ORE] -= b[3]
            res[CLAY] -= b[4]
            bots[OBSIDIAN] += 1
        if bots[CLAY] < bot_limits[CLAY] and res[ORE] >= b[2]:
            res[ORE] -= b[2]
            bots[CLAY] += 1
        if bots[ORE] < bot_limits[ORE] and res[ORE] >= b[1]:
            res[ORE] -= b[1]
            bots[ORE] += 1
        # Can we collect anything?
        for i in range(len(res)):
            res[i] += existing_bots[i]

    return bots, res


best = {b[0]: -1 for b in blueprints}

for b in blueprints:
    for bot_limits in [(1, 4, 2, 2)]:  # itertools.product((1, 2, 3, 4, 5), repeat=4):
        bots, res = run(b, bot_limits, 24)
        if best[b[0]] < 0 or res[OBSIDIAN] > best[b[0]]:
            best[b[0]] = res[OBSIDIAN]
            print("Blueprint", b[0])
            print(" Bots:", bots, " Resources:", res)
