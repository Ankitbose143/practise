import pandas as pd


def initial_transform(data):
    """ Initial transformation of files."""
    data = data.iloc[11:]
    new_header = data.iloc[0]
    data = data[1:]
    data.columns = new_header
    data = data.iloc[1:]
    return data
