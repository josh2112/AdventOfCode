import itertools

from more_itertools import set_partitions

shit = [
    [["<", "v", "<", "A"], ["v", "<", "<", "A"]],
    [["A"]],
    [[">", "^", "A"]],
    [["A"]],
    [[">", "A"]],
]
# Expected output: <v<AA>^AA>A, v<<AA>^AA>A
# shit = [[[1, 1], [2, 2]], [[3]], [[4, 4], [5, 5]]]
# combos_to_try = (
#    [n for pr in x for n in pr]
#    for combo in combinations(shit, bag_size)
#    for x in set_partitions(combo, bag_size // 2, 2, 2)
# )

print([[c for part in seq for c in part] for seq in itertools.product(*shit)])
