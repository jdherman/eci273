import numpy as np 
import matplotlib.pyplot as plt

cfs_to_tafd = 2.29568411*10**-5 * 86400 / 1000

# we'll use the "loadtxt" function from numpy to read the CSV
# the delimiter is a comma (other options might be tab or space)
# we want to skip the header row and the first (0th) column
# In general it's better to use the pandas library for this, which we'll see later
data = np.loadtxt('data/SHA.csv', delimiter=',', 
  skiprows=1, usecols=[1,2,3,4])

inflow = data[:,0] * cfs_to_tafd # TAF/d
outflow = data[:,1] * cfs_to_tafd # TAF/d
storage = data[:,2] / 1000 # AF to TAF

# first plot: time series of storage
# plt.plot(storage)
# plt.xlabel('Days since Oct 1 2000')
# plt.ylabel('Storage (TAF)')
# plt.ylim([0,4500])
# plt.show()

# # second plot: time series of inflow and outflow
# plt.plot(inflow)
# plt.plot(outflow)
# plt.xlabel('Days since Oct 1 2000')
# plt.ylabel('Flows (TAF/d)')
# plt.legend(['Inflow', 'Outflow'])
# plt.show()

# # third plot: exceedance plot of inflow and outflow
# T = len(inflow)
# # before log-transforming, replace ~zeros with small values to avoid warning
# inflow[inflow < 0.01] = 0.01
# outflow[outflow < 0.01] = 0.01
# log_inflow = np.log(inflow)
# log_outflow = np.log(outflow)
# plt.plot(np.arange(T)/T, np.sort(log_inflow)[::-1])
# plt.plot(np.arange(T)/T, np.sort(log_outflow)[::-1])
# plt.legend(['Inflow', 'Outflow'])
# plt.ylabel('Log(Q)')
# plt.xlabel('Exceedance')
# plt.show()

# # fourth plot:
# # plot historical storage for folsom, oroville, and shasta
# # on the same graph

# reservoirs = ['FOL', 'ORO', 'SHA']

# for r in reservoirs:
#   data = np.loadtxt('data/' + r + '.csv', 
#                     delimiter=',', 
#                     skiprows=1, 
#                     usecols=[1,2,3])

#   storage = data[:,2] / 1000 # AF to TAF
#   plt.plot(storage, linewidth=2)

# plt.xlabel('Days since Oct 1 2000')
# plt.ylabel('Storage (TAF)')
# plt.legend(reservoirs)
# plt.show()

# optional - save to file
# plt.savefig('whatever.pdf') # or .png, .svg, etc
