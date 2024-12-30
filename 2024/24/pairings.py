import itertools

import more_itertools as mi

n = ["z00", "z01", "z02", "z03", "z04", "z05"]
print(list(itertools.combinations(n, 4)))

for combo in itertools.combinations(n, 4):
    print(list(mi.set_partitions(combo, 2, 2, 2)))

"""
abcdef

ab cd ef
ac bd ef
ad bc ef
ae bc df
af bc de
be ac df
bf ac de
ce ab df
de ab cf
df ab ce

[['a', 'b'], ['c', 'd'], ['e', 'f']],
[['a', 'b'], ['d', 'e'], ['c', 'f']],
[['a', 'b'], ['c', 'e'], ['d', 'f']],
[['b', 'c'], ['a', 'd'], ['e', 'f']],
[['a', 'c'], ['b', 'd'], ['e', 'f']],
[['b', 'c'], ['d', 'e'], ['a', 'f']],
[['a', 'c'], ['d', 'e'], ['b', 'f']],
[['b', 'c'], ['a', 'e'], ['d', 'f']],
[['a', 'c'], ['b', 'e'], ['d', 'f']],
[['c', 'd'], ['b', 'e'], ['a', 'f']],
[['c', 'd'], ['a', 'e'], ['b', 'f']],
[['b', 'd'], ['c', 'e'], ['a', 'f']],
[['a', 'd'], ['c', 'e'], ['b', 'f']],
[['b', 'd'], ['a', 'e'], ['c', 'f']],
[['a', 'd'], ['b', 'e'], ['c', 'f']]

'ab', 'ac', 'ad', 'ae', 'af', 'bc', 'bd', 'be', 'bf', 'cd', 'ce', 'cf', 'de', 'df', 'ef'
"""
