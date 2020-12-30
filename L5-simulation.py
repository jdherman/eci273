import numpy as np 
import matplotlib.pyplot as plt

# added a spill variable since that counts
# for downstream environmental flows too

def simulate(K, D, Q):
  T = len(Q)
  S = np.zeros(T)
  R = np.zeros(T)
  spill = np.zeros(T)

  S[0] = K # start simulation full
  R[0] = min(D, Q[0]) # fix

  for t in range(1,T):

    spill[t-1] = max(S[t-1] + Q[t-1] - R[t-1] - K, 0)
    S[t] = S[t-1] + Q[t-1] - R[t-1] - spill[t-1]

    if S[t] + Q[t] > D:
      R[t] = D
    else:
      R[t] = S[t] + Q[t]

  # this metric would account for timing
  # but it's not quite the same as the "ecochange" metric
  alteration = np.abs(Q - R - spill).sum() / Q.sum()
  return R[R==D].size / float(T), alteration

# data setup
Q = np.loadtxt('data/FTO-FNF.csv', delimiter=',', skiprows=1, usecols=[1])
Q /= 1000 # TAF
D = 300 # target demand, TAF/month

K = np.arange(0,10000,100) # make an array of storage values
reliability = np.zeros(len(K)) # we'll calculate these for each K
alteration = np.zeros(len(K)) # we'll calculate these for each K

for i in range(len(K)):
  reliability[i], alteration[i] = simulate(K[i], D, Q)

plt.scatter(reliability, alteration)
plt.xlabel('Reliability')
plt.ylabel('Hydrologic alteration (unitless)')
plt.title('Reliability-Alteration tradeoff, varying capacity')
plt.show()


