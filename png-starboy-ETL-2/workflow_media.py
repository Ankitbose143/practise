import pandas as pd
from pdb import set_trace
from utils_media import Util
from db import Database
from generate_query import Query
from generate_params import Params


class WorkflowMedia:
    def __init__(self):
        self.params = Params()
        self.query = Query()
        self.query_country_id = self.query.select_query_country_id()
        self.query_prd_media = self.query.select_query_prd_media()
        self.query_prd_media_insert = self.query.insert_media_prd()
        self.query_fact_media = self.query.insert_fact_media()

    def run(self, xlsx, sheet_name, type_data):
        df = pd.read_excel(xlsx, sheet_name=sheet_name)
        util = Util()
        df, prd, country = util.process_data_frame(df, type_data)
        self.transform_country_db(country)
        self.transform_data_prd(prd)
        params_fct_media = self.transform_data_all(df)
        if(len(params_fct_media) > 0):
            self.initiate_insert_db(
                params_fct_media, self.query_fact_media)

    def initiate_insert_db(self, data, query):
        Db = Database()
        if(len(data) >= 1):
            Db.insert_many(query, data)
        else:
            pass
        Db.close()
        return True

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
                prd_param = self.params.generate_params_prd_media(row)
                prd_id = Db.select(self.query_prd_media, prd_param)
                if prd_id is None:
                    self.initiate_insert_db(
                        [prd_param], self.query_prd_media_insert)
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
                prd_id_param = self.params.generate_params_prd_media(row)
                prd_id = Db.select(self.query_prd_media, prd_id_param)
                if prd_id is not None and country_id is not None:
                    param = self.params.generate_params_fct_media(
                        row, country_id, prd_id)
                    list.append(param)
        except Exception as err:
            print(err)
        finally:
            Db.close()
            return list
