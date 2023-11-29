with open("input.txt", "r") as f:
    c = f.read()


def find_n_distinct(n):
    for i in range(len(c) - n):
        if len(set(c[i : i + n])) == n:
            print(i + n)
            return


part1 = lambda: find_n_distinct(4)
part2 = lambda: find_n_distinct(14)

part1()
part2()
