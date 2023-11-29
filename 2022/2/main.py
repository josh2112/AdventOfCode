with open("input.txt", "r") as f:
    rounds = [l.strip().split() for l in f.readlines()]

score = 0

ROCK, PAPER, SCISSORS = "A", "B", "C"
LOSE, DRAW, WIN = "X", "Y", "Z"

guess = {
    WIN: {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK},
    LOSE: {ROCK: SCISSORS, SCISSORS: PAPER, PAPER: ROCK},
    DRAW: {ROCK: ROCK, PAPER: PAPER, SCISSORS: SCISSORS},
}

for r in rounds:
    g = (r[0], guess[r[1]][r[0]])
    score += ord(g[1]) - ord("A") + 1
    if g[0] == g[1]:
        score += 3
    elif g == (SCISSORS, ROCK) or g == (PAPER, SCISSORS) or g == (ROCK, PAPER):
        score += 6

print(score)
