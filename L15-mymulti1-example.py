import numpy as np 
import matplotlib.pyplot as plt
from scipy import optimize
import seaborn as sns
sns.set_style('whitegrid')

# two-objective problem, no constraints
def f1(x):
  return x[0]**4 - 10*x[0]**2+x[0]*x[1] + x[1]**4 -(x[0]**2)*(x[1]**2)

def f2(x):
  return x[1]**4 - (x[0]**2)*(x[1]**2) + x[0]**4 + x[0]*x[1]

x_keep = []
f_keep = []
dw = 0.05 # how much to change weights by

for w in np.arange(0,1+dw,dw):

  # redefine the single-objective function with new weights
  # yea you can do this, maybe don't make a habit of it though
  def objfun(x):
    return w*f1(x) + (1-w)*f2(x)

  sol = optimize.minimize(objfun, x0 = [1,-1])
  x_keep.append(sol.x)
  f_keep.append([f1(sol.x), f2(sol.x)]) # re-run separate objective functions


# just plotting below here ...
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
x_keep = np.array(x_keep)
f_keep = np.array(f_keep)

plt.subplot(1,2,1)

X1,X2 = np.meshgrid(np.arange(0,3,0.01), np.arange(-2,0,0.01))

plt.contour(X1,X2,f1([X1,X2]),50,cmap=plt.cm.Blues_r)
plt.contour(X1,X2,f2([X1,X2]),50,cmap=plt.cm.Reds_r)
plt.scatter(x_keep[:,0], x_keep[:,1], zorder=5, color='k', s=30)
plt.ylim([-2,0])
plt.xlim([0,3])
plt.title('Decision Space')

plt.subplot(1,2,2)
plt.scatter(f_keep[:,0], f_keep[:,1], color='k', s=30)
plt.xlim([-40,-5])
plt.ylim([0,35])
plt.title('Objective Space')

plt.show()

