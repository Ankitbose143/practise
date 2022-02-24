s1 = "2+3"
s2 = "-200+300*3"
# ['-','200','+','300','*','3']
# o = []
# import re
# for y in s2:
#     print(y)
#     if '+' in y or '*' in y:
#         print(s2[:s2.index(y)])
#         o = o.append(s2[:s2.index(y)])
# print("split",s2.split('+'))#+
# s2 = s2.split('+')
# s2 = ''.join(s2)
# print("split",s2.split('*'))#*
# d = re.findall(s2,'1234567890')
# f = re.findall(s1,'/+-/*^')
# print(d, f)
# #BODMAS () / * 
# def func(sd):
#         k = 0
#         r = 0
#         for t in sd:
#             print(t)
#             try:
#                 if int(t):
#                     f = int(t)
#                     print("f", f, k)
#                     if '+' in sd:
#                         k = k+f
#                         print("add",f)
#                     elif '*' in sd:
#                         r = r*f
#                         print("mul",r)
#             except Exception:
#                 pass


# func(s1)

def custom_deco(f):
    k = 0
    def just(func):
        print("func", func,f)
        def wrapper(*args):
            print("args", func,f)
            k = func(*args)
            # k = a+b
            # print(k)
            return f+" "+str(k)
        return wrapper
    return just

@custom_deco("hi")
def add(a,b):
    return a+b

print(add(3,4))
# def custom_deco(func):
#     print(func)
#     def func_wrapper(a, b):
#         print(a,b)
#         return a+b
#     return func_wrapper






