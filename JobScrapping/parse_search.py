import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pymongo
from selenium.webdriver.common.keys import Keys
import math
from utils import database
driver = webdriver.Chrome('resources/chromedriver')
driver.get('http://www.rabota.ua/')


time.sleep(3)
wait = WebDriverWait(driver, 5)
s_box = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys("junior java dev")
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys(Keys.ENTER)
f_text=driver.find_elements_by_class_name("card")

vac_text=""
cl_vac_text=[]
cl_vac_link=[]

vac_num=wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#ctl00_content_vacancyList_ltCount > span')))


page_num=int(vac_num.text)/40
page_num=math.ceil(page_num)


def parse_vacancy_main_page(page):
    title = page.find_elements_by_css_selector('.card-title > a')[0].text
    company = page.find_elements_by_css_selector('.company-profile-name')[0].text
    location = page.find_elements_by_css_selector('.location')[0].text
    salary= page.find_elements_by_css_selector('.salary')[0].text
    link=page.find_elements_by_css_selector('.card-title > a')[0].get_attribute('href')
    return {
        'title': title,
        'company': company,
        'location': location,
        'salary': salary or None,
        # 'link': link,
        'url': link,
        # 'time_parsed': datetime.now(),
    }

def parse_title(page_num):
    page = 1
    vac_collect=[]

    while True:
        f_text = driver.find_elements_by_class_name("card")
        print(page)
        for f in f_text:
            vac_collect.append(parse_vacancy_main_page(f))

        if page == page_num:
            break
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#ctl00_content_vacancyList_gridList_ctl43_pagerInnerTable > dd.nextbtn'))).click()
        page = page + 1
    return vac_collect



if __name__ == '__main__':
    vacancies = parse_title(page_num)
    database.update_vacancies(vacancies)
    driver.close()
