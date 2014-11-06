
# This code will simulate the ising model in one dimension using the monte carlo method.
# 
# Written by Poruri Sai Rahul
# 
# Added comments on 6 Nov 2014

# Theory
# =======
# 
# The ising model is a theoretical model used to understand the interactions of spins and a 1-d ising model, as the name suggests is a system of spins arranged in a 1-dimensional chain or string. There are different kinds of coupling in literature and for the sake of our simulations here, we will only look at the nearest neighbor interaction i.e any spin in the string can only interact with it's neighbors on the left and the right. The hamiltonian of the system can be written as 
# 
# $$H = \Sigma_{i!=j} J_{i,j} S_i S_j$$
# 
# where J is the strength of the interaction between adjacent spins. One other assumption we make in our simulations is that the spins are discrete and not continuous i.e the spins can only take values +1 or -1 or pointing upwards or downwards. We also assume that the interaction term $J_{i,j}$ is the same for all spins, making the hamiltonian
# 
# $$H = J \Sigma_{i!=j} S_i S_j$$
# 
# The following simulations study the equilibrium conditions of a 1-dim ising model of various sizes and at various temperatures. The equilibrium conditions of the model are arrived at using monte carlo simulations. In a a monte carlo (mc hereforth) of the ising model, we choose a spin site randomly from the string of spins and flip it. Well, we choose to flip it with a probability depending on the energy of the post-flip state. Assuming we flip the spin, we measure the energy of the post-flip state. If the flip will decrease the energy of the system, then we probability of the flip is 1. Otherwise, the probability of the flip is $exp(-\beta \Delta E)$ where $\beta$ is $1/k_bT$ and $\Delta E$ is the change in energy before and after flip.b

# Code
# =====
# 
# There are multiple instances of monte carlo code below. The first one is a preliminary look at how the system energy and magnetization change over monte carlo steps for various values of temperature. The second one repeats the first step increasing the number of monte carlo iterations and making the use of monte carlo sweep to measure system energy and system magnetization for fewer instances. We also measure the auto-correlation function of magnetization here. Finally, we look at how the system size itself will manifest as change in average value of magnetization and in the auto-correlation function of the same.
# 
# *NOTE: The average value of magnetization isnt zero, as it is supposed to be and the auto-correlation function is giving negative values, which doesnt make sense! need to debug!*

# Structure
# ======
# 
# We first initialize the lattice or system, either with uniform spins or random spins. We have defined functions that take lattice as input and measure the system energy & magnetization. And then we have the main monte carlo loop where we choose a spin from the lattice and see what the probability of flipping it is, depending on what the post flip energy is. At the end of the mc loop, we also measured the auto-correlation function of magnetization.

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[5]:

#lattice = np.ones(200) # initializing a uniform lattice
lattice = np.zeros(200) # initializing a random lattice
for i in xrange(200):
    temp = np.random.random()
    if temp > 1./2:
        lattice[i] = 1
    else :
        lattice[i] = -1

# function that initializes a lattice of size i with random values
def initialize(i):
    lattice = np.zeros(i)
    for i in xrange(len(lattice)):
        temp = np.random.random()
        if temp > 1./2:
            lattice[i] = +1
        if temp < 1./2:
            lattice[i] = -1
    
# defines the local energy i.e product of neighbor spins.
# used to compare the change in energy before and after a flip
# the boundary condition is that the 0th spin is coupled to the nth spin
def energy_local(site):
    if site == 0:
        return lattice[0]*lattice[1] - lattice[0]*lattice[-1]
    # we dont actually need to specify the condition for 0 because in numpy arrays
    # array[-1] is the same as array[n-1] where n is the length of the array.
    elif site == len(lattice)-1 :
        return lattice[len(lattice)-1]*lattice[len(lattice)-2] - lattice[len(lattice)-1]*lattice[0]
    else :
        return lattice[site]*lattice[site-1] - lattice[site]*lattice[site+1]

# computes the total energy of the system i.e sum of products of all spins
# assuming J = 1 and nearest neighbor coupling
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
# we intend to study the system behavior at different temperatures
# therefore, we keep J constant at 1 and scale the value of $\beta$ as that of $1./T$
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
        for mcsweep in xrange(200):                              # an mcsweep is the n number of iterations, n = system size
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
    # to plot the auto-correlation function using magnetization
    tmax = len(magnetization) # the total number of iterations
    chi = []
    for t in xrange(1,100): # the upper limit of the range should be ~1/2 of that of tmax!
        # first term in the equation
        temp = 0
        for tprime in xrange(tmax-t):
            temp += magnetization[tprime]*magnetization[tprime+t]
        temp = (1./(tmax-t))*temp
        # second term in the equation
        # it was mentioned that this second term is not necessary.
        # it is a correction for mean value!
        temp1 = 0
        for tprime in xrange(tmax-t):
            temp1 += magnetization[tprime]
        temp2 = 0
        for tprime in xrange(tmax-t):
            temp2 += magnetization[tprime+t]
        tempo = (1./((tmax-t)**2))*temp1*temp2
        # auto-correlation function value
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

# In[ ]:

# two different ways to measure the auto-correlation function
# first way by summing elements using for loops
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
    # auto-correlation function value
    chi.append(temp-tempo)
