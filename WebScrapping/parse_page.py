from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import time
import math
import pymongo

vac_collect1=[]

def update_vac1(data):
    connect = pymongo.MongoClient()
    vac = connect["job_seeking"]["vacancy"]
    for i in data:
        print('i', i)
        vac.update_one({'_id': i.pop('url')}, {'$set': i}, upsert=True)


# urls=['https://rabota.ua/company277662/vacancy8313749', 'https://rabota.ua/company322333/vacancy8476607','https://rabota.ua/company53660/vacancy8461632']
urls = []
client = pymongo.MongoClient()
for doc in client["job_seeking"]["vacancy"].find():
    # print('doc=',doc.keys())
    if 'time_parsed'not in doc.keys() or doc['time_parsed']<datetime.datetime(2021, 4, 1):
        urls.append(doc['_id'])
        print(doc)

# print('urls')
# print(urls)

for i_url in urls:
    driver = webdriver.Chrome('resources/chromedriver')  # Optional argument, if not specified will search path.
    driver.get(i_url)
    flag = driver.find_elements_by_css_selector(".f-main-wrapper")[0].text
    print('flag=', flag)
    if 'Вакансия закрыта' in flag:
        vac_collect1.append({'url': i_url,'time_parsed': datetime.datetime.now(),
        })
        update_vac1(vac_collect1)
        driver.close()
        continue
    f_text = driver.find_elements_by_tag_name("h1")[0].text
    city=driver.find_elements_by_css_selector("p.address-string > span")[0].text
    key_skills=driver.find_elements_by_css_selector("app-clusters li li")
    details=driver.find_elements_by_css_selector('#description-wrap')[0].text

    sk = []
    for skill in key_skills:
        sk.append(skill.text)

    vac_collect1.append({
        'url': i_url,
        'title': f_text,
        'city': city,
        'skills': sk,
        'details':details,
        'time_parsed': datetime.datetime.now(),
        })
    driver.close()
    update_vac1(vac_collect1)
    vac_collect1=[]
# print(vac_collect1)










