import pandas as pd
import numpy as np


def map_column_name(file_name):
    """Select appropriate column name based on the file."""
    col_name = "KOI TTL + National Month" if(
        "Monthly" in file_name) else "KOI Total National Weekly"
    return col_name


def split_packsize(data):
    """ Split the column values based on the delimiter."""
    new = data["AislexCCGushes_Weekly"].str.split(":", n=1, expand=True)
    data.drop(columns=["AislexCCGushes_Weekly"], inplace=True)

    data.insert(4, "CCGushes", new[0])
    data.insert(5, "Aisle_PG", new[1])
    return data


def init_transform(data):
    """ Initial transformation of the file."""
    data = data.iloc[11:]
    data.columns = data.iloc[0]
    data = data[2:]
    for i in range(5, 9):
        data.columns.values[i] = 'cols'
    data.drop('cols', axis=1, inplace=True)
    return data


def file_transformation(data, col_name):
    """ Final transformation."""
    data1 = split_packsize(data)
    data1.columns.values[6] = 'Facts'
    del data1["TOTAL"]
    data1['Aisle_PG'] = data1["Aisle_PG"].fillna("TTL")

    # delete rows where first column has Total National and next 5 columns has TTL as their value.
    data1 = data1[~((data1[col_name] == 'Total National') & (data1['MAIN BRAND'] == 'TTL') & (data1['BRAND'] == 'TTL') &
                    (data1['FORM'] == 'TTL') & (data1['CCGushes'] == 'TTL') & (data1['Aisle_PG'] == 'TTL'))]

    # replace TTL in column1 with Total National based on the condition.
    data1[col_name] = np.where(((data1[col_name] == "TTL") & (data1['MAIN BRAND'] == "TTL") &
                                (data1['BRAND'] == "TTL") & (data1['FORM'] == "TTL") & (data1['CCGushes'] == "TTL") &
                                (data1['Aisle_PG'] == "TTL")), "Total National", data1[col_name])
    return data1
