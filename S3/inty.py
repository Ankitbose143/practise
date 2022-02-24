def func(f):
    def wrapper(*args):
        print("hi")
        k =f(*args)
        return k
    return wrapper

@func
def add(a,b):
    return a+b

print(add(5,6))
# ===============closure
def outer(a):
    def iner(b):
        return a+b
        # print(a+b)
    return iner
asd = outer(13)
print(asd(21))
# asd
print(asd(1))

a = [1,2,3]
d = list(map(lambda x:x**2, a))

# import math

# print(add(5,6))
d = {3: 100, 2: 200, 1: 10}
f = {}
k = 0
for i in sorted (d.keys()) :
     print({i:d[i]},end = " ")
print("keys",sorted(d.keys()))
print("items",sorted(d.items()))
# for t in d:

# for i, j in d.items():
#     if i<k:
#         f[i] = j
#         k = i
# print(d)

A = [1, 2]
B = [-2, 1]
C = [-1, 2]
D = [0, 2]

averages = [((w+ x + y+ z) ==0) for (w, x, y, z) in zip(A, B, C,D)]
print("avg", averages)
# A[0] + B[0] + C[0] + D[1] = 1 + (-2) + (-1) + (2) = 0
# O(n*2)
for a in A:
    for b in B:
        for c in C:
            for d in D:
                if a+b+c+d ==0:
                    print(a,b,c,d)
# []
# d = lambda x,y,z,w:w+y+x+z ==0
# from itertools import permutations

# e = permutations(a,2)
# print(e)

# f = []
# 0,1,1,2,3,5,7
# bob, bib [::-1]
a1 = ['bob', 'bib']
r = 0
for t in a1:
    g = 0
    for ty in range(len(t), 0):
        if t[ty] != t[g]:
            r = 1
    if r==1:
        print("it is not a anagram")
    
# 1, 1, 2, 3, 5, 8, 13, 21
# count(20)
# def func(n):
#  for t in range(g):
#     if n == 0
#          return 1
#     else
        # return n+func(n)

import json

# with open('assa.json', 'rb') as f:
#     data = json.load(f)
# g = json.load(df)
# d = json.dump(data, f)

#data =  [list of dataframes] [{0:{}}, {1}]
x = """{
    "Name": "Jennifer Smith",
    "Contact Number": 7867567898,
    "Email": "jen123@gmail.com",
    "Hobbies":["Reading", "Sketching", "Horse Riding"]
    }"""

y = json.loads(x)
  
# the result is a Python dictionary:
print(y, type(y))
res = json.load(x)
# print(res, type(res))




