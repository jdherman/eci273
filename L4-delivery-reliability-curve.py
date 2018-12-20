import numpy as np 
import matplotlib.pyplot as plt

# this function should be general to any system
# input capacity, demand (constant), and inflow array
# returns reliability
def simulate(K, D, Q):
  T = len(Q)
  S = np.zeros(T)
  R = np.zeros(T)

  S[0] = K # start simulation full
  R[0] = D

  for t in range(1,T):

    S[t] = min(S[t-1] + Q[t-1] - R[t-1], K)

    if S[t] + Q[t] > D:
      R[t] = D
    else:
      R[t] = S[t] + Q[t]

  return R[R==D].size / float(T)

# data setup
Q = np.loadtxt('data/FTO-FNF.csv', delimiter=',', skiprows=1, usecols=[1])
Q /= 1000 # TAF

D = np.arange(0,1000,50) # make an array of storage values
reliability = np.zeros(len(D)) # we'll calculate these for each K

# plot a curve for different fixed storage amounts
for K in [0, 3500, 9500]:
  for i in range(len(D)):
    reliability[i] = simulate(K, D[i], Q)
  
  plt.plot(reliability, D, '.', linewidth=2)

plt.xlabel('Reliability')
plt.ylabel('Demand (TAF/m)')
plt.title('Delivery-Reliability Curve')
plt.legend(['K = 0 TAF', 'K = 3500 TAF', 'K = 9500 TAF'])
plt.show()


