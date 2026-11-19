"""https://adventofcode.com/2018/day/10"""

import os
import re

from PIL import Image

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1

pattern = re.compile("^position=<\\s?(-?\\d+),\\s+(-?\\d+)> velocity=<\\s?(-?\\d+),\\s+(-?\\d+)>$", flags=re.MULTILINE)

img_cnt = 0


def draw(pts: list[list[int]]):
    global img_cnt
    img_cnt += 1

    xmin, ymin = min(pt[0] for pt in pts), min(pt[1] for pt in pts)
    normalized = [(pt[0] - xmin, pt[1] - ymin) for pt in pts]
    w, h = max(pt[0] for pt in normalized) + 1, max(pt[1] for pt in normalized) + 1

    img = Image.new("L", (w, h), 0)
    px = img.load()
    assert px

    for pt in normalized:
        try:
            px[pt[0], pt[1]] = 255
        except IndexError:
            print(pt[0], pt[1], w, h)

    os.makedirs("cache", exist_ok=True)
    img.save(f"cache/img{img_cnt}.png")


def prob_1(data: list[str]) -> int:
    pts = [list(map(int, line)) for line in pattern.findall("\n".join(data))]

    for _ in range(100):
        for pt in pts:
            pt[0] += pt[2]
            pt[1] += pt[3]

        # Find ymax and ymin. Check every row in between for a point.
        ymin, ymax = min(pt[1] for pt in pts), max(pt[1] for pt in pts)
        if all(any(pt[1] == y for pt in pts) for y in range(ymin + 1, ymax)):
            draw(pts)

    global img_cnt
    return img_cnt


def prob_2(data: list[str]) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
