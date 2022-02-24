import json

import csv
import pandas as pd
f = open(r'convf.json')
d = json.load(f)
# print(d)
# print(d.items())
# df1= pd.read_json(r'convf.json')
data_frame = pd.DataFrame.from_dict(d.items())
print(data_frame.columns)
# print(df1,df1.reset_index())
df = pd.DataFrame(d.items())
data_frame.reset_index(drop=True)
data_frame.to_csv("sdf.csv", index = False)

# 1.Weather API Accuweather.com 
# 2.Passing City name(Newyork) as query parameter as a input to weather API.
# 3.How can you write a scritp to save the API response in a JSON file.
# 4.How do you validate headers of API response?
# 5.API response contations city latitude /longitude,Temperature, Pressue, Humidity in the form of Json.?
# 6.How do you extract the values of JSON and how do you validate response.?
# 7.How do you do data value validations with different type of assertions?

import requests
from urllib.parse import urlparse

# PARAMS = {'search-locations':"newyork"}
# # url = 'https://docs.djangoproject.com/'
# PARAMS = {'query' :'Mumbai'}
# url = 'https://www.accuweather.com/en/search-locations'
# url = 'http://127.0.0.1:8100/operations/Amazon%20Inventory/Dash/'
# d = requests.GET.get('search-locations', '')
# print(d)
# # s = requests.get(url, params = PARAMS)
# s = requests.get(url)
# o = urlparse(s)
# print("o=============", s,o)
# r = requests.post(url = url, data = PARAMS)
#1 or 2
# print(s.content.decode())
# print(s.json())


Input1 = [7, 2, 8, 9, 1, 3, 4]
import copy
Input2 = copy.deepcopy(Input1)
Input2.append(3)
print(Input1, Input2)
for t , y in zip(Input1,Input2):
    if t:
        print(t)
    else:
        print(y)

for t,y in Input1:
    print(t,y)
# Pull out the elements from a and b, for which the sum a+b is also in the list.

# Ex:
# a+b = c(Resultant Sum)
# 7+ 2=9
# 7 +8=15
# 7 +9 =16
# 7+ 1 =8
# 7+ 3 =10
# 7+ 4 =11

# Output list = [7, 2, 8, 9, 1, 3, 4, 9,15,16,8,10,11]

for t in range(len(Input2)):
    # print("in2",Input2)
    for y in range(t+1, len(Input2)):
        Input1.append(Input2[t]+Input2[y])

print(Input1)
# print("input2",Input2)

# import cx_oracle
# import pandas as pd

# conn = cx_oracle(dbname,host)
# cur = conn.cursor()
# s = cur.execute("select ename from emp")
# cur.executemany("select ename from emp")

# namepd = pd.DataFrame(s['ename'])





