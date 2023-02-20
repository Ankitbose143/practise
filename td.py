# from multithreading import MultiThread
import threading
import multiprocessing
import asyncio

def calc_madd(a,b):
    print(a,b,a+b)
    return a+b

def calc_mul(a,b):
    print(a,b,a*b)
    return a*b

t1 = threading.Thread(target = calc_mul, args=(3,4))
t2 = threading.Thread(target = calc_madd, args=(3,4))
print("sasas",multiprocessing.cpu_count())
# pool = multiprocessing.Pool(multiprocessing.cpu_count()-2)
print(multiprocessing.Pool(2))
a = 4
b= 6
def work(x):
    return x*x

with multiprocessing.Pool() as p:
    results = p.map(work, range(5))
assert results == [x*x for x in range(5)]
# with pool as p:
    # p.map(calc_mul, a,b)
# pool.map(calc_mul(3,4))
# pool.map(calc_madd(3,4))
t1.start()
t2.start()
t1.join()
t2.join()