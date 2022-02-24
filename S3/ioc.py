t1 = (1,2,3)
t2 = (3,4,5)

print(t1+t2)

import pandas as pd

sr = pd.read_csv('data_file.csv')
print(sr.tail(2))


sd = open('res.txt', 'r',encoding='cp1252')
print(sd.readlines()[-2:])


# sr = [int(t) for t in input()]
# print("sr", sr)
# # ft = lis
# cd = list(map(lambda x:x**3, sr))
# print("cuube",cd)

# def fun(n):
#     count=0
#     n = int(n)
#     for i in range(1,n+1):
#         if n%i==0:
#             count+=1
#     if count==2:
#         print("prime")
#     else:
#         print("composite")

# fun(input())

l = [2,3,4,5,6]
d = sorted(l)
print("sec min",d[1])