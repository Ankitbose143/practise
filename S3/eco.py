# from pickletools import TAKEN_FROM_ARGUMENT1
# from re import A, T


# A(get_data)
# B(A)(get_data)
# C(A)(get_data)
# D(B,C)
class X:
    def get_data():
        print("X")
class Y:
    def get_data():
        print("Y")
class Z:
    def get_data():
        print("Z")
class A(X,Y): pass
    # def get_data():
        # print("A")
class B(Y,Z): pass
    # def get_data():
        # print("B")
class M(B,A,Z): pass
    # def get_data():
    #     print("M")

x = M
print(x.mro())
x.get_data()#A get_data
print("hiiiiiiiiiiiiiiiiiiiiiiiii-")

def testgen(index):
    weekdays = ['sun','mon','tue','wed','thu','fri','sat']
    yield weekdays[index]

day = testgen(1)
print (next(day))
a=int(input("Enter number: "))
k=0
for i in range(2,a//2+1):
    if(a%i==0):
        k=k+1
if(k<=0):
    print("Number is prime",a)
else:
    print("Number isn't prime",a)
# y = D(C,B)#A
l = [1,23,4,5,5,6,6,77,7]
d = 0
s = 0
f = []

for t in l:
    if d<t:
        d = t
        f.append(t)
        l.remove(t)
        # d = t
l1 = [1,23,4,5,5,6,6,77,7]
g = l1[0]
r = []
for t1 in range(len(l1)):
    if l1[t1]<g:
        r.append(g)
        # l1.remove(t1)
        g = l1[t1]
print("list", l1)
print("r===", r)
print("mininmum of 3",l1[2])
print("maximum of 3", l1[-3])

l = [1,23,4,5,5,6,6,77,7]
print("The list is ",l)
 
# Assign first element as a minimum.
min1 = l[0]
f = []
for i in range(len(l)):
 
    # If the other element is min than first element
    if l[i] > min1:
        min1 = l[i] #It will change
        f.append(min1)
 
print("The smallest element in the list is ",min1)
print("trtrtrtrt", f)
#fibonaaci 1*2*3 =6
#0,1,1,2,3,5

def fibo(n):
    if n<=1:
        return n
    else:
        return fibo(n-1)+fibo(n-2)
    
nterms = 10
if nterms <= 0:
       print("Plese enter a positive integer")
else:
   print("Fibonacci sequence:")
   for i in range(nterms):
       print(fibo(i))
# fibo(6)
# t = 10
# for i in range(t):
#     print(fibo(i))

def fibonac():
    a = 0
    b = 1
    c = 0
    for t in range(5):
        # if t ==1:
        c = a+b
        a = b
        b = c
        yield a
    # print(a)
    # yield a
for y in fibonac():
    print(y)
# print(fibonac())

# select * from emp group by design;
# where design max(sal)

# select * from (select dense_rank() over(partition by designation order by sal desc)) as xyz
# where xyz = 1;

# a b c
# 10000 10000 10000
# 1 1
# 1 1 
# 1 1
# 4 2

# django MVT
lad = [1, 2,3 ,4 ,5,6,15,0]
def sml(lad):
    largest = lad[0]
    largest2 = None
    largest3 = None
    # item = lad[0]
    for item in lad[1:]:
        if item > largest: 
            largest2 = largest
            largest = item
            print("==1",largest, largest2, largest3) 
        elif largest2 == None or largest2 < item:
            largest3 = largest2
            largest2 = item
            print("==2",largest, largest2, largest3) 
        elif largest3 == None or largest3 < item:# and largest3<largest2: 
            largest3 = item
            print("==3",largest, largest2, largest3)  
        # if item < lowest: 
        #     lowest2 = lowest
        #     lowest = item 
        # elif lowest2 == None or lowest2 > item: 
        #     lowest2 = item 
    print("largest", largest)
    print("largest2", largest2)
    print("largest3", largest3)
sml(lad)

NumList = lad
for index, item in enumerate(lad):
    print(index, item)
print("===Numlist", NumList)
for i in range(len(lad)):
    for j in range(i + 1, len(lad)):
        if(lad[i] > lad[j]):
            temp = lad[i]
            lad[i] = lad[j]
            lad[j] = temp
            print(NumList, i,j)
# asd = [ for i,j in zip(len(lad), )]
# from emp

my_list = [-15, -26, 15, 1, 23, -64, 23, 76]
new_list = []

while my_list:
    min = my_list[0]  
    for x in my_list: 
        if x < min:
            min = x
    print(min,x)
    new_list.append(min)
    my_list.remove(min)    

print(new_list)

# def is_sorted(iterable):
#     for a1,a2 in zip(iterable, iterable[1:]):
#         if a1 > a2: return False
#   return True

# is_sorted(lad)


