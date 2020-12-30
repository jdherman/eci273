import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

# assumes minimization
# a dominates b if it is <= in all objectives and < in at least one
def dominates(a, b):
  return (np.all(a <= b) and np.any(a < b))

# accepts a matrix of points, returns a matrix of only the nondominated ones
# not the most efficient way to do this
# 'keep' is an array of booleans used to index the matrix at the end
def pareto_sort(P):
  N = len(P)
  keep = np.ones(N, dtype=bool) # all True to start

  for i in range(N):
    for j in range(i+1,N):
      if keep[j] and dominates(P[i,:], P[j,:]):
        keep[j] = False

      elif keep[i] and dominates(P[j,:], P[i,:]):
        keep[i] = False
  
  return P[keep,:]


# a matrix of data points for a hypothetical 2-objective problem
circle_points = np.loadtxt('data/circle-points.csv', delimiter=',')
pareto = pareto_sort(circle_points)

plt.scatter(circle_points[:,0],circle_points[:,1], c='0.7')
plt.scatter(pareto[:,0], pareto[:,1], c='red')
plt.legend(['Dominated Points', 'Non-dominated points'])
plt.show()
