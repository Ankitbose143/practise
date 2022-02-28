# def run(a,s,f = None):
#     if a and s and f:
#         print("a,s,f")
#     elif not f:
#         print(a,s)

# run(10,20,30)

# run(20,30)

# from abc import ABC, abstractmethod
# from asyncore import file_dispatcher
# import errno


# # class Polygon:
# #     def __init__(self,x):
# #         self.x=x

# #     @abstractmethod
# #     def noofsides(self,x):
# #         return x

# # class Traingle(A):
# #     def noofsides(self,x):
# #         print("x")

# # class Rectangle(A):
# #     def noofsides(self,x):
# #         print("x")

# # d = Rectangle()
# # d.noofsides(4)

# class ankit(Exception):
#     def __init__(self):
#         pass

#     def __str__(self):
#         return '{}'.format("Hi,this is the error")

# try:
#     # a = 2/0
#     raise ankit
# except ankit as ae:
#     print(ae)

# # file
# # 1 2 3
# # 4 5 6
# # __entry__():
# # __exit__():len(str)

# def mydec(f):
#     def wrapper(*args,**kwargs):
#         print("hi")
#         d = f(*args)
#         return d
#     return wrapper

# @mydec
# def printnm():
#     print("Ankit")

# # A()
# # B()
# # C()

# import threading

# # t1 = threading.Thread(A(), args = {})
# # t2 = threading.Thread(B(), args = {})
# # t3 = threading.Thread(C(), args = {})
# # t1.join()
# # t2.join()
# # t3.join()
# # t1.start()
# l = [1,2,3,4,5]
# l2 = [0 if t%2!=0 else t for t in l ]
# print(l2)

# l3 = list(map(lambda x:x**2, l))
# print("square",l3)

# g = [1,3,6]
# sum = 20
# # 15
# 20
# 6*3+2
# 1 <2> 3
# # smallest value
# 6*3+1*2==20
# 6*3+3*1==20
# 6*3+1*2 #6*3+3*1
# 6+2+3+4
# 6 3 1 1
# 1,6 1,3
# permutations ((1,3),(1,6),(3,6))

# from itertools import combinations
# from turtle import radians

# n = 2
# s = combinations(g,n)
# k = []
# mx = 0
# f = []
# r = 0
# if sum in g:
#     print(sum)
# else:
#     mx= max(g)
#     if sum>mx:
#         f.append(mx)
#         r = sum%mx
#     for i in range(1,mx):
#         print(r)
        # if f[0]*i+
# print(f)

# for per in s:
#     k.append(per)
#     print(per)
# print(sorted(k, key = lambda i:i[1]))

l = [1,3,4,6,2,6,3,4,56,2,1]

# smallest non repeating no 3
i = 1
count = 0
k = []
# for u in range(5):
# for t in l:
    # if l.count(t)==u:
        # print("smallest",t)
        # count+=1
        # break
    # if count==1:
    #     break
l = [1,2,6,3,4,56,2,1,56,3,4,6,6]
g = [[t,l.count(t)] for t in set(l)]
h = [l.count(t) for t in set(l)]
s = g
# s = sorted(g, key=lambda i:i[1], reverse= True)
print("g-------------",g)
print("sg-------------",s)
print(sorted(g, key=lambda i:i[1], reverse= True))
print("sgsh-------------",h, max(h), set(h))
# if len(set(h))==1:
    # print("no repeat")
if max(h)==1:

    iw = 1
else:
    iw = max(h)
    print(iw)
for iwe in range(1,iw):
    for i in range(len(s)):
        # print(s[i])
        if s[i][1]==iwe:
            print("asasasasas",s[i][0])
            break

from collections import defaultdict
 
def firstNonRepeating(arr, n):
    mp = defaultdict(lambda:0)
    print(mp)
    # Insert all array elements in hash table
    for i in range(n):
        mp[arr[i]] += 1
    print("mp",mp)
    # print([k for k,v in mp.items() if mp.values().count(v) > 1])
    # Traverse array again and return
    # first element with count 1.
    # fot in range
    # print(list(map(lambda x,y:x[1]==y[1], mp)))
    for i in range(n):
        if mp[arr[i]] == 1:
            return arr[i]
    for k,v in mp.items():
        if len(set(mp.values())) ==1:
            return "no repeat12"
    return -1
 
# Driver Code
arr = [9, 4, 9, 6, 7, 4,6,6,7]
n = len(arr)
mp2 = defaultdict(lambda:0)
print(mp2)
    # Insert all array elements in hash table
for i in range(n):
    mp2[arr[i]] = mp2[arr[i]]+1
    print("mp2222======", mp2)

print("mp2",mp2)
print(firstNonRepeating(arr, n))
d = {9: 2, 4: 2, 6: 2, 7: 2}
for k,v in d.items():
    if len(set(d.values())) ==1:
        print("no repeat")
    # print(d.values())
    # print(set(d.values()))
# o =list(k for k,v in d.items() ]#if d.values().count(v) > 1)

sml=[a for a in d.values() if a ==min(d.values())][0]
print("adda", sml)

l = [("abc",8),("asd",10),('abc', 12), ('wer',11), ("opi",7),('wer',7)]
df = {}
f = []
for t in l:
    f = []
    if t[0] not in df:
        f.append(t[1])
        df[t[0]] = f
        print(df)
    else:
        print(t)
        e = df.get(t[0])
        e.append(t[1])
    #     f.append({t[0]:t[1]})
    # print(t,t[0] in f)
print("df=-------",df)

dict1={"one":1,"two":2,"three":3,"three1":4,"three32":1}
list1=[]
for i in range(len(dict1)):
    sml=[a for a in dict1.values() if a ==min(dict1.values())][0]
    key1=[k for k,v in dict1.items() if v ==min(dict1.values())][0]
    print(sml, key1)
    del dict1[key1]
    print(dict1)
    list1.append(sml)

print("list1==",list1,sml)
# 
# int(x = 

def ty(*args):
    print("===", args)

def rt(*args):
    d = list(map(ty,*args))
    print(args, type(args))
    for t in d:
        print("t",t)
    print(d)

rt("h")
