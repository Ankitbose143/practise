n = [1,2,3,4]

from functools import reduce
d = reduce(lambda a,b:a+b,n)
print(d)

f = map(lambda a:a**2,n)
print(list(f))


g = filter(lambda a:a>2,n)
print(list(g))

import pandas as pd

df = pd.DataFrame(n)
print(df.apply(lambda g:g**2))
print(df.applymap(lambda g:g**2))


print((lambda n,s:n*s)(3,4))

print(list(map(lambda n:n**2,range(len(n)))))

gf = lambda a=2,b=3:lambda c:a+b+c
print(gf()(5))

# Python program to demonstrate
# nested lambda functions


square = lambda x: x**2
product = lambda f, n: lambda x: f(x)*n

ans = product(square, 2)(10)
print("and",ans)

