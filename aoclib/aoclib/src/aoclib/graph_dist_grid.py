from dataclasses import dataclass
from sys import maxsize


@dataclass
class Node:
    name: str
    neighbors: "list[Node]"


def dist_graph(nodes: list[Node]):
    """Returns a grid of minimum distance between every pair of nodes"""
    dist = {n: {n: maxsize for n in nodes} for n in nodes}
    for n in nodes:
        dist[n][n] = 0
        for n1 in n.neighbors:
            dist[n][n1] = 1

    for n in nodes:
        for i in nodes:
            for j in nodes:
                dist[i][j] = min(dist[i][j], dist[i][n] + dist[n][j])

    return dist
