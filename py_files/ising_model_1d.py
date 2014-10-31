
# In[2]:

import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[5]:

#lattice = np.ones(200) # initializing the lattice with all ones
lattice = np.zeros(200) # initializing the lattice randomly
for i in xrange(200):
    temp = np.random.random()
    if temp > 1./2:
        lattice[i] = 1
    else :
        lattice[i] = -1

# defines the local energy i.e product of neighbor spins.
# used to compare the change in energy before and after a flip
# with the boundary condition that the 0th spin is coupled to the nth spin
def energy_local(site):
    if site == 0:
        return - lattice[0]*lattice[1] - lattice[0]*lattice[-1]
    elif site == len(lattice)-1 :
        return - lattice[len(lattice)-1]*lattice[len(lattice)-2] - lattice[len(lattice)-1]*lattice[0]
    else :
        return - lattice[site]*lattice[site-1] - lattice[site]*lattice[site+1]

# computes the total energy of the system i.e sum of products of all spins
# assuming J = 1
def global_energy():
    temp = 0
    for i in xrange(len(lattice)-1):
        temp += -(lattice[i-1]*lattice[i]+lattice[i]*lattice[i+1])
    return (1./2)*temp/len(lattice)

# computing the total magnetization i.e the sum of all spins in the lattice
def global_magnetization():
    return np.sum(lattice)/len(lattice)

T = np.array([5,5./2,1,1./2,2./10])
betaJ = 1./T
for bJ in betaJ:
    plt.hold(True)
    plt.legend(loc='upper center')
    global_e = []
    global_e.append(global_energy())                         # the initial system energy
    magnetization = []
    magnetization.append(global_magnetization())             # the initial system magnetization
    accepted_moves = 0
    for i in xrange(50000):
        site = np.random.choice(np.linspace(0,199,200))      # choose a site randomly from the lattice
        pre_flip_e = energy_local(site)                      # compute local energy before flip
        lattice[site] = -lattice[site]  
        post_flip_e = energy_local(site)                     # compute local energy after flip
        if post_flip_e - pre_flip_e < 0:
            global_e.append(global_energy())                 # update the system energy at this step
            accepted_moves += 1
            magnetization.append(global_magnetization())     # update the system magnetization at this step
        else :
            temp = np.random.random()
            if temp < np.exp(-bJ*(post_flip_e - pre_flip_e)):
                global_e.append(global_energy())
                accepted_moves += 1
                magnetization.append(global_magnetization())
            else :
                lattice[site] = -lattice[site]               # reverse the flip to initial state if the transition isnt valid
                global_e.append(global_energy())
                magnetization.append(global_magnetization())
    print "accepted_moves", accepted_moves, "temperature", 1./bJ
    plt.subplot(121)
    plt.plot(global_e,label=1./bJ)
    plt.subplot(122)
    plt.plot(magnetization,label=1./bJ)


# Out[5]:

#     accepted_moves 40025 temperature 5.0
#     accepted_moves 30828 temperature 2.5
#     accepted_moves 11615 temperature 1.0
#     accepted_moves 3051 temperature 0.5
#     accepted_moves 1822 temperature 0.2
# 

# image file:

# In[3]:

#lattice = np.ones(200) # initializing the lattice with all ones
lattice = np.zeros(200) # initializing the lattice randomly
for i in xrange(200):
    temp = np.random.random()
    if temp > 1./2:
        lattice[i] = 1
    else :
        lattice[i] = -1

# defines the local energy i.e product of neighbor spins.
# used to compare the change in energy before and after a flip
# with the boundary condition that the 0th spin is coupled to the nth spin
def energy_local(site):
    if site == 0:
        return - lattice[0]*lattice[1] - lattice[0]*lattice[-1]
    elif site == len(lattice)-1 :
        return - lattice[len(lattice)-1]*lattice[len(lattice)-2] - lattice[len(lattice)-1]*lattice[0]
    else :
        return - lattice[site]*lattice[site-1] - lattice[site]*lattice[site+1]

# computes the total energy of the system i.e sum of products of all spins
# assuming J = 1
def global_energy():
    temp = 0
    for i in xrange(len(lattice)-1):
        temp += -(lattice[i-1]*lattice[i]+lattice[i]*lattice[i+1])
    return (1./2)*temp/len(lattice)

# computing the total magnetization i.e the sum of all spins in the lattice
def global_magnetization():
    return np.sum(lattice)/len(lattice)

