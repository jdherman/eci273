import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

cfs_to_taf = 2.29568411*10**-5 * 86400 / 1000

def get_monthly_stats(x):
  '''calculate monthly 
  mean, std. dev., and lag-1 autocorrelation
  from historical data x. Assumes each month
  is lognormally distributed.'''

  x = np.log(x)
  N = len(x)
  mu = np.zeros(12)
  sigma = np.zeros(12)
  rho = np.zeros(12)

  for m in range(12):
    mu[m] = x[m::12].mean()
    sigma[m] = x[m::12].std()
    x1 = x[m:N-1:12]
    x2 = x[m+1::12]
    rho[m] = np.corrcoef(x1,x2)[0,1]

  return mu,sigma,rho # log space


def thomasfiering_monthly(mu, sigma, rho, N_years):
  '''Lag-1 model. use historical monthly statistics 
  to generate a synthetic sequence of N years'''

  Q = np.zeros(N_years*12) # initialize
  Q[0] = np.random.normal(mu[0],sigma[0],1)

  for y in range(N_years):
    for m in range(12):
      i = 12*y + m # index
      Z = np.random.standard_normal()
      Q[i] = mu[m] + rho[m-1]*(Q[i-1] - mu[m-1]) + Z*sigma[m]*np.sqrt(1-rho[m-1]**2)

  return np.exp(Q) # real space 


# read in data and generate synthetic timeseries
df = pd.read_csv('data/FOL.csv', index_col=0, parse_dates=True)
Q = (cfs_to_taf * df.FOL_INFLOW_CFS).resample('M').sum().values
mu,sigma,rho = get_monthly_stats(Q)
Q_synthetic = thomasfiering_monthly(mu, sigma, rho, N_years=15)


# compare synthetic stats to historical
a,b,c = get_monthly_stats(Q_synthetic)

for m in range(12):
  print('Month %d means: %f, %f' % (m,mu[m],a[m]))
for m in range(12):
  print('Month %d stdev: %f, %f' % (m,sigma[m],b[m]))
for m in range(12):
  print('Month %d rho: %f, %f' % (m,rho[m],c[m]))

# plot timeseries

plt.subplot(2,1,1)
plt.plot(Q)
plt.subplot(2,1,2)
plt.plot(Q_synthetic)
plt.show()

# compare ACF/PACF in historical and synthetic
# from statsmodels.tsa import stattools

# plt.subplot(2,2,1)
# acf,ci = stattools.acf(Q, nlags = 12, alpha=0.05)
# plt.plot(acf, linewidth=2)
# plt.plot(ci, linestyle='dashed', color='0.5')
# plt.title('ACF, Historical')

# plt.subplot(2,2,2)
# pacf,ci = stattools.pacf(Q, nlags = 12, alpha=0.05)
# plt.plot(pacf, linewidth=2)
# plt.plot(ci, linestyle='dashed', color='0.5')
# plt.title('PACF, Historical')

# plt.subplot(2,2,3)
# acf,ci = stattools.acf(Q_synthetic, nlags = 12, alpha=0.05)
# plt.plot(acf, linewidth=2)
# plt.plot(ci, linestyle='dashed', color='0.5')
# plt.title('ACF, Synthetic')

# plt.subplot(2,2,4)
# pacf,ci = stattools.pacf(Q_synthetic, nlags = 12, alpha=0.05)
# plt.plot(pacf, linewidth=2)
# plt.plot(ci, linestyle='dashed', color='0.5')
# plt.title('PACF, Synthetic')

# plt.show()

