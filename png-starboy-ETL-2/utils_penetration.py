import pandas as pd
import numpy as np
from pdb import set_trace


class Utils:
    def __init__(self):
        self.column_map_koi = {
            "MAIN BRAND": "Brand",
            "AISLE_PG": "Type_PG",
            "CC/GUSHES RANGE_PG": "Pack_Count_PG",
            "CC/GUSHES ABSOLUTE": "Pack_Count_PG",
            "BRAND": "Subbrand",
            "PACK COUNT": "Packsize"
        }
        self.column_map_baby = {
            "MAIN BRAND": "Brand",
            "TYPE": "Type_PG",
            "PACK SIZE": "Packsize",
            "Size": "Size",
            "BRAND": "Subbrand"
        }
        self.country_prd_koi = "Fem"
        self.country_prd_baby = "Baby"
        self.column_name = ["Country", "country_prd", "Brand", "Packsize",
                            "Type_PG", "Subbrand", "Pack_Count_PG", "Region",
                            "Facts", "Size"]
        self.fact_map = {
            "Purchase rate (Purchaser)": "Penetration"
        }
        self.column_name_pivot = ["Region", 'Type_PG', 'Subbrand', 'Brand',
                                  'Pack_Count_PG', 'Size', "Packsize",
                                  'Date', "Country", "country_prd"]
        self.ref_prd_combination = ["Brand", "Subbrand",
                                    "Type_PG", "Pack_Count_PG",
                                    "Packsize", "Size"]

    def rename_col(self, df, product_type):
        try:
            if product_type == "japan_koi":
                df = df.rename(columns=self.column_map_koi)
            else:
                df = df.rename(columns=self.column_map_baby)
        except Exception as err:
            print(err)
        finally:
            return df

    def add_columns(self, df, product_type):
        try:
            if product_type == "japan_koi":
                df["Size"] = ''
                df["country_prd"] = self.country_prd_koi
            else:
                df["Pack_Count_PG"] = ''
                df["country_prd"] = self.country_prd_baby

            df["Country"] = "Japan"
            df["Region"] = "TTL National"

        except Exception as err:
            print(err)
        finally:
            return df

    def convert_date_rows(self, df):
        try:
            df = df.melt(id_vars=self.column_name,
                         var_name="Date",
                         value_name="Stats")
            df = df.where((pd.notnull(df)), None)
        except Exception as err:
            print("Error while converting the date into rows")
            print(err)
        finally:
            return df

    def add_month_year(self, df):
        try:
            df[["Year", "Month"]] = df.Date.str.split("/", expand=True)
            df['Month'] = df['Month'].apply(lambda x: x.replace("-", ""))
            df['Month'] = df['Month'].apply(lambda x: '{0:0>2}'.format(x))
            df["Date"] = df["Year"].map(str)+df["Month"].map(str)
            df['Date'] = pd.to_numeric(df['Date'], errors='coerce')
            df = self.remove_col(df, "Year")
            df = self.remove_col(df, "Month")
        except Exception as err:
            print(err)
        finally:
            return df

    def remove_col(self, df, col_name):
        try:
            df = df.drop([col_name], axis=1)
        except Exception as err:
            print("Error while removing the column i.e. column does not exist")
            print(err)
        finally:
            return df

    def clean_value_col(self, df):
        try:
            df['Stats'] = pd.to_numeric(df['Stats'], errors='coerce')
            df['Stats'] = df['Stats'].replace(np.nan, 0.0)
        except Exception as err:
            print(err)
        finally:
            return df

    def map_facts(self, df):
        try:
            df["Facts"] = df["Facts"].map(self.fact_map)
            df = df.dropna(subset=["Facts"])
        except Exception as err:
            print(err)
        finally:
            return df

    def remove_nan_null(self, df):
        df = df.replace('TTL', df.replace(['TTL'], [None]))
        df = df.replace('', df.replace([''], [None]))
        df = df.where((pd.notnull(df)), None)
        df = df.dropna(subset=["Brand"])
        return df

    def transform_date_row_col(self, df):
        try:
            df = df.pivot_table(index=self.column_name_pivot,
                                values='Stats',
                                columns='Facts',
                                aggfunc='sum')
            df.reset_index(inplace=True)
        except Exception as err:
            print(err)
        finally:
            return df

    def get_country(self, df):
        country = df[["Country", "country_prd"]]
        country = country.drop_duplicates(
            subset=["Country", "country_prd"], keep="first")
        return country

    def uniq_prd(self, df):
        ref_prd = df[self.ref_prd_combination]
        ref_prd = ref_prd.drop_duplicates(
            subset=self.ref_prd_combination, keep="first")
        return ref_prd

    def process_data(self, df, product_type):
        country = pd.DataFrame()
        ref_prd = pd.DataFrame()
        df = self.rename_col(df, product_type)
        df = self.add_columns(df, product_type)
        df = self.convert_date_rows(df)
        df = self.add_month_year(df)
        df = self.clean_value_col(df)
        df = self.map_facts(df)
        df = self.transform_date_row_col(df)
        df = self.remove_nan_null(df)
        country = self.get_country(df)
        ref_prd = self.uniq_prd(df)
        return (df, country, ref_prd)
