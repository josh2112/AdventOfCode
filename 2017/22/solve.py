"""https://adventofcode.com/2017/day/22"""

from aoclib.runner import solve

# Input file path (default is "input.txt")
INPUT = "input.txt"

# Part to solve, 1 or 2
PART = 1

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def parse(data: list[str]):
    w, h = len(data[0]), len(data)
    return (
        w,
        h,
        [
            (x - w // 2, y - h // 2)
            for y in range(h)
            for x in range(w)
            if data[y][x] == "#"
        ],
    )


def run(data: list[str], rounds: int, part2: bool = False) -> int:
    w, h, inf = parse(data)
    flg, wkd = [], []
    p, d = (0, 0), 0

    def dirch_pt2(p_inf, p_wkd, p_flg):
        if p_inf:
            return 1
        elif p_wkd:
            return 0
        elif p_flg:
            return 2
        else:
            return -1

    def recat_pt1(p_inf):
        if p_inf:
            inf.remove(p)
        else:
            inf.append(p)

    def recat_pt2(p_inf, p_wkd, p_flg):
        if p_inf:
            inf.remove(p)
            flg.append(p)
        elif p_wkd:
            wkd.remove(p)
            inf.append(p)
        elif p_flg:
            flg.remove(p)
        else:
            wkd.append(p)

    num_rounds_infection = 0

    for _ in range(rounds):
        p_inf = p in inf
        if part2:
            p_wkd = p in wkd
            p_flg = p in flg
        dd = (1 if p_inf else -1) if not part2 else dirch_pt2(p_inf, p_wkd, p_flg)
        d = (d + dd) % len(DIRS)

        recat_pt2(p_inf, p_wkd, p_flg) if part2 else recat_pt1(p_inf)

        if (part2 and p_wkd) or (not part2 and not p_inf):
            num_rounds_infection += 1

        p = (p[0] + DIRS[d][0], p[1] + DIRS[d][1])

        # print(f"Round {_ + 1}:\n{printgrid(p, inf, flg, wkd)}")

    return num_rounds_infection


def prob_1(data: list[str]) -> int:
    w, h, inf = parse(data)
    p, d = (0, 0), 0

    num_rounds_infection = 0

    for _ in range(10000):
        p_inf = p in inf
        d = (d + (1 if p_inf else -1)) % len(DIRS)

        if p_inf:
            inf.remove(p)
        else:
            inf.append(p)
            num_rounds_infection += 1

        p = (p[0] + DIRS[d][0], p[1] + DIRS[d][1])

    return num_rounds_infection


def prob_2(data: list[str]) -> int:
    w, h, inf = parse(data)
    flg, wkd = [], []
    p, d = (0, 0), 0

    num_rounds_infection = 0

    for _ in range(100_000):
        dd = -1
        if p_inf := p in inf:
            dd = 1
        elif p_wkd := p in wkd:
            dd = 0
        elif p_flg := p in flg:
            dd = 2
        d = (d + dd) % len(DIRS)

        if p_inf:
            inf.remove(p)
            flg.append(p)
        elif p_wkd:
            wkd.remove(p)
            inf.append(p)
            num_rounds_infection += 1
        elif p_flg:
            flg.remove(p)
        else:
            wkd.append(p)

        p = (p[0] + DIRS[d][0], p[1] + DIRS[d][1])

    return num_rounds_infection


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
