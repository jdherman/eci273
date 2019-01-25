import numpy as np 
import matplotlib.pyplot as plt
from utility import simulate

# data setup
Q = np.loadtxt('data/FTO-FNF.csv', delimiter=',', skiprows=1, usecols=[1])
Q /= 1000 # TAF
D = 300 # target demand, TAF/month

K = np.arange(0,10000,100) # make an array of storage values
reliability = np.zeros(len(K)) # we'll calculate these for each K

for i in range(len(K)):
  reliability[i] = simulate(K[i], D, Q)

plt.plot(K, reliability)
plt.xlabel('Capacity (TAF)')
plt.ylabel('Reliability')
plt.title('Reliability-Capacity Curve for 300 TAF/m Yield')
plt.show()


