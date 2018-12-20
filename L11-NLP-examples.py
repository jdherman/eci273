import numpy as np 
import matplotlib.pyplot as plt
from scipy import optimize

# Lecture 11 2-user water allocation example
# First approach: scipy.optimize.minimize
# does not return duals

# objective function (x is decision variable vector)
# def f(x):
#   return -1*(30*x[0] - 4*x[0]**2 + 10*x[1] - 2*x[1]**2)

# # if returns > zero, constraint satisfied
# def f_constraint(x):
#     return -(x[0] + x[1] - 5)

# constraint = {'type': 'ineq', 'fun': f_constraint}

# sol = optimize.minimize(f, x0 = [0,5], constraints=[constraint])
# print(sol)


# Second approach: cxvpy

from cvxpy import * # potentially confusing

x1 = Variable()
x2 = Variable()
Q = 5 # units of water

obj = Maximize(30*x1 - 4*x1**2 + 10*x2 - 2*x2**2)

constraints = [x1 + x2 <= Q, x1 >= 0, x2 >= 0] # magic?

prob = Problem(obj, constraints)
prob.solve()

print('Objective = %f' % obj.value)
print('X1 = %f' % x1.value)
print('X2 = %f' % x2.value)

for c in constraints:
  print('Dual (%s) = %f' % (c, c.dual_value))

