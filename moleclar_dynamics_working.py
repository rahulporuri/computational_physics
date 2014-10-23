
# In[1]:

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import nano, pico, N_A, m_p, milli, micro
get_ipython().magic(u'matplotlib inline')
import time
import scipy.spatial.distance as spd


# In[2]:

n = 400 # number of atoms in the system
#e = sigma = 1.
system = np.zeros([n,2,2])
# initialization
for i in xrange(n):
    system[i][0][0] = i%20 + 15 # positions in a 3X3 lattice
    system[i][0][1] = i/20 + 15 # 3 is the square root of 9. if n is changed, so should this value!
    system[i][1] = np.array([np.random.normal(),np.random.normal()])


# In[15]:

def update_position():
    for i in xrange(len(system)):
        system[i][0] += system[i][1]*step
        if system[i][0][0] > 50:
            system[i][0][0] = system[i][0][0]%50
        if system[i][0][1] > 50:
            system[i][0][0] = system[i][0][0]/50
        if system[i][0][0] < -0:
            system[i][0][0] = system[i][0][0]%50
        if system[i][0][1] < -0:
            system[i][0][1] += 50
    return system

def update_momentum():
    for i in xrange(len(system)):
        system[i][1] += force[i]*step/2
    return system

def lennard_jones(r):
    return (2*(1./r)**13 - (1./r)**7)*milli

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

def radial_number_density():
    rad_dist = []
    for i in xrange(len(system)):
        for j in xrange(len(system)):
            if i != j:
                temp = spd.euclidean(system[i][0],system[j][0])
                rad_dist.append(temp)
    return rad_dist

initial_dist = radial_number_density()

#step = 1./np.power(10,2) - doesnt work. NaN!!!
step = 1.*milli # works
#step = 1.
total_time = time.time()
force_step_time = []
for timestep in range(100):
    #start_time = time.time()
    update_momentum()
    #print "first momemtum update %f" %(time.time()-start_time)
    #start_time = time.time()
    update_position()
    #print "position update %f" %(time.time()-start_time)
    start_time = time.time()
    update_forces()
    force_step_time.append(time.time()-start_time)
    #print "force update %f" %(time.time()-start_time)
    #start_time = time.time()
    update_momentum()
    #print "second momemtum update %f" %(time.time()-start_time)
    #print timestep
print "total time %f" %(time.time()-total_time)
final_dist = radial_number_density()


# Out[15]:

#     total time 3229.049972
# 

# In[16]:

np.mean(np.asarray(force_step_time))


# Out[16]:

#     32.230867798328397

# In[17]:

plt.subplot(121)
plt.hist(initial_dist,10);
plt.subplot(122)
plt.hist(final_dist,10);


# Out[17]:

# image file:

# In[18]:

x = []
y = []
for i in xrange(len(system)):
    x.append(system[i][0][0])
    y.append(system[i][0][1])
plt.scatter(x,y);
#plt.ylim([-200,200])


# Out[18]:

#     <matplotlib.collections.PathCollection at 0xb136c8ec>

# image file:

# parallelized code
# =======

# In[6]:

import multiprocessing as mp
import random
import string


# In[11]:

def update_position():
    for i in xrange(len(system)):
        system[i][0] += system[i][1]*step
        if system[i][0][0] > 50:
            system[i][0][0] = system[i][0][0]%50
        if system[i][0][1] > 50:
            system[i][0][0] = system[i][0][0]/50
        if system[i][0][0] < -0:
            system[i][0][0] = system[i][0][0]%50
        if system[i][0][1] < -0:
            system[i][0][1] += 50
    return system

def update_momentum():
    for i in xrange(len(system)):
        system[i][1] += force[i]*step/2
    return system

def lennard_jones(r):
    return (2*(1./r)**13 - (1./r)**7)*milli

force = np.zeros([n,2])

###################################

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
    force = np.asarray(results, dtype = float)
    return force

###################################

def radial_number_density():
    rad_dist = []
    for i in xrange(len(system)):
        for j in xrange(len(system)):
            if i != j:
                temp = spd.euclidean(system[i][0],system[j][0])
                rad_dist.append(temp)
    return rad_dist

initial_dist = radial_number_density()

#step = 1./np.power(10,2) - doesnt work. NaN!!!
step = 1.*milli # works
#step = 1.
total_time = time.time()
force_step_time = []
for timestep in range(100):
    #start_time = time.time()
    update_momentum()
    #print "first momemtum update %f" %(time.time()-start_time)
    #start_time = time.time()
    update_position()
    #print "position update %f" %(time.time()-start_time)
    start_time = time.time()
    parallel_force_update()
    force_step_time.append(time.time()-start_time)
    #print "force update %f" %(time.time()-start_time)
    #start_time = time.time()
    update_momentum()
    #print "second momemtum update %f" %(time.time()-start_time)
    #print timestep
print "total time %f" %(time.time()-total_time)
final_dist = radial_number_density()


# Out[11]:

#     total time 219.692911
# 

# In[12]:

np.mean(np.asarray(force_step_time))


# Out[12]:

#     21.882663345336915

# In[13]:

plt.subplot(121)
plt.hist(initial_dist,10);
plt.subplot(122)
plt.hist(final_dist,10);


# Out[13]:

# image file:

# In[19]:

x = []
y = []
for i in xrange(len(system)):
    x.append(system[i][0][0])
    y.append(system[i][0][1])
plt.scatter(x,y);
#plt.ylim([-200,200])


# Out[19]:

#     <matplotlib.collections.PathCollection at 0xb143b04c>

# image file:

# In[ ]:



