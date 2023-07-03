import fake_headers
import requests
from fake_headers import Headers
import bs4
import json
from pprint import pprint


def get_vacancy():
    headers = fake_headers.Headers(browser="firefox", os="win")
    headers_dict = headers.generate()

    main_html = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_dict).text
    main_soup = bs4.BeautifulSoup(main_html, 'lxml')

    data = main_soup.find('div', id='HH-React-Root')
    vacancy_tags = data.find_all('div', class_='serp-item')
    vacancy_list = []

    for vacancy in vacancy_tags:
        vacancy_title = vacancy.find_all('a', class_='serp-item__title')
        for title in vacancy_title:
            if "python" or 'django' in str(title).lower():
                link = title['href']
                sallary = vacancy.find('span', attrs={'class': 'bloko-header-section-3'})
                if sallary != None:
                    sallary = vacancy.find('span', attrs={'class': 'bloko-header-section-3'}).text
                else:
                    sallary ='зп не указана'
                company_name = vacancy.find('a', attrs={'data-qa': "vacancy-serp__vacancy-employer"}).text
                company_address = vacancy.find(attrs={'data-qa': "vacancy-serp__vacancy-address"}).text

            vacancy_list.append(
                {
                    'link': link,
                    'sallary': sallary,
                    'company': company_name,
                    'address': company_address
                }
            )

    return vacancy_list


def write_file(vacancy_list):
    with open("vacancy.json", "w", encoding='utf-8') as f:
        data_writer = json.dump(vacancy_list, f, ensure_ascii=False)

if __name__=='__main__':
    write_file(get_vacancy())
