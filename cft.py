l = [1,2,3,4]
m = [2,3,9,7,0,1]
n = [1,3]
s = [1,1,1,2,3,3,4,5,5,6,6,6,7,8,8,8,89,11,12,12,12,13,12]

import itertools

for t in l:
    for y in m:
        if t==y:
            pass
            # print("t==", t)

for t,r,a,b in itertools.product(l,m,n,s):
    if t==r and r==a and a==b:
        pass
        # print(t,r,a,b)

# s= 100
# print(" ".join(list(map(int, str(s)))))
# for t in range(s,10**12):
m = [1,2,3]
n = [4,5,6]
for i, val in enumerate(m):
    print(i,val)
    print(m[i]+n[i])
# for t,r in itertools.product(n,s):#,list(map(int, str(s)))):
#     # s+=1
#     print(t,r)
    # print(list(filter(lambda x:x%2==0, list(map(int, str(s))))))