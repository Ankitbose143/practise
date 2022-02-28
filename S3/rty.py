from re import A


d = [1,2,3,4,5,6,7,8,9,10,2,3,4]
df = [r for t in range(1001) for r in set(d) if r == t]
print(df)

d.append(5)
print("append 5",d)
d.insert(0,5)
print("insert 0, 5",d)
d.pop()
print("delte or pop last element",d)
d.extend("ankit")
print(d)


class ankit(Exception):
    def __str__(self):
        return '{}'.format("hi this is eankit excpetion")
try:
    raise ankit

except ankit as ae:
    print(ae)

#table =transaction
#transaction_dtm
date12 = '25-02-2022'
# select * from transaction where to_date(transaction_dtm, "DD--MM-YYYY ")=(date12)

l = [2,3,3,4,5,6]
l2 = []
for t in range(len(l)):
    # for y in range(0,len(l)):
    h = l[0]
    # k = list(filter(lambda x:x==h ,l[1:]))
    for z in range(1,len(l)):
        # pass
        print("hi", h, l[z])
        if l[z]==h:
            l2.append(l[z])
            #     print("good")
    print("===",l,l[t], l[-1])
    l.append(l[0])
    l.pop(0)
    print(l)

print("lis2",l2)

class A:
    def __init__(self, a):
        self.a = a
 
    # Overloading ~ operator, but with two operands
    def __invert__(self, other):
        return "This is the ~ operator, overloaded as binary operator."
 
 
ob1 = A(2)
ob2 = A(3)
 
print(ob1,ob2)