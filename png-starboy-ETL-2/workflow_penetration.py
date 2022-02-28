import pandas as pd
from utils_penetration import Utils
from db import Database
from pdb import set_trace
from generate_params import Params
from generate_query import Query


class WorkflowPenetration:
    def __init__(self):
        self.params = Params()
        self.query = Query()
        self.query_country_id = self.query.select_query_country_id()
        self.insert_country = self.query.generate_query_insert_country()
        self.query_prd_id = self.query.select_query_prd_id
        self.query_ref_prd = self.query.generate_query_rf_product()
        self.query_fct_mkt_mth = self.query.generate_query_fact_penetration_japan()

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

    def initiate_insert_db(self, data, query):
        Db = Database()
        if(len(data) >= 1):
            Db.insert_many(query, data)
        else:
            pass
        Db.close()
        return True

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
                    param = self.params.generate_params_fct_mkt_mth_penetration(
                        row, country_id, prd_id)
                    list.append(param)
        except Exception as err:
            print(err)
        finally:
            Db.close()
            return list

    def process_dataframe(self, df, country, ref_prd):
        self.transform_country_db(country)
        self.transform_data_prd(ref_prd)
        params_fct_mkt = self.transform_data_all(df)
        if(len(params_fct_mkt) > 0):
            self.initiate_insert_db(params_fct_mkt, self.query_fct_mkt_mth)

    def run(self, agg_type, csv_name, product_type):
        df = pd.read_csv(csv_name, sep=',', error_bad_lines=False,
                         index_col=False, dtype='unicode')
        Util = Utils()
        df, country, ref_prd = Util.process_data(df, product_type)
        # set_trace()
        '''Write the program for inserting the penetration data'''
        self.process_dataframe(df, country, ref_prd)
