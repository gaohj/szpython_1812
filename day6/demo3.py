#encoding:utf-8

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
dirver_path = r"C:\www\chromedriver\chromedriver.exe"

driver = webdriver.Chrome(executable_path=dirver_path)
driver.get("https://www.baidu.com/")

# print(driver.get_cookies())
for cookie in driver.get_cookies():
    print(cookie)

print("="*30)

print(driver.get_cookie('PSTM'))

driver.delete_cookie('PSTM')
print("="*30)
print(driver.get_cookie('PSTM'))
driver.delete_all_cookies()
print("="*30)
print(driver.get_cookies())