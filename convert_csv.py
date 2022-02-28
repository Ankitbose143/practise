import xlrd
import csv
import pandas as pd


def csv_from_excel(xlsFile, sheet_name, csv_name):
    try:
        wb = xlrd.open_workbook(xlsFile)
        sh = wb.sheet_by_name(sheet_name)
        your_csv_file = open(csv_name, 'w')
        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))
        your_csv_file.close()
        return True
    except Exception as e:
        print(e)
        return False
