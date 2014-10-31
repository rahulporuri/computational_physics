
# initialize 2 dim matrix 100X100 - with zeros
# set one corner of this array 10X10 with particles, which we want to see evolving - with one
# particle positions shown with value 1 in the 2dim matrix to visualize easier!
# define function which will measure the interaction energy - lennard jones potential
# 
# md monte carlo - ising
# > one random number generator to choose a position in the matrix
#     then we check if its filled by a particle already, otherwise restart
#         another random number generator to move it somewhere in the matrix
#             check if this new position is filled
#                 if free, what is the energy difference?
#                     if -ve, flip
#                     else flip with probability
# 
# arena = np.zeros([12,12])
# for i in xrange(3):
#     for j in range(3):
#         arena[i,j] = 1
# 
# move_posn = np.arange(144)
# for i in xrange(10):
#     site = np.random.choice(move_posn)
#     if arena[site%12,site/12] = 1
#         tmp = np.random.random()
#         if arena[tmp%12,tmp/12] != 1
#             arena[site%12,site/12] = 0
#             arena[tmp%12,tmp/12] = 1
# 
# md monte carlo - taught
# > initial positions defined - [particle no., x, y] for n particles, boundary conditions defined
# > random number generator to choose a particle!
# > 2 random number generators to choose move in x and move in y,
# > if already filled, dont move
# > if not move! - hard balls
# """
# > if moved, change in energy?
# > if energy (final-energy)< 0; flip!
# > else: flip with probability exp(energy) - lennard jones potential.
# """
# np.zeros([n,2]) n - no. of particles, 2 x & y coordinates
# np.zeros([n,2,2])

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
"""
import time, time.time()
arena = np.zeros([100,100])
for i in xrange(10):
    for j in range(10):
        arena[i,j] = 1
plt.imshow(arena)
"""


# Out[1]:

#     '\narena = np.zeros([100,100])\nfor i in xrange(10):\n    for j in range(10):\n        arena[i,j] = 1\nplt.imshow(arena)\n'

# In[2]:

arena = np.zeros([12,12])
for i in xrange(3):
    for j in range(3):
        arena[i,j] = 1
plt.imshow(arena)
        
move_posn = np.arange(144)
for i in xrange(10):
    site = np.random.choice(move_posn)
    if arena[site%12,site/12] == 1 :
        tmp = np.random.choice(move_posn)
        if arena[tmp%12,tmp/12] != 1:
            arena[site%12,site/12] = 0
            arena[tmp%12,tmp/12] = 1


# Out[2]:

# image file:

# In[6]:

arena = np.zeros([12,12])
for i in xrange(3):
    for j in xrange(3):
        arena[i,j] = 1
        
#plt.imshow(arena)

move_posn = np.arange(144)
for i in xrange(100000):
    site = np.random.choice(move_posn)
    if (arena[site%12,site/12] == 1) :
        #print "yes! there's a ball at", site
        tmp = np.random.choice(move_posn)
        if (arena[tmp%12,tmp/12] != 1):
            #print "yes, you can move", site, "to", tmp
            arena[tmp%12, tmp/12] =1
            arena[site%12, site/12] =0


# In[7]:

print arena


# Out[7]:

#     [[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  1.]
#      [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  1.]
#      [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
#      [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
#      [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
#      [ 0.  0.  0.  0.  1.  0.  0.  0.  0.  0.  0.  0.]
#      [ 0.  0.  0.  0.  0.  0.  0.  0.  1.  0.  0.  0.]
#      [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
#      [ 0.  0.  0.  0.  0.  0.  0.  1.  0.  0.  0.  0.]
#      [ 0.  0.  0.  0.  0.  0.  0.  0.  1.  0.  0.  0.]
#      [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
#      [ 1.  0.  0.  0.  0.  1.  0.  0.  0.  1.  0.  0.]]
# 

# In[8]:

plt.imshow(arena)


# Out[8]:

#     <matplotlib.image.AxesImage at 0xb133ac2c>

# image file:

# In[ ]:




# In[93]:

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
arena = np.zeros([9,2])
for i in xrange(9):
    arena[i][1] = i%3
    arena[i][0] = i/3
print arena


# Out[93]:

#     [[ 0.  0.]
#      [ 0.  1.]
#      [ 0.  2.]
#      [ 1.  0.]
#      [ 1.  1.]
#      [ 1.  2.]
#      [ 2.  0.]
#      [ 2.  1.]
#      [ 2.  2.]]
# 

