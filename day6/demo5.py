#encoding:utf-8

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
dirver_path = r"C:\www\chromedriver\chromedriver.exe"

driver = webdriver.Chrome(executable_path=dirver_path)
driver.get("https://www.baidu.com/")
#执行js代码
driver.execute_script("window.open('https://www.douban.com')")
print(driver.window_handles)

print(driver.current_url)
driver.switch_to_window(driver.window_handles[1])
print(driver.current_url)
print(driver.page_source)