import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from scipy import stats

df = pd.read_csv('data/L6-FOL-daily.csv', index_col=0, parse_dates=True)
# print(df[df.isnull().any(axis=1)])
df.fillna(method='ffill', inplace=True) # fill missing data

df.plot.scatter('storage', 'elevation')
plt.xlabel('Storage (TAF)')
plt.ylabel('Water Surface Elevation (ft)')


# then fit a quadratic and keep the equation for the next code example.
p = np.polyfit(df.storage.values, df.elevation.values, 2)
print('Regression: Elevation = %f S**2 + %f S + %f' % tuple(p))
f = np.poly1d(p)

plt.plot(df.storage.values, f(df.storage.values), color='r', linewidth=2)
plt.show()
