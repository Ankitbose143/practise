# from lib2to3.pgen2.token import SLASHEQUAL


input=[2,4,6,9,10,12,13,12,13,13]

# output=[13,13,13,12,12,2,4,6,9,10]
dt = {}

for t in set(input):
    dt[t]= input.count(t)
    # print(t,input.count(t))

# print(sorted(dt, reverse= True))
sf = sorted(dt, reverse= True)
fg = []
for yr in sf:
    for y, z in dt.items():
        if yr ==y:
            for u in range(z):
                # print("y",y,z)
                fg.append(y)

print("new list", fg)


class A():
    def __init__(adf, sd):
        adf.fg =sd
        print(adf.fg)
        print("hi", A)
        # pass

    #class method
    @classmethod
    def clm(xyz):
        print("class")
        # pass
    
    # instance method
    def trm(abc):
        print("instance",abc)
        # pass

    @staticmethod
    def ty():
        s = 10
        print("static", s)
        # pass

d = A(23)
print(d.clm)
d.clm()
d.trm()
d.ty()

s = 'google'

# print(s.split())
print(s[:3])
d = [{t:s.count(t)} for t in set(s)]
print(d)

l = [1,2,3,4,5,6,7,8,9,10]

d = list(filter(lambda x:x%2==0,l))
e = list(filter(lambda x:x%2!=0,l))

print("even", d)
print("odd", e)
# print((123))
map

# select name,sal,id, dept from emp group by dept
# order by sal
# having count(sal)>1
