def mydec(f):
    def wp():
        print("hi111")
        print(f())
    return wp


@mydec
def f():
    print("why")
    return "hello"


f()
d = ("weert", 'sdds', 'dsdsd')
f = iter(d)
print(next(f))

dr = range(10)
print(dr)

if 1 in range(10):
    print("hi its there")

i = 'welcome'

def welcome(i):
    i = i+',welcome to turing'
    return i

welcome('Developers')
print(i)

l = [1,2,3,4]
m = [2,3,9,7,0,1]
n = [1,3]
s = [1,1,1,2,3,3,4,5,5,6,6,6,7,8,8,8,89,11,12,12,12,13,12]

import itertools

# for t in l:
#     for y in m:
#         if t==y:
#             pass
            # print("t==", t)
print(itertools.product(l,m,n,s))

for t,r,a,b in itertools.product(l,m,n,s):
    if t==r and r==a and a==b:
        # pass
        print(t,r,a,b)

l = [1,2,3,4,2,3,4]
filtered_result = list(filter(lambda x: (l.count(x))==1, l))
filtered_result12 = list(filter(lambda x: (l.count(x))>1, l))
print(filtered_result12)
print(filtered_result)

from itertools import permutations
from nltk import ngrams

n = 'ankit is a working i a good company'

ng = ngrams(n.split(),2)
print(ng)
ng1 = [' '.join(x) for x in ng]
print(ng1)
perms =  [' '.join(x) for x in permutations(ng1)]
# print(perms)