plt.hold(True)
plt.plot(np.asarray(chi)-110,label='old method')
print time.time()-start_time
# second way by summing elements using numpy.sum and some array manipulation
chi = []
start_time = time.time()
for t in xrange(1,100): # the upper limit of the range should be ~1/2 of that of tmax!
    # first term in the equation
    #temp = 0
    temp_array_1 = np.asarray(magnetization[0:tmax-t])
    temp_array_2 = np.asarray(magnetization[t-1:tmax-1])
    temp = (1./(tmax-t))*np.sum(temp_array_1*temp_array_2)
    # second term in the equation
    #temp1 = 0
    temp_array = np.asarray(magnetization[0:tmax-t])
    temp = (1./(tmax-t))*np.sum(temp_array)
    #temp2 = 0
    temp_array = np.asarray(magnetization[t-1:tmax-1])
    temp2 = (1./(tmax-t))*np.sum(temp_array)
    tempo = temp1*temp2
    # auto-correlation function value
    chi.append(temp-tempo)
print time.time()-start_time
plt.plot(chi,label='new method')
plt.legend(loc='upper right')


# In[54]:

#lattice = np.ones(200) # initializing the lattice with all ones
#lattice = np.zeros(200) # initializing the lattice randomly
#for i in xrange(200):
#    temp = np.random.random()
#    if temp > 1./2:
#        lattice[i] = 1
#    else :
#        lattice[i] = -1

def initialize(i):
    lattice = np.zeros(i)
    for i in xrange(i):
        temp = np.random.random()
        if temp > 1./2:
            lattice[i] = 1
        else :
            lattice[i] = -1
    return lattice
        
# defines the local energy i.e product of neighbor spins.
# used to compare the change in energy before and after a flip
# with the boundary condition that the 0th spin is coupled to the nth spin
def energy_local(site):
    if site == 0:
        return lattice[0]*lattice[1] - lattice[0]*lattice[-1]
    elif site == len(lattice)-1 :
        return lattice[len(lattice)-1]*lattice[len(lattice)-2] - lattice[len(lattice)-1]*lattice[0]
    else :
        return lattice[site]*lattice[site-1] - lattice[site]*lattice[site+1]
    
#def energy_local(site):
#    if site == len(lattice)-1:
#        return lattice[i]*lattice[i-1] + lattice[i]*lattice[0]
#    else :
#        return lattice[i]*lattice[i-1] + lattice[i]*lattice[i+1]

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

#T = np.array([5,5./2,1,1./2,2./10])
#betaJ = 1./T
T = 1./2
bJ = 1./T
for i in [10,50,100,200]:
#for bJ in betaJ:
    plt.hold(True)
    plt.legend(loc='upper center')
    lattice = initialize(i)
    global_e = []
    global_e.append(global_energy())                             # the initial system energy
    magnetization = []
    magnetization.append(global_magnetization())                 # the initial system magnetization
    accepted_moves = 0
    for step in xrange(100):
        for mcsweep in xrange(i):                              
            site = np.random.choice(np.arange(i))      # choose a site randomly from the lattice
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
    print i, np.mean(global_e), np.mean(magnetization), np.var(global_e), np.var(magnetization)
    plt.subplot(131)
    plt.plot(global_e,label=1./bJ)
    plt.subplot(132)
    plt.plot(magnetization,label=1./bJ)
    # to measure the auto-correlation of magnetization or correlation time!
    tmax = len(magnetization) # the total number of iterations
    chi = []
    for t in xrange(1,i/10): # the upper limit of the range should be ~1/2 of that of tmax!
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
    plt.plot(chi,label=i)


# Out[54]:

#     accepted_moves 688 temperature 0.5
#     10 -0.00792079207921 0.0574257425743 0.0967689442212 0.106405254387
#     accepted_moves 3706 temperature 0.5
#     50 -0.0166336633663 0.0134653465347 0.0213629252034 0.0193671992942
#     accepted_moves 7513 temperature 0.5
#     100 -0.00811881188119 -0.00633663366337 0.00815784726988 0.0125222233114
#     accepted_moves 14990 temperature 0.5
#     200 0.00128712871287 0.00128712871287 0.00561616508185 0.00571418488383
# 

# image file:

# In[53]:

np.mean(global_e), np.mean(magnetization)


# Out[53]:

#     (0.02772277227722772, -0.023762376237623763)

# In[44]:

lattice[site]*lattice[site-1] + lattice[site]*lattice[site+1]


# Out[44]:

#     0.0

# In[28]:

for sites in xrange(len(lattice)):
    print sites, energy_local(sites)


# Out[28]:

#     0 0.0
#     1 0.0
#     2 2.0
#     3 -2.0
#     4 2.0
#     5 0.0
#     6 0.0
#     7 0.0
#     8 0.0
#     9 -2.0
# 

# In[33]:

#for i in xrange(len(lattice)-1):
    #print lattice[i]*lattice[i-1] + lattice[i]*lattice[i+1]
def energy_temp(site):
    if site == len(lattice)-1:
        return lattice[i]*lattice[i-1] + lattice[i]*lattice[0]
    else :
        return lattice[i]*lattice[i-1] + lattice[i]*lattice[i+1]
for i in xrange(len(lattice)-1):
    print i, energy_temp(i)


# Out[33]:

#     0 2.0
#     1 2.0
#     2 0.0
#     3 0.0
#     4 0.0
#     5 -2.0
#     6 -2.0
#     7 -2.0
#     8 -2.0
# 

# In[37]:

i = 10
print np.arange(i)


# Out[37]:

#     [0 1 2 3 4 5 6 7 8 9]
# 

# In[ ]:



