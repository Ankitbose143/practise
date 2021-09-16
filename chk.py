def func(b=20):
    print("==",b)
    # b =100
    print(b)

a = 10
s = 'a'
func(a)
print(a)
from itertools import permutations
from nltk import ngrams

n = 'ankit is a working i a good company'

ng = ngrams(n.split(),2)
print(ng)
ng1 = [' '.join(x) for x in ng]
print(ng1)
perms =  [' '.join(x) for x in permutations(ng1)]
# print(perms)