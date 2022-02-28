# l = [7,5,3,2,9]
# p = 0
# # for t in l:
# #     if t>p:
# #         p=t
# # #removing first highest
# # l.remove(p)
# # # print(l)
# # q = 0
# # #finding second highest
# # for t1 in l:
# #     if t1>q:
# #         q=t1
# # print(q)
# # l = []
# f = l[0]
# l[0]= l[1]
# l[1]=f
# print(l)
# #=====================================
# l = [2,2,3,4,5]
# e = []
# for y in l:
#     if y not in e:
#         e.append(y)
# print(e)


f = None
for i in range(5):
    with open("app.log", 'w') as f:
        if i>2:
            break

print(f.closed)

def f(x,l = []):
    for i in range(x):
        l.append(i*i)
    print(l)

f(2)
f(3, [3,2,1])
f(3)

ar1 = [1,2,3,4,5]
ar2 = ar1
ar2[0] = 0
print(ar1)
ar3 = ar1.copy()
print(ar3)

i = 'welcome'

def welcome(i):
    i = i+',welcome to turing'
    return i

welcome('Developers')
print(i)

t = '%(a)s %(b)s %(c)s'
print(t %dict(a = 'welcome', b = 'to', c = 'Turing'))
l1 = [1,2,3,12]
l2 = [12,6,2,1]
print(l1==l2)
print(set(l1)==set(l2))     

import re
res = re.findall('Welcome', 'Welcome to turin',5)
print("res==",res)

data = [1,2,3]
def incr(x):
    return x+1

print(list(map(incr, data)))

array = ['Welcome', 'To', 'turing']
print("jkkjkjk","-".join(array))
x= 'abcdef'
isf= 'abcd'

for i in range(len(isf)):
    isf[i].upper()

print(isf)
# while i in x[:1]:
#     print(i, end = " ")


# x = ['ab', 'cd']
# print(list(map(lambda x:len,x)))
# print("a".capitalize())

# def fun1():
#     x = 50
#     return x
# fun1()
# print(x)

z = set('abc')
z.add('san')
z.update(set(['p','q']))
print(z)

def ls(val, le =[]):
    le.append(val)
    return le

le1 = ls('NodeJs')
le2 = ls('Java', [])
le3 = ls('ReactJS')
print('%s' % le1)
print('%s' % le2)
print('%s' % le3)