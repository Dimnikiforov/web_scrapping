import fake_headers
import requests
from fake_headers import Headers
import bs4
import re
from pprint import pprint


headers = fake_headers.Headers(browser="firefox", os="win")
headers_dict = headers.generate()

main_html = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_dict).text
main_soup = bs4.BeautifulSoup(main_html, 'lxml')

data = main_soup.find('div', id='HH-React-Root')
vacancy_tags = data.find_all('div', class_='serp-item')
vacancy_list = []

for vacancy in vacancy_tags:
    h2_tag = vacancy.find('a')
    # тут хотелось бы с помощью регулярок отсеить те тэги где есть джанго, но не понимаю как - target="_blank"> 're.compile(r"[django]", re.I)'
    # или, если пройтись циклом по vacancy.find('a').text и искать там re.compile(r"[django]", re.I) выходит ошибка - https://www.google.com/search?q=TypeError:+%27in+%3Cstring%3E%27+requires+string+as+left+operand,+not+re.Pattern&sxsrf=APwXEdfAnSRhIGDz44vc1kCgUxNw8duIpg:1687814205186&lr=lang_ru&sa=X&ved=2ahUKEwiGmJbx7eH_AhWDp4sKHWkDAbYQuAF6BAgEEAI&biw=1536&bih=714&dpr=1.25#ip=1
    link = h2_tag['href']
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

pprint(vacancy_list)