# In[94]:

x = []
y = []
for i in xrange(len(arena)):
    x.append(arena[i][0])
    y.append(arena[i][1])
plt.scatter(x,y)


# Out[94]:

#     <matplotlib.collections.PathCollection at 0xb00a20cc>

# image file:

# In[96]:

atom_list = np.arange(9)
disp = np.arange(99)
for iterations in xrange(10):
    atom = np.random.choice(atom_list)
    x = np.random.choice(disp)
    y = np.random.choice(disp)
    if arena[:].all() != np.array([x, y]).all():
        arena[atom] = np.array([x, y])


# In[97]:

print arena[:]
print len(arena)
x = []
y = []
for i in xrange(len(arena)):
    x.append(arena[i][0])
    y.append(arena[i][1])
print x,y
#plt.scatter(arena[:][0],arena[:][1])
plt.scatter(x,y);


# Out[97]:

#     [[ 27.  46.]
#      [ 86.   8.]
#      [ 29.  76.]
#      [ 13.  82.]
#      [  1.   1.]
#      [ 81.  86.]
#      [ 37.  22.]
#      [  2.   1.]
#      [  2.   2.]]
#     9
#     [27.0, 86.0, 29.0, 13.0, 1.0, 81.0, 37.0, 2.0, 2.0] [46.0, 8.0, 76.0, 82.0, 1.0, 86.0, 22.0, 1.0, 2.0]
# 

# image file:

# In[65]:

if arena[0].all() == np.array([1., 1.]).all():
    print "ohhyeah!!!"


# Out[65]:

#     ohhyeah!!!
# 

# In[72]:

if arena[:].all() != np.array([5.,5.]).all():
    print "ohhyeah!!!"


# Out[72]:

#     ohhyeah!!!
# 

# In[21]:

import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
from scipy.constants import N_A, nano, pico, m_p, k
#import scipy.spatial.distance as spd

atom_list = np.arange(900)
disp = np.arange(125)

a = 0.3405*nano
e = 119.8*k
beta = 1./np.power(10,3)
J = 0.5

def potential_e(site):
    #dist= np.zeros(len(atoms)-1)
    dist = []
    for i in xrange(len(arena)):
        #j = 0
        if i != site:
            temp = np.sqrt((arena[site][0]-arena[i][0])**2+(arena[site][0] - arena[i][1])**2)
            dist.append(temp)
            # temp = spd.euclidean(arena[i],arena[j])
            #j += 1
            #dist[j] = temp
    sum_u = 0
    for i in xrange(len(dist)):
        sum_u += ((a/dist[i])**12 - (a/dist[i])**6)*4*e
    
    return sum_u

arena = np.zeros([900,2])
for i in xrange(len(arena)):
    arena[i][1] = i%30
    arena[i][0] = i/30

sys_energy = []
accepted_moves = 0

for i in xrange(9000):
    to_move = np.random.choice(atom_list)
    pre_move_e = potential_e(to_move)
    new_x = np.random.choice(disp)
    new_y = np.random.choice(disp)
    old_posn = arena[to_move]
    arena[to_move] = np.array([new_x, new_y])
    post_move_e = potential_e(to_move)
    if post_move_e - pre_move_e < 0 :
        sys_energy.append(potential_e(to_move))
        accepted_moves += 1
    else :
        temp = np.random.random()
        if temp < np.exp(-beta*J*(post_move_e-pre_move_e)):
            sys_energy.append(potential_e(to_move))
            accepted_moves += 1
        else :
            sys_energy.append(potential_e(to_move))
            arena[to_move] = old_posn


# Out[21]:

#     -c:40: RuntimeWarning: divide by zero encountered in double_scalars
#     -c:40: RuntimeWarning: invalid value encountered in double_scalars
# 

# In[ ]:

import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[39]:

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

