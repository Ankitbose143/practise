def mydec(f):
    def wrapper(dr):
        t = f(dr)+"hi222"
        # ty = f(dr)
        # ty.append("hi")
        return t
    return wrapper

def mydec2(f):
    def wrapper(dre):
        print("-------------------tr")
        # t = dre+"bye"
        t = f(dre)+"bye"
        # rt = f(dre)
        # rt.append("bye")
        print("-------------------ft")
        # return dre+"bye"
        return t
    return wrapper
@mydec2
@mydec
def pt(nm):
    print(nm)
    return nm

# pt("Ankit")
print("yes",pt("Ankit"))
