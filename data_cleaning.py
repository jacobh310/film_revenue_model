import numpy as np
import pandas as pd
from datetime import datetime
import re

df = pd.read_csv('wiki_data.csv')
df = df[df.columns[1:]]
nan_values = df[df.columns[:26]].isna().sum().sort_values()
columns_keeping = nan_values[nan_values < 6000].index
df = df[columns_keeping]
df['Based on'] = df['Based on'].apply(lambda x: 0 if pd.isna(x) else 1)

for col in df.columns[1:].drop('Genres'):
    try:
        df[col] = df[col].str[3:-3]
    except:
        continue

df['Running time'] = df['Running time'].str.extract(r'(\d+)')
df['Running time'] = pd.to_numeric(df['Running time'])

## making all these columns into list becasue they have mulitple names and will make creating dummy variables for each
## later in the cleaning process
df['Directed by'] = df['Directed by'].str.split(',')
df['Starring'] = df['Starring'].str.split(',')
df['Produced by'] = df['Produced by'].str.split(',')
df['Screenplay by'] = df['Screenplay by'].str.split(',')
df['Edited by'] = df['Edited by'].str.split(',')
df['Cinematography'] = df['Cinematography'].str.split(',')
df['Written by'] = df['Written by'].str.split(',')
df['Music by'] = df['Music by'].str.split(',')
df['Productioncompanies '] = df['Productioncompanies '].str.split(',')
df['Distributed by'] = df['Distributed by'].str.split(',')
df['Productioncompany '] = df['Productioncompany '].str.split(',')


df['Release date'] = df['Release date'].str.split('(')
df['Release date length'] = df['Release date'].apply(lambda x: len(x) if type(x) == list else x)
df['Release date'] = df['Release date'][df['Release date length'] != 10]

def clean_release(row):
    if type(row) == list:
        if len(row) == 1:
            return row[0]
        else:
            return row[1][:-1]
    else:
        return row

df['Release date'] = df['Release date'].apply(clean_release).str.split(')').str[0]


def fix_dates(row):
    if pd.isna(row):
        return row
    else:
        try:
            return datetime.strptime(row, "%Y-%m-%d")
        except:
            try:
                return datetime.strptime(row, "%B %d, %Y")
            except:
                return row

df['Release date'] = df['Release date'].apply(fix_dates)
df['Release date'] = df['Release date'].apply(lambda x: x if type(x) == datetime else np.nan)



df = df[df['Box office'].str.contains('$', na=False, regex=False)]  # remove any non dollar currency
df = df[~df['Box office'].str.contains('admission', na=False,
                                       regex=False)]  # removes the 5 rows with admission in the box office col


def clean_box(row):
    box = row[1:]
    box = box.replace('$', '')
    box = re.split(" |\(|\[", box)
    box = box[0].split('\\')[0]

    if bool(re.match(r".*million.*", row)):
        try:
            return float(box) * 1000000
        except:
            return np.nan
    elif bool(re.match(r".*billion.*", row)):
        try:
            return float(box) * 1000000000
        except:
            return np.nan

    else:
        try:
            return float(box.replace(',', ''))
        except:
            return np.nan


df['Box office'] = df['Box office'].apply(clean_box)


df['million'] = df['Budget'].str.contains('millio', na=False, regex=False)
df['Budget'] = df['Budget'].apply(lambda x: x if '$' in str(x) else 'Unknown')
df['Budget'] = \
df['Budget'].str[1:].apply(lambda x: re.split(' |\[', str(x))).str[0].str.replace(',', '').str.split('\\').str[0]

def clean_budget(x):
    if x == 'Unknown':
        return np.nan
    if '???' in x:
        try:
            return (float(x.replace(',', '').split('???')[0]) + float(x.replace(',', '').split('???')[1])) / 2
        except:
            return np.nan
    else:
        try:
            return float(x)
        except:
            return np.nan

df['Budget'] = df['Budget'].apply(clean_budget)


def million(x):
    budget = x['Budget']
    if x['million'] == True:
        return budget * 1000000
    else:
        return budget


df['Budget'] = df.apply(million, axis=1)
df = df.drop(columns=['Release date length', 'million'])
budget_drop = df[df['Budget'] > 500000000].index
df = df.drop(index=budget_drop)


def clean_names(row):
    row_list = []
    if type(row) == list:
        for word in row:
            word = word.replace("'", '')
            word = word.replace('"', '')
            word = word.strip()
            if ']' in word:
                word = word[:-3]
            if len(word) < 40:
                row_list.append(word)
        return row_list
    else:
        return np.nan

df['Starring'] = df['Starring'].apply(clean_names)
df['Produced by'] = df['Produced by'].apply(clean_names)
df['Edited by'] = df['Edited by'].apply(clean_names)
df['Cinematography'] = df['Cinematography'].apply(clean_names)
df['Directed by'] = df['Directed by'].apply(clean_names)
df['Written by'] = df['Written by'].apply(clean_names)
df['Productioncompanies '] = df['Productioncompanies '].apply(clean_names)
df['Music by'] = df['Music by'].apply(clean_names)
df['Screenplay by'] = df['Screenplay by'].apply(clean_names)
df['Distributed by'] = df['Distributed by'].apply(clean_names)
df['Productioncompany '] = df['Productioncompany '].apply(clean_names)


def strip_genres(row):
    if type(row) == list:
        return [x.strip().lower() for x in row]
    else:
        return np.nan

df['Genres'] = df['Genres'].apply(lambda x: x if len(x) > 2 else np.nan).str[1:-1]
df['Genres'] = df['Genres'].str.replace("'", '').str.replace('film', '').str.split(',')
df['Genres'] = df['Genres'].apply(strip_genres)

# Merge productioncompanies and productioncompany columns
def production(x):
    comp = x['Productioncompany ']
    comps = x['Productioncompanies ']
    if type(comp) == list and type(comps) != list:
        return comp
    elif type(comps) == list and type(comp) != list:
        return comps
    else:
        return comp + comps

df['Production companies'] = df.apply(production, axis=1)
df['Production companies'] = df['Production companies'].apply(clean_names)
df = df.drop(columns=['Productioncompanies ', 'Productioncompany '])

# Feature Engineering: Category reduction

df['Country'] = df['Country'].str.split('[').str[0].apply(
    lambda x: 'other' if 'United States' not in str(x) else 'United States')
df['Language'] = df['Language'].str.split('[').str[0]
lang_counts = df['Language'].value_counts()
drop_langs = lang_counts[lang_counts < 6].index
df['Language'] = df['Language'].apply(lambda x: 'other' if x in drop_langs else x)

def list_counts(col):
    names = {}
    for i in df[col]:
        if type(i) == list:
            for j in i:
                if j not in names:
                    names[j] = 1
                else:
                    names[j] += 1
    count_df = pd.DataFrame.from_dict(names, orient='index', columns=['Count'])
    count_df = count_df.sort_values(by='Count', ascending=False)
    return count_df


upper = list_counts('Genres')[list_counts('Genres') >= 16]
upper.dropna(inplace=True)
keep_genres = upper.index


def drop_genres(row):
    if type(row) == list:
        genres = []
        for i in row:
            if i in keep_genres:
                genres.append(i)
            else:
                genres.append('other')
        return genres
    else:
        return np.nan


df['Genres'] = df['Genres'].apply(drop_genres)

df.to_csv('cleaned_data.csv',index=False)
