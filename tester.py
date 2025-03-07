var = "{[()()]}"
var2 = "{[()()}]"
var3 = "{[()(]}"


print(var,var[::-1])
print(var2,var2[::-1])
print(var3,var3[::-1])

count = 0
for i in range(len(var)-1):
    print(var[i][0],var[::-1][i][0])
    if var[i][0]==var[::-1][i][0] or var[i][0]==var[i+1][0]:
        
        print("123",var[i][0],var[::-1][i][0])
    #     count+=1
print(count, len(var))
        



# @decorator - connection with db
# @decorator - calling api

# func  - calll api
# func2 - call db
# exception comes decorater should retry 2 times
def mydec(f):
    def wrapper():
        try:
            # print(args)
            f()
            # raise Exception
        except Exception as e:
            # call_api()
            f()
            # pass
        
    return wrapper
    
@mydec(2)
def call_api():
    # try:
    raise Exception
        # pass
    # except Exception as e:
    #     # call_api()
    #     pass
    
    # pass
    
call_api()


@mydec
def call_db():
    pass
    
class Person:
    def __init__(self):
        pass
    
obj = Person


# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
#call person nanameme, age
class Person:
    # By defining __slots__, you prevent the creation of any attributes not listed in __slots__.
    __slots__ = ['name', 'age']  # Restricts attributes to 'name' and 'age'
    
    def __init__(self,name,age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        # name = self.name
        # age = self.age
        # print(self.name + " "+ str(self.age))
        return str((self.name, self.age))
        
obj = Person('Ankit', 32)
print(obj)

obj2 = Person('Akhil', 30)
obj3 = Person("Amit", 24)

var_list = [obj, obj2, obj3]
# print(var_list)
# print(type(var_list))
# sorted(var_list, key = lambda x: x[1])
# print(var_list.sort())
obj.address = 'Bangalore'
print(obj)

l = [1, 2, 3]

def foo(param):
    param = param.copy()  # Create a copy to avoid modifying the original list
    param.append(4)  # Modify the copy
    print(param)  # Output: [1, 2, 3, 4]

foo(l)  # Pass the original list
print(l)  # Output: [1, 2, 3] (Original list remains unchanged)



