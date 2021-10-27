import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# read CSV data into a "dataframe" - pandas can parse dates
# this will be familiar to R users (not so much matlab users)
df = pd.read_csv('data/SHA.csv', index_col=0, parse_dates=True)

Q = df.SHA_INFLOW_CFS # a pandas series (daily)
# Q = Q.resample('AS-OCT').sum() # annual values
print(Q.autocorr(lag=1))

# plot a correlogram with confidence bounds
pd.plotting.autocorrelation_plot(Q)
plt.xlim([0,365])
plt.show()

from statsmodels.tsa import stattools
pacf,ci = stattools.pacf(Q, nlags=7, alpha=0.05)
plt.plot(pacf, linewidth=2)
plt.plot(ci, linestyle='dashed', color='0.5')
plt.show()

# we did this with pandas to simplify the resampling operations
# but we can also do it with numpy
# (using annual flow values)
Q = df.SHA_INFLOW_CFS.resample('AS-OCT').sum().values # now a numpy array

def autocorr(x,k):
  return np.corrcoef(x[:len(x)-k], x[k:])[0,1]

print(autocorr(Q,k=1))


