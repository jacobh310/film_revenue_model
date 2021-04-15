# Film Revenue Model
---
Project at a Glance
- EDA project with American film data scrapped by myself. Exploring different characterisitics of high grossing films with data before release
- Built a model predicting box office revenue

Checkout the Web App: https://filme-revenue-model.herokuapp.com/

# Introduction
---
Production companies and studios alike always aim for the biggest budget often disregarding creative integrity. Often times these studios resort to uncreative ideas like reboots, endless sequels, and book adaptations. These attempts are often seen as a cash grab to the more savy film audience. This projects devles deeper into what characteristics correlate with higher box office revenues. The data is for this project is scrapped of Wikipedia which often had ranges for their box office and budgets so take these results with a grain of salt. Also the data only include films from 1990 to 2019. In the final part of the project, I built a model that predicts box office revenues

# Exploratory Data Analysis
### Numeric Variable Correlation Plot 

![Alt text](https://github.com/jacobh310/film_revenue_model/blob/master/images/corr.JPG?raw=true "Sentiment")
- Budget has a .745 correlation with box office revenue. Compnaies that invest more money into a movie expect to make more money in return.
Movies have largebudgets for good reason. Great starting cast and crew cost more than a relatively unknown cast and/or crew. Expensive set pieces, CGI, special effects, time filming are all factors that affect budget.

### Adapatation, reboots, sequels, and prequels
*rsp stands for reboot, sequel, prequel
#### Counts
![Alt text](https://github.com/jacobh310/film_revenue_model/blob/master/images/rsp_based_counts.JPG?raw=true "Sentiment")
- A little over a quarter of all films in the data set were either based on a true story or a book
- Reboots, sequels, and prequels make up a small majority of total films released
#### Box Office averages
![Alt text](https://github.com/jacobh310/film_revenue_model/blob/master/images/rsp_based_avgs.JPG?raw=true "Sentiment")
- Box office adaptaions, reboots, sequels, and prequels are, on average, higher than their opposite counterparts 
- Explains why studios want to produce these kinds of films


## resources 
Code for part scrapers:
  - github: https://gist.github.com/alexanderholt/d08fef44153672807c571166b592aa4e
  - medium:https://medium.com/@Alexander_H/scraping-wikipedia-with-python-8000fc9c9e6c
  - Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow

