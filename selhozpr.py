import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv

agent = UserAgent()
url = 'https://www.agrobase.ru/selxozpredpriyatiya/rossiya'


def parse_links_ocr():
    response = requests.get(url=url, params={
        'user-agent': f'{agent.random}'
    }).text
    soup = BeautifulSoup(response, 'lxml')
    links = list()
    ocr_links = soup.find_all('a', class_='')
    for i in ocr_links:
        if 'selxozpredpriyatiya/rossiya' in i.get('href') and i.get('href').count('/') == 3:
            links.append('https://www.agrobase.ru' + i.get('href'))
    parse_basic(links)


def parse_basic(links):
    with open('data.csv', 'w', encoding='utf-8') as F:
        writer = csv.writer(F)
        writer.writerow(
            ('Компания', 'Руководство', 'Телефон', 'Вид деятельности')
        )
    for i in links:
        response = requests.get(url=i, params={
            'user-agent': f'{agent.random}'
        }).text
        soup = BeautifulSoup(response, 'lxml')

        for j in soup.find_all('div', class_='ac-company'):
            if 'Факс' in j.text:
                with open('data.csv', 'a', encoding='utf-8') as F:
                    writer = csv.writer(F)
                    writer.writerow(
                        [j.text[1:j.text.find('Адрес:')-2], j.text[j.text.find('Телефон:')+8:j.text.find('Факс')-1],
                         j.text[j.text.find('Руководство:')+12:j.text.find('Телефон:')-1],
                         j.text[j.text.find('Вид деятельности:')+17:-2]]
                    )
                # print(j.text[1:j.text.find('Адрес:')-2])
                # print(j.text[j.text.find('Телефон:')+8:j.text.find('Факс')-1])
                # print(j.text[j.text.find('Руководство:')+12:j.text.find('Телефон:')-1])
                # print(j.text[j.text.find('Вид деятельности:')+17:-2])
            else:
                with open('data.csv', 'a', encoding='utf-8') as F:
                    writer = csv.writer(F)
                    writer.writerow(
                        [j.text[1:j.text.find('Адрес:')-2], j.text[j.text.find('Телефон:')+8:j.text.find('Факс')-1],
                         j.text[j.text.find('Руководство:')+12:j.text.find('Телефон:')-1],
                         j.text[j.text.find('Вид деятельности:')+17:-2]]
                    )
                # print([j.text[1:j.text.find('Адрес:')-2]])
                # print([j.text[j.text.find('Телефон:')+8:j.text.find('Вид деятельности')-1]])
                # print([j.text[j.text.find('Руководство:')+12:j.text.find('Телефон:')-1]])
                # print([j.text[j.text.find('Вид деятельности:')+17:-2]])

def main():
    parse_links_ocr()


if __name__ == '__main__':
    main()