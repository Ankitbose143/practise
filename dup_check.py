def find_dup(lst):
    seen = set()
    dup = set()

    for num in lst:
        if num in seen:
            dup.add(num)
        else:
            seen.add(num)

    print(dup, type(dup), type(sorted(dup)))
    return sorted(dup)

lst = [1,1,1,1,2,2,4,5,5,6]
print(find_dup(lst))

class addit:
    def sumer(a,b):
        print(a+b)
        return a+b

class firt(addit):
    def sumer(*args):
        # print(a+b)
        return sum(args) 

obj = firt
print(obj.sumer(3,4,5,5))

class ker:
    def __init__(self,**kwrgs):
        print(kwrgs)
        print(kwrgs.keys())
        print(kwrgs.values())
        for g,f in kwrgs.items():
            print(g,f)

obj = ker(a=3,b=4)
print(obj)