import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

cfs_to_taf = 2.29568411*10**-5 * 86400 / 1000

def autocorr(x,k):
  '''returns the lag-k autocorrelation of vector x'''
  return np.corrcoef(x[:len(x)-k], x[k:])[0,1]

def thomasfiering(x1, x2, N):
  '''Lag-1 model for two sites. use historical data x 
  to generate a synthetic sequence of N timesteps.
  Assumes x is lognormally distributed.'''
  # being lazy here, do it in a loop instead
  x1 = np.log(x1) # log-space avoids negative values
  m1 = x1.mean()
  s1 = x1.std()
  r1 = autocorr(x1,1)
  Q1 = np.zeros(N) # initialize
  Q1[0] = np.random.normal(m1,s1,1) 

  x2 = np.log(x2) # log-space avoids negative values
  m2 = x2.mean()
  s2 = x2.std()
  r2 = autocorr(x2,1)
  Q2 = np.zeros(N) # initialize
  Q2[0] = np.random.normal(m2,s2,1) 

  Sigma = np.corrcoef(x1, x2)

  for i in range(1,N):
    Z = np.random.multivariate_normal([0,0], Sigma, 1)
    Q1[i] = m1 + r1*(Q1[i-1] - m1) + Z[0,0]*s1*np.sqrt(1-r1**2)
    Q2[i] = m2 + r2*(Q2[i-1] - m2) + Z[0,1]*s2*np.sqrt(1-r2**2)
  
  return np.exp(Q1), np.exp(Q2)

# read in data and upscale to annual. rename the column we're going to use.
# this is an example of "method chaining" with pandas dataframes
# it's not required to use multiple lines, but usually makes it more readable.
dfF = (pd.read_csv('data/FOL.csv', index_col=0, parse_dates=True)
         .rename(columns={'FOL_INFLOW_CFS':'inflow'}))
dfS = (pd.read_csv('data/SHA.csv', index_col=0, parse_dates=True)
         .rename(columns={'SHA_INFLOW_CFS':'inflow'}))

dfS.inflow *= cfs_to_taf
dfF.inflow *= cfs_to_taf
dfS = dfS.resample('AS-OCT').sum()
dfF = dfF.resample('AS-OCT').sum()

# generate synthetic (input numpy arrays)
Q1, Q2 = thomasfiering(dfS.inflow.values, dfF.inflow.values, N=200)

# compare spatial correlation (this is in real space, not log)
print('Historical r = %0.3f' % np.corrcoef(dfS.inflow.values, dfF.inflow.values)[0,1])
print('Synthetic r = %0.3f' % np.corrcoef(Q1, Q2)[0,1])

