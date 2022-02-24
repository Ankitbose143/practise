class A:
    def __init__(addr,a,b):
        addr.a = a
        addr.b = b
        # self.a = 13
        # print(self.a)

    def sum(self,a,b, c= None):
        s = self.a+b+c
        return s

d = A(10,12)
print(d.sum(3,4,5))
# print(d.sum(3,5))

import copy
f = [1,2,[3,5],4]
# s = f.copy()
s = copy.copy(f)
t = copy.deepcopy(f)
print(f,s,t)
s[2][0] = 4
# f.append(5)
print(f,s,t)