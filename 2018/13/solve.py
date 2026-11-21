"""https://adventofcode.com/2018/day/13"""

from dataclasses import dataclass

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
CART_TO_DIR = ">v<^"


@dataclass
class Cart:
    pos: tuple[int, int]
    dir: tuple[int, int]
    next_intx: int = -1  # -1 = left, 0 = center, 1 = right

    def move(self):
        self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])

    def turn(self, d: int):
        # Turns clockwise (d == 1) or counterclockwise (d == -1)
        self.dir = DIRS[(DIRS.index(self.dir) + d) % len(DIRS)]

    def intersect(self):
        # Turns (if next intersection not center) and set next intersection dir
        if self.next_intx:
            self.turn(self.next_intx)
        self.next_intx = self.next_intx + 1 if self.next_intx < 1 else -1


def parse_track(data: list[str]):
    track = [list(row) for row in data]
    carts: list[Cart] = []

    for y, row in enumerate(track):
        for x, c in enumerate(row):
            if c in CART_TO_DIR:
                dir_ = CART_TO_DIR.index(c)
                carts.append(Cart((x, y), DIRS[dir_]))
                track[y][x] = "-" if dir_ in (0, 2) else "|"

    return track, carts


def prob_1(data: list[str]) -> str:
    track, carts = parse_track(data)

    while True:
        # print("---------------")
        # Move carts in y then x order
        for cart in sorted(carts, key=lambda c: (c.pos[1], c.pos[0])):
            # Move, then turn (if we're at a corner or intersection)
            _old = cart.pos
            cart.move()
            # print(_old, "->", cart.pos)
            t = track[cart.pos[1]][cart.pos[0]]
            if t == "+":
                cart.intersect()
            elif t == "/":
                cart.turn(1 if cart.dir[1] else -1)
            elif t == "\\":
                cart.turn(1 if cart.dir[0] else -1)
            elif t == " ":
                raise Exception("Cart off track!")

        if len(set(c.pos for c in carts)) < len(carts):
            seen: set[tuple[int, int]] = set()
            crash = next(c.pos for c in carts if c.pos in seen or seen.add(c.pos))
            return ",".join(map(str, crash))

    return ""


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
