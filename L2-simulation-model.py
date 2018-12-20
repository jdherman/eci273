import numpy as np 
import matplotlib.pyplot as plt

# really simple reservoir simulation
cfs_to_taf = 2.29568411*10**-5 * 86400 / 1000

# Set some parameters
K = 975 # capacity, TAF
D = 5 # target demand, TAF/day

# data setup
Q = np.loadtxt('data/FOL.csv', delimiter=',', 
                skiprows=1, usecols=[4])
Q *= cfs_to_taf
T = len(Q)

S = np.zeros(T)
R = np.zeros(T)
shortage = np.zeros(T)

S[0] = K # start simulation full
R[0] = D # first day meets demand
met_demand = 1 # counter

for t in range(1,T):

  # new storage: mass balance, max value is K
  S[t] = min(S[t-1] + Q[t-1] - R[t-1], K)

  # release is based on demand
  if S[t] + Q[t] > D:
    R[t] = D
    met_demand += 1
  else:
    R[t] = S[t] + Q[t]

  shortage[t] = D-R[t]

reliability = met_demand / T
print('The reliability is', reliability)

# just plotting below here
plt.subplot(3,1,1)
plt.plot(S)
plt.ylabel('Storage (TAF)')

plt.subplot(3,1,2)
plt.plot(Q)
plt.plot(R)
plt.legend(['Inflow', 'Delivery'])
plt.ylabel('Flow (TAF/day)')

plt.subplot(3,1,3)
plt.plot(shortage)
plt.ylabel('Shortage (TAF/day)')
plt.xlabel('Days (from 10/1/2000)')
plt.show()