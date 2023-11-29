USE_SAMPLE = 0

with open("input-sample.txt" if USE_SAMPLE else "input.txt", "r") as f:
    jets = [-1 if c == "<" else 1 for c in f.read().strip()]

num_rocks = 1000000000000

rocks = (
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]],
)

surface_rels = []
cycle, cycle_start, cycle_repeat = [], 0, 0

roomwidth = 7
room = [0 for _ in range(roomwidth * 3)] + [1 for _ in range(roomwidth)]
highest_terrain = 3
total_height = 0

glyph = ".", "#", "@"


def print_room(room, rock, rx, ry):
    ghost = makeghost(rock, rx) if rock else None
    for row in range(len(room) // roomwidth):
        start = row * roomwidth
        line = room[start : start + roomwidth]
        if ghost and row >= ry and row < ry + len(rock):
            line = [
                2 if b else (1 if a else 0)
                for a, b in zip(line, ghost[(row - ry) * roomwidth : (row - ry) * roomwidth + roomwidth])
            ]
        print(f"|{''.join(glyph[b] for b in line)}|")


ij = 0


def is_overlap(ghost, room, ry):
    start = ry * roomwidth
    return next((a + b for a, b in zip(ghost, room[start : start + len(ghost)]) if a + b > 1), None) != None


def makeghost(rock, rx):
    ghost = [0 for _ in range(roomwidth * len(rock))]
    for row in range(len(rock)):
        start = row * roomwidth + rx
        ghost[start : start + len(rock[row])] = rock[row]
    return ghost


def simulate(start, count):
    global highest_terrain, room, total_height, ij, cycle, cycle_start, cycle_repeat, num_rocks

    for ir in range(start, count):
        # print("-- NEW ROCK --")
        rock = rocks[ir % len(rocks)]
        rx, ry = 2, 0

        # Add enough rows to hold this rock
        rows_to_add = len(rock) + 3 - highest_terrain
        if rows_to_add > 0:
            room = [0 for _ in range(roomwidth * rows_to_add)] + room
            highest_terrain += rows_to_add
        else:
            ry += -rows_to_add

        while True:
            # print_room(room, rock, rx, ry)
            # Apply jet
            jet = jets[ij % len(jets)]
            ij += 1
            # Can we apply the jet without hitting the wall?
            will_hit_wall = (jet == -1 and rx == 0) or (jet == 1 and rx + len(rock[0]) == roomwidth)
            # Can we apply the jet without hitting the terrain? ('Ghost' the piece left or right, then
            # collision-check each row)
            ghost = makeghost(rock, rx + jet)
            if not will_hit_wall and not is_overlap(ghost, room, ry):
                # print("Applying jet", jet)
                rx += jet
            else:
                pass  # print(f"Can't apply jet of {jet}, will hit wall or terrain")
            # Can we apply the fall without hitting the terrain? ('Ghost' the piece, then
            # collision-check each row)
            ghost = makeghost(rock, rx)
            if not is_overlap(ghost, room, ry + 1):
                # print("Applying fall")
                ry += 1
            else:
                # print("Rock impacted terrain")
                # print_room(room, rock, rx, ry)
                # print("HEIGHT GAIN:", highest_terrain - ry)
                ghost = makeghost(rock, rx)
                start = ry * roomwidth
                room[start : start + len(ghost)] = [a | b for a, b in zip(ghost, room[start : start + len(ghost)])]
                break

        total_height += max(0, highest_terrain - ry)
        highest_terrain = min(highest_terrain, ry)

        # if ir % len(jets) == len(jets) - 1:
        surface = [0 for _ in range(roomwidth)]
        for y in range(highest_terrain, len(room) // roomwidth):
            for x in range(roomwidth):
                if not surface[x] and room[y * roomwidth + x]:
                    surface[x] = y
            if next((i for i in surface if i == 0), None) == None:
                break

        # Cut off the room below the lowest surface
        room = room[: (max(surface) + 1) * roomwidth]

        if not cycle:
            surface_rel = [i - min(surface) for i in surface] + [ir % len(rocks), ij % len(jets), total_height]
            if surface_rel[:-1] in [c[:-1] for c in surface_rels]:
                cycle = surface_rel
                cycle_start = [c[:-1] for c in surface_rels].index(cycle[:-1])
                cycle_repeat = ir - cycle_start
                return
            else:
                surface_rels.append(surface_rel)
        # else:


# Find cycle
simulate(0, num_rocks)

print("Found cycle", cycle[:-3], "ir =", cycle[-2])
print("Repeats every", cycle_repeat, "rocks")

h_start = surface_rels[cycle_start][-1]
h_inc = cycle[-1] - h_start
print("height at first instance =", h_start, " increases by", h_inc, "every cycle")
rpt_count = (num_rocks - cycle_start) // cycle_repeat

ir = cycle_start + cycle_repeat * rpt_count
ij = cycle[-2]
total_height = h_start + rpt_count * h_inc
print("Configuring board for ir =", ir, ", total height =", total_height)

ys = cycle[:roomwidth]
room = [0 for _ in range(roomwidth * (max(ys) + 1))]
for x in range(len(ys)):
    room[ys[x] * roomwidth + x] = 1
highest_terrain = 0
# TODO: What if just capturing the highest block in each row is not enough?
# i.e. it might leave a hole for future blocks to slide into that wasn't
# there in the cycle
print_room(room, None, 0, 0)

simulate(ir + 1, num_rocks)

print(total_height)
# print_room(room, None, 0, 0)
