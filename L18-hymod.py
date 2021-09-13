import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import differential_evolution
from SALib.sample import saltelli
from SALib.analyze import sobol

# hymod as defined by Gharari et al. HESS 2013
# load daily data for 1 year (P,PET,Q)
ndays = 365
data = np.loadtxt('data/leaf-river-data.txt', skiprows=1)
data_P = data[0:ndays,3]
data_PET = data[0:ndays,4]
data_Q = data[0:ndays,5]


def hymod(x, mode='optimize'):

  # assign parameters
  Sm_max,B,alpha,Kf,Ks = list(x)

  # initialize storage, all empty to start
  Sm,Sf1,Sf2,Sf3,Ss1 = [np.zeros(ndays) for _ in range(5)]
  Q = np.zeros(ndays)

  for t in range(1,ndays):

    # calculate all fluxes
    P = data_P[t]
    Peff = P*(1 - max(1-Sm[t-1]/Sm_max,0)**B) # PDM model Moore 1985
    Evap = min(data_PET[t]*(Sm[t-1]/Sm_max), Sm[t-1])

    Qf1 = Kf*Sf1[t-1]
    Qf2 = Kf*Sf2[t-1]
    Qf3 = Kf*Sf3[t-1]
    Qs1 = Ks*Ss1[t-1]
    
    # update state variables
    Sm[t] = Sm[t-1] + P - Peff - Evap
    Sf1[t] = Sf1[t-1] + alpha*Peff - Qf1
    Sf2[t] = Sf2[t-1] + Qf1 - Qf2
    Sf3[t] = Sf3[t-1] + Qf2 - Qf3
    Ss1[t] = Ss1[t-1] + (1-alpha)*Peff - Qs1

    Q[t] = Qs1 + Qf3

  if mode=='simulate':
    return Q
  else:
    return np.sqrt(np.sum((Q-data_Q)**2))


bounds = [(0,500), (0,2), (0,1), (0.1,1), (0,0.1)]

# to calibrate parameters and plot
# result = differential_evolution(hymod, bounds=bounds)
# print(result)
# Q = hymod(result.x, mode='simulate')
# plt.plot(Q)
# plt.plot(data_Q)
# plt.legend(['Simulated', 'Observed'])
# plt.show()


# to run SA
problem = {
  'num_vars': 5,
  'names': ['Cmax', 'B', 'alpha', 'Kq', 'Ks'],
  'bounds': bounds
}

param_values = saltelli.sample(problem, 1024)
N = len(param_values) # number of parameter samples
Y = np.zeros(N)

# Run model for each parameter set, save the output in array Y
for i in range(N):
  if i % 1000 == 0:
    print(i)
  Y[i] = hymod(param_values[i])

Si = sobol.analyze(problem, Y, print_to_console=True)

