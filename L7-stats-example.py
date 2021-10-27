import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats

# Folsom annual inflow data
# summary statistics, histogram, QQ plot
annQ = np.loadtxt('data/folsom-annual-flow.csv', delimiter=',', skiprows=1, usecols=[1])
N = len(annQ)

m = np.mean(annQ)
s = np.std(annQ)
g = stats.skew(annQ)

# print('Mean = %f' % m)
# print('Std. Dev. = %f' % s)
# print('Skew Coef. = %f' % g) # no skew function in numpy

# other keyword arguments: bins, normed (for PDF instead of count)
# plt.hist(annQ, density=True, color='gray', edgecolor='none')

# plot the fitted pdf on top of the histogram
# x = np.arange(min(annQ),max(annQ), 10) # points to plot at
# pdf = stats.norm.pdf(x, loc=m, scale=s)
# plt.plot(x, pdf, color='k', linewidth=2)
# plt.xlabel('inflow (taf/yr)')
# plt.ylabel('pdf')
# plt.show()

# next figure - qq plot and find ppcc
# plt.figure()
# quantiles = np.arange(1,N+1)/float(N+1)
# print(quantiles)
# Zp = stats.norm.ppf(quantiles)

# Qpred = m + s*Zp
# plt.scatter(Qpred, np.sort(annQ), color='red')
# plt.plot([-1000,7000],[-1000,7000], color='k', linewidth=2)
# plt.xlabel('Theoretical Quantiles (TAF/yr)')
# plt.ylabel('Observed Quantiles (TAF/yr)')
# plt.show()

# r,p = stats.pearsonr(Qpred, np.sort(annQ))
# print('PPCC = %f' % r)

