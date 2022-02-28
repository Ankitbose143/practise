# m = int(input())
# n = int(input())
# print(m,n)
a = [int(j) for j in input().split()]
b = [int(j) for j in input().split()]
c = [int(j) for j in input().split()]
d = [int(j) for j in input().split()]
p = []
p.append(a)
p.append(b)
p.append(c)
p.append(d)
print(p)
cnt = 0
m = 4
n = 4
h = 0
g = 4
for i in range(m-1):
    flag = 0
    for j in range(h,g-1):
        print("i",i,"j", j)
        print(p[i][j])
        if p[i][j] ==1:
            cnt +=1
        else:
            flag = 1
            if i!=n-1 and i>=0:
                i = i+1
            if j>=1 and j<3:
                for y in range(j-1,j+1):
                    print("y",y)
                j+=1
    if flag ==1:
        h+=1
# import numpy as np
# arr = np.array([[8, 3, 2],
#           [3, 6, 5],
#           [6, 1, 4]])
# #sort the array using np.sort
# print(arr.view([('',arr.dtype)] * arr.shape[1]))
# arr = np.sort(arr.view([('',arr.dtype)] * arr.shape[1]),
#        order=['f1'],
#        axis=0).view(np.int)

# print(arr)
