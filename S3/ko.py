from msilib.schema import tables
from turtle import update
import numpy as np
# from pymemcache.client import base
# from functools import cache
# @cache
# client = base.Client(('localhost', 11211))
#.52#.56
#[0.52,0.56]
# 0.52
l = [0.52,0.56,0.67,0.55,0.54,0.51,0.62,0.89,0.21,0.55]
# # d = l[0]
d = float(input())
# # print(type(d),type(l[0]))
# g = 0
l = sorted(l)
dq = []
print("l==",l)
f = []
for i in l:
    if d<float(i):
        f.append(i)
print(f)
# client.set('some_key', 'some value')
dq.append(id(f))
# dq.append(client)
print("out",f[0],id(f))
print("fun", dq)

i = 0
# while i < 5:
for i in range(5):
    print(i)
    i += 1
    if i > 3:
        # break
        continue
else:
    print(0,"ki")

# # 0
# # 1
# # 2
# # 0
# # tables
# rnk
# 1 
# 2
# 3
# 3
# 5
# 6
# 7
# # group by
# # rank count(employees)
# 1 1
# 2 1
# 3 2
# 5 1
# 6 1
# 7 1

# # with dup as
# select count(emp),rank() over order by salary as rnk from emp order by salary
# group by rnk;
# where rnk;

# where r;

# import request , response

# request.get(url)
# get = read
# post = add(insert)
# put = update(u), add(expectional when the data is not there)
# delete - delete
# patch 








# AZSPJ0571C
# 7829618682