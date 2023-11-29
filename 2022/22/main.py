from recordclass import RecordClass
import re
import sys


class Vec(RecordClass):
    x: int
    y: int
    d: int


SAMPLE = 0

with open("input-sample.txt" if SAMPLE else "input.txt", "r") as f:
    board, cmds = f.read().split("\n\n")
    board = [[c for c in line] for line in board.split("\n")]
    w = max(len(l) for l in board) + 2
    for i in range(len(board)):
        board[i] = [" "] + board[i] + [" " for _ in range(w - len(board[i]) - 1)]
    board.insert(0, [" " for _ in range(w)])
    board.append([" " for _ in range(w)])
    cmds = re.split(r"([RL])", cmds)


def output_board():
    with open("output.txt", "w") as f:
        f.write("\n".join(["".join(l) for l in board]))


dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
dirnames = ["right", "down", "left", "up"]


def print_solution(v: Vec):
    r, c, f = v.y, v.x, v.d
    print(f"row: {r} col: {c} facing: {f}")
    print("Part 1:", 1000 * r + 4 * c + f)


def part1():
    v = Vec(x=board[1].index("."), y=1, d=0)

    for cmd in cmds:
        if cmd == "R":
            v.d = (v.d + 1) % len(dirs)
        elif cmd == "L":
            v.d = (v.d - 1) % len(dirs)
        else:
            for _ in range(int(cmd)):
                x1, y1 = (v.x + dirs[v.d][0]) % len(board[0]), (v.y + dirs[v.d][1]) % len(board)
                c = board[y1][x1]
                while c == " ":  # Wrap around
                    x1, y1 = (x1 + dirs[v.d][0]) % len(board[0]), (y1 + dirs[v.d][1]) % len(board)
                    c = board[y1][x1]
                if c == ".":
                    v.x, v.y = x1, y1

    print_solution(v)


faces = ((-1, 0, 1, -1), (-1, 2, -1, -1), (3, 4, -1, -1), (5, -1, -1, -1), (-1, -1, -1, -1))


def facexy(n):
    for y in range(len(faces)):
        for x in range(len(faces[0])):
            if faces[y][x] == n:
                return x * 50 + 1, y * 50 + 1
    return -1, -1


class Transition(RecordClass):
    f1: int
    d1: int
    y_inv: bool
    xy_flip: bool


def part2():
    xns = {}
    with open("faces.txt", "r") as f:
        """2 right, 1, flip x/y, dir = up"""
        for line in f.readlines():
            t = [i.strip() for i in line.split(",")]
            xns[(int(t[0]), dirnames.index(t[1]))] = Transition(
                int(t[2]),
                dirnames.index(next(i for i in t if i.startswith("dir = ")).split("=")[1].strip()),
                "invert y" in t,
                "flip x/y" in t,
            )

    v = Vec(x=board[1].index("."), y=1, d=0)
    # cmds = ("L", "L", 10)

    board[v.y][v.x] = "X"

    for cmd in cmds:
        if cmd == "R":
            v.d = (v.d + 1) % len(dirs)
        elif cmd == "L":
            v.d = (v.d - 1) % len(dirs)
        else:
            for _ in range(int(cmd)):
                f = faces[(v.y - 1) // 50][(v.x - 1) // 50]
                x1, y1 = (v.x + dirs[v.d][0]) % len(board[0]), (v.y + dirs[v.d][1]) % len(board)
                d1 = v.d
                c1 = board[y1][x1]
                if faces[(y1 - 1) // 50][(x1 - 1) // 50] != f:
                    # We've walked off a face
                    # From old face and direction, figure out transition (face x -> face y)
                    if (f, v.d) in xns:
                        transition = xns[(f, v.d)]
                        d1 = transition.d1
                        # then calculate new x1 and y1
                        dx, dy = (x1 - dirs[v.d][0] - 1) % 50, (y1 - dirs[v.d][1] - 1) % 50
                        if transition.xy_flip:
                            tmp = dy
                            dy = dx
                            dx = tmp
                        elif transition.y_inv:
                            dy = 49 - dy
                        newxy = facexy(transition.f1)
                        x1, y1 = newxy[0] + dx, newxy[1] + dy
                        c1 = board[y1][x1]
                if c1 == "#":
                    break
                print(v.x, v.y)
                v.x, v.y, v.d = x1, y1, d1
                board[v.y][v.x] = "X"
        #if cmd == cmds[6]:
        #    output_board()
        #    sys.exit(0)

    print_solution(v)


# part1()
part2()
