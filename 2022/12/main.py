import numpy

FORREAL = 1
PART = 2


def find(ltr):
    p = numpy.where(rows == ltr)
    return p[0][0], p[1][0]


with open("input.txt" if FORREAL else "input-sample.txt", "r") as f:
    rows = numpy.array([list(l.strip()) for l in f.readlines()])


def part1():
    start, end = find("S"), find("E")
    rows[start] = "a"
    rows[end] = "z"

    dist = numpy.full(rows.shape, sys.maxsize)
    dist[start] = 0
    prev = numpy.full(rows.shape, None)
    q = [(x, y) for x in range(len(rows)) for y in range(len(rows[0]))]

    while len(q):
        u, mind = q[0], dist[q[0]]
        for v in q:
            if dist[v] < mind:
                u = v
                mind = dist[v]
        q.remove(u)

        adjacent = [(u[0] + d[0], u[1] + d[1]) for d in ((-1, 0), (1, 0), (0, -1), (0, 1))]
        for v in [n for n in adjacent if n in q and ord(rows[n]) - ord(rows[u]) < 2]:
            if dist[u] + 1 < dist[v]:
                dist[v] = dist[u] + 1
                prev[v] = u

    print(dist)
    print(dist[end])


def part2():
    start, end = find("E"), find("S")
    rows[end] = "a"
    rows[start] = "z"

    INTMAX = len(rows) * len(rows[0]) * 2

    dist = numpy.full(rows.shape, INTMAX)
    dist[start] = 0
    prev = numpy.full(rows.shape, None)
    q = [(x, y) for x in range(len(rows)) for y in range(len(rows[0]))]

    while len(q):
        u, dmin = q[0], dist[q[0]]
        for v in q:
            if dist[v] < dmin:
                u = v
                dmin = dist[v]
        q.remove(u)

        adjacent = [(u[0] + d[0], u[1] + d[1]) for d in ((-1, 0), (1, 0), (0, -1), (0, 1))]
        for v in [n for n in adjacent if n in q and ord(rows[u]) - ord(rows[n]) < 2]:
            if dist[u] + 1 < dist[v]:
                dist[v] = dist[u] + 1
                prev[v] = u

    print(dist)
    dmin = numpy.max(dist)
    besta = None
    for v in ((x, y) for x in range(len(rows)) for y in range(len(rows[0])) if rows[x][y] == "a"):
        if dist[v] < dmin:
            besta = v
            dmin = dist[v]

    print(besta, dmin)


part1() if PART == 1 else part2()
