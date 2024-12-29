from collections import defaultdict
from dataclasses import dataclass


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


template = """graph g {
  rankdir="LR";

  node [shape=circle];

%EDGES%

%NODES%
  
}"""


@dataclass
class Wire:
    name: str
    value: int


@dataclass
class Gate:
    i1: Wire
    i2: Wire
    op: str
    out: Wire


with open("input.txt", "r") as f:
    data = [ln.strip() for ln in f.readlines()]

split = data.index("")
wires = keydefaultdict(
    lambda w: Wire(w, -1),
    {w: Wire(w, int(v)) for w, v in [line.split(": ") for line in data[:split]]},
)
gates = [
    Gate(wires[i1], wires[i2], op, wires[out])
    for i1, op, i2, _, out in [line.split() for line in data[split + 1 :]]
]

edges, nodes = [], []

for i, g in enumerate(gates):
    edges += [
        f"  {g.i1.name} -- n{i};",
        f"  {g.i2.name} -- n{i};",
        f"  n{i} -- {g.out.name}",
    ]
    nodes.append(f"  n{i} [label={g.op},shape=box];")

with open("input.txt.graphviz", "w") as f:
    f.write(
        template.replace("%EDGES%", "\n".join(edges)).replace(
            "%NODES%", "\n".join(nodes)
        )
    )
