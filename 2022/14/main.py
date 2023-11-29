import pygame
import numpy as np

C_EMPTY = (0, 0, 0)
C_ROCK = (128, 128, 128)
C_SAND_FALLING = (255, 0, 0)
C_SAND_REST = (225, 198, 128)

delta = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

parse_points = lambda pr: tuple(int(v.strip()) for v in pr.split(","))

with open("input.txt", "r") as f:
    paths = [[parse_points(pt) for pt in line.split("->")] for line in f.readlines()]

allpoints = [pt for path in paths for pt in path]
w, h = max(pt[0] for pt in allpoints) + 1, max(pt[1] for pt in allpoints) + 3

w *= 2  # fuck it

arr = np.zeros((w, h, 3))

for x in range(w):
    arr[x, h - 1] = C_ROCK

for path in paths:
    for line in zip(path, path[1:]):
        arr[line[1][0], line[1][1]] = C_ROCK
        dx, dy = delta(line[1][0] - line[0][0]), delta(line[1][1] - line[0][1])
        x, y = line[0][0], line[0][1]
        while x != line[1][0] or y != line[1][1]:
            arr[x, y] = C_ROCK
            x += dx
            y += dy

pt_grain = None
grain_count = 0

sim_speed = 5000
frame_ct = 0

pygame.init()
display = pygame.display.set_mode((w * 3, h * 3))

running = True


def move_grain(x, y):
    global pt_grain
    arr[pt_grain[0], pt_grain[1]] = C_EMPTY
    pt_grain = (pt_grain[0] + x, pt_grain[1] + y)
    arr[pt_grain[0], pt_grain[1]] = C_SAND_FALLING


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not pt_grain:
        if tuple(arr[500, 0]) == C_EMPTY:
            pt_grain = (500, 0)
        else:
            print(f"Done, grain count {grain_count}")
            running = False
    elif tuple(arr[pt_grain[0], pt_grain[1] + 1]) == C_EMPTY:
        move_grain(0, 1)
    elif tuple(arr[pt_grain[0] - 1, pt_grain[1] + 1]) == C_EMPTY:
        move_grain(-1, 1)
    elif tuple(arr[pt_grain[0] + 1, pt_grain[1] + 1]) == C_EMPTY:
        move_grain(1, 1)
    else:
        arr[pt_grain[0], pt_grain[1]] = C_SAND_REST
        grain_count += 1
        pt_grain = None

    frame_ct += 1
    if frame_ct == sim_speed:
        frame_ct = 0

        surf = pygame.surfarray.make_surface(arr.astype("uint8"))
        surf = pygame.transform.scale(surf, display.get_size())
        display.blit(surf, (0, 0))

        pygame.display.update()

print(f"Done, grain count {grain_count}")
