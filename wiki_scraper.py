from bs4 import BeautifulSoup as bs
import requests
import csv

def get_movie_list():
    url = "https://en.wikipedia.org/wiki/Lists_of_American_films"
    page = requests.get(url)
    soup = bs(page.text, 'lxml')

    year_links = []

    for i in soup.find_all('li'):
        # pull the actual link for each one
        for link in i.find_all('a', href=True):
            try:
                year = int(link['href'][-4:])
            except:
                continue
            if 1990<=year<2020:
                year_links.append(link['href'])


    year_links = ['https://en.wikipedia.org/'+ i for i in year_links]
    film_titles = []
    film_links = []

    for year in year_links:
        print(f'Collecting films from {year}')
        html = requests.get(year)
        b = bs(html.text, 'lxml')
        # get to the table on the page
        for i in b.find_all(name='table', class_='wikitable'):
            # get to the row of each film
            for j in i.find_all(name='tr'):
                #get just the title cell for each row.
                # contains the title and the URL
                for k in j.find_all(name='i'):
                    # get within that cell to just get the words
                    for link in k.find_all('a', href=True):
                        # get the title and add to the list
                        film_titles.append(link['title'])
                        # get the link and add to that list
                        film_links.append(link['href'])
    print(f'Number of Film Links Collected: {len(film_links)}')
    print(f'Number of Film Titles Collected: {len(film_titles)}')
    # remove film links that don't have a description page on Wikipedia
    new_film_links = [i for i in film_links if 'redlink' not in i]
    # same goes for titles
    new_film_titles = [i for i in film_titles if '(page does not exist)' not in i]
    new_film_links =  ['https://en.wikipedia.org/'+ i for i in new_film_links]
    print(f'Number of Film Links with Wikipedia Pages: {len(new_film_links)}')
    print(f'Number of Film Titles with Wikipedia Pages: {len(new_film_titles)}')
    #use this list to fetch from the API
    title_links = {new_film_titles: new_film_links for new_film_titles, new_film_links in zip(new_film_titles, new_film_links)}

    return title_links
links = get_movie_list()

file  = open("movie_links.csv", "w")

w = csv.writer(file,lineterminator = '\n')
for key, val in links.items():
    try:
        w.writerow([key, val])
    except:
        continue