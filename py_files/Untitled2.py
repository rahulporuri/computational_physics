
# In[48]:

import scipy.spatial.distance as spd
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import numpy as np
import time
# used to compare energy before and after a move
# we assumed that epsilon and alpha are 1

e = 1.
def local_energy(site):
    local_sum = 0
    for i in xrange(len(system)):
        if site != i:
            dist = spd.euclidean(system[site],system[i])
            local_sum += -((1/dist)**12-(1/dist)**6)*e
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
global_e_cycle = system_energy()
global_energy.append(temp)
#print temp, "0 energy"
accepted_moves = 0

#plt.subplot(131)
radial_dist_before = radial_number_density()
#anarray = np.asarray(alist)
#plt.hist(anarray,10);

T = 1
# T = np.array([5.,5./2,1./1./2,1./10])
beta = 1./T
# B = 1./T
#for beta in B:
time_per_loop = []
for looptime in xrange(200):
    start_time = time.time()
    site = np.random.choice(np.arange(n)) # atom to be moved
    # this atom can now move in the range (-alpha,alpha) in x & y
    #xmove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    #ymove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    xmove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    ymove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    #print xmove, ymove, "xmove, ymove"
    #xmove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    #ymove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    pre_move_e = local_energy(site)
    #print pre_move_e, "pre move e"
    system[site] = system[site] + np.array([xmove,ymove])
    if system[site][0] > 20 :
        system[site][0] = system[site][0]%20
    #if system[site][0] < 0 :
    #    system[site][0] = system[site][0]%100
    if system[site][1] > 20 :
        system[site][1] = system[site][1]%20
    #if system[site][1] < 0 :
    #    system[site][1] = system[site][1]%100
    post_move_e = local_energy(site)
    #print post_move_e, "post move e"
    #print post_move_e-pre_move_e, "difference"
    diff = post_move_e - pre_move_e
    #print diff, "difference in energy", looptime, "iteration"
    #temp = system_energy()
    #temp = temp + diff
    #print temp, "is system energy at step", looptime
    #print system_energy()
    if post_move_e - pre_move_e < 0:
        #global_energy.append(system_energy())
        global_e_cycle += diff
        global_energy.append(global_e_cycle)
        accepted_moves += 1
        #print "yes"
    else :
        temp = np.random.random()
        if temp < np.exp(-beta*(post_move_e - pre_move_e)):
            global_e_cycle +=diff
            global_energy.append(global_e_cycle)
        #    global_energy.append(system_energy())
            accepted_moves += 1
        #    print "barely yes"
        else :
            system[site] = system[site] - np.array([xmove,ymove])
            global_energy.append(global_e_cycle)
            #print looptime
        #    global_energy.append(system_energy())
        #    print "nyooo!!!!"
    #print "we're done with the mc loop %f" % (time.time()-start_time)
    time_per_loop.append(time.time()-start_time)
# we get global_energy, accepted moves as the outputs here.
#plt.subplot(132)
radial_dist_after = radial_number_density()
#anarray = np.asarray(alist)
#plt.hist(anarray,10);
#plt.subplot(133)
#plt.plot(global_energy)
#print "we're done with plotting routine %f" % (time.time()-start_time)
print "accepted_moves", accepted_moves


# Out[48]:

#     accepted_moves 142
# 

# In[49]:

plt.plot(global_energy)


# Out[49]:

#     [<matplotlib.lines.Line2D at 0xb0e7516c>]

# image file:

# In[50]:

np.mean(time_per_loop)
#start_time = time.time()
#print system_energy()
#print time.time() - start_time


# Out[50]:

#     0.026244132518768309

# In[52]:

plt.subplot(121)
anarray = np.asarray(radial_dist_before)
plt.hist(anarray,10);
plt.subplot(122)
anotherarray = np.asarray(radial_dist_after)
plt.hist(anotherarray,10);


# Out[52]:

# image file:

# In[53]:

x = []
y = []
for i in xrange(len(system)):
    x.append(system[i][0])
    y.append(system[i][1])
plt.scatter(x,y);


# Out[53]:

# image file:

# In[ ]:



