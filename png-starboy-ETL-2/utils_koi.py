from koi_clean import map_column_name
from koi_clean import init_transform
from koi_clean import file_transformation
from utils_japan import Util
import pandas as pd


class UtilKoi:
    def __init__(self):
        self.rename_map = {
            "CC/GUSHES RANGE_PG": "Pack_Count_PG",
            "CC/GUSHES ABSOLUTE": "Pack_Count_PG",
            "AISLE_PG": "Type_PG",
            "MAIN BRAND": "Brand",
            "BRAND": "Subbrand",
            "KOI TTL + National Month": "Channel",
            "KOI Total National Weekly": "Channel"
        }

    def process_data(self, xlsx, df, agg_type, country_prd):
        Utils = Util()
        country = pd.DataFrame()
        ref_prd = pd.DataFrame()
        try:
            # df = self.clean_data(xlsx, df)
            df = self.rename_cols(df)
            df = self.add_columns(df)
            df, country, ref_prd = Utils.process_data(
                df, agg_type, country_prd, "koi")
        except Exception as err:
            print(err)
        finally:
            return (df, country, ref_prd)

    def add_columns(self, df):
        df["Packsize"] = None
        df["Size"] = None
        return df

    def clean_data(self, xlsx, df):
        try:
            col_name = map_column_name(xlsx)
            df = init_transform(df)
            df = file_transformation(df, col_name)
        except Exception as err:
            print(err)
        finally:
            return df

    def rename_cols(self, df):
        try:
            df = df.rename(columns=self.rename_map)
        except Exception as err:
            print("Error while renaming the column i.e. column does not exist")
            print(err)
        finally:
            return df
