"""https://adventofcode.com/2018/day/13"""

from dataclasses import dataclass, field

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
CART_TO_DIR = ">v<^"


def track_to_str(track: list[list[str]]) -> str:
    return "\n" + "\n".join("".join(r) for r in track)


@dataclass
class Cart:
    pos: tuple[int, int]
    dir: tuple[int, int]
    next_intx: int = -1  # -1 = left, 0 = center, 1 = right
    crashed = False

    history: list[tuple[int, int]] = field(default_factory=lambda: [])

    def move(self):
        self.history.append(self.pos)
        self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])

    def turn(self, d: int):
        # Turns clockwise (d == 1) or counterclockwise (d == -1)
        self.dir = DIRS[(DIRS.index(self.dir) + d) % len(DIRS)]

    def intersect(self):
        # Turns (if next intersection not center) and set next intersection dir
        if self.next_intx:
            self.turn(self.next_intx)
        self.next_intx = self.next_intx + 1 if self.next_intx < 1 else -1


def run(data: list[str], clear_crashes: bool = False):
    track = [list(row) for row in data]
    carts: list[Cart] = []

    for y, row in enumerate(track):
        for x, c in enumerate(row):
            if c in CART_TO_DIR:
                dir_ = CART_TO_DIR.index(c)
                carts.append(Cart((x, y), DIRS[dir_]))
                track[y][x] = "-" if dir_ in (0, 2) else "|"

    while True:
        # Move, check for crash, then turn (if we're at a corner or intersection)
        for cart in sorted(filter(lambda c: not c.crashed, carts), key=lambda c: (c.pos[1], c.pos[0])):
            if cart.crashed:
                continue

            cart.move()

            # Did we hit another cart?
            crashes = [c for c in carts if c != cart and c.pos == cart.pos and not c.crashed]
            if crashes:
                if not clear_crashes:
                    return ",".join(map(str, cart.pos))
                else:
                    for c in [*crashes, cart]:
                        c.crashed = True
                    continue

            t = track[cart.pos[1]][cart.pos[0]]
            if t == "+":
                cart.intersect()
            elif t == "/":
                cart.turn(1 if cart.dir[1] else -1)
            elif t == "\\":
                cart.turn(1 if cart.dir[0] else -1)

        uncrashed = [c for c in carts if not c.crashed]
        if len(uncrashed) == 1:
            return ",".join(map(str, uncrashed[0].pos))


if __name__ == "__main__":
    solve(__file__, PART, INPUT, lambda d: run(d), lambda d: run(d, True), no_strip_input=True)
