
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
mpl.style.use(['ggplot'])

df = pd.read_json('data/json-strings/places-01-27-23.json')

print(df)

def format_df(places, place):
	return places[place]

for n in range(14):
	df[(n+1)] = df['places'].apply(format_df, place=n)

df = df.set_index('display_name')
# places = np.arange(1,14)
# df_herd = df.loc['Marshall', places]

df.drop(['places', 'byes'], axis=1, inplace=True)
print(df)
# df = df.set_index('display_name')
df = df[:5]
df = df.transpose()


df.plot(kind="area", stacked=False, figsize=(20,7))
plt.xticks(np.arange(1, 15, 1.0))
plt.show()
