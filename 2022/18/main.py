SAMPLE = 0

with open("input-sample.txt" if SAMPLE else "input.txt", "r") as f:
    cubes = [[int(n) for n in l.strip().split(",")] for l in f.readlines()]

xmin, ymin, zmin = tuple(min(c[i] for c in cubes) for i in range(3))
xmax, ymax, zmax = tuple(max(c[i] for c in cubes) for i in range(3))


def count_edges(arr):
    return sum(2 if b - a > 1 else 0 for a, b in zip(arr, arr[1:])) + 2 if len(arr) else 0


def calc_surface_area(cubes):
    edges = 0

    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            edges += count_edges(sorted(c[2] for c in cubes if c[0] == x and c[1] == y))

    for x in range(xmin, xmax + 1):
        for z in range(zmin, zmax + 1):
            edges += count_edges(sorted(c[1] for c in cubes if c[0] == x and c[2] == z))

    for y in range(ymin, ymax + 1):
        for z in range(zmin, zmax + 1):
            edges += count_edges(sorted(c[0] for c in cubes if c[1] == y and c[2] == z))

    return edges


edges = calc_surface_area(cubes)
print("Part 1:", edges)

d = {x: {y: {z: 0 for z in range(zmin, zmax + 1)} for y in range(ymin, ymax + 1)} for x in range(xmin, xmax + 1)}
for c in cubes:
    d[c[0]][c[1]][c[2]] = 1


def empty_boundaries():
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            if not d[x][y][zmin]:
                yield x, y, zmin
            if not d[x][y][zmax]:
                yield x, y, xmax

    for x in range(xmin, xmax + 1):
        for z in range(zmin, zmax + 1):
            if not d[x][ymin][z]:
                yield x, ymin, z
            if not d[x][ymax][z]:
                yield x, ymax, z

    for y in range(ymin, ymax + 1):
        for z in range(zmin, zmax + 1):
            if not d[xmin][y][z]:
                yield xmin, y, z
            if not d[xmax][y][z]:
                yield xmax, y, z


# Add all empty outer cubes to queue
# While queue is not empty:
#   Remove first item
#   If 0, set to 1 and add the 4 surrounding to cube
q = list(empty_boundaries())

while q:
    x, y, z = q[0]
    del q[0]
    if not d[x][y][z]:
        d[x][y][z] = 1
        for x, y, z in ((x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)):
            if x in range(xmin, xmax + 1) and y in range(ymin, ymax + 1) and z in range(zmin, zmax + 1):
                if not d[x][y][z]:
                    q.append((x, y, z))

interior = []

for x, dx in d.items():
    for y, dy in dx.items():
        for z, v in dy.items():
            if not v:
                interior.append((x, y, z))

interior_edges = calc_surface_area(interior)

print("Part 2:", edges - interior_edges)
