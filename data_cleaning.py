import pandas as pd
df = pd.read_csv('wiki_data.csv')
df = df[df.columns[1:25]]
df['Based on'] = df['Based on'].apply(lambda x: 0 if pd.isna(x) else 1)

