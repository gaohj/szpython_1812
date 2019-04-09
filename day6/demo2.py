#encoding:utf-8

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
dirver_path = r"C:\www\chromedriver\chromedriver.exe"

driver = webdriver.Chrome(executable_path=dirver_path)
driver.get("https://www.baidu.com/")
inputTag = driver.find_element_by_id('kw')
subTag = driver.find_element_by_id('su')

actions = ActionChains(driver)
#让输入框获取焦点
actions.move_to_element(inputTag)
actions.send_keys_to_element(inputTag,'苍老师现在怎么样了')
actions.move_to_element(subTag)
actions.click(subTag)

actions.perform()