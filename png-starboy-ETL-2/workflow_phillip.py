
import pandas as pd
from generate_query import Query
from generate_params import Params
from db import Database
import numpy as np
# from concurrent.futures import ThreadPoolExecutor
from time import sleep
from pdb import set_trace


class WorkflowPhillip:
    def __init__(self):
        self.month = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
                      "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11,
                      "DEC": 12}
        self.chunk_size = 180559
        self.query = Query()
        self.params = Params()
        self.insert_country = self.query.generate_query_insert_country()
        self.query_ref_prd = self.query.generate_query_rf_product()
        self.query_fct_mkt_mth = self.query.generate_query_fact_market_perf_agg_mth()
        self.query_fct_mkt_wk = self.query.generate_query_fact_market_perf_agg_wk()
        self.query_country_id = self.query.select_query_country_id()
        self.query_prd_id = self.query.select_query_prd_id
        self.country_prd = "Baby"
        # self.executor = ThreadPoolExecutor(5)
        self.region_channel_cut = ['GMA Drugstores',
                                   'GMA Provision/Convenience', 'GMA Supermarket',
                                   'Mindanao Drugstores', 'Mindanao Provision/Convenience',
                                   'Mindanao Supermarket',
                                   'North Luzon Drugstores', 'North Luzon Prvsn/CV',
                                   'North Luzon Supermarket', 'South Luzon Drugstores',
                                   'South Luzon Prvsn/CV', 'South Luzon Supermarket',
                                   'Visayas Drugstores', 'Visayas Provision/Convenience',
                                   'Visayas Supermarket']

    def map_channel(self, row):
        if row["Region"] == "Total Drug/Pharmacy":
            return "Total Drug/Pharmacy"
        elif row["Region"] == "Total Provision/Convenience":
            return "Total Provision/Convenience"
        elif row["Region"] == "Total Supermarket":
            return "Total Supermarket"
        else:
            return None

    def map_region(self, row):
        if row["Region"] == "Total Drug/Pharmacy" or \
                row["Region"] == "Total Provision/Convenience" or \
                row["Region"] == "Total Supermarket":
            return None
        else:
            return row["Region"]

    def transpose_month(self, data):
        # Converting the FEB16,MAR16 as rows under Date Column
        # df = df[df["Sub Region/Channel"]!=]
        df = data.melt(id_vars=["Region", "Sub Region/Channel", "Brand",
                                "Type_PG", "Subbrand", "Pack_Count_PG", "Size",
                                "Packsize", "Facts"],
                       var_name="Date",
                       value_name="Value")
        df[["Month", "Year"]] = df.Date.str.split("\d+", expand=True)
        df[["Year"]] = df.Date.str[-2:]
        df.Year = pd.to_numeric(df.Year, errors='coerce')
        df.Year = 2000+df.Year
        df = df.replace({"Month": self.month})
        df['Month'] = df['Month'].apply(lambda x: '{0:0>2}'.format(x))
        df["Date"] = df["Year"].map(str)+df["Month"].map(str)
        df = df.rename(columns={"Region": "Country",
                                "Sub Region/Channel": "Region"})
        df = df.where((pd.notnull(df)), "")
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        df['Value'] = df['Value'].replace(np.nan, 0)
        df = df.pivot_table(values="Value", index=["Country",
                                                   "Region", "Brand", "Type_PG",
                                                   "Subbrand", "Pack_Count_PG",
                                                   "Size", "Packsize", "Date"],
                            columns="Facts", aggfunc='sum')

        df.reset_index(inplace=True)
        df = df.apply(lambda row: self.map_null(row), axis=1)
        df["country_prd"] = self.country_prd
        country = df[["Country", "country_prd"]]
        country = country.drop_duplicates(
            subset=["Country", "country_prd"], keep="first")
        ref_prd = df[["Brand", "Subbrand", "Type_PG",
                      "Pack_Count_PG", "Size", "Packsize"]]
        ref_prd = ref_prd.drop_duplicates(subset=["Brand", "Subbrand",
                                                  "Type_PG", "Pack_Count_PG",
                                                  "Size", "Packsize"],
                                          keep="first")

        df["Channel"] = df.apply(lambda row: self.map_channel(row), axis=1)
        df["Region"] = df.apply(lambda row: self.map_region(row), axis=1)
        return (df, country, ref_prd)

    def map_null(self, row):
        if row["Brand"] == "":
            row["Brand"] = None
        if row["Subbrand"] == "":
            row["Subbrand"] = None
        if row["Type_PG"] == "":
            row["Type_PG"] = None
        if row["Pack_Count_PG"] == "":
            row["Pack_Count_PG"] = None
        if row["Size"] == "":
            row["Size"] = None
        if row["Packsize"] == "":
            row["Packsize"] = None
        return row

    def loop_month(self, data, type):
        list = []
        Db = Database()
        if type == "country":
            for index, row in data.iterrows():
                param = self.params.generate_params_country_id(
                    row, "tuple")
                country_id = Db.select(self.query_country_id, param)
                if country_id is None:
                    list.append(param)
        elif type == "ref_prd":
            for index, row in data.iterrows():
                param = self.params.generate_params_ref_product(row)
                db_param = tuple(x for x in param if x is not None)
                prd_id = Db.select(self.query_prd_id(param), db_param)
                if prd_id is None:
                    list.append(param)
        elif type == "fct_mth":
            for index, row in data.iterrows():
                country_param = self.params.generate_params_country_id(
                    row, "row")
                country_id = Db.select(self.query_country_id, country_param)
                prd_id_param = self.params.generate_params_ref_product(row)
                db_param = tuple(
                    x for x in prd_id_param if x is not None and x != '')
                query_prd = self.query_prd_id(prd_id_param)
                prd_id = Db.select(query_prd, db_param)
                if len(country_id) > 0 and len(prd_id) > 0:
                    param = self.params.generate_params_fct_mkt_mth(
                        row, country_id, prd_id)
                    list.append(param)
        Db.close()
        return list

    def initiate_insert_db(self, data, query):
        Db = Database()
        if(len(data) >= 1):
            Db.insert_many(query, data)
            sleep(1)
        else:
            pass
        Db.close()
        return True

    def insert_region_prd_fact_month(self, csv_file):
        try:
            chunk = pd.read_csv(csv_file, sep=",")
            chunk = chunk[~chunk["Sub Region/Channel"]
                          .isin(self.region_channel_cut)]
            data, country, ref_prd = self.transpose_month(chunk)
            # set_trace()
            params_region = self.loop_month(country, "country")
            params_ref_prd = self.loop_month(ref_prd, "ref_prd")
            # set_trace()
            if(len(params_region) > 0):
                self.initiate_insert_db(params_region, self.insert_country)
            if(len(params_ref_prd) > 0):
                self.initiate_insert_db(params_ref_prd, self.query_ref_prd)
            params_fct_mkt = self.loop_month(data, "fct_mth")
            if(len(params_fct_mkt) > 0):
                self.initiate_insert_db(
                    params_fct_mkt, self.query_fct_mkt_mth)
        except Exception as e:
            print(e)
            print("ERRROOOORRRR")

    def run(self, csv_file, agg_type):
        if agg_type == "month":
            print("Step2")
            self.insert_region_prd_fact_month(csv_file)
        else:
            print("Step 2")
            self.insert_region_prd_fact_week(csv_file)
        return 1
