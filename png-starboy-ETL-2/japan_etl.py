import pandas as pd
from init_transformation import initial_transform
from utils_japan import Util
from workflow_japan import WorkflowJapan
# from workflow_koi import WorkflowJapanKOI
# df1 = pd.read_excel("data/Baby Diaper Monthly 1.xlsx", sheet_name="Sheet1", header=None)
# df2 = pd.read_excel("data/Baby Diaper Monthly 2.xlsx", sheet_name="Sheet1", header=None)
# df3 = pd.read_excel("data/Baby Diaper Monthly 3.xlsx", sheet_name="Sheet1", header=None)

file1 = "data/Baby Diaper Monthly1.xlsx"
file2 = "data/Baby Diaper Monthly2.xlsx"
file3 = "data/Baby Diaper Monthly3.xlsx"
file4 = "data/KOI Monthly Gramener_FINAL_v2.xlsx"
file5 = "data/KOI HHP Gramener_FINAL.xlsx"

df1 = pd.read_excel(file1, sheet_name="Sheet1", header=None)
df2 = pd.read_excel(file2, sheet_name="Sheet1", header=None)
df3 = pd.read_excel(file3, sheet_name="Sheet1", header=None)
df4 = pd.read_excel(file4, sheet_name="Sheet1", header=None)
df5 = pd.read_excel(file5, sheet_name="Sheet1", header=None)


def split_packsize(data):

    # dropping null value columns to avoid errors
    # data.dropna(inplace=True)

    # new data frame with split value columns
    new = data["packsize cust1"].str.split(":", n=1, expand=True)

    # Dropping old Name columns
    data.drop(columns=["packsize cust1"], inplace=True)

    data.insert(4, "PACK SIZE", new[0])
    data.insert(5, "SIZE", new[1])
    return data


def file1_transformation(data):
    for i in range(5, 9):
        data.columns.values[i] = 'col'
    cols = [5, 6, 7, 8]
    data.drop(data.columns[cols], axis=1, inplace=True)
    new_data = split_packsize(data)
    new_data.insert(6, "PACK COUNT", " ")
    new_data = new_data[~new_data["PACK SIZE"].str.contains("TTL")]
    new_data.columns.values[7] = 'FACTS'
    return new_data


def file2_transformation(data):
    for i in range(5, 9):
        data.columns.values[i] = 'col'
    cols = [5, 6, 7, 8]
    data.drop(data.columns[cols], axis=1, inplace=True)
    data.columns.values[5] = 'FACTS'
    data.insert(loc=5, column='SIZE', value="")
    data.insert(loc=6, column='PACK COUNT', value="")
    return data


def file3_transformation(data):
    """Transforms Monthly / Weekly 3 file."""
    for i in range(3, 9):
        data.columns.values[i] = 'col'
    cols = [3, 4, 5, 6, 7, 8]
    data.drop(data.columns[cols], axis=1, inplace=True)
    data.insert(loc=2, column='TYPE', value="")
    data.insert(loc=3, column='BRAND', value="")
    data.insert(loc=4, column='PACK SIZE', value="")
    data.insert(loc=6, column='PACK COUNT', value="")
    data.columns.values[7] = 'FACTS'
    data = data[~data.Size.str.contains("TTL")]
    data.rename(columns={'Size': 'SIZE'}, inplace=True)
    return data

def file4_transformation(data):
    """Transform KOI Monthly Gramener_FINAL_v2 data file:"""
    for i in range(5,9):
        data.columns.values[i] = 'col'
    data.columns.values[10] = 'col'
    cols =[5,6,7,8,10]
    data.drop(data.columns[cols],axis=1,inplace=True)
    data.columns.values[5] = 'FACTS'
    print("Line83",data.head(5))
    return data

def file5_transformation(data):
    """Transform KOI HHP Gramener data file:"""
    for i in range(5,9):
        data.columns.values[i] = 'col'
    data.columns.values[10] = 'col'
    cols =[5,6,7,8,10]
    data.drop(data.columns[cols],axis=1,inplace=True)
    data.columns.values[5] = 'FACTS'
    print("Line96",data.head(5))
    return data


data1 = initial_transform(df1)
# if("Weekly" in file1):
#     del data1["8.12-2019"]
#     del data1["8.19-2019"]

data1 = file1_transformation(data1)

data2 = initial_transform(df2)
data2 = file2_transformation(data2)


data3 = initial_transform(df3)
data3 = file3_transformation(data3)

data4 = initial_transform(df4)
data4 = file4_transformation(data4)

data5 = initial_transform(df5)
data5 = file5_transformation(data5)

merged_data = data2.append(data3, sort=False)
final_merged = merged_data.append(data1, sort=False)

cols = ["TYPE", "BRAND", "MAIN BRAND",
        "TTL + Channels", "PACK SIZE", "SIZE", "PACK COUNT"]
for index in cols:
    final_merged[index] = final_merged[index].replace("", "TTL")

del final_merged["TOTAL"]

final_merged.drop(final_merged.index[[7, 8, 9, 10, 11, 12, 13]], inplace=True)
final_merged["TTL + Channels"] = final_merged["TTL + Channels"].replace(
    "TTL", "TTL National")
final_merged["TTL + Channels"] = final_merged["TTL + Channels"].replace(
    "Total National", "TTL National")
# final_merged.to_excel("transformation_weekly.xlsx", encoding='UTF-8', index=False)
final_merged.rename(columns={'PACK COUNT': 'Pack Count',
                             'SIZE': 'Size', 'FACTS': 'Facts'}, inplace=True)


data4["KOI TTL + National Month"] = data4["KOI TTL + National Month"].replace("TTL", "TTL National")
data4["KOI TTL + National Month"] = data4["KOI TTL + National Month"].replace("Total National", "TTL National")
# data4.to_excel('file123.xlsx', index=False)
# data5.to_excel('file273.xlsx', index=False)

# def process_data_frame(df, agg_type):
#     Utils = Util()
#     workflowJapan = WorkflowJapan()
#     try:
#         workflowJapan.process_data_frame(df, agg_type)
#     except Exception as err:
#         print(err)

# process_data_frame(final_merged, "month")

# def process_data_frame(df, agg_type):
#     Utils = UtilKoi()
#     workflowJapanKOI = WorkflowJapanKOI()
#     try:
#         workflowJapanKOI.process_data_frame(df, agg_type)
#     except Exception as err:
#         print(err)

# process_data_frame(data4, "month")
