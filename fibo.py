import pandas as pd
import re , time
df = pd.read_excel(r'sd.xlsx')
print(df.columns)
de = ['sc', 'pharmacy']
st = time.time()
import geocoder
g = geocoder.ip('me')
print(g.latlng)

dplicate_bool = df.duplicated(subset=['Attribute Name'])
# print(df.loc[dplicate_bool == True].index.to_list())
# print(df[df['Attribute Name']=='atmf_batch_number'])
# print(df[df['Attribute Name']=='swy_year'].shape[0]>1)
sd = []
if df[df['Attribute Name']=='atmf_batch_number'].shape[0]>1:
    # print(df[df['Attribute Name']=='atmf_batch_number']['Analytic call'])
    print(df.loc[df['Attribute Name','Analytic call']], type(df[df['Attribute Name']=='atmf_batch_number']['Analytic call'].values))
df1 = pd.Dataframe()
df1.apply()
# print("fsd", df)
# for y in df:
#     print(y,df[df['Attribute Name']==y]['Analytic call'].values)
# print("time",time.time()-st,df.memory_usage())
# print(df[df['Analytic call']==4]['Attribute Name'].values)
st = time.time()
for y1 in df:
    d1 = df['Analytic call'].to_list()#numbers
    k = df['Attribute Name'].to_list()
# print("time12",time.time()-st)
d1 = df['Analytic call'].to_list()#numbers
k = df['Attribute Name'].to_list()
dfg = []
er = []
for kw in k:
    j = kw.split()
    for d in de:
        for i in j:
            if re.findall(r'(\b){}(\b)'.format(i),d):
                dfg.append(d1[k.index(kw)])
                er.append(k.index(kw))
                # print(k.index(kw))
                # print(k[k.index(kw)],d1[k.index(kw)])
sd = list(set(dfg))
# print(list(set(dfg)))
# sd.append(2.0)
# print("sd",sd)
# print(er)
for sf in sd:
    print([index for index, value in enumerate(d1) if value == sf])
# print(d1)
# for index, value in enumerate(d1):
    # print(index,value)
# d = {item: idx for idx, item in enumerate(d1)}
# print([d1.get(item) for item in d])
# print([d1.index(i) for i in sd])
# sde = list(map())
# print(k)
# for h in sd:
    # print(d1.index(h))
# for t in er:
# if t == h:
    # print(k[t])




# def fibo(n):
#     i =0
#     j = 1
#     sd = None
#     # if sd:
#     #     print(sd)
#     print(i)
#     print(j)
#     for k in range(2,n):
#         l=i+j
#         print(l)
#         j = l
#         l = i
        # j =i

# fibo(5)
        