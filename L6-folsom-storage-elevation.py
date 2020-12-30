import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

# load data, grab only the storage and elevation columns. rename them.
# the column names in the original file are CDEC defaults
df = pd.read_csv('data/FOL.csv', index_col=0, parse_dates=True)
df = df[['FOL_STORAGE_AF', 'FOL_RES ELE_FEET']]
df.rename(columns={'FOL_STORAGE_AF': 'storage', 'FOL_RES ELE_FEET': 'elevation'}, inplace=True)

df.plot.scatter('storage', 'elevation')
plt.xlabel('Storage (TAF)')
plt.ylabel('Water Surface Elevation (ft)')

# # then fit a quadratic and keep the equation for the next code example.
p = np.polyfit(df.storage.values, df.elevation.values, 2)
print('Regression: Elevation = %f S**2 + %f S + %f' % tuple(p))
f = np.poly1d(p)

plt.plot(df.storage.values, f(df.storage.values), color='r', linewidth=2)
plt.show()






