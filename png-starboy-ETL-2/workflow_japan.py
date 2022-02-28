import pandas as pd
from generate_query import Query
from generate_params import Params
# from db import Database
from utils_japan import Util


class WorkflowJapan:
    def __init__(self):
        self.query = Query()
        # self.insert_db_query = self.query.insert_japan_query()
        self.params = Params()
        self.query_prd_id = self.query.select_query_prd_id
        self.query_country_id = self.query.select_query_country_id()
        self.query_fct_mkt_mth = self.query.generate_query_fact_market_perf_agg_mth_japan()
        self.query_fct_mkt_wk = self.query.generate_query_fact_market_perf_agg_wk_japan()
        self.insert_country = self.query.generate_query_insert_country()
        self.query_ref_prd = self.query.generate_query_rf_product()
        self.country_prd = "Baby"

    def process_data_frame(self, df, agg_type):
        Utils = Util()
        try:

            df, country, ref_prd = Utils.process_data(
                df, agg_type, self.country_prd)
            self.transform_country_db(country)
            self.transform_data_prd(ref_prd)
            params_fct_mkt = self.transform_data_all(df)
            if(len(params_fct_mkt) > 0):
                if agg_type == "month":
                    self.initiate_insert_db(
                        params_fct_mkt, self.query_fct_mkt_mth)
                else:
                    self.initiate_insert_db(
                        params_fct_mkt, self.query_fct_mkt_wk)
        except Exception as err:
            print(err)

    def transform_data_all(self, data):
        list = []
        Db = Database()
        try:
            for index, row in data.iterrows():
                country_param = self.params.generate_params_country_id(
                    row, "row")
                country_id = Db.select(self.query_country_id, country_param)
                prd_id_param = self.params.generate_params_ref_product(row)
                db_param = tuple(x for x in prd_id_param if x is not None)
                prd_id = Db.select(self.query_prd_id(prd_id_param), db_param)
                if prd_id is not None and country_id is not None:
                    param = self.params.generate_params_fct_mkt_mth_japan(
                        row, country_id, prd_id)
                    list.append(param)
        except Exception as err:
            print(err)
        finally:
            Db.close()
            return list

    def transform_country_db(self, data):
        Db = Database()
        try:
            for index, row in data.iterrows():
                param = self.params.generate_params_country_id(row, "tuple")
                country_id = Db.select(self.query_country_id, param)
                if country_id is None:
                    self.initiate_insert_db(param, self.insert_country)
        except Exception as err:
            print(err)
        finally:
            Db.close()

    def transform_data_prd(self, data):
        Db = Database()
        try:
            for index, row in data.iterrows():
                prd_id_param = self.params.generate_params_ref_product(row)
                db_param = tuple(x for x in prd_id_param if x is not None)
                prd_id = Db.select(self.query_prd_id(prd_id_param), db_param)
                if prd_id is None:
                    self.initiate_insert_db([prd_id_param], self.query_ref_prd)
        except Exception as err:
            print(err)
            print("Error while transforming the data in the PRD table")
        finally:
            Db.close()

    def initiate_insert_db(self, data, query):
        Db = Database()
        if(len(data) >= 1):
            Db.insert_many(query, data)
        else:
            pass
        Db.close()
        return True

    def run(self, csv_name, agg_type):
        df = pd.read_csv(csv_name, sep=',', error_bad_lines=False,
                         index_col=False, dtype='unicode')
        self.process_data_frame(df, agg_type)
