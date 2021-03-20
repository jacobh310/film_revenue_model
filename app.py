import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import util


st.set_page_config(layout="wide")
option = st.sidebar.selectbox('Which Dash Board',('Exploratory Data Analysis','Machine Learning Model'))

if option == 'Exploratory Data Analysis':

    st.markdown("<h1 style='text-align: center; color:#295E61 ;'>Film Box Office Exploratory Data Analysis and Model</h1>",
                unsafe_allow_html=True)

    st.write(
        """This web app contains an Exploratory Data Analysis on American Films since the 1990s with a total of around 6000 movies. 
        It also contains a Random Forest  model that predicts a films box office with data from before released. All the 
         app is scrapped from wikipedia so data and algorithm results may be a little off""")


    ## counts bar charts
    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Movie Statistical Counts  </h2>", unsafe_allow_html=True)
    st.pyplot(util.plot_counts())
    st.markdown("<h4 style='text-align: center; color:#295E61 ;'>Observations</h4>", unsafe_allow_html=True)
    st.markdown("""<p style='text-align: center; color:#000000 ;'>Friday (4) is the day with the most film releases 
                        <br> September (9) is the month with the most movie releases
                         <br> Movies released per year seems consistent   <
                         <br> Reboots, sequels, prequels make up a small amount of total movies released/p>""", unsafe_allow_html=True)


    ## means bar chart
    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Movie Box Office Averages  </h2>", unsafe_allow_html=True)
    st.write("""       
       """)
    st.pyplot(util.plot_box_means())
    st.markdown("""<p style='text-align: center; color:#000000 ;
                        '>Movies in hindi have the highest average. This is because India has huge audience so they're is a substantial American and Indian 
                        <br> Even though Friday has the most amount of movie releases, it us amounts the lowest for average. More more selection means less revenue
                         <br> Sequels, prequels and reboots have a higher box office average than their opposite counter part
                         <br> Movies based on a book or true story also have  higher box averages their opposite counter part
                          <br> Box Office sales are increase on a yearly bases which is probably inline with inflation
                          </p>""", unsafe_allow_html=True)


    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>More Movie Box Office Averages  </h2>", unsafe_allow_html=True)
    st.write("""       
       """)
    st.pyplot(util.plot_lists())

else:
    st.header('Random Forest Model')