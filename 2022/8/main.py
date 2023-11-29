import numpy
import functools

with open("input.txt", "r") as f:
    trees = numpy.array([[int(t) for t in l.strip()] for l in f.readlines()])


def part1():
    def treevis(trees, vis):
        for r in range(len(trees)):
            m = -1
            for c in range(len(trees[r])):
                if trees[r][c] > m:
                    vis[r][c] = 1
                    m = trees[r][c]

    vis = numpy.zeros(trees.shape)

    treevis(trees, vis)
    treevis(numpy.fliplr(trees), numpy.fliplr(vis))
    treevis(numpy.transpose(trees), numpy.transpose(vis))
    treevis(numpy.fliplr(numpy.transpose(trees)), numpy.fliplr(numpy.transpose(vis)))

    print(numpy.count_nonzero(vis))


def part2():
    scores = numpy.zeros(trees.shape)

    def scenic_score(r, c, trees):
        def score_line(line):
            score = 0
            for t in line[1:]:
                score += 1
                if t >= line[0]:
                    break
            return score

        scores[r][c] = numpy.multiply.reduce(
            [
                score_line(l)
                for l in (trees[r, c:], numpy.flip(trees[r, : c + 1]), trees[r:, c], numpy.flip(trees[: r + 1, c]))
            ]
        )

    for r in range(len(trees)):
        for c in range(len(trees[r])):
            scenic_score(r, c, trees)

    print(scores)
    print("Max:", numpy.max(scores))


# part1()
part2()
