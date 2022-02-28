l = 'batman'
# ls = l[1]
print(type(l[0]))
ls = l[0]+'o'+l[2:]
# l[1] = ls
# d = list(l)
# print(ls, l)
l1 = [1, 2, 0, 9, 4, 0, 1, 7, 0]
output = [0, 0, 0, 1, 2, 9, 4, 1, 7]
op = [] #0
print(l1.count(0))
# l1 = 
l1.remove(0)
print(l1)
for t in l1:
    if t == 0:
        op.append(t)
        ind = l1.index(t)
        l1.pop(ind)
        # t.remove(0)
# op.append(l1)
print(l1)
op.extend(l1)
print(op)
