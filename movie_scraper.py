from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
import re

common_genres = ['action', 'comedy', 'drama', 'fantasy', 'horror', 'mystery', 'romance', 'romantic', 'thriller',
                 'western', 'crime', 'war', 'spy', 'horror', ' computer-animated', 'superhero', ' science-fiction',
                 ' supernatural', 'heist', 'survival', 'comedy-drama','romantic comedy']
movie_list = pd.read_csv('movie_links.csv', names=['title', 'link'])

urls = movie_list['link']
# urls = ['https://en.wikipedia.org//wiki/Zero_Dark_Thirty','https://en.wikipedia.org/wiki/127_Hours','https://en.wikipedia.org/wiki/Intolerable_Cruelty']
# urls = ['https://en.wikipedia.org/wiki/Star_Wars:_Episode_I_%E2%80%93_The_Phantom_Menace','https://en.wikipedia.org/wiki/The_Amazing_Spider-Man_(film)','https://en.wikipedia.org/wiki/Iron_Man_3']

movies_df = pd.DataFrame()
count = 1
for url in urls:
    page = requests.get(url)
    soup = bs(page.text, 'lxml')
    infobox = {}
    # grabs title
    try:
        title = soup.find_all(id='firstHeading')[0].i.text
    except:
        continue
    try:
        p1 = soup.find_all('p')[1].text
        if 'sequel' in p1:
            infobox['rsp'] = 'sequel'
        elif 'reboot' in p1:
            infobox['rsp'] = 'reboot'
        elif 'prequel' in p1:
            infobox['rsp'] = 'prequel'
    except:
        try:
            p1 = soup.find_all('p')[0].text
            if 'sequel' in p1:
                infobox['rsp'] = 'sequel'
            elif 'reboot' in p1:
                infobox['rsp'] = 'reboot'
            elif 'prequel' in p1:
                infobox['rsp'] = 'prequel'
        except: continue

    # grabs genre
    para = soup.find_all('p')[0].b
    para = str(para)
    tag_title = re.sub('<[^<]+?>', '', para)

    if title in tag_title:
        genres = soup.find_all('p')[0].find_all('a')
        genre_list = []
        for genre in genres[:4]:
            try:
                link = genre['href']
            except:
                continue
            if 'film' in link or  genre.text.lower() in common_genres:
                genre_list.append(genre.text)

    else:
        genres = soup.find_all('p')[1].find_all('a')
        genre_list = []
        for genre in genres:
            try:
                link = genre['href']
            except:
                continue
            if 'film' in link or genre.text.lower() in common_genres:
                genre_list.append(genre.text)


    try:
        summary = soup.find_all(name='table', class_='infobox')[0]
    except:
        continue


    infobox['Title'] = title
    infobox['Genres'] = genre_list
    print(count, title)

    for tr in summary.find_all('tr')[2:]:
        try:
            col = tr.th.text
        except:
            continue

        infobox[col] = []
        if len(tr.find_all('li')) == 0:
            try:
                infobox[col].append([tr.td.text])
            except:
                continue
        items = []
        for td in tr.find_all('td'):
            for ul in td.find_all('ul'):
                for li in ul.find_all('li'):
                    items.append(li.text)
                infobox[col].append(items)

    count += 1
    movies_df = movies_df.append(infobox, ignore_index=True)

movies_df.to_csv('wiki_data.csv')
