import sys


def to_graphviz(src: str):
    with open(src, "r") as f:
        nodes = {line.split(":")[0]: line.split()[1:] for line in f.readlines()}

    with open(src + ".dot", "w") as f:
        f.write("digraph {\nnode [style=filled, fillcolor=white];\n")
        for n in nodes:
            for c in nodes[n]:
                f.write(f"{n} -> {c};\n")
        f.write("you [fillcolor=aqua];\n")
        f.write("fft [fillcolor=chartreuse];\n")
        f.write("dac [fillcolor=hotpink];\n")
        f.write("}\n")


if __name__ == "__main__":
    to_graphviz(sys.argv[1])
