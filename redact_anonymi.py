import pandas as pd
import fitz
import re
import os
# from gramex.debug import lineprofile
# print(os.path)
for (root,dirs,files) in os.walk('D:\sorting_searching', topdown=True):
    print(root)
    print(dirs)
    print(files)
    print('--------------------------------')
# print(os.walk())
from pprint import pprint
from pathlib import Path

file = r'C:\Users\ankit.bose\Downloads\Bike Insurance PolicyCopy (4).pdf'
entity = ['2020','2021']
doc = fitz.open(file)
# print("doc",doc.pages.getFontList )
# pprint(doc.get_page_fonts(0, full=False))
# page = doc.loadpage(1)
for page in doc:
    page._wrapContents()
    # print(page.get_fonts(full=False))
    # print(page.getFontList())
    for y in entity:
        if '2020' in y:
            areas = page.searchFor(y)
            print(areas)
            for j in range(len(areas)):
                areas[j][1] = areas[j][1]
                areas[j][3] = areas[j][3]-1
                
        # if areas:
        #     block = page.getText('blocks')
        #          areas = page.searchFor(data)
        #     for i in range(len(block)):
        #         lt = list(block[i])
        #         block[i] = lt
                [page.addRedactAnnot(area,fontname="Arial", text = '2021') for area in areas]
                # break
        elif '2021' in y:
            areas = page.searchFor(y)
            print("11",areas)
            for j in range(len(areas)):
                areas[j][1] = areas[j][1]

                areas[j][3] = areas[j][3]-1
                # break
    # if areas:
    #     block = page.getText('blocks')
    #          areas = page.searchFor(data)
    #     for i in range(len(block)):
    #         lt = list(block[i])
    #         block[i] = lt
            # page.insertFont(fontname="ceshi", fontfile="font.ttf")
            [page.addRedactAnnot(area,fontname="Arial",fontsize=21, text = '2022') for area in areas]
    
    page.apply_redactions()
doc.save('Bike Insurance PolicyCopy.pdf')
print("Successfully redacted")