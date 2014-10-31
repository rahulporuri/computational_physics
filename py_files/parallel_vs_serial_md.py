
# In[39]:

import multiprocessing as mp
import random
import string
import numpy as np

import time
from scipy.constants import nano, pico, N_A, m_p, milli, micro
import scipy.spatial.distance as spd

# Define an output queue
output = mp.Queue()
"""
# define a example function
def rand_string(length, output):
    Generates a random string of numbers, lower- and uppercase chars.
    rand_str = ''.join(random.choice(
                    string.ascii_lowercase
                    + string.ascii_uppercase
                    + string.digits)
               for i in range(length))
    output.put(rand_str)"""

n = 400 # number of atoms in the system
#e = sigma = 1.
system = np.zeros([n,2,2])
# initialization
for i in xrange(n):
    system[i][0][0] = i%20 + 15 # positions in a 3X3 lattice
    system[i][0][1] = i/20 + 15 # 3 is the square root of 9. if n is changed, so should this value!
    system[i][1] = np.array([np.random.normal(),np.random.normal()])

force = np.zeros([n,2])
    
def lennard_jones(r):
    return (2*(1./r)**13 - (1./r)**7)*milli
    
def update_force(site):
    pxdot = 0
    pydot = 0
    for j in xrange(len(system)):
        if j != site :
            r = spd.euclidean(system[site][0],system[j][0])
            theta = np.arctan((system[j][0][1] - system[site][0][1])/(system[j][0][0] - system[site][0][0]))
            theta = theta*180/np.pi
            pxdot += lennard_jones(r)*np.cos(theta)
            pydot += lennard_jones(r)*np.sin(theta)
    return np.array([pxdot, pydot])

def parallel_force_update():
    pool = mp.Pool(processes=4)
    results = [pool.apply_async(update_force, args=(i,)) for i in range(399)]
    for i in xrange(len(results)):
        results[i] = results[i].get()
    results = np.asarray(results, dtype = float)
    
force = np.zeros([n,2])

def update_forces():
    for i in xrange(len(system)):
        pxdot = 0
        pydot = 0
        for j in xrange(len(system)):
            if j != i :
                r = spd.euclidean(system[i][0],system[j][0])
                theta = np.arctan((system[j][0][1] - system[i][0][1])/(system[j][0][0] - system[i][0][0]))
                theta = theta*180/np.pi
                pxdot += lennard_jones(r)*np.cos(theta)
                pydot += lennard_jones(r)*np.sin(theta)
        force[i] = np.array([pxdot, pydot])
    return force


# In[42]:

get_ipython().magic(u'timeit parallel_force_update()')


# Out[42]:

#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
# 

#     1 loops, best of 3: 4.01 s per loop
# 

#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:43: RuntimeWarning: divide by zero encountered in double_scalars
# 

# In[41]:

get_ipython().magic(u'timeit update_forces()')


# Out[41]:

#     1 loops, best of 3: 8.93 s per loop
# 

# In[ ]:



