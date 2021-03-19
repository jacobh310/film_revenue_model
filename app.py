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
    st.write("""       
       """)
    st.write(
        """This web app contains an Exploratory Data Analysis on American Films since the 1990s with a total of around 6000 movies. 
        It also contains a Random Forest  model that predicts a films box office with data from before released. All the 
         app is scrapped from wikipedia so data and algorithm results may be a little off""")


    ## counts bar charts
    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Movie Statistical Counts  </h2>", unsafe_allow_html=True)
    st.write("""       
       """)
    st.pyplot(util.plot_counts())

    ## means bar chart
    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Movie Box Office Averages  </h2>", unsafe_allow_html=True)
    st.write("""       
       """)
    st.pyplot(util.plot_box_means())

    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Movie Box Office Averages  </h2>", unsafe_allow_html=True)
    st.write("""       
       """)
    st.pyplot(util.plot_lists())

else:
    st.header('Random Forest Model')