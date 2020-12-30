import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# function from last class
def sequent_peak(R, Q):
  T = len(Q)
  K = np.zeros(T+1)
  for t in range(T):
    K[t+1] = max(R[t] - Q[t] + K[t], 0)
  return np.max(K)

mu = 4400 # average annual flow
alphas = np.arange(0.0, 1.0, 0.1) # unitless demand
N = 100000 # arbitrary large number
Ks = np.zeros(len(alphas))

for sigma in mu*np.array([0.2, 0.4, 0.6]):
  inflows = np.random.normal(mu, sigma, size=(N))

  for i,alpha in enumerate(alphas):
    demand = alpha * mu * np.ones(N,)
    Ks[i] = sequent_peak(demand, inflows) / mu

  plt.plot(alphas, Ks, '.-', linewidth=2)

plt.title('Storage Required')
plt.ylabel(r'$S / \mu$ (Years)') # TeX in $_$
plt.xlabel(r'$\alpha$ (unitless)')
plt.legend([r'$C_v = 0.2$', r'$C_v = 0.4$', r'$C_v = 0.6$'])
plt.show()

