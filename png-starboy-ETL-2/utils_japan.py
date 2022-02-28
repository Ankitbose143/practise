import pandas as pd
import numpy as np
from pdb import set_trace
from datetime import date


class Util:
    def __init__(self):
        self.column_name = ["Channel", "Brand", "Packsize",
                            "Type_PG", "Subbrand", "Pack_Count_PG",
                            "Facts", "Size"]
        self.column_name_pivot = ['Channel', 'Type_PG', 'Subbrand', 'Brand',
                                  'Pack_Count_PG', 'Size', "Packsize",
                                  'Date']
        self.col_map = {
            "Market share (1000SU)": "Volume_share",
            "Market size (Value) x1/1,000": "Value_sales",
            "Market size (1000SU) x1/1,000": "Volume_msu",
            "Total Distribution Point (Sales 1000SU)": "Tdp",
            "Average selling price (1000SU)": "Avg_price",
            "Distribution (PCW; Sales Volume)": "Acv",
            "Distribution (PCW; Sales 1000SU)": "Acv",
            "Sales per PCW (Sales 1000SU) x1/1,000": "Volume_sppd"
        }
        self.rename_map = {'TTL + Channels': 'Channel',
                           'MAIN BRAND': 'Brand',
                           'TYPE': 'Type_PG',
                           'BRAND': 'Subbrand',
                           'PACK SIZE': 'Pack_Count_PG',
                           'Pack Count': 'Packsize'}
        self.ref_prd_combination = ["Brand", "Subbrand",
                                    "Type_PG", "Pack_Count_PG",
                                    "Packsize", "Size"]

    def process_data(self, df, agg_type, country_prd, product="baby"):
        country = pd.DataFrame()
        ref_prd = pd.DataFrame()
        try:

            df = self.rename_cols(df, product)
            df = self.convert_nan_empty_str(df)
            df = self.convert_date_rows(df)
            df = self.add_month_year(df, agg_type)
            df = self.clean_value_col(df)
            df = self.map_facts(df)
            df = self.transform_date_row_col(df)
            df = self.remove_nan_null(df)
            df = self.add_country_region(df, country_prd)
            country = self.get_country(df)
            ref_prd = self.uniq_prd(df)
        except Exception as err:
            print(err)
        finally:
            return (df, country, ref_prd)

    def convert_nan_empty_str(self, df):
        df['Packsize'] = df['Packsize'].replace(np.nan, "")
        df['Size'] = df['Size'].replace(np.nan, "")
        df['Subbrand'] = df['Subbrand'].replace(np.nan, "")
        df['Type_PG'] = df['Type_PG'].replace(np.nan, "")
        df['Pack_Count_PG'] = df['Pack_Count_PG'].replace(np.nan, "")
        return df

    def remove_nan_null(self, df):
        df = df.replace('TTL', df.replace(['TTL'], [None]))
        df = df.replace('', df.replace([''], [None]))
        df = df.where((pd.notnull(df)), None)
        df = df.dropna(subset=["Brand"])
        return df

    def remove_col(self, df, col_name):
        try:
            df = df.drop([col_name], axis=1)
        except Exception as err:
            print("Error while removing the column i.e. column does not exist")
            print(err)
        finally:
            return df

    def rename_cols(self, df, product):
        try:
            if product == "baby":
                df = df.rename(columns=self.rename_map)
        except Exception as err:
            print("Error while renaming the column i.e. column does not exist")
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

    def process_date_month(self, df):
        df[["Year", "Month"]] = df.Date.str.split("/", expand=True)
        df['Month'] = df['Month'].apply(lambda x: x.replace("-", ""))
        df['Month'] = df['Month'].apply(lambda x: '{0:0>2}'.format(x))
        df["Date"] = df["Year"].map(str)+df["Month"].map(str)
        df['Date'] = pd.to_numeric(df['Date'], errors='coerce')
        df = self.remove_col(df, "Year")
        df = self.remove_col(df, "Month")
        return df

    def process_date_week(self, df):
        try:
            df["Date"] = df.Date.apply(lambda x: x.replace(".", "-"))
            df[["Month", "Day", "Year"]] = df.Date.str.split("-", expand=True)
            df["Week"] = df.Date.apply(lambda x: self.map_week_number(x))
            df["Year"] = df.Date.apply(lambda x: self.map_year_number(x))
            df['Week'] = df['Week'].apply(lambda x: '{0:0>2}'.format(x))
            df["Date"] = df["Year"].map(str)+df["Week"].map(str)
            df['Date'] = pd.to_numeric(df['Date'], errors='coerce')
            df = self.remove_col(df, "Day")
            df = self.remove_col(df, "Year")
            df = self.remove_col(df, "Month")
            df = self.remove_col(df, "Week")
        except Exception as err:
            print(err)
        finally:
            return df

    def add_month_year(self, df, agg_type):
        try:
            if agg_type == "month":
                df = self.process_date_month(df)
            else:
                df = self.process_date_week(df)
        except Exception as err:
            print(err)
        finally:

            return df

    def map_week_number(self, temp):
        temp_date = list(map(int, temp.split("-")))
        temp_date = date(temp_date[2], temp_date[0], temp_date[1])
        week = temp_date.isocalendar()[1]
        return week

    def map_year_number(self, temp):
        temp_date = list(map(int, temp.split("-")))
        temp_date = date(temp_date[2], temp_date[0], temp_date[1])
        year = temp_date.isocalendar()[0]
        return year

    def clean_value_col(self, df):
        try:
            df['Stats'] = pd.to_numeric(df['Stats'], errors='coerce')
            df['Stats'] = df['Stats'].replace(np.nan, 0.0)
        except Exception as err:
            print(err)
        finally:
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

    def map_facts(self, df):
        try:
            df["Facts"] = df["Facts"].map(self.col_map)
        except Exception as err:
            print(err)
        finally:
            return df

    def add_country_region(self, df, country_prd):
        df["Country"] = "Japan"
        df["country_prd"] = country_prd
        df["Channel"] = df.apply(lambda row: self.map_channel(row), axis=1)
        df["Region"] = df.apply(
            lambda row: self.map_region(row), axis=1)
        return df

    def map_region(self, row):
        if row["Channel"] is None:
            return "TTL National"
        else:
            return None

    def map_channel(self, row):
        if row["Channel"] == "TTL National" or row["Channel"] == "Total National":
            return None
        else:
            return row["Channel"]

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
