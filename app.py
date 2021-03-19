import plotly.graph_objs as go
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime



df = pd.read_csv('cleaned_data.csv')

df.rename({'rsp': 'Reboot Sequel or Prequel'}, axis=1, inplace=True)
df['Release date'] = df['Release date'].apply(lambda x: np.nan if pd.isna(x) else datetime.strptime(x, "%Y-%m-%d"))
df['Year'] = df['Release date'].dt.year
df['Month'] = df['Release date'].dt.month
df['Day'] = df['Release date'].dt.day
df['Day of week'] = df['Release date'].apply(lambda x: x.weekday())
df['is_weekend'] = df['Day of week'].apply(lambda x: 1 if x >= 4 else 0)
df = df[df['Year'] >= 1990]

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color:#295E61 ;'>Film Box Office Model</h1>",
            unsafe_allow_html=True)

st.write(
    """This web app contains an Exploratory Data Analysis on American Films since the 1990s. 
    It also contains a Random Forest  model that predicts a films box office with data from before released. All the 
     app is scrapped from wikipedia so data and algorithm results may be a little off""")


def list_counts(col, df):
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


def plot_counts():
    cats = ['Language', 'Country', 'Year', 'Month', 'Day', 'Day of week', 'Based on', 'Reboot Sequel or Prequel']
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(16, 28))

    for i, ax in enumerate(axes.flatten()):
        sns.countplot(df[cats[i]], ax=ax)
        ax.set_title(cats[i] + ' counts', fontsize=20)
        ax.set_xlabel(cats[i], fontsize=16)
        ax.set_ylabel('Count', fontsize=16)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    plt.tight_layout()
    plt.show()


st.pyplot(plot_counts())