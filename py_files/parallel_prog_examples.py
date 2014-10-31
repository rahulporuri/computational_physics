
# http://sebastianraschka.com/Articles/2014_multiprocessing_intro.html
# 
# https://docs.python.org/dev/library/multiprocessing.html

# In[1]:

import multiprocessing as mp
import random
import string
import numpy as np


# In[2]:

def lj_force(x):
    return (2*(1./x)**13-(1./x)**7)


# In[3]:

pool = mp.Pool(processes=4)
results = [pool.apply(lj_force, args=(x,)) for x in range(1,7)]
print(results)


# Out[3]:

#     [1.0, -0.007568359375, -0.0004559929198788449, -6.1005353927612305e-05, -1.2798361600000004e-05, -3.5720919533714294e-06]
# 

# In[4]:

dist = np.array([0,1,2,3,4,5,6,7,8])
def lj_force(x):
    return (2*(1./dist[x])**13-(1./dist[x])**7)
pool = mp.Pool(processes=4)
results = [pool.apply(lj_force, args=(x,)) for x in range(1,7)]
print(results)


# Out[4]:

#     [1.0, -0.007568359375, -0.0004559929198788449, -6.1005353927612305e-05, -1.2798361600000004e-05, -3.5720919533714294e-06]
# 

# In[5]:

from scipy.constants import nano, pico, N_A, m_p, milli, micro
import scipy.spatial.distance as spd
import numpy as np
import time


# In[6]:

n = 400 # number of atoms in the system
#e = sigma = 1.
system = np.zeros([n,2,2])
# initialization
for i in xrange(n):
    system[i][0][0] = i%20 +15# positions in a 3X3 lattice
    system[i][0][1] = i/20 +15 # 3 is the square root of 9. if n is changed, so should this value!
    system[i][1] = np.array([np.random.normal(),np.random.normal()])


# In[7]:

def lj_force_sum(i):
    iforces = 0
    for j in xrange(len(system)):
        if i != j:
            temp = spd.euclidean(system[i][0],system[j][0])
            iforces += 2*(1./temp)**13-(1./temp)**7
    return iforces


# In[8]:

def lennard_jones(r):
    return (2*(1./r)**13 - (1./r)**7)*milli

def update_force(i):
    pxdot = 0
    pydot = 0
    for j in xrange(len(system)):
        if j != i :
            r = spd.euclidean(system[i][0],system[j][0])
            theta = np.arctan((system[j][0][1] - system[i][0][1])/(system[j][0][0] - system[i][0][0]))
            theta = theta*180/np.pi
            pxdot += lennard_jones(r)*np.cos(theta)
            pydot += lennard_jones(r)*np.sin(theta)
    return np.array([pxdot, pydot])


# In[9]:

start_time = time.time()
pool = mp.Pool(processes=3)
results = [pool.apply(update_force, args=(i,)) for i in range(399)]
print time.time()-start_time
#print(results)


# Out[9]:

#     11.0007920265
# 

#     -c:10: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:10: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:10: RuntimeWarning: divide by zero encountered in double_scalars
# 

# In[18]:

alist = []
start_time = time.time()
for i in xrange(len(system)):
    alist.append(update_force(i))
print time.time()-start_time


# Out[18]:

#     8.54602313042
# 

# In[10]:

#alist


# In[11]:

#np.asarray(alist)


# In[12]:

start_time = time.time()
pool = mp.Pool(processes=4)
results = [pool.apply_async(update_force, args=(i,)) for i in range(399)]
output = [p.get() for p in results]
print time.time()-start_time
#print(output)


# Out[12]:

#     4.18861508369
# 

#     -c:10: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:10: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:10: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:10: RuntimeWarning: divide by zero encountered in double_scalars
# 

# In[ ]:



