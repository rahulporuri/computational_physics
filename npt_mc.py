
# In[ ]:




# In[29]:

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
    #xmove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    #ymove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
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


# Out[29]:

#     0 done
#     1 done
#     2 done
#     3 done
#     4 done
#     5 done
#     6 done
#     7 done
#     8 done
#     9 done
#     10 done
#     11 done
#     12 done
#     13 done
#     14 done
#     15 done
#     16 done
#     17 done
#     18 done
#     19 done
#     20 done
#     21 done
#     22 done
#     23 done
#     24 done
#     25 done
#     26 done
#     27 done
#     28 done
#     29 done
#     30 done
#     31 done
#     32 done
#     33 done
#     34 done
#     35 done
#     36 done
#     37 done
#     38 done
#     39 done
#     40 done
#     41 done
#     42 done
#     43 done
#     44 done
#     45 done
#     46 done
#     47 done
#     48 done
#     49 done
#     50 done
#     51 done
#     52 done
#     53 done
#     54 done
#     55 done
#     56 done
#     57 done
#     58 done
#     59 done
#     60 done
#     61 done
#     62 done
#     63 done
#     64 done
#     65 done
#     66 done
#     67 done
#     68 done
#     69 done
#     70 done
#     71 done
#     72 done
#     73 done
#     74 done
#     75 done
#     76 done
#     77 done
#     78 done
#     79 done
#     80 done
#     81 done
#     82 done
#     83 done
#     84 done
#     85 done
#     86 done
#     87 done
#     88 done
#     89 done
#     90 done
#     91 done
#     92 done
#     93 done
#     94 done
#     95 done
#     96 done
#     97 done
#     98 done
#     99 done
#     accepted_moves 95
# 

# image file:

# In[26]:

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



