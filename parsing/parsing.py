import datetime
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

data = []

#inserting resources
with open('resources.csv', 'w', newline='') as csvfile:
    fieldnames = ["RESOURCE_ID", "RESOURCE_NAME", "RESOURCE_URL", "news", "top_tag", "bottom_tag", "title_cut", "date_cut"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'RESOURCE_ID': '1',
                     'RESOURCE_NAME': 'Nur Kz',
                     'RESOURCE_URL': "https://www.nur.kz/latest/",
                     'news': "soup.findAll('a', class_='article-preview-category__content')",
                     'top_tag': "n.get('href')",
                     'bottom_tag': "n.find('div', class_='article-preview-category__info').find('h2', class_='article-preview-category__subhead').text",
                     'title_cut': "n.find('div', class_='article-preview-category__info').find('span', class_='article-preview-category__text').text",
                     'date_cut': "n.find('div', class_='article-preview-category__date').find('time', class_='article-preview-category__date-time').get('datetime')"
                     })

    writer.writerow({'RESOURCE_ID': '2',
                     'RESOURCE_NAME': 'Baige News',
                     'RESOURCE_URL': "https://baigenews.kz/news/",
                     'news': "soup.findAll('a', class_='finded__content__item__link uk-flex')",
                     'top_tag': "n.get('href')",
                     'bottom_tag': "n.find('div', class_='finded__content__item__content uk-flex uk-flex-column uk-flex-space').find('div').find('span', class_='finded__content__item__content__caption').text.strip()",
                     'title_cut': "n.find('div', class_='finded__content__item__content uk-flex uk-flex-column uk-flex-space').find('span', class_='finded__content__item__content__title').text.strip()",
                     'date_cut': "n.get('data-time')",
                     })

with open('resources.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        url = row['RESOURCE_URL']

        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'lxml')

        news = eval(row['news'])

        for n in news:
            res_id = eval(row['RESOURCE_ID'])

            link = eval(row['top_tag'])
            title = eval(row['title_cut'])
            content = eval(row['bottom_tag'])
            date = eval(row['date_cut'])

            try:
                date_correct = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+06:00').strftime('%Y/%m/%d %H:%M:%S')
                date_format = datetime.datetime.strptime(date_correct, "%Y/%m/%d %H:%M:%S")
                nd_date = datetime.datetime.timestamp(date_format)
                not_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+06:00').strftime('%Y/%m/%d')
            except:
                date_correct = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S').strftime('%Y/%m/%d %H:%M:%S')
                date_format = datetime.datetime.strptime(date_correct, "%Y/%m/%d %H:%M:%S")
                nd_date = datetime.datetime.timestamp(date_format)
                not_date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S').strftime('%Y/%m/%d')

            ms = datetime.datetime.now()
            s_date = time.mktime(ms.timetuple()) * 1000
            data.append([res_id, link, title, content, nd_date, s_date, not_date])

        header = ['res_id', 'link', 'title', 'content', 'nd_date', 's_date', 'not_date']
        df = pd.DataFrame(data, columns=header)
        df['id'] = df[['title', 'content']].sum(axis=1).map(hash)
        df.to_csv('C:/python/django/parsing/data/news.csv', sep=';', encoding='utf-8-sig')


"""
url = "https://www.nur.kz/latest/"

r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

'''
link = soup.find('a', class_='article-preview-category__content').get('href')
title = soup.find('a', class_='article-preview-category__content').find('div', class_='article-preview-category__info').find('span', class_='article-preview-category__text').text
content = soup.find('a', class_='article-preview-category__content').find('div', class_='article-preview-category__info').find('h2', class_='article-preview-category__subhead').text
date = soup.find('a', class_='article-preview-category__content').find('div', class_='article-preview-category__date').find('time', class_='article-preview-category__date-time').get('datetime')
'''

news = soup.findAll('a', class_='article-preview-category__content')

for n in news:
    res_id = '-'
    link = n.get('href')
    title = n.find('div', class_='article-preview-category__info').find('span', class_='article-preview-category__text').text
    content = n.find('div', class_='article-preview-category__info').find('h2', class_='article-preview-category__subhead').text

    date = n.find('div', class_='article-preview-category__date').find('time', class_='article-preview-category__date-time').get('datetime')
    date_correct = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+06:00').strftime('%Y/%m/%d %H:%M:%S')
    date_format = datetime.datetime.strptime(date_correct, "%Y/%m/%d %H:%M:%S")
    nd_date = datetime.datetime.timestamp(date_format)

    ms = datetime.datetime.now()
    s_date = time.mktime(ms.timetuple()) * 1000
    not_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+06:00').strftime('%Y/%m/%d')
    data.append([res_id, link, title, content, nd_date, s_date, not_date])


header = ['res_id', 'link', 'title', 'content', 'nd_date', 's_date', 'not_date']
df = pd.DataFrame(data, columns=header)
df['id'] = df[['title', 'content']].sum(axis=1).map(hash)
df.to_csv('C:/python/django/parsing/data/nurkz.csv', sep=';', encoding='utf-8-sig')
"""