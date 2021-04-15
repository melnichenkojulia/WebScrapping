import datetime

from JobScrapping.utils.database import update_vacancies



def get_urls_parsing(client, date):
    urls = []
    for doc in client["job_seeking"]["vacancy"].find():
        if 'time_parsed' not in doc.keys() or doc['time_parsed'] < date:
            urls.append(doc['_id'])
    return urls


def parse_vacancy_page_by_link(driver, url):
    driver.get(url)
    flag = driver.find_elements_by_css_selector(".f-main-wrapper")[0].text
    if 'Вакансия закрыта' in flag:
        return {'url': url, 'time_parsed': datetime.datetime.now()}
    f_text = driver.find_elements_by_tag_name("h1")[0].text
    city = driver.find_elements_by_css_selector("p.address-string > span")[0].text
    key_skills = driver.find_elements_by_css_selector("app-clusters li li")
    details = driver.find_elements_by_css_selector('#description-wrap')[0].text
    sk = []
    for skill in key_skills:
        sk.append(skill.text)
    return {
        'url': url,
        'title': f_text,
        'city': city,
        'skills': sk,
        'details': details,
        'time_parsed': datetime.datetime.now(),
    }

def parse_vacancies_pages(driver, urls):
    vac_collect = []
    for i_url in urls:
        info = parse_vacancy_page_by_link(driver, i_url)
        vac_collect.append(info)
        update_vacancies([info])
