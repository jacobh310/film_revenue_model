import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import streamlit as st


df = pd.read_csv('cleaned_data.csv')

df.rename({'rsp': 'Reboot Sequel or Prequel'}, axis=1, inplace=True)
df['Release date'] = df['Release date'].apply(lambda x: np.nan if pd.isna(x) else datetime.strptime(x, "%Y-%m-%d"))
df['Year'] = df['Release date'].dt.year
df['Month'] = df['Release date'].dt.month
df['Day'] = df['Release date'].dt.day
df['Day of week'] = df['Release date'].apply(lambda x: x.weekday())
df = df[df['Year'] >= 1990]
df = df[df['Budget'] != 0]

df['Year'] = df['Year'].astype('int')
df['Month'] = df['Month'].astype('int')
df['Day'] = df['Day'].astype('int')
df['Day of week'] = df['Day of week'].astype('int')
df['Reboot Sequel or Prequel'] = df['Reboot Sequel or Prequel'].apply(lambda x: True if x ==1 else False)
df['Based on'] = df['Based on'].apply(lambda x: True if x ==1 else False)

days = {0:'Monday',1:'Tuesday' , 2:'Wednesday' , 3:'Thursday' ,4:'Friday' ,5:'Saturday' , 6:'Sunday'}
df['Day of week'] = df['Day of week'].map(days)

cats = ['Language', 'Country', 'Year', 'Month', 'Day', 'Day of week', 'Based on', 'Reboot Sequel or Prequel']
roles = df.select_dtypes('object').columns.drop(['Language','Country','Title'])
new_df = df.copy()
for role in roles:
    new_df[role] = new_df[role].str.replace('[','').str.replace(']','').str.replace("'",'').str.split(',')


def list_counts(col,df):
    names = {}
    for i in df[col]:
        if type(i) == list:
            for j in i:
                if j != '':
                    if j.strip() not in names:
                        names[j.strip()] = 1
                    else:
                        names[j.strip()] +=1
                else: pass
    count_df = pd.DataFrame.from_dict(names, orient='index', columns = ['Count'])
    count_df = count_df.sort_values(by='Count', ascending=False)
    return count_df


def plot_counts():
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(22, 10))

    for i, ax in enumerate(axes.flatten()):
        sns.countplot(df[cats[i]], ax=ax)
        if cats[i] == 'Based on':
            ax.set_title(cats[i] + ' true story or book counts', fontsize=14)
        elif cats[i] == 'Reboot Sequel or Prequel':
            ax.set_title(cats[i] + 'counts', fontsize=14)
        else:
            ax.set_title(cats[i] + ' counts', fontsize=20)
        ax.set_xlabel(cats[i], fontsize=16)
        ax.set_ylabel('Count', fontsize=16)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=75)
    plt.tight_layout()
    return  fig


def plot_box_means():
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize = (22,10))

    for i, ax in enumerate(axes.flatten()):
        sns.barplot(x=cats[i],y='Box office',data=df, ci=None, ax=ax)
        if cats[i] == 'Based on':
            ax.set_title(cats[i] + ' true story or book Box Office Mean', fontsize=14)
        elif cats[i] == 'Reboot Sequel or Prequel':
            ax.set_title(cats[i] + 'Box Office Mean', fontsize=14)
        else:
            ax.set_title(cats[i] + ' Box Office Mean', fontsize=20)

        ax.set_xlabel(cats[i],fontsize=16)
        ax.set_ylabel('Average',fontsize=16)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=75)
    plt.tight_layout()
    return fig


def plot_lists():
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize = (24,30))
    feature='Box office'

    for j, ax in enumerate(axes.flatten()):

        if j<11:
            top_ = list_counts(roles[j],new_df)[:15].index
            means = [df[feature][df[roles[j]].str.contains(f"'{i}'", na=False)].mean() for i in top_]

            sns.barplot(x=top_,y= means, data=df, ax =ax, ci=None)
            ax.set_title(roles[j] + ' Box Office Averages', fontsize=20)
            ax.set_xlabel(roles[j],fontsize=16)
            ax.set_ylabel('Average',fontsize=16)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=75, fontsize=12)
    fig.delaxes(axes[3,2])
    plt.tight_layout()
    return fig

def histograms():
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10,8))
    axes[0,0].hist(df['Box office'], bins=75)
    axes[0,0].set_title('Box office ($)')

    axes[0,1].hist(df['Budget'], bins=75)
    axes[0,1].set_title('Box office ($)')

    axes[1,0].hist(df['Running time'], bins=75)
    axes[1,0].set_title('Running time (minutes')

    fig.delaxes(axes[1,1])
    plt.tight_layout()
    return fig



top_films_list = pd.read_csv('top_films_index.csv')
top_df = pd.read_csv('top_films_scaled.csv',index_col=0)
# top_titles = top_films_dum['Title'].tolist()
# top_new = new_df[new_df.apply(lambda x: True if x['Title'] in top_titles else False, axis =1)]