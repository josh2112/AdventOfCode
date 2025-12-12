"""https://adventofcode.com/2025/day/11"""

from math import prod

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def prob_1(data: list[str]) -> int:
    nodes = {line.split(":")[0]: line.split()[1:] for line in data}

    def hop(n: str):
        return 1 if n == "out" else sum(hop(c) for c in nodes[n])

    return hop("you")


def count_routes(nodes: dict[str, list[str]], start: str, goal: str) -> int:
    # Since this is such a heavily-connected graph we end up with lots of duplicate states in the queue. Instead of
    # adding repeat states, just increment a count of the number of times we've seen it. Current count will get passed
    # on to each new state.

    q = [(start, 0, 1)]  # (node,hops,count)

    num_routes = 0

    while q:
        node, hops, count = q.pop(0)

        if node == goal:
            num_routes += count
            continue

        hops += 1

        for n in nodes[node]:
            # Look for matching state (node,hops) and increment the count
            if i := next(
                (i for i, s in enumerate(q) if (s[0], s[1]) == (n, hops)),
                None,
            ):
                q[i] = (n, hops, q[i][2] + count)
            else:
                q.append((n, hops, count))

    return num_routes


def prob_2(data: list[str]) -> int:
    nodes = {line.split(":")[0]: line.split()[1:] for line in data} | {"out": []}

    # Count possible routes between each subroute (fft->dac, etc.) that we care about and multiply them together
    # so we don't waste time checking routes that skip important nodes

    # We know fft comes before dac (inspecting the input graph), but I imagine that's not guaranteed...
    # so try it both ways

    return sum(
        prod(count_routes(nodes, a, b) for a, b in zip(p, p[1:]))
        for p in (("svr", "dac", "fft", "out"), ("svr", "fft", "dac", "out"))
    )


def main() -> float:
    return solve(__file__, PART, INPUT, prob_1, prob_2)


if __name__ == "__main__":
    main()
