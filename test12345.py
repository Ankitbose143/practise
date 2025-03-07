#list of integers
#search element in list using binary search
l = [1,2,23,4,5]
l = sorted(l)#[1,2,4,5,23]
# 0th element
# 4< # l = 0,
def arr1(arr,l,r,x):
    # try:
    if r>=l:
        mid = int((l+r)/2)
        # print("mid",mid, x)
        if arr[mid] == x:
            # print(arr[mid],x, mid)
            return arr[mid]
        elif arr[mid] <x:
            print("less",arr[mid],x, mid)
            return arr1(arr, mid+1,r ,x)
        elif arr[mid] >x:
            print("greater",arr[mid],x, mid)
            return arr1(arr, l,mid-1,x)
    else:
        print("Not found")
    # except Exception as e:
        # print("Not found", x, str(e))

print(l)
print(arr1(l,0,len(l),15))

# palindrome
# l == l[::-1]
# t = 'maam'
# k = 0
# for i in range(len(t), 0,-1):
#     if t[k] == t[i]
#       k+=1

my_frozen_set = frozenset([1, 2, 3])
print(my_frozen_set, type(my_frozen_set))


class addi:
    def addi(self,a,b):
        return a+b

class addit(addi):
    def addi(self,*args):
        for i in args:
            print(i)
        return sum(args)

ob = addi()
print("sum",ob.addi(5,6))

ob1 = addit()
print("sum",ob1.addi(5,6,4,5))

l = [3,4,[5],[6,7]]
from itertools import chain

from collections import deque
dq = deque(l)
print("df1",dq)
dq.append(5)   # Adds 5 to the right end
dq.appendleft(0) 
print("df2",dq)
# d.push(5)
print("l", l)
h = list(chain(*l))
print("h111111", h)
# print(list(chain.from_iterable(l)))
l = [[x] if not isinstance(x, list) else x for x in l]

print(list(chain.from_iterable(l)))
j = list(chain.from_iterable(l))
print(j)
import heapq
h = heapq.heapify(j)
print("j",j)
h1 = heapq.heappop(j)
print("j11",j)
h3 = j.pop()
print("j123",j)
import copy
r = {1: [1,2,3]}
f = r.copy()
t = copy.deepcopy(r)
print("f,t",f,t)
r[1].append(6)
print("f,t1",f,t)