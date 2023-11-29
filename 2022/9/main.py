import math

with open("input.txt", "r") as f:
    cmds = [l.strip().split() for l in f.readlines()]

knots = [(0, 0) for i in range(10)]
visited = set()

dirs = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}

roundaway = lambda v: math.floor(v) if v < 0 else math.ceil(v)

for cmd in cmds:
    for i in range(int(cmd[1])):
        x, y = dirs[cmd[0]]
        knots[0] = (knots[0][0] + x, knots[0][1] + y)
        for i in range(1, len(knots)):
            hx, hy = knots[i - 1]
            tx, ty = knots[i]
            dx, dy = hx - tx, hy - ty
            if abs(dx) < 2 and abs(dy) < 2:
                pass
            elif dx != 0 and dy != 0:
                tx += roundaway(dx / 2)
                ty += roundaway(dy / 2)
            else:
                tx += int(dx / 2)
                ty += int(dy / 2)
            knots[i] = (tx, ty)
        visited.add(knots[-1])

print(len(visited))
