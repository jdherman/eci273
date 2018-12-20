import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv('CAISO-all-hourly.csv', index_col=0, parse_dates=True)
df = df.fillna(method='ffill') # fill in missing hours/days
df.drop(['renewables'], axis=1, inplace=True) # because it's already added up

# Duck curve: compare hydro/solar hourly generation between summer 2011 to 2017
df[['hydro','solar']]['7/1/2011':'7/31/2011'].plot()
df[['hydro','solar']]['7/1/2017':'7/31/2017'].plot()
plt.ylabel('Generation (MWh)')
plt.show()

# to plot the full dataset, may need to upscale
# stacked area plot
df = df.resample('M').sum()
df.plot.area()
plt.ylabel('Generation (MWh)')
plt.show()