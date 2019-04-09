#encoding:utf-8

from selenium import webdriver
import time

dirver_path = r"C:\www\chromedriver\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("--proxy-server=http://120.236.130.132:8060")

driver = webdriver.Chrome(executable_path=dirver_path,chrome_options=options)

driver.get("http://httpbin.org/ip")
