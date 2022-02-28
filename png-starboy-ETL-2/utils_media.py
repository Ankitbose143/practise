import pandas as pd
from pdb import set_trace


class Util:
    def __init__(self):
        self.columns_map = {
            'Analysis: PostBuy  ': "Product",
            'Unnamed: 1': "Year",
            'Unnamed: 2': "Month",
            'Unnamed: 3': "insertion",
            'Unnamed: 4': 'insert_twenty_five_plus',
            'Unnamed: 5': "insert_sixteen_to_twenty_four",
            'Unnamed: 6': "grp",
            'Unnamed: 7': "grp_twenty_five_plus",
            'Unnamed: 8': "grp_sixteen_to_twenty_four",
            'Unnamed: 9': "grp_per_spot",
            'Unnamed: 10': "grp_per_spot_twenty_five_plus",
            'Unnamed: 11': "grp_per_spot_sixteen_to_twenty_four"
        }
        self.month_map = {
            'Jan': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
            'August': 8, 'September': 9, 'October': 10, 'November': 11,
            'December': 12, 'January': 1, "Feb": 2, "Mar": 3, "Apr": 4, "Jun": 6,
            "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11,
            "Dec": 12
        }
        self.brand_map = {
            "EQ BABY DIAPERS": "EQ",
            "PAMPERS DIAPERS": 'Pampers'
        }

    def process_data_frame(self, df, type_data):
        prd = pd.DataFrame()
        country = pd.DataFrame()
        try:
            df = self.drop_nan(df)
            df = self.map_columns(df)
            df = self.map_product(df)
            df = self.map_month_year(df)
            df = self.add_country(df, type_data)
            prd = self.get_uniq_product(df)
            country = self.get_uniq_country(df)
        except Exception as err:
            print(err)
        finally:
            return (df, prd, country)

    def map_product(self, df):
        try:
            df = df.replace({"Product": self.brand_map})
        except Exception as err:
            print(err)
        finally:
            return df

    def drop_nan(self, df):
        df = df.dropna()
        return df

    def map_columns(self, df):
        try:
            df = df.rename(columns=self.columns_map)
            df = df.iloc[1:]
        except Exception as err:
            print(err)
        finally:
            return df

    def map_month_year(self, df):
        try:
            df[['Month', "Temp_Year"]] = df['Month'].str.split(
                '\s', expand=True)
            df = df.replace({"Month": self.month_map})
            df['Month'] = df['Month'].apply(lambda x: '{0:0>2}'.format(x))
            df["Date"] = df["Year"].map(str)+df["Month"].map(str)
            df = self.remove_col(df, "Month")
            df = self.remove_col(df, "Temp_Year")
            df = self.remove_col(df, "Year")
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

    def get_uniq_product(self, df):
        prd = df.Product
        prd = prd.to_frame()
        prd = df.drop_duplicates(subset=["Product"], keep="first")
        return prd

    def get_uniq_country(self, df):
        country = df.Country
        country = country.to_frame()
        country = df.drop_duplicates(subset=["Country"], keep="first")
        return country

    def add_country(self, df, type_data):
        if type_data == "phillp":
            df["Country"] = "Philippines"
        else:
            df["Country"] = "Japan"
        return df
