# d = [2, 7, 4]
d = [9,10,4,7,2]
k = 2
res = []
t = 0
tr = []
st = []
for y in range(len(d)):
    if d[y]<=k:
        tr.append(y+1)
        d.insert(y,-1)
        print("aaa",d,y,d[y+1])
        # d.remove(d[y+1])
        d.pop(y+1)
        print("oooo",y,d)
# for y in d:
    elif d[y]>k:
        print("yd1",y,d, d[y])
        d.insert(y,abs(d[y]-k))
        print("===", d,y)
        d.pop(y+1)
        st.append(d[y]-k)
        print("yd",y,d)
print("=====12", tr,st,d)
pos = []
pos1 = []
for i in d:
    if i<=k and i>=0:
        pos1.append(d.index(i)+1)
print("pos1",pos1)

for r in range(12):
    for u in d:
        if r == u:
            pos.append(d.index(u)+1)
print("posss===", pos)
print(tr)
if pos and len(pos)>len(pos1):
    tr.extend(pos)
    print(tr)
else:
    if pos1:
        tr.extend(pos1)
    print(tr)
# for y in d:

# for u in st:
# while t<len(d):
# # for t in range(len(d)):
#     print("t", t, d)
#     if d[t]<=k:
#         res.append(t+1)
#         d.remove(d[t])
#         d.insert(t,'j')
#         print("rs", res, d[t])
#     else:
        
#         print("hi12", t, d[t], d)
#         d.append(abs(d[t]-k))
#         d.remove(d[t])
#         d.insert(t,'j')
#         # d.remove(d[t])
#         print("hi", t, d[t], d)
#     t+=1
#     print(res,d)
