import numpy as np 
import matplotlib.pyplot as plt

# sequent peak example from LVB Table 11.2

Q = np.tile([1, 3, 3, 5, 8, 6, 7, 2, 1], 2)

T = len(Q)
R = 3.5*np.ones(T)
for t in range(T):
  K[t+1] = max(R[t] - Q[t] + K[t], 0)

print('Reservoir size needed: %f' % np.max(K))


# Or...let's do this as a function instead

# def sequent_peak(R, Q):
#   # accepts inflow and outflow arrays
#   # returns sequent peak reservoir capacity
#   assert len(R) == len(Q), 'R and Q must be the same length'
  
#   T = len(Q)
#   K = np.zeros(T+1)

#   for t in range(T):
#     K[t+1] = max(R[t] - Q[t] + K[t], 0)

#   return np.max(K)


# Kmax = sequent_peak(R,Q)
# print(Kmax)

