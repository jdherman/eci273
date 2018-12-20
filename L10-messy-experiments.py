import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
# sns.set_style('whitegrid')

def cfs_to_taf(Q):
  return Q * 2.29568411*10**-5 * 86400 / 1000

dfF = pd.read_csv('data/FOL.csv', index_col=0, parse_dates=True)
dfS = pd.read_csv('data/SHA.csv', index_col=0, parse_dates=True)


# from statsmodels.tsa import stattools
# Q = dfS.inflow.values
# pacf = stattools.pacf(Q, nlags=1000)
# plt.plot(pacf)
# plt.show()

# monthly boxplots
# Q = dfS.inflow.to_frame()
# Q = Q.resample('M').sum()
# Q['month'] = Q.index.month
# Q.boxplot(by='month', column='inflow', sym='*')
# plt.show()

# print Q.inflow.autocorr(1)

# monthly autocorrelations
# rho_m = np.zeros(12)

# for m in range(1,13):
#   x1 = Q.inflow[Q.month==m].values
#   if m < 12:
#     x2 = Q.inflow[Q.month==(m+1)].values
#   else:
#     x2 = Q.inflow[Q.month==1].values

#   rho_m[m-1] = np.corrcoef(x1,x2)[0,1]

# plt.plot(range(1,13), rho_m)
# plt.ylabel(r'$\rho_m$')
# plt.xlabel('Month')
# plt.xlim([1,12])
# plt.ylim([0,1])
# plt.show()

# spatial correlations

# dfS.inflow = cfs_to_taf(dfS.inflow)
# dfF.inflow = cfs_to_taf(dfF.inflow)

# dfS = dfS.resample('AS-OCT').sum()
# dfF = dfF.resample('AS-OCT').sum()

# r = np.corrcoef(dfS.inflow.values, dfF.inflow.values)[0,1]
# print r

# plt.scatter(dfS.inflow.values, dfF.inflow.values)
# plt.xlabel('Shasta inflows')
# plt.ylabel('Folsom inflows')
# plt.title('Annual, r = %f' % r)
# plt.show()


# sampling from MVN
Qfol = cfs_to_taf(dfF.inflow).resample('M').sum().values
Qsha = cfs_to_taf(dfS.inflow).resample('M').sum().values

mu = [Qfol.mean(), Qsha.mean()]
Sigma = np.cov(Qfol, Qsha)
# print Qfol.shape

# turn off correlation
print(Sigma)
# Sigma[0,1] = 0.0
# Sigma[1,0] = 0.0

x = np.random.multivariate_normal(mu, Sigma, 1000)

plt.scatter(x[:,0], x[:,1])
plt.show()




