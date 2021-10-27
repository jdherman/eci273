import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats

x = np.loadtxt('data/folsom-annual-peak-flow.csv', 
                delimiter=',', 
                skiprows=1, usecols=[1]) # data in cfs
y = np.log(x)
N = len(y)

# plt.hist(y)
# plt.show()

# what is the estimate of the 100-year flood?
# assuming 2-parameter lognormal distribution
T = 100
m = np.mean(y)
s = np.std(y)
Zp = stats.norm.ppf(1 - 1/T)
Qt = np.exp(m + Zp*s)
print('Lognormal %d-year flood: %0.2f cfs' % (T,Qt))

# how different is the LP3?
# g = stats.skew(y)
# Kp = (2/g)*(1 + g*Zp/6 - g**2/36)**3 - 2/g
# Qt = np.exp(m + Kp*s)
# print('LP3 %d-year flood: %0.2f cfs' % (T,Qt))

# confidence interval for lognormal
# comment out LP3 part first
halfwidth = stats.norm.ppf(0.975)*np.sqrt((s**2/N)*(1 + Zp**2/2))
lb = np.exp(m + Zp*s - halfwidth)
ub = np.exp(m + Zp*s + halfwidth)
print('95%% CI: [%f, %f]' % (lb,ub))



