# 1.python
# vehicleid,stops,start
# 1,a,1000
# 2,a,1200
# 1,b,1100
# 1,c,1200
# 2,d,1500

# expected
# vehicleid,stops,start,end
# 1,a->b>c,1000,1200
# 2,a->d,1200,1500

d = [{"vehicleid":1,"stops":"a","start":1000},
{"vehicleid":2,"stops":"a","start":1200},
{"vehicleid":1,"stops":"b","start":1100},
{"vehicleid":1,"stops":"c","start":1200},
{"vehicleid":2,"stops":"d","start":1500}]
l = []
l2 = []
f = []
c = 0
d1 = 0
for t in d:
    if t['vehicleid']==1:
        if c==0:
            f.append(t['vehicleid'])
            c+=1
        f.append(t['stops'])
        f.append(t['start'])
    elif  t['vehicleid']==2:
        if d1==0:
            l.append(t['vehicleid'])
            d1+=1
        l.append(t['stops'])
        l.append(t['start'])
    # f.append(t['vehicleid'])
    # f.append(l)
    # f.append(l2)
print(f,l)


# id
# 1
# 2
# 1
# 0
# 4
# Null

# Id
# 2
# 0
# 3
# 1
# null

# innerjoin 3
# left join 6
#right join 5
#full outer join 5
l = [("abc",8),("asd",10),('abc', 12), ('wer',11), ("opi",7),('wer',7)]

f = []
g = []
k= []
d = {}
print("tr,", l)
for t in l:
    g = []
    print("2323", t)
    if t[0] not in d:
        g.append(t[1])
        d[t[0]]= g
        # print("t",t)
    else:
        print(t[1], d, g)
        if t[0] in d:
            g=d.get(t[0])
            g.append(t[1])
            print(g, t[0])
            # d[t[1]].append(t[1])
        # d[t[0]]= g
    #     k.append(t[1])
lis = []
for i in range(len(d)):
    sml=[a for a in d.values() if a ==max(d.values())][0]
    key1=[k for k,v in d.items() if v ==max(d.values())][0]
    print(sml, key1[0], sml)
    del d[key1]
    lis.append(sml)
# print(sml, key1, sml)
# print(lis)
# print(f,k, d)
# print(sorted(d, lambda x:(x[0],x[1])))
# cmr = {'take':10,'bake':10,'cake':5,'rake':5,'sake':2,'pake':2}
# d ={'abc': [8, 12], 'asd': [10], 'wer': [11, 7], 'opi': [7]}
# s = [val for val in sorted(d.items(), key = lambda x: len(x[1]), reverse=True)]
# print("s",s)