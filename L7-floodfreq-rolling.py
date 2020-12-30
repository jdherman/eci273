from __future__ import division # for Python 2 people
import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

def ln2(x,T):
  # what is the estimate of the T-year flood?
  # 2-parameter lognormal distribution
  y = np.log(x)
  N = len(y)
  m = np.mean(y)
  s = np.std(y)
  Zp = stats.norm.ppf(1 - 1/T)
  Qt = np.exp(m + Zp*s)
  return Qt

df = pd.read_csv('data/folsom-annual-peak-flow.csv', index_col=0, parse_dates=True)
w = 50
T = 100

# rolling window (the 'raw=True' option passes the values as numpy arrays)
Q100Rolling = df.rolling(w).apply(ln2, kwargs={'T':T}, raw=True)
ax = Q100Rolling.plot()

# expanding window
Q100Expanding = df.expanding(w).apply(ln2, kwargs={'T':T}, raw=True)
Q100Expanding.plot(ax=ax)

plt.ylabel('Estimate of 100-year flood event (cfs)')
plt.legend(['Rolling', 'Expanding'])
plt.show()
