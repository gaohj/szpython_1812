#encoding:utf-8

from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
dirver_path = r"C:\www\chromedriver\chromedriver.exe"

driver = webdriver.Chrome(executable_path=dirver_path)
driver.get("https://www.baidu.com/")
# driver.implicitly_wait(20) #如果没有隐士的等待 立马抛错误
# #有的话 等20秒  然后再抛出错误
# texts = driver.find_element(By.CLASS_NAME,'ASDFA')
# print(texts)

elementes = WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.ID,'asdfasdf'))
)
print(elementes)