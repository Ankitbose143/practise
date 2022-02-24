class A:
    def __init__(self):
        print("An instance of A was initialized")
    def __call__(self, *args, **kwargs):
        for i in args:
            print("Arguments are:", args, i, type(i))
        print("keyArguments are:", kwargs)
x = A()
print("now calling the instance:")
x({3,4}, k=28)
# x(3, (4,3,3,),'sas', [2,3], x=11, y=10, z=20)

for i in range(3):
    print("frt", i)
    if i>1:
        print("frty", i)
        # break
        continue
else:
    print("next")