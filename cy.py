# def f(*args, **kwargs):
    
#     d = *args
#     print("hi")



# f = ([1,2,3])
# print(f)

# import datetime
# df = datetime.datetime('1990-12-01', 'YYYY-MM-DD')

# print(df)
def func():
    for i in range(10):
        yield i
for t in func():
    print(t)
# print(func())



def func(f):
    def wrapper(*args,**kwargs):
        print("====1")
        f()
        print("====2")
    return wrapper

@func
def hi():
    a = 1+1
    print(a)
    return a

# hi = func(f)
