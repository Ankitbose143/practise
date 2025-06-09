# decorator
l = [1,2,3,2,2,2,2,3,4,45]
l.remove(2)
print("l123", l)

for i in range(l.count(2)):
    l.remove(2)
print('l234', l)
# remove 2 without new list or set
d = 'ankit.bose@gmail.com, rahul.kumar@gmail.com'
# output = [email.split('@')[0].split('.')[::-1] for email in d]
output = [[part.title() for part in email.split('@')[0].split('.')[::-1]] for email in d]
print(output)
# print(output)[['bose','ankit'],['kumar', 'rahul']]

# for email in d:
    # print("email.split('@')[0].split('.')", email.split('@'))
    # for part in email.split('@')[0].split('.')[::-1]:
        # print("part", part)
# from emp table find 4th hihest salry with limit function
# SELECT DISTINCT salary 
# FROM emp 
# ORDER BY salary DESC 
# LIMIT 1 OFFSET 3;
r1 = ['hi', 'hello']
def f(*args):
    for i in args:
        print("i",i)
    return sum(*args)

print(f(r1))
# print(sum(*r))