T = np.array([5,5./2,1,1./2,2./10])
betaJ = 1./T
for bJ in betaJ:
    plt.hold(True)
    plt.legend(loc='upper center')
    global_e = []
    global_e.append(global_energy())                             # the initial system energy
    magnetization = []
    magnetization.append(global_magnetization())                 # the initial system magnetization
    accepted_moves = 0
    for step in xrange(1000):
        for mcsweep in xrange(200):                              
            site = np.random.choice(np.linspace(0,199,200))      # choose a site randomly from the lattice
            pre_flip_e = energy_local(site)                      # compute local energy before flip
            lattice[site] = -lattice[site]  
            post_flip_e = energy_local(site)                     # compute local energy after flip
            if post_flip_e - pre_flip_e < 0:
    #            global_e.append(global_energy())                # update the system energy at this step
                accepted_moves += 1
    #            magnetization.append(global_magnetization())    # update the system magnetization at this step
            else :
                temp = np.random.random()
                if temp < np.exp(-bJ*(post_flip_e - pre_flip_e)):
    #                global_e.append(global_energy())
                    accepted_moves += 1
    #                magnetization.append(global_magnetization())
                else :
                    lattice[site] = -lattice[site]               # reverse the flip to initial state if the transition isnt valid
    #                global_e.append(global_energy())
    #                magnetization.append(global_magnetization())
        global_e.append(global_energy())
        magnetization.append(global_magnetization())
    print "accepted_moves", accepted_moves, "temperature", 1./bJ
    plt.subplot(131)
    plt.plot(global_e,label=1./bJ)
    plt.subplot(132)
    plt.plot(magnetization,label=1./bJ)
    # to measure the auto-correlation of magnetization or correlation time!
    tmax = len(magnetization) # the total number of iterations
    chi = []
    for t in xrange(1,100): # the upper limit of the range should be ~1/2 of that of tmax!
        # first term in the equation
        temp = 0
        for tprime in xrange(tmax-t):
            temp += magnetization[tprime]*magnetization[tprime+t]
        temp = (1./(tmax-t))*temp
        # second term in the equation
        temp1 = 0
        for tprime in xrange(tmax-t):
            temp1 += magnetization[tprime]
        temp2 = 0
        for tprime in xrange(tmax-t):
            temp2 += magnetization[tprime+t]
        tempo = (1./((tmax-t)**2))*temp1*temp2
        chi.append(temp-tempo)
    plt.subplot(133)
    plt.plot(chi,label=1./bJ)


# Out[3]:

#     accepted_moves 160425 temperature 5.0
#     accepted_moves 123831 temperature 2.5
#     accepted_moves 49086 temperature 1.0
#     accepted_moves 8315 temperature 0.5
#     accepted_moves 4330 temperature 0.2
# 

#     /usr/local/lib/python2.7/dist-packages/matplotlib/axes/_axes.py:475: UserWarning: No labelled objects found. Use label='...' kwarg on individual plots.
#       warnings.warn("No labelled objects found. "
# 

# image file:

# In[4]:

plt.plot(magnetization,label=1./bJ)
plt.legend(loc='upper right')
#plt.xticks([])


# Out[4]:

#     <matplotlib.legend.Legend at 0xb13acd8c>

# image file:

# In[37]:

#t = 10 # we need to iterate over this 
tmax = len(magnetization) # the total number of iterations
chi = []
import time
start_time = time.time()
for t in xrange(1,100): # the upper limit of the range should be ~1/2 of that of tmax!
    # first term in the equation
    temp = 0
    for tprime in xrange(tmax-t):
        temp += magnetization[tprime]*magnetization[tprime+t]
    temp = (1./(tmax-t))*temp
    # second term in the equation
    temp1 = 0
    for tprime in xrange(tmax-t):
        temp1 += magnetization[tprime]
    temp2 = 0
    for tprime in xrange(tmax-t):
        temp2 += magnetization[tprime+t]
    tempo = (1./((tmax-t)**2))*temp1*temp2
    chi.append(temp-tempo)
plt.plot(np.asarray(chi)-110,label='old method')
print time.time()-start_time


# Out[37]:

#     0.316520929337
# 

# image file:

# #t = 10 # we need to iterate over this 
# tmax = len(magnetization) # the total number of iterations
# chi = []
# import time
# start_time = time.time()
# for t in xrange(1,100): # the upper limit of the range should be ~1/2 of that of tmax!
#     # first term in the equation
#     temp = 0
#     for tprime in xrange(tmax-t):
#         temp += magnetization[tprime]*magnetization[tprime+t]
#     temp = (1./(tmax-t))*temp
#     # second term in the equation
#     temp1 = 0
#     for tprime in xrange(tmax-t):
#         temp1 += magnetization[tprime]
#     temp2 = 0
#     for tprime in xrange(tmax-t):
#         temp2 += magnetization[tprime+t]
#     tempo = (1./((tmax-t)**2))*temp1*temp2
#     chi.append(temp-tempo)
# plt.hold(True)
# plt.plot(np.asarray(chi)-110,label='old method')
# print time.time()-start_time
# chi = []
# start_time = time.time()
# for t in xrange(1,100): # the upper limit of the range should be ~1/2 of that of tmax!
#     # first term in the equation
#     #temp = 0
#     temp_array_1 = np.asarray(magnetization[0:tmax-t])
#     temp_array_2 = np.asarray(magnetization[t-1:tmax-1])
#     temp = (1./(tmax-t))*np.sum(temp_array_1*temp_array_2)
#     # second term in the equation
#     #temp1 = 0
#     temp_array = np.asarray(magnetization[0:tmax-t])
#     temp = (1./(tmax-t))*np.sum(temp_array)
#     #temp2 = 0
#     temp_array = np.asarray(magnetization[t-1:tmax-1])
#     temp2 = (1./(tmax-t))*np.sum(temp_array)
#     tempo = temp1*temp2
#     chi.append(temp-tempo)
# print time.time()-start_time
# plt.plot(chi,label='new method')
# plt.legend(loc='upper right')
