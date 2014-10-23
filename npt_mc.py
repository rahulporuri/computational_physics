
# In[ ]:




# In[4]:

import scipy.spatial.distance as spd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

# used to compare energy before and after a move
# we assumed that epsilon and alpha are 1
def local_energy(site):
    local_sum = 0
    for i in xrange(len(system)):
        if site != i:
            dist = spd.euclidean(system[site],system[i])
            local_sum += -((1/dist)**12-(1/dist)**6)
    return local_sum

# total energy of the system
def system_energy():
    total_sum = 0
    for i in xrange(len(system)):
        total_sum += local_energy(i)
    return total_sum

def radial_number_density():
    rad_dist = []
    for i in xrange(len(system)):
        for j in xrange(len(system)):
            if i != j:
                temp = spd.euclidean(system[i],system[j])
                rad_dist.append(temp)
    return rad_dist

n = 400 # number of particles
# initializing the system
# the atoms occupy a square of size 10X10
system = np.zeros([n,2])
for i in xrange(len(system)):
    system[i][0] = i%20 # np.sqrt(n) wont work as it will return a float
    system[i][1] = i/20 # we need an integer denominator for this to work!

global_energy = []
accepted_moves = 0

plt.subplot(131)
alist = radial_number_density()
anarray = np.asarray(alist)
plt.hist(anarray,10);

T = 1.
# T = np.array([5.,5./2,1./1./2,1./10])
beta = 1./T
# B = 1./T
#for beta in B:
for timestep in xrange(100):
    site = np.random.choice(np.arange(n)) # atom to be moved
    # this atom can now move in the range (-alpha,alpha) in x & y
    #xmove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    #ymove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    #xmove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    #ymove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    xmove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    ymove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    v_ratio = np.random.choice(np.array([0.90,0.95,1.0,1.05,1.10]))
    pre_move_e = local_energy(site)
    system[site] = system[site] + np.array([xmove,ymove])
    if system[site][0] > 50 :
        system[site][0] = system[site][0]%50
    #if system[site][0] < 0 :
    #    system[site][0] = system[site][0]%100
    if system[site][1] > 50 :
        system[site][1] = system[site][1]%50
    #if system[site][1] < 0 :
    #    system[site][1] = system[site][1]%100
    post_move_e = local_energy(site)
    if post_move_e - pre_move_e < 0:
        global_energy.append(system_energy())
        accepted_moves += 1
    else :
        temp = np.random.random()
        if temp < np.exp(-((v_ratio)**n)*beta*(post_move_e - pre_move_e)):
            global_energy.append(system_energy())
            accepted_moves += 1
        else :
            system[site] = system[site] - np.array([xmove,ymove])
            global_energy.append(system_energy())
    #print timestep, "done"
# we get global_energy, accepted moves as the outputs here.
plt.subplot(132)
alist = radial_number_density()
anarray = np.asarray(alist)
plt.hist(anarray,10);
plt.subplot(133)
plt.plot(global_energy)
print "accepted_moves", accepted_moves


# Out[4]:

#     accepted_moves 13
# 

# image file:

# In[ ]:




# In[ ]:

def local_energy(site):
    local_sum = 0
    for i in xrange(len(system)):
        if site != i:
            dist = spd.euclidean(system[site],system[i])
            local_sum += -((1/dist)**12-(1/dist)**6)
    return np.array([local_sum])


# In[11]:

import time
start_time = time.time()
temp = system_energy()
print time.time() - start_time


# Out[11]:

#     5.13577103615
# 

# In[27]:

import multiprocessing as mp
start_time = time.time()
pool = mp.Pool(processes=3)
results = [pool.apply_async(local_energy, args=(i,)) for i in range(399)]
output = [p.get() for p in results]
print time.time()-start_time
#print(output)


# Out[27]:

#     2.71200299263
# 

# In[ ]:




# In[ ]:




# In[2]:

import scipy.spatial.distance as spd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

# used to compare energy before and after a move
# we assumed that epsilon and alpha are 1
def local_energy(site):
    local_sum = 0
    for i in xrange(len(system)):
        if site != i:
            dist = spd.euclidean(system[site],system[i])
            local_sum += -((1/dist)**12-(1/dist)**6)
    return local_sum

# total energy of the system
def system_energy():
    total_sum = 0
    for i in xrange(len(system)):
        total_sum += local_energy(i)
    return total_sum

def radial_number_density():
    rad_dist = []
    for i in xrange(len(system)):
        for j in xrange(len(system)):
            if i != j:
                temp = spd.euclidean(system[i],system[j])
                rad_dist.append(temp)
    return rad_dist

n = 400 # number of particles
# initializing the system
# the atoms occupy a square of size 10X10
system = np.zeros([n,2])
for i in xrange(len(system)):
    system[i][0] = i%20 # np.sqrt(n) wont work as it will return a float
    system[i][1] = i/20 # we need an integer denominator for this to work!

global_energy = []
accepted_moves = 0
energy_now = system_energy() ####
accepted_moves = 0

plt.subplot(131)
alist = radial_number_density()
anarray = np.asarray(alist)
plt.hist(anarray,10);

T = 1.
# T = np.array([5.,5./2,1./1./2,1./10])
beta = 1./T
# B = 1./T
#for beta in B:
for timestep in xrange(5000):
    site = np.random.choice(np.arange(n)) # atom to be moved
    # this atom can now move in the range (-alpha,alpha) in x & y
    #xmove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    #ymove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    #xmove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    #ymove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    xmove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    ymove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    v_ratio = np.random.choice(np.array([0.90,0.95,1.0,1.05,1.10]))
    pre_move_e = local_energy(site)
    system[site] = system[site] + np.array([xmove,ymove])
    if system[site][0] > 50 :
        system[site][0] = system[site][0]%50
    #if system[site][0] < 0 :
    #    system[site][0] = system[site][0]%100
    if system[site][1] > 50 :
        system[site][1] = system[site][1]%50
    #if system[site][1] < 0 :
    #    system[site][1] = system[site][1]%100
    post_move_e = local_energy(site)
    diff = post_move_e - pre_move_e ###
    if post_move_e - pre_move_e < 0:
        energy_now += diff ####
        global_energy.append(energy_now) ####
        accepted_moves += 1
    else :
        temp = np.random.random()
        if temp < np.exp(-((v_ratio)**n)*beta*(post_move_e - pre_move_e)):
            energy_now += diff ####
            global_energy.append(energy_now) ####
            accepted_moves += 1
        else :
            system[site] = system[site] - np.array([xmove,ymove])
            global_energy.append(energy_now)
    #print timestep, "done"
# we get global_energy, accepted moves as the outputs here.
plt.subplot(132)
alist = radial_number_density()
anarray = np.asarray(alist)
plt.hist(anarray,10);
plt.subplot(133)
plt.plot(global_energy)
print "accepted_moves", accepted_moves


# Out[2]:

#     accepted_moves 2266
# 

#     -c:13: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:13: RuntimeWarning: invalid value encountered in double_scalars
# 

# image file:

# In[ ]:



