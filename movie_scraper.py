from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

movie_list = pd.read_csv('movie_links.csv', names=['title','link'])

urls = movie_list['link']
# urls = ['https://en.wikipedia.org/wiki/127_Hours', 'https://en.wikipedia.org/wiki/25th_Hour']
movies_df = pd.DataFrame()
count = 1
for url in urls:
    page = requests.get(url)
    soup = bs(page.text, 'lxml')
    try:
        summary = soup.find_all(name='table',class_='infobox')[0]
    except:
        continue

    infobox = {}
    print(count, movie_list['title'][count-1])

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
    infobox['title'] = movie_list['title'][count-1]
    count += 1

    movies_df = movies_df.append(infobox, ignore_index=True)

movies_df.to_csv('wiki_data.csv')