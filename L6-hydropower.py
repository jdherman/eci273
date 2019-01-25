import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

cfs_to_taf = 2.29568411*10**-5 * 86400 / 1000

def storage_to_elevation(S): # from regression
  return -0.000078*S**2 + 0.213526*S + 328.922121

# some parameters assumed specific to folsom
def simulate_folsom(Q):
  K = 975 # TAF capacity
  D = 3.5 # TAF/day demand
  # assume a constant downstream water elevation
  # (neglects the hydraulic effects of changing flowrate)
  downstream_wse = 134 # feet
  turbine_max_outflow = 8600 # cfs
  efficiency = 0.82

  T = len(Q)
  S = np.zeros(T) # storage, TAF
  WSE = np.zeros(T) # water surface elevation, ft
  R = np.zeros(T) # release (for demand), TAF/d
  spill = np.zeros(T) # additional release for spill, TAF/d

  S[0] = K # start simulation full
  WSE[0] = storage_to_elevation(S[0])
  R[0] = D

  for t in range(1,T):
    spill[t-1] = max(S[t-1] + Q[t-1] - R[t-1] - K, 0)
    S[t] = S[t-1] + Q[t-1] - R[t-1] - spill[t-1]
    WSE[t] = storage_to_elevation(S[t])

    if S[t] + Q[t] > D:
      R[t] = D
    else:
      R[t] = S[t] + Q[t]

  # metrics from before
  alteration = np.abs(Q - R - spill).sum() / Q.sum()
  reliability = R[R==D].size / float(T)

  # hydropower calculations
  h = WSE - downstream_wse # hydraulic head, feet
  turbine_outflow = np.clip((R+spill)/cfs_to_taf, 0, turbine_max_outflow) # this is a useful function
  power = efficiency * h * turbine_outflow / (1.181*10**4) # MW

  return S, R+spill, power


df = pd.read_csv('data/L6-FOL-daily.csv', index_col=0, parse_dates=True)

# some missing values to deal with first
# print(df[df.isnull().any(axis=1)])
df = df.fillna(method='ffill')
Q = df.inflow.values

S, R, power = simulate_folsom(Q)

# add these results into the original dataframe
df['S_sim'] = pd.Series(S, index=df.index)
df['R_sim'] = pd.Series(R, index=df.index)
df['power_sim'] = pd.Series(power, index=df.index)

df.power_sim.plot()
plt.ylabel('Power, mean daily MW')
plt.show()

# (24/1000*df.power_sim.resample('A').sum()).plot()
# plt.ylabel('Annual Energy Generation, GWh/yr')
# plt.show()
