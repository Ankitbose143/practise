# x = 10
# if x>=11:
#     y=3
# else:
#     if x<6:
#         y=4
#     else:
#         y = 2
#         z= x*y+1
#     print(z, z%7)
from gramex.debug import lineprofile
class A:
    def __init__(self, id):
        self.__id = id
        id = 100
        x = A(10)
        print(x.id)

# x = A(10)
# f = None
# with open("scores.txt", "r") as f:
#     score = 0
#     for line in f:
#         score += int(line)
#         print(f.closed)

# def g(a=1,b=2,c=3):
#     print("%d, %d, %d".format(a,b,c))

# g(2,b=3,c=1)

x,y =1,1
def f():
    global x
    y = 0
    for i in (10,20,30):
        x+=1
        y==1
f()
print(x,y)


x = ["B", "C", "A"]
x.extend(["X","Y"])
x.reverse()
x.append("S")
x.sort()
x.reverse()
print(x)

def f(L, incr):
    map(lambda x:x+incr,L)

arr = [1,2,3]
f(arr,1)
print(arr)

# from os import *
# # ...
# f = open('hello.txt')
from functools import reduce
def f(g, *args):
    return g(args)
print(f(lambda z: reduce(lambda x,y: x+y,z,0), 1,2,3))


def get_status(file):
    return open(file).readline()

def get_status(file):
    with open(file) as fp:
        return fp.readline()


a = tuple('abcde')
a,b,c,d,e = a
b=c='*'
a= (a,b,c,d,e)
print(a) 

import datetime as dt
from datetime import timedelta
format = '%A, %d-%B-%y'
re1 =(dt.datetime.now()-timedelta(4)).strftime(format)

print("Rere{}".format(re1))

nu1 = [105,40,42,40,35,14,9,6]
op = list(filter(lambda m:(m%7==0), nu1))
print(op)


# fo = open("file1.txt", "w")
# fo.write("Giid Evening.\nWelcome\n")
# fo.open("file1.txt", "r+")
# str = fo.read(10)
# print("Rea",str)
# fo.close()

inp = "Python is a Programming Language"
import re
if len(inp):
    print(re.findall(r'P.+n',inp))
    print(re.findall(r'P[a-z]*n',inp))
else:
    print("Inv")

def smp():
    print("pc")
p = smp()

class Ins:
    # legs  = 6

    # def __str__(self):
    #     legs = 4
    #     return legs
    def __init__(self):
        self.main_whl = 8
        self.ad_whl = 2
        self.whl = self.main_whl+self.ad_whl

class car(Ins):
    ad_whl = 1
    def __init__(self):
        super().__init__()
        self.whl = 4
# i = Ins()
# print(i.legs)
c = car()
print(c.whl)
print(c.ad_whl)

print("Content-Type: text/plain\n\n")
print("Welcome")


class inptext:
    def __init__(self, inp_text):
        self.inp_text =inp_text

        def display(self):
            return self.inp_text

        mynum = inptext('1234567890')
        print(mynum.display())


from collections import namedtuple
Car = namedtuple('Car', 'name color engine type')
Cars =[]
names = ['Scxdcdr','I1cx0',"Creta"]
color = ['Blcxck', 'Whxcxct', 'Silev']
engine_types = ['Diesel', 'petrol', 'petrol']

# for i in zip(names,color,engine_types):
#     newcar  = Car(name=i[0],color=i[1],engine_types=i[2])

with property(prop_name, prop_type, prop_val, environment) as (    select 'BANKING', 'A', 'true' , 'DEV'   from dual union all    select 'IT'     , 'B', 'false', 'TEST'  from dual union all    select 'TELECOM', 'C', 'false', 'TEST'  from dual union all    select 'MEDIA'  , 'A', 'false', 'STAGE' from dual union all    select 'APPLE'  , 'D', 'true' , 'PROD'  from dual union all    select 'MANGO'  , 'E', 'true' , 'UAT'   from dual union all    select 'ORANGE' , 'B', 'false', 'DEV'   from dual union all    select 'CARROT' , 'C', 'false', 'TEST'  from dual union all    select 'BURGER' , 'B', 'true' , 'DEV'   from dual)select prop_name, prop_type,       case environment when 'DEV'   then prop_val end dev,       case environment when 'TEST'  then prop_val end test,       case environment when 'STAGE' then prop_val end stage,       case environment when 'UAT'   then prop_val end uat,       case environment when 'PROD'  then prop_val end prodfrom   property;PROP_NA P DEV   TEST  STAGE UAT   PROD------- - ----- ----- ----- ----- -----BANKING A true  NULL  NULL  NULL  NULLIT      B NULL  false NULL  NULL  NULLTELECOM C NULL  false NULL  NULL  NULLMEDIA   A NULL  NULL  false NULL  NULLAPPLE   D NULL  NULL  NULL  NULL  trueMANGO   E NULL  NULL  NULL  true  NULLORANGE  B false NULL  NULL  NULL  NULLCARROT  C NULL  false NULL  NULL  NULLBURGER  B true  NULL  NULL  NULL  NULL9 rows selected.
#     Cars.append(newcar)

# print('{}{}{}'.format(Cars[0][1],Cars[2][0],Cars[1][2]))

import sys as s
n = len(s.argv)
print(n)


