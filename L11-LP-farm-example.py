import numpy as np 
import matplotlib.pyplot as plt
from scipy import optimize

# Lecture 11 2-user water allocation example
# First approach: scipy.optimize.linprog
# need matrix form: minimize c^T * x, subject to Ax <= b

# c = [-5, -3] # negative to maximize
# A = [[10,5], [1,1.5], [2,2], [-1,0], [0,-1]]
# b = [20, 3, 4.5, 0, 0]

# sol = optimize.linprog(c, A, b)
# print('Scipy Output:')
# print(sol)


# Second approach: cxvpy
from cvxpy import *

xc = Variable(name='xc')
xb = Variable(name='xb')
pc = 5
pb = 3

obj = Maximize(pc*xc + pb*xb)

constraints = [10*xc + 5*xb <= 20,
               xc + 1.5*xb <= 3,
               2*xc + 2*xb <= 4.5,
               xc >= 0,
               xb >= 0]

prob = Problem(obj, constraints)
prob.solve(verbose=True)

print('\ncvxpy Output:')
print('Objective = %f' % obj.value)
print('xc = %f' % xc.value)
print('xb = %f' % xb.value)
for c in constraints:
  print('Dual (%s) = %f' % (c, c.dual_value))
