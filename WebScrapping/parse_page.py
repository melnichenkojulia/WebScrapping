from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import math
from R_ua import *

driver = webdriver.Chrome('resources/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.rabota.ua/')

time.sleep(3)

wait = WebDriverWait(driver, 5)
s_box= wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys("Python")
s_button =wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'submit-button'))).click()

f_text=driver.find_elements_by_class_name("card")

vac_text=""
cl_vac_text=[]
cl_vac_link=[]

vac_num=wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#ctl00_content_vacancyList_ltCount > span')))
page_num=math.ceil(int(vac_num.text)/40)