n = 100 # number of particles
# initializing the system
# the atoms occupy a square of size 10X10
system = np.zeros([n,2])
for i in xrange(len(system)):
    system[i][0] = i%10 # np.sqrt(n) wont work as it will return a float
    system[i][1] = i/10 # we need an integer denominator for this to work!

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
for time in xrange(5000):
    site = np.random.choice(np.arange(n)) # atom to be moved
    # this atom can now move in the range (-alpha,alpha) in x & y
    #xmove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    #ymove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    #xmove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    #ymove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    xmove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    ymove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    pre_move_e = local_energy(site)
    system[site] = system[site] + np.array([xmove,ymove])
    if system[site][0] > 100 :
        system[site][0] = system[site][0]%100
    #if system[site][0] < 0 :
    #    system[site][0] = system[site][0]%100
    if system[site][1] > 100 :
        system[site][1] = system[site][1]%100
    #if system[site][1] < 0 :
    #    system[site][1] = system[site][1]%100
    post_move_e = local_energy(site)
    if post_move_e - pre_move_e < 0:
        global_energy.append(system_energy())
        accepted_moves += 1
    else :
        temp = np.random.random()
        if temp < np.exp(-beta*(post_move_e - pre_move_e)):
            global_energy.append(system_energy())
            accepted_moves += 1
        else :
            system[site] = system[site] - np.array([xmove,ymove])
            global_energy.append(system_energy())
# we get global_energy, accepted moves as the outputs here.
plt.subplot(132)
alist = radial_number_density()
anarray = np.asarray(alist)
plt.hist(anarray,10);
plt.subplot(133)
plt.plot(global_energy)
print "accepted_moves", accepted_moves


# Out[39]:

#     accepted_moves 4425
# 

# image file:

# In[30]:

import scipy.spatial.distance as spd
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import numpy as np
import time
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

n = 900 # number of particles
# initializing the system
# the atoms occupy a square of size 10X10
system = np.zeros([n,2])
for i in xrange(len(system)):
    system[i][0] = i%30 # np.sqrt(n) wont work as it will return a float
    system[i][1] = i/30 # we need an integer denominator for this to work!

global_energy = []
accepted_moves = 0

#plt.subplot(131)
radial_dist_before = radial_number_density()
#anarray = np.asarray(alist)
#plt.hist(anarray,10);

T = 1.
# T = np.array([5.,5./2,1./1./2,1./10])
beta = 1./T
# B = 1./T
#for beta in B:
time_per_loop = []
for looptime in xrange(100):
    start_time = time.time()
    site = np.random.choice(np.arange(n)) # atom to be moved
    # this atom can now move in the range (-alpha,alpha) in x & y
    #xmove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    #ymove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    xmove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    ymove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    #xmove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    #ymove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    pre_move_e = local_energy(site)
    system[site] = system[site] + np.array([xmove,ymove])
    if system[site][0] > 100 :
        system[site][0] = system[site][0]%100
    #if system[site][0] < 0 :
    #    system[site][0] = system[site][0]%100
    if system[site][1] > 100 :
        system[site][1] = system[site][1]%100
    #if system[site][1] < 0 :
    #    system[site][1] = system[site][1]%100
    post_move_e = local_energy(site)
    if post_move_e - pre_move_e < 0:
        global_energy.append(system_energy())
        accepted_moves += 1
        #print "yes"
    else :
        temp = np.random.random()
        if temp < np.exp(-beta*(post_move_e - pre_move_e)):
            global_energy.append(system_energy())
            accepted_moves += 1
            #print "barely yes"
        else :
            system[site] = system[site] - np.array([xmove,ymove])
            global_energy.append(system_energy())
            #print "nyooo!!!!"
    print "we're done with the mc loop %f" % (time.time()-start_time)
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


# Out[30]:

#     accepted_moves 353
# 

# image file:

# In[31]:

plt.subplot(121)
anarray = np.asarray(radial_dist_before)
plt.hist(anarray,10);
plt.subplot(122)
anotherarray = np.asarray(radial_dist_after)
plt.hist(anotherarray,10);


# Out[31]:


    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)

    <ipython-input-31-f0c3674573dd> in <module>()
          1 plt.subplot(121)
    ----> 2 anarray = np.asarray(radial_dist_before)
          3 plt.hist(anarray,10);
          4 plt.subplot(122)
          5 anotherarray = np.asarray(radial_dist_after)


    NameError: name 'radial_dist_before' is not defined


# image file:

# In[ ]:

plt.plot(global_energy)


# In[32]:

x = []
y = []
for i in xrange(len(system)):
    x.append(system[i][0])
    y.append(system[i][1])
plt.scatter(x,y);


# Out[32]:

# image file:

# In[ ]:



