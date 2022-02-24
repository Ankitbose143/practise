# ABCHAMP
# Version 2

import pandas as pd
import json
import csv , ast
from csv import DictWriter
f = open(r'Conversion.json')
# print(ast.literal_eval(f))
# print(pd.DataFrame(f))
# with open(f, 'r') as j:
#      contents = json.loads(j.read())
#      print(contents)
# with open('xyz.json', encoding='utf-8') as inputfile:
#     df = pd.DataFrame.from_dict(inputfile, orient='index')
#     df = df.transpose()
#     # df = pd.read_json(inputfile)
#     print(df)
# print("jssdf",json.load(f))
# print("jss",json.loads(f.read()))
# print(type(json.load(f)))
k = json.loads(f.read())
# k = json.load(f)
print("ass=================================",k, type(k))
# print(k.keys())
# print(k.values())
df = pd.DataFrame(k)
df.to_csv('sdf.csv')
# d = dict(k)
data_file = open('data_file1.csv', 'w', newline='')
# employee_data= k
count = 0
csv_file = csv.writer(data_file)
# for item in k:
#     csv_file.writerow(item)

# f.close()
# # create the csv writer object
csv_writer = csv.writer(data_file)

if count == 0:
    header = k.keys()
    # print("gddd", header)
    header = ['Name','acl_name', 'always_include', 'baselined_by', 'comment', 'dst_hostname', 'dst_network', 'dst_network_type', 'dst_port', 
        'editor', 'established', 'expiry', 'id', 'juniper_xml', 'last_baselined', 'last_modified', 'owner', 'protocol', 'request_tt', 'rule_type', 'src_hostname', 'src_network', 'src_network_type', 'src_port', 'uri']
    # dictwriter_object = DictWriter(data_file, fieldnames=header)
    # dictwriter_object.writerow(k)
    # csv_writer.writerow(f)
    csv_writer.writerow(header)
    # print("header==",header)
    # for j, v in k.items():
    te = []
    for t in list(k.keys()):
        # print("kjkhkhkjt",t)
        # if j == 'LOWER-LD-RIGOR':
        if not k[t]:
            # print("tererer", k[t], t)
            csv_writer.writerow([t])
        for i in k[t]:
        # for i in k['LOWER-LD-RIGOR']:
            # print("===========trrtri", i)
            f = dict(i)
            te = []
            te.insert(0,t)
            # print("ent",te)
            # print("eeee", te)
            # print(f)
            for y in range(len(header)):
                for u, vl in f.items():
    #                 # print("UUUU111", u)
                    if u ==header[y]:
                        # print("uy=================111",u,header[y],vl,y)
                        te.insert(y+1,vl)
            csv_writer.writerow(te)
            # print("eeeeewewwe", te)
            # t = list(f.values())
            
            # t.insert(0,'LOWER-LD-RIGOR')
            # print("f====1", f.values())
            # print("iiiiii1", te)
            # csv_writer.writerow(te)
        
                # csv_writer.writerow(['LOWER-LD-RIGOR'])
        # elif j == 'HIGHER-LD-RIGOR':
        #     # t = []
        #     for i in k['HIGHER-LD-RIGOR']:
        #         f = dict(i)
        #         t = []
        #         t.insert(0,'HIGHER-LD-RIGOR')
        #         for y in range(len(header)):
        #             for u, vl in f.items():
        #                 # print("UUUU111", u)
        #                 if u ==header[y]:
        #                     # print("uy=================111",u,header[y])
        #                     t.insert(y+1,vl)
        #         # t = list(f.values())
        #         # print("ty",t)
                
        #         # print("f====", f.values())
        #         print("iiiiii",t)
        #         csv_writer.writerow(t)
        #     if not k['HIGHER-LD-RIGOR']:
        #         csv_writer.writerow(['HIGHER-LD-RIGOR'])
            count += 1
 
#     # Writing data of CSV file
# csv_writer.writerow(k.values())
 
data_file.close()
# print(d)
# d.to_csv
# df = pd.read_json(r'xyz.json')
# print(df)