#encoding:utf-8

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
dirver_path = r"C:\www\chromedriver\chromedriver.exe"

driver = webdriver.Chrome(executable_path=dirver_path)
driver.get("https://www.douban.com/")

time.sleep(8)
rememberBtn = driver.find_element_by_xpath('//*[@id="account-form-remember"]')
rememberBtn.click()