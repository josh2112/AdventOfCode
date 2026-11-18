"""https://adventofcode.com/2018/day/9"""

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


def prob_1(data: list[str]) -> int:
    words = data[0].split(" ")
    num_players, num_rounds = int(words[0]), int(words[6])

    scores = [0 for _ in range(num_players)]

    circle: list[int] = [0]
    cur_idx = 0
    cur_player = -1

    def print_circle():
        print(
            f"[{cur_player + 1 if cur_player != -1 else '-'}] {' '.join(str(c) if i != cur_idx else f'({str(c)})' for i, c in enumerate(circle))}"
        )

    # print_circle()
    for i in range(1, num_rounds + 1):
        cur_player = (cur_player + 1) % num_players

        if not (i % 23):
            cur_idx = (cur_idx - 7) % len(circle)
            scores[cur_player] += i + circle.pop(cur_idx)
            if cur_idx == len(circle):
                cur_idx = 0
            continue

        cur_idx = (cur_idx + 2) % len(circle)
        if cur_idx == 0:
            circle.append(i)
            cur_idx = len(circle) - 1
        else:
            circle.insert(cur_idx, i)

        # print_circle()

    return max(scores)


# The circle gets too big if we do 100x more rounds... find some kind of pattern?
def prob_2(data: list[str]) -> int:
    words = data[0].split(" ")
    num_rounds = int(words[6]) * 100
    return prob_1([" ".join([words[0], "a", "a", "a", "a", "a", str(num_rounds)])])


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
