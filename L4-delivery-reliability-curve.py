import numpy as np 
import matplotlib.pyplot as plt
from utility import simulate

# data setup
Q = np.loadtxt('data/FTO-FNF.csv', delimiter=',', skiprows=1, usecols=[1])
Q /= 1000 # TAF

D = np.arange(0,1000,50) # make an array of storage values
reliability = np.zeros(len(D)) # we'll calculate these for each K

# plot a curve for different fixed storage amounts
for K in [0, 3500, 9500]:
  for i in range(len(D)):
    reliability[i] = simulate(K, D[i], Q)
  
  plt.plot(reliability, D, '.-', linewidth=2)

plt.xlabel('Reliability')
plt.ylabel('Demand (TAF/m)')
plt.title('Delivery-Reliability Curve')
plt.legend(['K = 0 TAF', 'K = 3500 TAF', 'K = 9500 TAF'])
plt.show()


