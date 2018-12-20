import numpy as np 
import matplotlib.pyplot as plt

# overly-simplified reservoir simulation
# Oroville

# Set some parameters
K = 3500 # capacity, TAF
D = 235 # target demand, TAF/month

# data setup
Q = np.loadtxt('data/FTO-FNF.csv', delimiter=',', skiprows=1, usecols=[1])
Q /= 1000
T = len(Q)

S = np.zeros(T)
R = np.zeros(T)

S[0] = K
R[0] = D

for t in range(1,T):

  # new storage: mass balance, max value is K
  S[t] = min(S[t-1] + Q[t-1] - R[t-1], K)

  # release is based on demand
  if S[t] + Q[t] > D:
    R[t] = D
  else:
    R[t] = S[t] + Q[t]

reliability = R[R==D].size / float(T)
print(reliability)
