import pandas as pd


class Util:
    def __init__(self):
        pass

    def process_data(self, df):
      #   df = self.map_header(df)
        return df

    def map_header(self, df):
        df.columns = df.iloc[1]
        return df
