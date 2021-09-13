import numpy as np 
import matplotlib.pyplot as plt

np.random.seed(1)

def autocorr(x,k):
  '''returns the lag-k autocorrelation of vector x'''
  return np.corrcoef(x[:len(x)-k], x[k:])[0,1]

def thomasfiering(x,N):
  '''Lag-1 model. use historical data x 
  to generate a synthetic sequence of N timesteps.
  Assumes x is lognormally distributed.'''
  x = np.log(x) # log-space avoids negative values
  mu = x.mean()
  sigma = x.std()
  rho = autocorr(x,1)
  Q = np.zeros(N) # initialize
  Q[0] = np.random.normal(mu,sigma,1) 

  for i in range(1,N):
    Z = np.random.standard_normal()
    Q[i] = mu + rho*(Q[i-1] - mu) + Z*sigma*np.sqrt(1-rho**2)

  return np.exp(Q) 

# assume annual flow data is lognormally distributed
# this will avoid negative flows
Q = np.loadtxt('data/folsom-annual-flow.csv', delimiter=',', skiprows=1, usecols=[1])
Q_synthetic = thomasfiering(Q, N=100)

print('Means: %f, %f' % (Q.mean(),Q_synthetic.mean()))
print('Stdev: %f, %f' % (Q.std(),Q_synthetic.std()))
print('Rho: %f, %f' % (autocorr(Q,1), autocorr(Q_synthetic,1)))
# note "retransformation bias" in rho

from scipy import stats

_, p = stats.ranksums(Q, Q_synthetic)

print('p = %0.4f' % p)

if p < 0.05:
  print('Reject null hypothesis that Q,Q_synth are from same distribution')
else:
  print('Fail to reject (this is a good thing)')



