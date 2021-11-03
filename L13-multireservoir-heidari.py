import numpy as np 
import matplotlib.pyplot as plt
from cvxpy import *

# multireservoir problem from Heidari et al. 1971
# the beginning is all data setup

T = 12
X = Variable((T+1, 4))
U = Variable((T, 4))

# benefits matrix from paper
B = np.array([[1.1,1.4,1.0,1.0,1.6],
            [1.0,1.1,1.0,1.2,1.7],
            [1.0,1.0,1.2,1.8,1.8],
            [1.2,1.0,1.8,2.5,1.9],
            [1.8,1.2,2.5,2.2,2.0],
            [2.5,1.8,2.2,2.0,2.0],
            [2.2,2.5,2.0,1.8,2.0],
            [2.0,2.2,1.8,2.2,1.9],
            [1.8,2.0,2.2,1.8,1.8],
            [2.2,1.8,1.8,1.4,1.7],
            [1.8,2.2,1.4,1.1,1.6],
            [1.4,1.8,1.1,1.0,1.5]])

# reservoir connectivity matrix
M = np.array([[-1,0,0,0],
              [0,-1,0,0],
              [0,1,-1,0],
              [1,0,1,-1]])

# inflows (constant)
y = np.zeros((T,4))
y[:,0] = 2
y[:,1] = 3

# storage upper bound
XUB = 10*np.ones((T+1,4))
XUB[:,3] = 15
# release upper bound
UUB = 4*np.ones((T,4))
UUB[:,0] = 3
UUB[:,3] = 7

# objective function (hydropower plus ag benefit)
# note: in cvxpy 1.1 and later, they recommend @ symbol for matrix multiplication
# if we use * instead it will give a warning
obj = Maximize(B[:,0].T @ U[:,0] + B[:,1].T @ U[:,1] 
             + B[:,2].T @ U[:,2] + B[:,3].T @ U[:,3] + B[:,4].T @ U[:,3])

# mass balance constraint in matrix form
c_mass_balance = [X[1:,:] == X[:-1,:] + y + U @ M.T]
c_nonneg = [U >= 0, X >= 0] # release lower/upper bounds
c_ub = [X <= XUB, U <= UUB]
c_init_final = [X[0,:] == 5, X[T,:] >= np.array([5,5,5,7])]
constraints = c_mass_balance + c_nonneg + c_ub + c_init_final

prob = Problem(obj, constraints)
prob.solve()

print('Status: %s' % prob.status)
print('Obj Fun: %f' % obj.value)

for i in range(4):
  plt.subplot(2,2,i+1)
  plt.plot(X[:,i].value)
  plt.ylim([0,10])
  plt.title('Reservoir %d storage' % (i+1))

plt.show()
