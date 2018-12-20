import numpy as np 
import matplotlib.pyplot as plt
from cvxpy import *
import seaborn as sns
sns.set_style('whitegrid')

Q = np.loadtxt('data/FOL-monthly-inflow-TAF.csv', delimiter=',', skiprows=0, usecols=[1])
T = len(Q)

K = 975 # reservoir capacity
h = 12 # foresight horizon (months) MUST divide evenly into T
d = 150*np.ones(h) # target demand (TAF/month)

# need some empty arrays to fill in
x_save = np.zeros(T+1)
u_save = np.zeros(T)
shortage_save = np.zeros(T)

for i in range(0,T,h): # zero to T in steps of h

  x = Variable(h+1)
  u = Variable(h)

  # objective function
  # subtract the storage to incentivize saving water
  # obj = Minimize(sum((pos(d - u))**2) - x[h])

  # objective function with carryover value target
  obj = Minimize(sum((pos(d - u))**2) + pos(200-x[h])**2)

  # initial condition
  if i==0:
    ic = K/2
  else:
    ic = x_save[i] # from previous optimization

  # constraints (define separately, then concatenate the lists)
  c_mass_balance = [x[1:] == x[:-1] - u + Q[i:i+h]] # state transition
  c_release = [u >= 0] # release lower/upper bounds
  c_storage = [x >= 0, x <= K] # storage lower/upper bounds
  c_init_final = [x[0] == ic, x[h] >= 0]
  constraints = c_mass_balance + c_release + c_storage + c_init_final

  prob = Problem(obj, constraints)
  prob.solve()

  # now look at the results
  print('Status: %s' % prob.status)
  print('Obj Fun: %f' % obj.value)

  # save in big array
  x_save[i:i+h+1] = x.value.A.flatten()

  if h > 1:
    u_save[i:i+h] = u.value.A.flatten()
    shortage_save[i:i+h] = (d-u.value.A.flatten()).clip(0,999)
  else:
    u_save[i:i+h] = u.value
    shortage_save[i:i+h] = (d-u.value).clip(0,999)

# plot the state variable (storage) and control variable (release)
plt.subplot(3,1,1)
plt.plot(x_save)
plt.ylabel('Storage (TAF)')

plt.subplot(3,1,2)
plt.plot(u_save)
plt.ylabel('Flow (TAFM)')

plt.subplot(3,1,3)
plt.plot(shortage_save, color='seagreen')
plt.ylabel('Shortage (TAFM)')
plt.xlabel('Months (from 10/1/2000)')

plt.show()

# hedging rule?
plt.scatter(x_save[:-1]+Q, u_save)
plt.plot([0,1000],[0,1000], color='k', linewidth=2)
plt.plot([975, 975+1000],[0,1000], color='k', linewidth=2)
plt.plot([0,2000],[150,150], '--', color='k')
plt.ylim([0,1000])
plt.xlim([0,2000])
plt.xlabel('Water Available (S+Q)')
plt.ylabel('Release (u)')
plt.show()