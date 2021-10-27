# Basics: variables, if statements, for loops, lists, dictionaries
# indentation matters!

number = 3
name = 'somestring'

# if number < 5:
#   print('less')
# else:
#   print('more')

# python has two main data types: 
# lists and dictionaries

# list: things in order
# fruits = ['apple', 'banana', 'coconut', 'date', 'eucalyptus']

# loop over items in a list
# for fruit in fruits:
#   print(fruit)

# indexing a list (zero-indexed)
# print(fruits[0])

# length of a list
# print(len(fruits))

# to loop over numbers 
# for i in range(len(fruits)):
#   print(fruits[i])

# dictionary: key-value pairs
# cost = {'apple': 0.50, 'banana': 0.30}

# indexing a dictionary with a key (string)
# print(cost['apple'])

# defining functions
# def square(x):
#   return x**2

# x = 10
# y = square(x)
# print(y)

# What about arrays and matrices?
# creating a numpy array (1D,2D)
# indexing
# zeros and ones functions to initialize
# vector/matrix operations (elementwise arithmetic, addition, sum, mean, etc.)
# loops/lists = bad (speed comparison)

# this is how to import a library (and name it something shorter)
# import numpy as np

# A = np.array([0, 1, 2, 3, 4])

# can we use our function from before?
# print(square(A))

# lists vs. arrays (IMPORTANT)
# a regular python list
# L = [6, 3, 4, 7, 5]

# a numpy array
# A = np.array([6, 3, 7, 4, 5])

# indexing [start:stop:step]
# defaults: start=0, stop=N, step=1 (N is the number of values in the array)
# print(A[2:]) # from i to end
# print(A[:2]) # from beginning to i (not inclusive)
# print(A[-1]) # negative indexing is allowed!
# print(A[::2]) # every other element (omit start and stop)
# print(A[::-1]) # reverse the array (step = -1)
# print(A[A < 5]) # logical indexing

# what's the difference?
# 'A' behaves like a matlab array
# what do you expect to happen?
# print(L*3)
# print(A*3)

# a 2d array (matrix)
# A2 = np.array([[6,3,7,4,5], [2,6,3,40,1]])

# indexing [i,j]
# print(A2[0,3])

# get a row (: means "all", just like matlab)
# print(A2[0,:])

# create a matrix of zeros
# M = np.zeros((10,5))
# M[:,:] = 4 
# print(M)

# vectorized functions (IMPORTANT)
# numpy has many built-in functions to simplify matrix operations
# N = 10000000
# M = np.ones((N,5))

# use vectorized functions whenever you can,
# e.g. don't do this...

# s = 0
# for i in range(N):
#   for j in range(5):
    # s += M[i,j]

# print(s)

# instead do this...
# print(M.sum())
# print(np.sum(M)) # either syntax is fine


# Matplotlib: how to make plots
# import matplotlib.pyplot as plt

# data = np.random.rand(100)

# plt.plot(data, color='red', linewidth=2)
# plt.xlabel('x value')
# plt.ylabel('Random number')
# plt.title('my title')

# plt.savefig('something.png', dpi = 300)
# plt.show()


