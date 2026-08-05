"""https://adventofcode.com/2018/day/5"""

from aoclib.runner import solve

# Input file path (or pass with -i <path>)
INPUT = "input.txt"

# Part to solve, 1 or 2 (or pass with -p <1|2|all>)
PART = 1


# NEXT STEP: Create random polys of increasing size,
# stop and print when we find one where solve.react and
# solve_alt.react don't match!
def react(polymer: str):
    d, i = [ord(c) for c in polymer], 0
    i, j, total, k = 0, 0, 0, 1

    while k < len(d):
        print(i, j, k)
        if abs(d[j] - d[k]) == 32:
            print("  ", i, j, k)
            skip = False
            while k < len(d) and abs(d[j] - d[k]) == 32:
                if j > i:
                    j -= 1
                    k += 1
                    print("  match, widening to ", j, k)
                else:
                    print("  hit front, skipping ahead...")
                    j = k + 1
                    k = j + 1
                    i = j
                    skip = True
                    break
            if not skip:
                print("no match, increasing total and skipping ahead...")
                total += j - i + 1
                i = j = k
                k += 1
        else:
            j += 1
            k += 1

    return total + len(d) - i


def prob_1(data: list[str]) -> int:
    return react(data[0])


def prob_2(data: list[str]) -> int:
    min_len = len(data[0])
    for i in range(ord("a"), ord("z") + 1):
        polymer = [c for c in data[0] if ord(c) not in (i, i - 32)]
        length = react(polymer)
        print(f"{chr(i)}: count={len(data[0]) - len(polymer)}, length={length}")
        min_len = min(min_len, length)
    return min_len


if __name__ == "__main__":
    solve(__file__, PART, INPUT, prob_1, prob_2)
