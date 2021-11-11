import numpy as np 
import matplotlib.pyplot as plt
from cvxpy import *
import seaborn as sns
sns.set_style('whitegrid')

Q = np.loadtxt('data/FOL-monthly-inflow-TAF.csv', delimiter=',', skiprows=1, usecols=[1])
T = len(Q)
K = 975 # reservoir capacity
d = 150*np.ones(T) # target demand (TAF/day)
dw = 0.1

results = []
i = 1

# weighted sum method
for w in np.arange(0,1+dw,dw):

  x = Variable(T+1)
  u = Variable(T)
  cost = sum((pos(d - u))**2)
  alteration = sum((u-Q)**2)

  obj = Minimize(w*cost + (1-w)*alteration) # sum squared deficit (vector form)

  # constraints (define separately, then concatenate the lists)
  c_mass_balance = [x[1:] == x[:-1] - u + Q] # state transition
  c_release = [u >= 0] # release lower/upper bounds
  c_storage = [x >= 0, x <= K] # storage lower/upper bounds
  c_init_final = [x[0] == 500, x[T] >= 200]
  constraints = c_mass_balance + c_release + c_storage + c_init_final

  prob = Problem(obj, constraints)
  prob.solve()
  results.append([cost.value, alteration.value])

  plt.subplot(11,1,i)
  plt.plot(Q, color='blue')
  plt.plot(u.value, color='red')
  plt.ylabel('Flow (TAF/m)')
  plt.legend(['Inflow', 'Outflow'])
  print(i)
  i += 1

plt.show()

results = np.array(results)
plt.scatter(results[:,0],results[:,1], s=30, c='k')
plt.xlabel('Shortage Cost ($)')
plt.ylabel('Env. Alteration (TAF)')
plt.show()

