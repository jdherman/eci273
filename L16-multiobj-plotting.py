import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

# load a 4-objective pareto front
data = np.loadtxt('data/example-pareto-front.csv', delimiter=',')

# Example 1: N-dimensional scatter plot
# from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # use 's' and 'c' for size/color, respectively
# h = ax.scatter(data[:,0], data[:,1], data[:,2], 
#            c=data[:,3], cmap=plt.cm.cool, s=50*data[:,0], edgecolor='none')

# plt.colorbar(h)
# plt.show()

# Example 2: parallel axis

# first normalize each objective to [0,1] range
for objs in data:
  objs = (objs - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))

  # filtering
  if objs[2] < 0.5:
    plt.plot(range(4), objs, color='steelblue', zorder=2)
  else:
    plt.plot(range(4), objs, color='0.8', zorder=1)

plt.gca().set_xticks(range(4))
plt.gca().set_xticklabels(['A','B','C','D'])
plt.show()

# Example 3: scatter plot matrix

# for i in range(4):
#   for j in range(4):
#     plt.subplot(4,4,i*4+j+1)

#     plt.scatter(data[:,i], data[:,j])

# plt.show()
