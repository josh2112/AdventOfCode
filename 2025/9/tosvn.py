import sys

with open(sys.argv[1], "r") as f:
    vertices = [tuple(map(int, line.split(","))) for line in f.readlines()]

with open(sys.argv[1] + ".svg", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
    f.write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewbox="0 0 {max(v[0] for v in vertices) + 5} {max(v[1] for v in vertices) + 5}">\n'
    )
    f.write(
        f'\t<polygon points="{" ".join(f"{v[0]},{v[1]}" for v in vertices)}" style="fill:red" />\n'
    )
    f.write("</svg>\n")
