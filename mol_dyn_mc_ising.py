
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

# In[2]:

import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
"""
arena = np.zeros([100,100])
for i in xrange(10):
    for j in range(10):
        arena[i,j] = 1
plt.imshow(arena)
"""


# Out[2]:

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

# In[88]:

arena[i][0]


# Out[88]:

#     36.0

# In[ ]:




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

# In[75]:

arena[0] = np.array([0.,0.])
print arena


# Out[75]:

#     [[ 4.  4.]
#      [ 0.  1.]
#      [ 0.  2.]
#      [ 1.  0.]
#      [ 1.  1.]
#      [ 1.  2.]
#      [ 2.  0.]
#      [ 2.  1.]
#      [ 2.  2.]]
# 

# In[23]:

import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
from scipy.constants import N_A, nano, pico, m_p, k

arena = np.zeros([900,2])
for i in xrange(len(arena)):
    arena[i][1] = i%30
    arena[i][0] = i/30
#print arena

atom_list = np.arange(900)
disp = np.arange(125)

#atoms = np.zeros([100,2])

#sites = np.linspace(0,99,100)

sys_energy = []
accepted_moves = 0

a = 0.3405*nano
e = 119.8*k

beta = 1./np.power(10,3)
J = 0.5

def potential_e(site):
    #dist= np.zeros(len(atoms)-1)
    dist = []
    for i in xrange(len(arena)):
        j = 0
        if i != site:
            temp = np.sqrt((arena[site][0]-arena[i][0])**2+(arena[site][0] - arena[i][1])**2)
            dist.append(temp)
            #j += 1
            #dist[j] = temp
    sum_u = 0
    for i in xrange(len(dist)):
        sum_u += ((a/dist[i])**12 - (a/dist[i])**6)*4*e
    
    return sum_u

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
        if temp < np.exp(beta*J*(post_move_e-pre_move_e)):
            sys_energy.append(potential_e(to_move))
            accepted_moves += 1
        else :
            sys_energy.append(potential_e(to_move))
            arena[to_move] = old_posn


# In[20]:

#print arena[:]
#print len(arena)
x = []
y = []
for i in xrange(len(arena)):
    x.append(arena[i][0])
    y.append(arena[i][1])
#print x,y
#plt.scatter(arena[:][0],arena[:][1])
plt.scatter(x,y);


# Out[20]:

# image file:

# In[21]:

plt.plot(sys_energy)


# Out[21]:

#     [<matplotlib.lines.Line2D at 0xae9d852c>]

# image file:

# In[22]:

accepted_moves


# Out[22]:

#     7456

# In[24]:

import time


# In[25]:

time.time()


# Out[25]:

#     1412010480.468961

# In[27]:

time.time()


# Out[27]:

#     1412010499.052519

# In[29]:

import IPython
IPython.__version__


# Out[29]:

#     '1.2.1'

# In[ ]:



