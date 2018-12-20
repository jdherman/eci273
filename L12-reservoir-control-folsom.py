import numpy as np 
import matplotlib.pyplot as plt
from cvxpy import *
import seaborn as sns
sns.set_style('whitegrid')

Q = np.loadtxt('data/FOL-monthly-inflow-TAF.csv', delimiter=',', skiprows=1, usecols=[1])

T = len(Q)
K = 975 # reservoir capacity
x = Variable(T+1) # storage vector
u = Variable(T) # release vector
d = 150*np.ones(T) # target demand (TAF/month)

# objective function
# these functions are imported from cvxpy
# be careful, because they override the default Python functions (sum, abs, etc.)
obj = Minimize(sum((pos(d - u))**2)) # sum squared deficit (vector form)

# constraints (define separately, then concatenate the lists)
c_mass_balance = [x[1:] == x[:-1] - u + Q] # state transition
c_release = [u >= 0] # release lower/upper bounds
c_storage = [x >= 0, x <= K] # storage lower/upper bounds
c_init_final = [x[0] == K/2, x[T] >= 200] # initial/final storage values
constraints = c_mass_balance + c_release + c_storage + c_init_final

prob = Problem(obj, constraints)
prob.solve()

print('Status: %s' % prob.status)
print('Obj Fun: %f' % obj.value)

#######################
# all plotting below here

plt.subplot(4,1,1)
plt.plot(x.value)
plt.ylabel('Storage (TAF)')

plt.subplot(4,1,2)
plt.plot(Q)
plt.plot(u.value)
plt.legend(['Inflow', 'Delivery'])
plt.ylabel('Flow (TAF/month)')

plt.subplot(4,1,3)
shortage = (d-u.value.A.flatten()).clip(0,999)
plt.plot(shortage, color='seagreen')
plt.ylabel('Shortage (TAF/month)')

# Duals (don't show at first)
plt.subplot(4,1,4)
plt.plot(constraints[0].dual_value, color='steelblue')
plt.plot(constraints[3].dual_value, color='#B94E48')
plt.ylabel(r'$\lambda(t)$')
plt.legend(['Mass Balance Constraint', 'Capacity Constraint'], loc=2)
plt.xlabel('Months (from Oct. 2000)')

plt.show()
