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
D = 500 # target demand, TAF/month

K = np.arange(0,10000,100) # make an array of storage values
reliability = np.zeros(len(K)) # we'll calculate these for each K

for i in range(len(K)):
  reliability[i] = simulate(K[i], D, Q)

plt.plot(K, reliability)
plt.xlabel('Capacity (TAF)')
plt.ylabel('Reliability')
plt.title('Reliability-Capacity Curve for 300 TAF/m Yield')
plt.show()


