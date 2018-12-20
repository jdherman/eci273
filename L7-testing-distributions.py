from __future__ import division # for Python 2 people
import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

x = np.loadtxt('data/folsom-annual-maxes.csv', delimiter=',', skiprows=1, usecols=[1]) # data in cfs
y = np.log(x)

# is it normal?
# sns.distplot(x, kde=False, fit=stats.norm)
# print(stats.kstest(x, 'norm', args=(x.mean(), x.std())))

# is it lognormal?
sns.distplot(y, kde=False, fit=stats.norm)
print(stats.kstest(y, 'norm', args=(y.mean(), y.std())))

plt.show()
