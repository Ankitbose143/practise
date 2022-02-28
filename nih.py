
# l.pop()
# print(l)

class stack:
    def __init__(self, a):
        self.a = a
        # print(self.a)

    def push(self, b):
        self.b = b
        # self.a= a.insert(-1,b)# insert(0,b)
        self.a= a.append(b)

    def pop(self):
        # self.g = g#remove(0)
        b = self.a.pop(-1)
        return b
        # self.a= a.pop()

l = [1,2,3,4]
# l = [1,2,3,4,5]
# l = [2,3,4,5]
a = stack(l)
# print(l[::-1])
# s = l[-1]
# a = l
# a.pop()
# print(a)
from collections import Counter

c = Counter(l)
print(c)
# print(a.pop())
