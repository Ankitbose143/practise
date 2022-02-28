import pandas as pd
from generate_query import Query
from generate_params import Params
from db import Database


class WorkflowAnalysis:
    def __init__(self):
        self.query = Query()
        self.insert_db_query = self.query.insert_analyis_query()
        self.params = Params()

    def read_file(self, csv_name):
        df = pd.read_csv(csv_name, sep=',')
        return df

    def process_data_frame(self, df):
        try:
            df = df.melt(id_vars=["Segment", "Fact"],
                         var_name="Date", value_name="Value")
            df = df.iloc[9:]
            df[["Year", "Month", "Day"]] = df["Date"].str.split(
                "-", expand=True)
            df["Date"] = df["Year"].map(str)+df["Month"].map(str)
            df = df.drop(["Day", "Month", "Year"], axis=1)
            df["Country"] = 1
            return df
        except Exception as error:
            print(error)

    def transform_db_format(self, data):
        list = []
        for index, row in data.iterrows():
            param = self.params.generate_params_analysis(row)
            list.append(param)
        return list

    def initiate_db(self, list):
        Db = Database()
        Db.insert_many(self.insert_db_query, list)
        Db.close()

    def run(self, csv_name):
        print("Started")
        df = self.read_file(csv_name)
        df = self.process_data_frame(df)
        list = self.transform_db_format(df)
        self.initiate_db(list)
        print("Completed")
