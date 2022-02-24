li = [0,0,1,0,1,1,0]


# def func(li):
#     mn = min(li)
#     mx = max(li)
#     d = []
#     # d = lambda x,y: [0,1]
#     # f = (b,a)[a<b]
#     s = []
#     # s= [lambda x: x==0 for x in range(mx)]
#     fr = filter(lambda x: x==0, range(mn,mx+1))
#     # for t in range(mn,mx+1):
#     #     filtered_list = list(filter(lambda num: num ==t, li))
#     #     print("fr1",filtered_list)
#     #     s.extend(filtered_list)
#     # for a in li:
#     print("fr",fr, type(fr))
#     print("s",s)
#     b = []
#     for i in fr:
#         # for j in i:
#         b.append(i)
#         print("i==",i, type(i))
#     #     s.append(list(filter(lambda x:x==a, range(mn,mx))))
#     print(b)

#     for t in range(mn,mx+1):
#         for l in li:
#             if l == t:
#                 d.append(l)
#     print(d)
#     # for t in range(mn,mx):
#     #     d.append(t)
# func(li)
# student
# student id, name, total_marks

# select student, dense_rank(order by total_marks) from as tm from students
# where tm =3;

# select rownum,
# rowdid=3
# with(select * from students where total_marks>3) as rer;
# select rer ;
# import pandas as pd
# df = pd.DataFrame("xyz.csv")
# df.columns()
# df.columns.name = ['a','b','c']
# df.isnull()
# df.
# kafka
    
# func(li)

for i in range(3):
    print("hi123",i)
    if i>=1:
        print("hi",i)
        continue
else:
    print("con",i)