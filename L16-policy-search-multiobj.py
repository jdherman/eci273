import numpy as np 
import matplotlib.pyplot as plt
from platypus.algorithms import NSGAII
from platypus.core import Problem
from platypus.types import Real

# Set some parameters
K = 975 # capacity, TAF
D = 150 # target yield, TAF
a = 0.35
b = 2.3 # cost function parameters

# data setup
Q = np.loadtxt('data/FOL-monthly-inflow-TAF.csv', delimiter=',', skiprows=1, usecols=[1])
T = len(Q)

# same function, but now returns 2 objectives
def simulate(x):
  S = np.zeros(T)
  R = np.zeros(T)
  cost = np.zeros(T)
  h0 = x[0]
  hf = x[1]

  S[0] = K # start simulation full
  reliability = 0

  for t in range(1,T):

    # new storage: mass balance, max value is K
    S[t] = min(S[t-1] + Q[t-1] - R[t-1], K)

    # determine R from hedging policy
    W = S[t] + Q[t]
    if W > hf:
      R[t] = D
      reliability += 1.0/T
    elif W < h0:
      R[t] = W
    else:
      R[t] = (D-h0)/(hf-h0)*(W-h0)+h0

    shortage = D-R[t]
    cost[t] = a*shortage**b

  return [cost.mean(), reliability]



# Problem(number of decisions, number of objectives)
problem = Problem(2, 2)
problem.types[0] = Real(0,D)
problem.types[1] = Real(D,K+D)
problem.directions[1] = Problem.MAXIMIZE
problem.function = simulate

algorithm = NSGAII(problem)

# optimize the problem using 10000 function evaluations
algorithm.run(10000)


# just plotting below here ~~~~~~~~~~~~~
# convert data to numpy first..
obj = np.array([s.objectives for s in algorithm.result])
x = np.array([s.variables for s in algorithm.result])

# to make a contour plot...
h0s = np.arange(0,D,5)
hfs = np.arange(D,K+D,5)
X,Y = np.meshgrid(h0s, hfs)
costs = np.zeros((len(h0s),len(hfs)))
rels = np.zeros((len(h0s),len(hfs)))
i,j = 0,0

# fill in matrices for contour plot
for i,h0 in enumerate(h0s):
  for j,hf in enumerate(hfs):
    costs[i,j],rels[i,j] = simulate([h0,hf])

plt.subplot(1,2,1)
plt.contour(X,Y,costs.T, 50, cmap=plt.cm.cool)
plt.contour(X,Y,rels.T, 50, cmap=plt.cm.Reds)
plt.scatter(x[:,0],x[:,1], s=30, color='k', zorder=5)
plt.xlabel(r'$h_0$')
plt.ylabel(r'$h_f$')

plt.subplot(1,2,2)
plt.scatter(obj[:,0],obj[:,1], s=30, color='k')
plt.xlabel('Shortage Cost')
plt.ylabel('Reliability')

plt.show()

