from calendar import c
from ctypes.wintypes import tagPOINT
from optparse import Values

from eco import B


data = ["__11", "21_", "_121__"]
# o/p: "11-21-121"
sd = "-".join(data)
sd = sd.replace('__','')
sd = sd.replace('_','')
print("values", sd)


data2 = [10, 100, 1000]
# o/p: [100, 10000, 1000000]
ase = list(map(lambda x:x**2,data2))
print(ase)

info = [
{
 "name": "John",
 "age": 27,
 "location": "UAE"
},
{
 "name": "Marie",
 "age": 22,
 "location": "INDIA"
},
{
 "name": "Janet",
 "age": 18,
 "location": "US"
},
{
 "name": "Jane",
 "age": 34,
 "location": "LONDON"
}
]
# t = dict(info)
t = {}
dft = []
gty = []
rty = []
i = 0
for u in info:
    mi2 = u["age"]
    print(mi2)
    dft.append(u["age"])
    gty.append(u["name"])
    rty.append(u["location"])
    t[i] = u["age"]
    i+=1
    # for te, vl in u.items():
    #     # pass
    #     print(te, vl)
    #     if te == 'age' and mi2<vl:
    #         # print("val", vl)
    #         t.add(te,vl)

print("t",t,dft, gty,rty, sorted(t.items()))
s = sorted(t.items())
r = sorted(info, key = (lambda x:x['age']))
print("sassa",r)
        # t[te] = vl
# print(t)
# print(sorted(info))

class A():
    def __init__(self, A):
        self.A = A

    def __str__(self):
        return self.A


x = A("10")
print(x.__str__)

# A
# B
# c
# X(A,B)
# y(B,C)
# z(x,y)

class B():
    pass

d = B()

