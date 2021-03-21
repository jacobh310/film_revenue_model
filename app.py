import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')
from datetime import datetime
import util
import pickle

st.set_page_config(layout="wide")
option = st.sidebar.selectbox('Which Dash Board', ('Exploratory Data Analysis', 'Machine Learning Model'))
st.markdown("<h1 style='text-align: center; color:#295E61 ;'>Film Box Office Exploratory Data Analysis and Model</h1>",
            unsafe_allow_html=True)

st.write(
    """This web app contains an Exploratory Data Analysis on American Films since the 1990s with a total of around 6000 movies. 
    It also contains a Random Forest  model that predicts a films box office with data from before released. All the 
     data is scrapped from wikipedia so the data is expected to be slightly off""")

if option == 'Exploratory Data Analysis':

    col1, col2 = st.beta_columns(2)
    col1.markdown("<h3 style='text-align: center; color:#295E61 ;'> Numerical Distributions</h3>",
                  unsafe_allow_html=True)
    col1.pyplot(util.histograms())

    col2.markdown("<h3 style='text-align: center; color:#295E61 ;'> Numerical Data Overview</h3>",
                  unsafe_allow_html=True)
    col2.dataframe(util.df[['Box office', 'Budget', 'Running time']].describe())

    ## counts bar charts
    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Movie Statistical Counts  </h2>",
                unsafe_allow_html=True)
    st.pyplot(util.plot_counts())
    st.markdown("<h4 style='text-align: center; color:#295E61 ;'>Observations</h4>", unsafe_allow_html=True)
    st.markdown("""<p style='text-align: left; color:#000000 ;'>- Friday is the day with the most film releases 
                        <br> - September (9) is the month with the most movie releases
                         <br> - Movies released per year seems consistent   <
                         <br> - Reboots, sequels, prequels make up a small amount of total movies released
                         /p>""", unsafe_allow_html=True)

    ## means bar chart
    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Movie Box Office Averages  </h2>",
                unsafe_allow_html=True)
    st.write("""       
       """)
    st.pyplot(util.plot_box_means())
    st.markdown("<h4 style='text-align: center; color:#295E61 ;'>Observations</h4>", unsafe_allow_html=True)
    st.markdown("""<p style='text-align: left; color:#000000 ;
                        '> - Movies in hindi have the highest average. This is because India has huge audience so they're is a substantial American and Indian 
                        <br> - Even though Friday has the most amount of movie releases, it us amounts the lowest for average. More more selection means less revenue
                        <br> - September was also the month with the month with the most releases but had the lowest average box office revenue
                         <br> - Sequels, prequels and reboots have a higher box office average than their opposite counter part
                         <br> - Movies based on a book or true story also have  higher box averages their opposite counter part
                          <br> - Box Office sales are increase on a yearly bases which is probably inline with inflation
                          <br> - Box Office sales also decrease for a little around the 
                          </p>""", unsafe_allow_html=True)

    st.markdown(
        "<h2 style='text-align: center; color:#295E61 ;'>Movie Box Office Averages for most popular in each category  </h2>",
        unsafe_allow_html=True)
    st.write("""       
       """)
    st.pyplot(util.plot_lists())
    # st.markdown("<h4 style='text-align: center; color:#295E61 ;'>Observations</h4>", unsafe_allow_html=True)
    # st.markdown("""<p style='text-align: left; color:#000000 ;
    #                     '> - Disney is an outlier in both for Distribution and Production
    #                     <br> - Quentin Tarintino, M. Night
    #                       </p>""", unsafe_allow_html=True)

else:
    st.header('Random Forest Model')
    with open('final_film_model', 'rb') as f:
        model = pickle.load(f)

    title = st.selectbox('Which Film', tuple(util.top_films_list['Title'].tolist()))
    features = util.top_films_list[util.top_films_list['Title'] == title].index[0]
    prediction = model.predict(util.top_df.values[features].reshape(1, -1))[0]
    st.markdown(
        f"<h2 style='text-align: center; color:#00000 ;'>The predicted box office for {title} is ${prediction:0.0f}</h2>",
        unsafe_allow_html=True)

    col1, col2 = st.beta_columns(2)

    title_df = util.new_df[util.new_df.columns.drop(['Year', 'Month', 'Day'])][util.new_df['Title'] == title]
    title_df = title_df[title_df['Box office'] == title_df['Box office'].max()]
    tran_df = title_df.reset_index().drop(columns='index').T
    tran_df.rename({0: 'Attributes'}, axis=1, inplace=True)

    col1.dataframe(tran_df, height=600)


    def model_bar():
        fig, ax = plt.subplots()
        sns.barplot(x=['Actual Box Office', 'Predicted Box Office', 'Budget', 'Mean'],
                    y=[title_df['Box office'].values[0], prediction, title_df['Budget'].values[0],
                       util.new_df['Box office'].mean()], ax=ax)
        ax.set_title(f"{title}'s Financials")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=60)
        ax.set_ylabel('US Dollars')
        return fig


    col2.pyplot(model_bar())
