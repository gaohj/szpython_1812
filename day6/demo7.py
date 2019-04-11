from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
dirver_path = r"C:\www\chromedriver\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--proxy-server=http://183.63.101.62:55555")

driver = webdriver.Chrome(executable_path=dirver_path)
driver.get('http://www.baidu.com')

subBtn = driver.find_element_by_id('su')
#print(type(subBtn))
print(subBtn.get_attribute("value"))
#driver.save_screenshot('baodi.png')