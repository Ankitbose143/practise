from workflow_phillip import WorkflowPhillip
from workflow_japan import WorkflowJapan
from workflow_koi import WorkflowJapanKOI
from workflow_media import WorkflowMedia
from workflow_analysis import WorkflowAnalysis
from convert_csv import csv_from_excel
from concurrent.futures import ThreadPoolExecutor
from workflow_media_equity import WorkflowMediaEquity
from workflow_penetration import WorkflowPenetration
import time


class Main:
    def __init__(self):
        self.workflowPhillip = WorkflowPhillip()
        self.workflowAnalysis = WorkflowAnalysis()
        self.workflowJapan = WorkflowJapan()
        self.workflowMedia = WorkflowMedia()
        self.workflowMediaEquity = WorkflowMediaEquity()
        self.workflowKoi = WorkflowJapanKOI()
        self.workflowPenetration = WorkflowPenetration()

    def main(self, xlsx, sheet_name, csv_name, agg_type, type_data, product_type, status):
        # status = True
        print("Step 1")
        start_time = time.time()
        print(start_time)
        if status is False:
            status = csv_from_excel(xlsx, sheet_name, csv_name)
        if status:
            if type_data == "phillp":
                if product_type == "baby":
                    self.workflowPhillip.run(csv_name, agg_type)
                elif product_type == "media":
                    self.workflowMedia.run(xlsx, sheet_name, type_data)
                else:
                    self.workflowMediaEquity.run(csv_name, agg_type)
            elif type_data == "analysis":
                self.workflowAnalysis.run(csv_name)
            elif type_data == "japan":
                if product_type == "baby":
                    self.workflowJapan.run(csv_name, agg_type)
                elif product_type == "japan_koi":
                    self.workflowKoi.run(xlsx, sheet_name, agg_type, csv_name)
                else:
                    pass
            elif type_data == "penetration":
                self.workflowPenetration.run(agg_type, csv_name, product_type)
            else:
                print("No worflow Registered")
        else:
            print(status)
            print("some error")
        end_time = time.time()
        diff = end_time-start_time
        print(diff)


class Execute:
    def __init__(self):
        self.executor = ThreadPoolExecutor(5)

    def exec(self):
        main = Main()
        with ThreadPoolExecutor(max_workers=1) as executor:

            # executor.submit(main.main, "Dummy Data Table_Screen3.xlsx",
            #                 "Equity", "screen3.csv", "month", "analysis")
            '''This is for the Japan Data MOnth'''
            # executor.submit(main.main, "data/Baby Diaper Japan-Manual.xlsx",
            #                 "Sheet1", "converted/japan_brand.csv",
            #                 "month", "japan", "baby", False)
            '''This is for the Japan Data Weekly'''
            # executor.submit(main.main, "data/Baby Diaper Weekly Manual Transformed.xlsx",
            #                 "Sheet1", "converted/japan_brand.csv",
            #                 "weekly", "japan", "baby",False)
            '''This is for the Phillpenes Data'''
            # executor.submit(main.main, "data/PH Diaper category & Brand with Region & Channel _Dec'19.xlsx",
            #                 "Brand", "converted/phillip_brand.csv",
            #                 "month", "phillp", "baby", False)
            '''This is for Media data Phillpenes'''
            # executor.submit(main.main, "data/3. Pampers EQ GRP 2016 - 2019_Media KPI.xlsx",
            #                 "(P) - Monthly Product reach, fr", "converted/media.csv",
            #                 "month", "phillp", "media", True)

            '''This is for the Media Equity Data Phillpenes'''
            # executor.submit(main.main, "data/Baby Care BHT PH AMJ19 Brand Funnel by Region - sent to Shenoy 10Sep2019.xlsx",
            #                 "Brand Funnel - Total PH", "converted/media_equity.csv",
            #                 "month", "phillp", "media_quity", False)
            '''This is for the Japan KOI data Monthly'''
            executor.submit(main.main, "data/KOI Monthly Gramener_FINAL_v2 - Manual.xlsx",
                            "Sheet1", "converted/japan_koi.csv",
                            "month", "japan", "japan_koi", True)

            '''This is for the Japan KOI data weekly'''
            # executor.submit(main.main, "data/Weekly KOI Data_Manual.xlsx",
            #                 "Sheet1", "converted/japan_koi_weekly.csv",
            #                 "weekly", "japan", "japan_koi", True)

            '''This is for the Japan KOI Penetration Data Monthly'''
            # executor.submit(main.main, "data/KOI HHP Gramener_FINAL-18th Oct.xlsx",
            #                 "Sheet1", "converted/japan_koi_penetration.csv",
            #                 "month", "penetration", "japan_koi", False)

            '''This is for the Japan Baby Penetration Data Monthly'''
            # executor.submit(main.main, "data/Baby Diaper HHP Gramener Quarterly-Manual-18th Oct.xlsx",
            #                 "Sheet1", "converted/japan_baby_penetration.csv",
            #                 "month", "penetration", "japan_baby", False)


if __name__ == "__main__":
    execute = Execute()
    execute.exec()
