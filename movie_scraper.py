from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

movie_list = pd.read_csv('movie_links.csv', names=['title','link'])

urls = movie_list['link'][:15]
# urls = ['https://en.wikipedia.org/wiki/127_Hours', 'https://en.wikipedia.org/wiki/25th_Hour','https://en.wikipedia.org//wiki/Zero_Dark_Thirty']
movies_df = pd.DataFrame()
count = 1
for url in urls:
    page = requests.get(url)
    soup = bs(page.text, 'lxml')
    title = soup.find_all(id='firstHeading')[0].i.text

    try:
        summary = soup.find_all(name='table',class_='infobox')[0]
    except:
        continue

    infobox = {}
    infobox['Title'] = title
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

# movies_df.to_csv('wiki_data.csv')