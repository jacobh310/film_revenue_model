# # imbd data set collection and minor cleaning
# import pandas as pd
# df = pd.read_csv('data.tsv', sep ="\t")
# df['startYear'] = pd.to_numeric(df['startYear'], errors='coerce')
# df = df[(df['startYear'] >1980) & (df['titleType']=='tvSeries')]
# df = df.dropna()
# df.to_csv('tv_shows_imdb.csv')