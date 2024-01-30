from __future__ import annotations

import itertools
import operator


sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
# print(list(itertools.accumulate(sample)))
# print(list(itertools.accumulate(sample, min)))
# print(list(itertools.accumulate(sample, max)))
# print(list(itertools.accumulate(sample, operator.mul)))

# print(list(enumerate('albatroz', start=7)))
# print(list(map(operator.mul, range(11), range(11))))
# print(list(map(lambda a, b: (a, b), range(11), [2, 4, 8])))
# print(list(enumerate('albatroz', 1)))
# print(list(itertools.starmap(operator.mul, enumerate('albatroz', 1))))

print(list(itertools.starmap(lambda n, t: t/n,  enumerate(itertools.accumulate(sample), 1))))