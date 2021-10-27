import numpy as np 

# this function should be general to any system
# input capacity, demand (constant), and inflow array
# returns reliability
def simulate(K, D, Q):
  T = len(Q)
  S = np.zeros(T)
  R = np.zeros(T)

  S[0] = K # start simulation full
  R[0] = D
  met_demand = 1

  for t in range(1,T):

    S[t] = min(S[t-1] + Q[t-1] - R[t-1], K)

    if S[t] + Q[t] > D:
      R[t] = D
      met_demand += 1
    else:
      R[t] = S[t] + Q[t]

  return met_demand / T
