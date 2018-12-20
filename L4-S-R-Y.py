import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# function from last class
def sequent_peak(R, Q):
  T = len(Q)
  K = np.zeros(T)
  for t in range(T):
    K[t] = max(R[t] - Q[t] + K[t-1], 0)
  return np.max(K)

mu = 100 # average annual flow
alphas = np.arange(0.0, 1.0, 0.1) # unitless demand
N = 100000
Ks = np.zeros(len(alphas))

for sigma in [20,40,60]:
  for i,alpha in enumerate(alphas):
    demand = alpha*mu*np.ones(N,)
    inflows = np.random.normal(mu, sigma, size=(N))
    Ks[i] = sequent_peak(demand, inflows) / mu

  plt.plot(alphas, Ks)

plt.title('Storage Required')
plt.ylabel(r'$S / \mu$ (Years)')
plt.xlabel(r'$\alpha$ (unitless)')
plt.legend([r'$C_v = 0.2$', r'$C_v = 0.4$', r'$C_v = 0.6$'])
plt.show()

