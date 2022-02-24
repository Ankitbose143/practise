t1= (10,20,[2,3])
# t1 = [1,2,3,(1,3)]
t1[2].append(4)

print(t1)
t3 = [1,2,3]
t3.extend(int(10))
print(t3)

# from itertools import OrderedDictionary

# print(OrderedDictionary)
# *args
# demo([1,2,3])
# demo(a=3,b=4)

import cx_oracle
conn =cx_oracle.connect()
cur = conn.cursor()
cur.execute("select * from emp")
cur.ex

d = [9,5,4,1]
#9,5 5,4 4,1
#4 1 3
#1
d1 = []
i = 0
s = []
for t in range(len(d)-1):
    # print(d[t],d[t+1])
    d1.append([d[t], d[t+1]])
    print(d1)
    s.append(abs(d1[i][0]-d1[i][1]))
    i+=1
print("minimumval",min(s))


