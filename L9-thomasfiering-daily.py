import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

cfs_to_taf = 2.29568411*10**-5 * 86400 / 1000

def water_day(d):
  return d - 274 if d >= 274 else d + 91

def thomasfiering_daily(mu, sigma, rho, N_years):
  '''Lag-1 model. use historical monthly statistics 
  to generate a synthetic sequence of N years'''

  Q = np.zeros(N_years*365) # initialize
  Q[0] = np.random.normal(mu[0],sigma[0],1)

  for y in range(N_years):
    for d in range(365):
      i = 365*y + d # index
      Z = np.random.standard_normal()
      Q[i] = mu[d] + rho*(Q[i-1] - mu[d-1]) + Z*sigma[d]*np.sqrt(1-rho**2)

  return np.exp(Q) # return real space values

# load data and add column for "day of water year" (dowy)
df = pd.read_csv('data/FOL.csv', index_col=0, parse_dates=True)
df.rename(columns={'FOL_INFLOW_CFS': 'inflow'}, inplace=True)
df.loc[df.inflow < 0, 'inflow'] = 0.001 # fix bad data
Q = np.log(cfs_to_taf * df.inflow).to_frame()
Q['dowy'] = pd.Series([water_day(d) for d in Q.index.dayofyear], index=Q.index)

# get the mean value on each day (0-365). Moving average smoothing.
mean_daily_flow = Q.groupby(Q.dowy).mean()
mu = mean_daily_flow.rolling(1, center=True, min_periods=0).mean()
mu = mu.values # numpy

# same for standard deviation
std_daily_flow = Q.groupby(Q.dowy).std()
sigma = std_daily_flow.rolling(1, center=True, min_periods=0).mean()
sigma = sigma.values # numpy

# plot these daily values

# plt.subplot(1,2,1)
# plt.plot(mean_daily_flow, color='0.5')
# plt.plot(mu, color='k', linewidth=2)
# plt.xlabel('Day of water year')
# plt.xlim([0,365])
# plt.ylabel('Log Mean streamflow')

# plt.subplot(1,2,2)
# plt.plot(std_daily_flow, color='0.5')
# plt.plot(sigma, color='k', linewidth=2)
# plt.xlabel('Day of water year')
# plt.xlim([0,365])
# plt.ylabel('Stdev log streamflow')
# plt.tight_layout()
# plt.show()

# generate synthetic values and compare plots
# assume a constant lag-1 autocorrelation
Q_synthetic = thomasfiering_daily(mu, sigma, rho=0.95, N_years=20)
Q.inflow = np.exp(Q.inflow) # convert the original data back to real space

plt.subplot(2,1,1)
plt.plot(Q.inflow.values)
plt.ylim([0,300])

plt.subplot(2,1,2)
plt.plot(Q_synthetic)
plt.ylim([0,300])
plt.show()

# compare ACF/PACF in historical and synthetic
# from statsmodels.tsa import stattools
# Q = Q.inflow.values

# plt.subplot(2,2,1)
# acf,ci = stattools.acf(Q, nlags = 40, alpha=0.05)
# plt.plot(acf, linewidth=2)
# plt.plot(ci, linestyle='dashed', color='0.5')
# plt.title('ACF, Historical')

# plt.subplot(2,2,2)
# pacf,ci = stattools.pacf(Q, nlags = 40, alpha=0.05)
# plt.plot(pacf, linewidth=2)
# plt.plot(ci, linestyle='dashed', color='0.5')
# plt.title('PACF, Historical')

# plt.subplot(2,2,3)
# acf,ci = stattools.acf(Q_synthetic, nlags = 40, alpha=0.05)
# plt.plot(acf, linewidth=2)
# plt.plot(ci, linestyle='dashed', color='0.5')
# plt.title('ACF, Synthetic')

# plt.subplot(2,2,4)
# pacf,ci = stattools.pacf(Q_synthetic, nlags = 40, alpha=0.05)
# plt.plot(pacf, linewidth=2)
# plt.plot(ci, linestyle='dashed', color='0.5')
# plt.title('PACF, Synthetic')

# plt.show()

