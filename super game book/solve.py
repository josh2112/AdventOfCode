with open("graph.txt", "r") as f:
    data = [line.strip() for line in f.readlines()]

idx = next(i for i, line in enumerate(data) if line.startswith("win"))
win = [int(v) for v in data[idx][4:].split()]
lose = [int(v) for v in data[idx + 1][5:].split()]

graph = dict()
for i, line in enumerate(data[:idx]):
    graph[i] = set([int(v) for v in line.split()])

print(graph)

with open("graph.dot", "w") as f:
    f.write("digraph {\n")
    for k, dests in graph.items():
        for v in dests:
            f.write(f"  {k} -> {v};\n")
    f.write("}\n")
