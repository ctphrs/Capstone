'''
given a movement_string, this program will integrate the total amount of
movement that was observed over the course of the entire path.
'''

import numpy as np

#Given a movement_string of x and y data, euclidify into a single vertical array.
def euclidify(movement_string):
    a = movement_string[:,0]
    b = movement_string[:,1]
    a = np.square(a)
    b = np.square(b)
    c = np.add(a,b)
    c = np.sqrt(c)
    c = np.array([c])
    c = np.transpose(c)
    return c

#Given a string of euclidean space deltas, integrate the total motion over the
#course of the string. This is a little too simple to be a function, but what-
#ever.
def integrate(euclid_string):
    discrete_integral = np.sum(euclid_string)
    return discrete_integral
