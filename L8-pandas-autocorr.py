import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# read CSV data into a "dataframe" - pandas can parse dates
# this will be familiar to R users (not so much matlab users)
df = pd.read_csv('data/SHA.csv', index_col=0, parse_dates=True)

Q = df.inflow # a pandas "Series"
Q = Q.resample('AS-OCT').sum()
print(Q.autocorr(lag=1))

# plot a correlogram with confidence bounds
# pd.tools.plotting.autocorrelation_plot(Q)
# plt.xlim([0,4])
# plt.show()

# from statsmodels.tsa import stattools
# pacf = stattools.pacf(Q, nlags=40)
# plt.plot(pacf)
# plt.show()

# we did this with pandas to simplify the resampling operations
# but we can also do it with numpy
# Q = df.inflow.values # now a numpy array

# def autocorr(x,k):
#   return np.corrcoef(x[:len(x)-k], x[k:])[0,1]

# print(autocorr(Q,k=1))


