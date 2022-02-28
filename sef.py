# import pandas as pd
# import re , time
# df = pd.read_excel(r'sd.xlsx', sheet_name='Sheet3')
# print(df.columns)
# print(type(df['A']), type(df))

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(r'C:\Users\ankit.bose\Downloads\chromedriver.exe')
driver.get("https://www.instagram.com/")

print(driver.title)
#email id pie
search_bar = driver.find_element_by_name("username")

search_bar.clear()
search_bar.send_keys("swatisucharita21@gmail.com")
#password pie
search_bar2 = driver.find_element_by_name("password")
search_bar2.clear()
search_bar2.send_keys("swatisucharita21@gmail.com")

# login
search_bar3 = driver.find_element_by_name("q")
search_bar3.click()

# search_bar.send_keys(Keys.RETURN)

#pytest

# driver.close()