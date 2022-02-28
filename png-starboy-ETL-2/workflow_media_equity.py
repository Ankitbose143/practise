from util_media_equity import Util
from pdb import set_trace
import pandas as pd


class WorkflowMediaEquity:
    def __init__(self):
        pass

    def run(self, csv_name, agg_type):
        try:
            df = pd.read_csv(csv_name, sep=",", skiprows=2)
            util = Util()
            df = util.process_data(df)
            set_trace()
        except Exception as err:
            print(err)
        finally:
            return df
