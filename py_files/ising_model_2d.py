
# Refer to ising_model_1d for a brief introduction to the theory behind the ising model and what the monte carlo methods are. Here, we shall implement the ising model in a 2-dim lattice i.e spins are arranged in a uniform 2-dim grid pattern and given our dependence on nearest neighbor interaction, each spin has 4 neighbors with which it can interact.
# 
# Before we go ahead with the 2-dim ising model study, here's an overview of different random number generators that come as standard in a python installation. Refer to the docs [here][https://docs.python.org/2/library/random.html]. Given that the random number generator is at the heart of a monte-carlo simulation, the library or function we should be sufficiently *random*. For instance, we look at the performance of the functions numpy.random.random and numpy.random.uniform from the library random below

# In[11]:

import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
plt.ion()

x = []
for i in xrange(10000):
    tmp = np.random.random()
    # np.random.random() will generate a random number between 0 & 1
    x.append(tmp)

plt.hist(x,100);

y = []
for i in xrange(10000):
    tmp = np.random.uniform(0,1)
    # np.random.uniform(a,b) will generate random numbers in the range a,b 
    y.append(tmp)

print "the mean of the random.random output is", np.mean(x), "\n" "the variance of the random.random output is", np.var(x), "\n" "the mean of the random.uniform output is", np.mean(y), "\n" "the variance of the random.uniform output is", np.var(y)
    
plt.subplot(121)
plt.hist(x,100);
plt.subplot(122)
plt.hist(y,100);


# Out[11]:

#     the mean of the random.random output is 0.508082509051 
#     the variance of the random.random output is 0.0828779728855 
#     the mean of the random.uniform output is 0.50030226968 
#     the variance of the random.uniform output is 0.0824666758476
# 

# image file:

# Had the functions np.random.random() and np.random.uniform(0,1) been perfect random number generators, all of the histograms would've had the same height. Maybe if i generate more random numbers, more than 10,000, we might see a difference. *need to check this*. We can also see that the function np.random.uniform(0,1) is performing better than np.random.random() generating a mean close to 0.5. *how should the variance look for a perfect random number generator?*

# In[94]:

array = np.arange(144)
a = []
for i in xrange(14400):
    tmp = np.random.choice(array)
    # picks an element at random from the input array
    a.append(tmp)
plt.hist(a,144);


# Out[94]:

# image file:

# Now, to get started with the actual 2-dim ising model study, the structure of the code is very similar to that of the ising_model_1d. There are functions that measure the global energy of the lattice, global magnetization of the lattice which are what we want to study. There is a function to measure the local energy i.e sum_neighbors which measures the interaction energy of a spin at site i.

# In[2]:

import numpy as np
import matplotlib.pyplot as plt
import time
get_ipython().magic(u'matplotlib inline')

#---> global energy of the lattice
def global_energy(lattice):
    temp = 0
    for i in xrange(-1,len(lattice)-1):
        temp += np.sum(lattice[i,:]*lattice[i+1,:]) # need to take into account the 0th and nth rows
    for j in xrange(-1,len(lattice)-1):
        temp += np.sum(lattice[:,j]*lattice[:,j+1]) # need to take into account the 0th and nth columns
    return -bJ*temp/(len(lattice)**2)
    #return -bJ*temp

def global_magnetization(lattice):
    return np.sum(lattice)/(len(lattice)**2)
    
#---> function to sum the interaction energy b/w nearest neighbors
#def sum_neighbors(array, site):
	#var = len(array)
    #if site < var*(var-1) :
	#	return -(array[(site-1)%var, site/var]*array[site%var, site/var] + array[(site+1)%var, site/var]*array[site%var, site/var] + array[site%var, site/var-1]*array[site%var, site/var] + array[site%var, site/var + 1]*array[site%var, site/var])
	#if site > var*(var-1)-1:
		#site = 143-site
		#return -(array[(site-1)%var, site/var]*array[site%var, site/var] + array[(site+1)%var, site/var]*array[site%var, site/var] + array[site%var, site/var-1]*array[site%var, site/var] + array[site%var, site/var + 1]*array[site%var, site/var])

def sum_neighbors(array,site):
    var = len(array)
    if site < var*(var-1):
        #return site
        return -(array[(site-1)%var, site/var]*array[site%var, site/var] + array[(site+1)%var, site/var]*array[site%var, site/var] + array[site%var, (site/var)-1]*array[site%var, site/var] + array[site%var, site/var + 1]*array[site%var, site/var])
    if site > var*(var-1)-1:
        #return site
        #site = (var**2-1)-site
        return -(array[(site-1)%var, site/var]*array[site%var, site/var] + array[(site+1)%var, site/var]*array[site%var, site/var] + array[site%var, (site/var)-1]*array[site%var, site/var] + array[site%var, 0]*array[site%var, site/var])


# In[2]:

#lattice = np.ones([12,12]) for a uniform start
n = 24
lattice = np.zeros([n,n])
for i in xrange(len(lattice)):
	for j in xrange(len(lattice)):
		tmp = np.random.random()
		if tmp > 1./2:
			lattice[i,j] = +1
		elif tmp < 1./2:
			lattice[i,j] = -1
            
# function to initialize the 2-dim lattice of spins, randomly in this case.
#def initilaize(n):
    #lattice = np.zeros([n,n])
    #for i in xrange(len(lattice)):
        #for j in xrange(len(lattice)):
         #   tmp = np.random.random()
        #    if tmp > 1./2:
       #         lattice[i,j] = +1
      #      elif tmp < 1./2:
     #           lattice[i,j] = -1
    #return lattice   
            
#plt.imshow(lattice,cmap='gist_gray_r')
flip_posn = np.arange(n**2)
# let's assume J = 1
T = np.array([5,5./2,1,1./2,1./10])
#T = np.array([1./2])
betaJ = 1./T
for bJ in betaJ:
    plt.hold(True)
    plt.legend(loc='upper right')
    successful_flip = 0
    misfire = 0
    global_e = []
    global_e.append(global_energy(lattice))
    magnetization = []
    magnetization.append(global_magnetization(lattice))
    for i in xrange(50000):
        site = np.random.choice(flip_posn)
        #print "site to flip", site, "x,y", site%12, site/12
        pre_flip_e = sum_neighbors(lattice,site)
        #print initial_e
        lattice[site%n,site/n] = -lattice[site%n,site/n]
        post_flip_e = sum_neighbors(lattice,site)
        #print final_e
        #print np.exp()
        if post_flip_e - pre_flip_e < 0:
        #    print "flip!"
            successful_flip += 1
            global_e.append(global_energy(lattice))
            magnetization.append(global_magnetization(lattice))
        else :
            tmp = np.random.random()
            if tmp < np.exp(-bJ*(post_flip_e-pre_flip_e)):
        #        print "flip!"
                successful_flip += 1
                global_e.append(global_energy(lattice))
                magnetization.append(global_magnetization(lattice))
            else:
                lattice[site%n,site/n] = -lattice[site%n,site/n]
        #        print "no flip!"
                misfire += 1
                global_e.append(global_energy(lattice))
                magnetization.append(global_magnetization(lattice))
    print "succesful flips", successful_flip, "temp", 1./bJ
    #plt.ylim([0,1.2])
    plt.subplot(121)
    plt.plot(global_e,label=1./bJ)
    plt.subplot(122)
    plt.plot(magnetization,label=1./bJ)


# Out[2]:

#     succesful flips 34313  5.0
#     succesful flips 18064  2.5
#     succesful flips 2994  1.0
#     succesful flips 449  0.5
#     succesful flips 0  0.1
# 

#     /usr/lib/pymodules/python2.7/matplotlib/axes.py:4747: UserWarning: No labeled objects found. Use label='...' kwarg on individual plots.
#       warnings.warn("No labeled objects found. "
# 

# image file:

# Unlike the previous case where we just ran the system for 50,000 monte carlo time steps and measured system energy and magnetization at each of these steps, here we run 100 monte carlo sweeps where 1 monte carlo sweep is n squared monte carlo time steps and we only measure the system energy and magnetization at each mc sweep. This is a convention, one that is convenient given that the system energy and magnetization don't change by a large value with each mc time step giving us leniancy in measuring system variables.

# In[4]:

#lattice = np.ones([12,12])
#---> random start
n = 24
lattice = np.zeros([n,n])
for i in xrange(len(lattice)):
	for j in xrange(len(lattice)):
		tmp = np.random.random()
		if tmp > 1./2:
			lattice[i,j] = +1
		elif tmp < 1./2:
			lattice[i,j] = -1

#plt.imshow(lattice,cmap='gist_gray_r')
flip_posn = np.arange(n**2)
# let's assume J = 1
T = np.array([5,5./2,1,1./2,1./10])
#T = np.array([1./2])
betaJ = 1./T
for bJ in betaJ:
    plt.hold(True)
    plt.legend(loc='upper right')
    successful_flip = 0
    misfire = 0
    global_e = []
    global_e.append(global_energy(lattice))
    magnetization = []
    magnetization.append(global_magnetization(lattice))
    for i in xrange(100):
        for mcsweep in xrange(n**2):
            site = np.random.choice(flip_posn)
            #print "site to flip", site, "x,y", site%12, site/12
            pre_flip_e = sum_neighbors(lattice,site)
            #print initial_e
            lattice[site%n,site/n] = -lattice[site%n,site/n]
            post_flip_e = sum_neighbors(lattice,site)
            #print final_e
            #print np.exp()
            if post_flip_e - pre_flip_e < 0:
            #    print "flip!"
                successful_flip += 1
#                global_e.append(global_energy(lattice))
#                magnetization.append(global_magnetization(lattice))
            else :
                tmp = np.random.random()
                if tmp < np.exp(-bJ*(post_flip_e-pre_flip_e)):
            #        print "flip!"
                    successful_flip += 1
#                    global_e.append(global_energy(lattice))
#                    magnetization.append(global_magnetization(lattice))
                else:
                    lattice[site%n,site/n] = -lattice[site%n,site/n]
            #        print "no flip!"
                    misfire += 1
        global_e.append(global_energy(lattice))
        magnetization.append(global_magnetization(lattice))
    print "succesful flips", successful_flip, "temp", 1./bJ
    #plt.ylim([0,1.2])
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


# Out[4]:

#     succesful flips 39650 temp 5.0
#     succesful flips 20174 temp 2.5
#     succesful flips 2683 temp 1.0
#     succesful flips 668 temp 0.5
#     succesful flips 0 temp 0.1
# 

# image file:

# We also measured the auto-correlation function of magnetization and plotted it to get a sense of correlation time of the system. *Auto correlation function shouldn't have negative values and i need to check the code that measures this!*

# In[11]:

# checking the neighbors!s
for site in xrange(len(flip_posn)):
    n = len(lattice)
    if site<n*(n-1):
        print "site", site%n, site/n, "left of site", (site-1)%n, site/n, "right of site", (site+1)%n, site/n, "top of site", (site)%n, (site+n)/n, "bottom of site", (site)%n, (site-n)/n
    if site > n*(n-1)-1:
        print "site", site%n, site/n, "left of site", (site-1)%n, site/n, "right of site", (site+1)%n, site/n, "top of site", (site)%n, 0, "bottom of site", (site)%n, (site-n)/n


# Out[11]:

#     site 0 0 left of site 23 0 right of site 1 0 top of site 0 1 bottom of site 0 -1
#     site 1 0 left of site 0 0 right of site 2 0 top of site 1 1 bottom of site 1 -1
#     site 2 0 left of site 1 0 right of site 3 0 top of site 2 1 bottom of site 2 -1
#     site 3 0 left of site 2 0 right of site 4 0 top of site 3 1 bottom of site 3 -1
#     site 4 0 left of site 3 0 right of site 5 0 top of site 4 1 bottom of site 4 -1
#     site 5 0 left of site 4 0 right of site 6 0 top of site 5 1 bottom of site 5 -1
#     site 6 0 left of site 5 0 right of site 7 0 top of site 6 1 bottom of site 6 -1
#     site 7 0 left of site 6 0 right of site 8 0 top of site 7 1 bottom of site 7 -1
#     site 8 0 left of site 7 0 right of site 9 0 top of site 8 1 bottom of site 8 -1
#     site 9 0 left of site 8 0 right of site 10 0 top of site 9 1 bottom of site 9 -1
#     site 10 0 left of site 9 0 right of site 11 0 top of site 10 1 bottom of site 10 -1
#     site 11 0 left of site 10 0 right of site 12 0 top of site 11 1 bottom of site 11 -1
#     site 12 0 left of site 11 0 right of site 13 0 top of site 12 1 bottom of site 12 -1
#     site 13 0 left of site 12 0 right of site 14 0 top of site 13 1 bottom of site 13 -1
#     site 14 0 left of site 13 0 right of site 15 0 top of site 14 1 bottom of site 14 -1
#     site 15 0 left of site 14 0 right of site 16 0 top of site 15 1 bottom of site 15 -1
#     site 16 0 left of site 15 0 right of site 17 0 top of site 16 1 bottom of site 16 -1
#     site 17 0 left of site 16 0 right of site 18 0 top of site 17 1 bottom of site 17 -1
#     site 18 0 left of site 17 0 right of site 19 0 top of site 18 1 bottom of site 18 -1
#     site 19 0 left of site 18 0 right of site 20 0 top of site 19 1 bottom of site 19 -1
#     site 20 0 left of site 19 0 right of site 21 0 top of site 20 1 bottom of site 20 -1
#     site 21 0 left of site 20 0 right of site 22 0 top of site 21 1 bottom of site 21 -1
#     site 22 0 left of site 21 0 right of site 23 0 top of site 22 1 bottom of site 22 -1
#     site 23 0 left of site 22 0 right of site 0 0 top of site 23 1 bottom of site 23 -1
#     site 0 1 left of site 23 1 right of site 1 1 top of site 0 2 bottom of site 0 0
#     site 1 1 left of site 0 1 right of site 2 1 top of site 1 2 bottom of site 1 0
#     site 2 1 left of site 1 1 right of site 3 1 top of site 2 2 bottom of site 2 0
#     site 3 1 left of site 2 1 right of site 4 1 top of site 3 2 bottom of site 3 0
#     site 4 1 left of site 3 1 right of site 5 1 top of site 4 2 bottom of site 4 0
#     site 5 1 left of site 4 1 right of site 6 1 top of site 5 2 bottom of site 5 0
#     site 6 1 left of site 5 1 right of site 7 1 top of site 6 2 bottom of site 6 0
#     site 7 1 left of site 6 1 right of site 8 1 top of site 7 2 bottom of site 7 0
#     site 8 1 left of site 7 1 right of site 9 1 top of site 8 2 bottom of site 8 0
#     site 9 1 left of site 8 1 right of site 10 1 top of site 9 2 bottom of site 9 0
#     site 10 1 left of site 9 1 right of site 11 1 top of site 10 2 bottom of site 10 0
#     site 11 1 left of site 10 1 right of site 12 1 top of site 11 2 bottom of site 11 0
#     site 12 1 left of site 11 1 right of site 13 1 top of site 12 2 bottom of site 12 0
#     site 13 1 left of site 12 1 right of site 14 1 top of site 13 2 bottom of site 13 0
#     site 14 1 left of site 13 1 right of site 15 1 top of site 14 2 bottom of site 14 0
#     site 15 1 left of site 14 1 right of site 16 1 top of site 15 2 bottom of site 15 0
#     site 16 1 left of site 15 1 right of site 17 1 top of site 16 2 bottom of site 16 0
#     site 17 1 left of site 16 1 right of site 18 1 top of site 17 2 bottom of site 17 0
#     site 18 1 left of site 17 1 right of site 19 1 top of site 18 2 bottom of site 18 0
#     site 19 1 left of site 18 1 right of site 20 1 top of site 19 2 bottom of site 19 0
#     site 20 1 left of site 19 1 right of site 21 1 top of site 20 2 bottom of site 20 0
#     site 21 1 left of site 20 1 right of site 22 1 top of site 21 2 bottom of site 21 0
#     site 22 1 left of site 21 1 right of site 23 1 top of site 22 2 bottom of site 22 0
#     site 23 1 left of site 22 1 right of site 0 1 top of site 23 2 bottom of site 23 0
#     site 0 2 left of site 23 2 right of site 1 2 top of site 0 3 bottom of site 0 1
#     site 1 2 left of site 0 2 right of site 2 2 top of site 1 3 bottom of site 1 1
#     site 2 2 left of site 1 2 right of site 3 2 top of site 2 3 bottom of site 2 1
#     site 3 2 left of site 2 2 right of site 4 2 top of site 3 3 bottom of site 3 1
#     site 4 2 left of site 3 2 right of site 5 2 top of site 4 3 bottom of site 4 1
#     site 5 2 left of site 4 2 right of site 6 2 top of site 5 3 bottom of site 5 1
#     site 6 2 left of site 5 2 right of site 7 2 top of site 6 3 bottom of site 6 1
#     site 7 2 left of site 6 2 right of site 8 2 top of site 7 3 bottom of site 7 1
#     site 8 2 left of site 7 2 right of site 9 2 top of site 8 3 bottom of site 8 1
#     site 9 2 left of site 8 2 right of site 10 2 top of site 9 3 bottom of site 9 1
#     site 10 2 left of site 9 2 right of site 11 2 top of site 10 3 bottom of site 10 1
#     site 11 2 left of site 10 2 right of site 12 2 top of site 11 3 bottom of site 11 1
#     site 12 2 left of site 11 2 right of site 13 2 top of site 12 3 bottom of site 12 1
#     site 13 2 left of site 12 2 right of site 14 2 top of site 13 3 bottom of site 13 1
#     site 14 2 left of site 13 2 right of site 15 2 top of site 14 3 bottom of site 14 1
#     site 15 2 left of site 14 2 right of site 16 2 top of site 15 3 bottom of site 15 1
#     site 16 2 left of site 15 2 right of site 17 2 top of site 16 3 bottom of site 16 1
#     site 17 2 left of site 16 2 right of site 18 2 top of site 17 3 bottom of site 17 1
#     site 18 2 left of site 17 2 right of site 19 2 top of site 18 3 bottom of site 18 1
#     site 19 2 left of site 18 2 right of site 20 2 top of site 19 3 bottom of site 19 1
#     site 20 2 left of site 19 2 right of site 21 2 top of site 20 3 bottom of site 20 1
#     site 21 2 left of site 20 2 right of site 22 2 top of site 21 3 bottom of site 21 1
#     site 22 2 left of site 21 2 right of site 23 2 top of site 22 3 bottom of site 22 1
#     site 23 2 left of site 22 2 right of site 0 2 top of site 23 3 bottom of site 23 1
#     site 0 3 left of site 23 3 right of site 1 3 top of site 0 4 bottom of site 0 2
#     site 1 3 left of site 0 3 right of site 2 3 top of site 1 4 bottom of site 1 2
#     site 2 3 left of site 1 3 right of site 3 3 top of site 2 4 bottom of site 2 2
#     site 3 3 left of site 2 3 right of site 4 3 top of site 3 4 bottom of site 3 2
#     site 4 3 left of site 3 3 right of site 5 3 top of site 4 4 bottom of site 4 2
#     site 5 3 left of site 4 3 right of site 6 3 top of site 5 4 bottom of site 5 2
#     site 6 3 left of site 5 3 right of site 7 3 top of site 6 4 bottom of site 6 2
#     site 7 3 left of site 6 3 right of site 8 3 top of site 7 4 bottom of site 7 2
#     site 8 3 left of site 7 3 right of site 9 3 top of site 8 4 bottom of site 8 2
#     site 9 3 left of site 8 3 right of site 10 3 top of site 9 4 bottom of site 9 2
#     site 10 3 left of site 9 3 right of site 11 3 top of site 10 4 bottom of site 10 2
#     site 11 3 left of site 10 3 right of site 12 3 top of site 11 4 bottom of site 11 2
#     site 12 3 left of site 11 3 right of site 13 3 top of site 12 4 bottom of site 12 2
#     site 13 3 left of site 12 3 right of site 14 3 top of site 13 4 bottom of site 13 2
#     site 14 3 left of site 13 3 right of site 15 3 top of site 14 4 bottom of site 14 2
#     site 15 3 left of site 14 3 right of site 16 3 top of site 15 4 bottom of site 15 2
#     site 16 3 left of site 15 3 right of site 17 3 top of site 16 4 bottom of site 16 2
#     site 17 3 left of site 16 3 right of site 18 3 top of site 17 4 bottom of site 17 2
#     site 18 3 left of site 17 3 right of site 19 3 top of site 18 4 bottom of site 18 2
#     site 19 3 left of site 18 3 right of site 20 3 top of site 19 4 bottom of site 19 2
#     site 20 3 left of site 19 3 right of site 21 3 top of site 20 4 bottom of site 20 2
#     site 21 3 left of site 20 3 right of site 22 3 top of site 21 4 bottom of site 21 2
#     site 22 3 left of site 21 3 right of site 23 3 top of site 22 4 bottom of site 22 2
#     site 23 3 left of site 22 3 right of site 0 3 top of site 23 4 bottom of site 23 2
#     site 0 4 left of site 23 4 right of site 1 4 top of site 0 5 bottom of site 0 3
#     site 1 4 left of site 0 4 right of site 2 4 top of site 1 5 bottom of site 1 3
#     site 2 4 left of site 1 4 right of site 3 4 top of site 2 5 bottom of site 2 3
#     site 3 4 left of site 2 4 right of site 4 4 top of site 3 5 bottom of site 3 3
#     site 4 4 left of site 3 4 right of site 5 4 top of site 4 5 bottom of site 4 3
#     site 5 4 left of site 4 4 right of site 6 4 top of site 5 5 bottom of site 5 3
#     site 6 4 left of site 5 4 right of site 7 4 top of site 6 5 bottom of site 6 3
#     site 7 4 left of site 6 4 right of site 8 4 top of site 7 5 bottom of site 7 3
#     site 8 4 left of site 7 4 right of site 9 4 top of site 8 5 bottom of site 8 3
#     site 9 4 left of site 8 4 right of site 10 4 top of site 9 5 bottom of site 9 3
#     site 10 4 left of site 9 4 right of site 11 4 top of site 10 5 bottom of site 10 3
#     site 11 4 left of site 10 4 right of site 12 4 top of site 11 5 bottom of site 11 3
#     site 12 4 left of site 11 4 right of site 13 4 top of site 12 5 bottom of site 12 3
#     site 13 4 left of site 12 4 right of site 14 4 top of site 13 5 bottom of site 13 3
#     site 14 4 left of site 13 4 right of site 15 4 top of site 14 5 bottom of site 14 3
#     site 15 4 left of site 14 4 right of site 16 4 top of site 15 5 bottom of site 15 3
#     site 16 4 left of site 15 4 right of site 17 4 top of site 16 5 bottom of site 16 3
#     site 17 4 left of site 16 4 right of site 18 4 top of site 17 5 bottom of site 17 3
#     site 18 4 left of site 17 4 right of site 19 4 top of site 18 5 bottom of site 18 3
#     site 19 4 left of site 18 4 right of site 20 4 top of site 19 5 bottom of site 19 3
#     site 20 4 left of site 19 4 right of site 21 4 top of site 20 5 bottom of site 20 3
#     site 21 4 left of site 20 4 right of site 22 4 top of site 21 5 bottom of site 21 3
#     site 22 4 left of site 21 4 right of site 23 4 top of site 22 5 bottom of site 22 3
#     site 23 4 left of site 22 4 right of site 0 4 top of site 23 5 bottom of site 23 3
#     site 0 5 left of site 23 5 right of site 1 5 top of site 0 6 bottom of site 0 4
#     site 1 5 left of site 0 5 right of site 2 5 top of site 1 6 bottom of site 1 4
#     site 2 5 left of site 1 5 right of site 3 5 top of site 2 6 bottom of site 2 4
#     site 3 5 left of site 2 5 right of site 4 5 top of site 3 6 bottom of site 3 4
#     site 4 5 left of site 3 5 right of site 5 5 top of site 4 6 bottom of site 4 4
#     site 5 5 left of site 4 5 right of site 6 5 top of site 5 6 bottom of site 5 4
#     site 6 5 left of site 5 5 right of site 7 5 top of site 6 6 bottom of site 6 4
#     site 7 5 left of site 6 5 right of site 8 5 top of site 7 6 bottom of site 7 4
#     site 8 5 left of site 7 5 right of site 9 5 top of site 8 6 bottom of site 8 4
#     site 9 5 left of site 8 5 right of site 10 5 top of site 9 6 bottom of site 9 4
#     site 10 5 left of site 9 5 right of site 11 5 top of site 10 6 bottom of site 10 4
#     site 11 5 left of site 10 5 right of site 12 5 top of site 11 6 bottom of site 11 4
#     site 12 5 left of site 11 5 right of site 13 5 top of site 12 6 bottom of site 12 4
#     site 13 5 left of site 12 5 right of site 14 5 top of site 13 6 bottom of site 13 4
#     site 14 5 left of site 13 5 right of site 15 5 top of site 14 6 bottom of site 14 4
#     site 15 5 left of site 14 5 right of site 16 5 top of site 15 6 bottom of site 15 4
#     site 16 5 left of site 15 5 right of site 17 5 top of site 16 6 bottom of site 16 4
#     site 17 5 left of site 16 5 right of site 18 5 top of site 17 6 bottom of site 17 4
#     site 18 5 left of site 17 5 right of site 19 5 top of site 18 6 bottom of site 18 4
#     site 19 5 left of site 18 5 right of site 20 5 top of site 19 6 bottom of site 19 4
#     site 20 5 left of site 19 5 right of site 21 5 top of site 20 6 bottom of site 20 4
#     site 21 5 left of site 20 5 right of site 22 5 top of site 21 6 bottom of site 21 4
#     site 22 5 left of site 21 5 right of site 23 5 top of site 22 6 bottom of site 22 4
#     site 23 5 left of site 22 5 right of site 0 5 top of site 23 6 bottom of site 23 4
#     site 0 6 left of site 23 6 right of site 1 6 top of site 0 7 bottom of site 0 5
#     site 1 6 left of site 0 6 right of site 2 6 top of site 1 7 bottom of site 1 5
#     site 2 6 left of site 1 6 right of site 3 6 top of site 2 7 bottom of site 2 5
#     site 3 6 left of site 2 6 right of site 4 6 top of site 3 7 bottom of site 3 5
#     site 4 6 left of site 3 6 right of site 5 6 top of site 4 7 bottom of site 4 5
#     site 5 6 left of site 4 6 right of site 6 6 top of site 5 7 bottom of site 5 5
#     site 6 6 left of site 5 6 right of site 7 6 top of site 6 7 bottom of site 6 5
#     site 7 6 left of site 6 6 right of site 8 6 top of site 7 7 bottom of site 7 5
#     site 8 6 left of site 7 6 right of site 9 6 top of site 8 7 bottom of site 8 5
#     site 9 6 left of site 8 6 right of site 10 6 top of site 9 7 bottom of site 9 5
#     site 10 6 left of site 9 6 right of site 11 6 top of site 10 7 bottom of site 10 5
#     site 11 6 left of site 10 6 right of site 12 6 top of site 11 7 bottom of site 11 5
#     site 12 6 left of site 11 6 right of site 13 6 top of site 12 7 bottom of site 12 5
#     site 13 6 left of site 12 6 right of site 14 6 top of site 13 7 bottom of site 13 5
#     site 14 6 left of site 13 6 right of site 15 6 top of site 14 7 bottom of site 14 5
#     site 15 6 left of site 14 6 right of site 16 6 top of site 15 7 bottom of site 15 5
#     site 16 6 left of site 15 6 right of site 17 6 top of site 16 7 bottom of site 16 5
#     site 17 6 left of site 16 6 right of site 18 6 top of site 17 7 bottom of site 17 5
#     site 18 6 left of site 17 6 right of site 19 6 top of site 18 7 bottom of site 18 5
#     site 19 6 left of site 18 6 right of site 20 6 top of site 19 7 bottom of site 19 5
#     site 20 6 left of site 19 6 right of site 21 6 top of site 20 7 bottom of site 20 5
#     site 21 6 left of site 20 6 right of site 22 6 top of site 21 7 bottom of site 21 5
#     site 22 6 left of site 21 6 right of site 23 6 top of site 22 7 bottom of site 22 5
#     site 23 6 left of site 22 6 right of site 0 6 top of site 23 7 bottom of site 23 5
#     site 0 7 left of site 23 7 right of site 1 7 top of site 0 8 bottom of site 0 6
#     site 1 7 left of site 0 7 right of site 2 7 top of site 1 8 bottom of site 1 6
#     site 2 7 left of site 1 7 right of site 3 7 top of site 2 8 bottom of site 2 6
#     site 3 7 left of site 2 7 right of site 4 7 top of site 3 8 bottom of site 3 6
#     site 4 7 left of site 3 7 right of site 5 7 top of site 4 8 bottom of site 4 6
#     site 5 7 left of site 4 7 right of site 6 7 top of site 5 8 bottom of site 5 6
#     site 6 7 left of site 5 7 right of site 7 7 top of site 6 8 bottom of site 6 6
#     site 7 7 left of site 6 7 right of site 8 7 top of site 7 8 bottom of site 7 6
#     site 8 7 left of site 7 7 right of site 9 7 top of site 8 8 bottom of site 8 6
#     site 9 7 left of site 8 7 right of site 10 7 top of site 9 8 bottom of site 9 6
#     site 10 7 left of site 9 7 right of site 11 7 top of site 10 8 bottom of site 10 6
#     site 11 7 left of site 10 7 right of site 12 7 top of site 11 8 bottom of site 11 6
#     site 12 7 left of site 11 7 right of site 13 7 top of site 12 8 bottom of site 12 6
#     site 13 7 left of site 12 7 right of site 14 7 top of site 13 8 bottom of site 13 6
#     site 14 7 left of site 13 7 right of site 15 7 top of site 14 8 bottom of site 14 6
#     site 15 7 left of site 14 7 right of site 16 7 top of site 15 8 bottom of site 15 6
#     site 16 7 left of site 15 7 right of site 17 7 top of site 16 8 bottom of site 16 6
#     site 17 7 left of site 16 7 right of site 18 7 top of site 17 8 bottom of site 17 6
#     site 18 7 left of site 17 7 right of site 19 7 top of site 18 8 bottom of site 18 6
#     site 19 7 left of site 18 7 right of site 20 7 top of site 19 8 bottom of site 19 6
#     site 20 7 left of site 19 7 right of site 21 7 top of site 20 8 bottom of site 20 6
#     site 21 7 left of site 20 7 right of site 22 7 top of site 21 8 bottom of site 21 6
#     site 22 7 left of site 21 7 right of site 23 7 top of site 22 8 bottom of site 22 6
#     site 23 7 left of site 22 7 right of site 0 7 top of site 23 8 bottom of site 23 6
#     site 0 8 left of site 23 8 right of site 1 8 top of site 0 9 bottom of site 0 7
#     site 1 8 left of site 0 8 right of site 2 8 top of site 1 9 bottom of site 1 7
#     site 2 8 left of site 1 8 right of site 3 8 top of site 2 9 bottom of site 2 7
#     site 3 8 left of site 2 8 right of site 4 8 top of site 3 9 bottom of site 3 7
#     site 4 8 left of site 3 8 right of site 5 8 top of site 4 9 bottom of site 4 7
#     site 5 8 left of site 4 8 right of site 6 8 top of site 5 9 bottom of site 5 7
#     site 6 8 left of site 5 8 right of site 7 8 top of site 6 9 bottom of site 6 7
#     site 7 8 left of site 6 8 right of site 8 8 top of site 7 9 bottom of site 7 7
#     site 8 8 left of site 7 8 right of site 9 8 top of site 8 9 bottom of site 8 7
#     site 9 8 left of site 8 8 right of site 10 8 top of site 9 9 bottom of site 9 7
#     site 10 8 left of site 9 8 right of site 11 8 top of site 10 9 bottom of site 10 7
#     site 11 8 left of site 10 8 right of site 12 8 top of site 11 9 bottom of site 11 7
#     site 12 8 left of site 11 8 right of site 13 8 top of site 12 9 bottom of site 12 7
#     site 13 8 left of site 12 8 right of site 14 8 top of site 13 9 bottom of site 13 7
#     site 14 8 left of site 13 8 right of site 15 8 top of site 14 9 bottom of site 14 7
#     site 15 8 left of site 14 8 right of site 16 8 top of site 15 9 bottom of site 15 7
#     site 16 8 left of site 15 8 right of site 17 8 top of site 16 9 bottom of site 16 7
#     site 17 8 left of site 16 8 right of site 18 8 top of site 17 9 bottom of site 17 7
#     site 18 8 left of site 17 8 right of site 19 8 top of site 18 9 bottom of site 18 7
#     site 19 8 left of site 18 8 right of site 20 8 top of site 19 9 bottom of site 19 7
#     site 20 8 left of site 19 8 right of site 21 8 top of site 20 9 bottom of site 20 7
#     site 21 8 left of site 20 8 right of site 22 8 top of site 21 9 bottom of site 21 7
#     site 22 8 left of site 21 8 right of site 23 8 top of site 22 9 bottom of site 22 7
#     site 23 8 left of site 22 8 right of site 0 8 top of site 23 9 bottom of site 23 7
#     site 0 9 left of site 23 9 right of site 1 9 top of site 0 10 bottom of site 0 8
#     site 1 9 left of site 0 9 right of site 2 9 top of site 1 10 bottom of site 1 8
#     site 2 9 left of site 1 9 right of site 3 9 top of site 2 10 bottom of site 2 8
#     site 3 9 left of site 2 9 right of site 4 9 top of site 3 10 bottom of site 3 8
#     site 4 9 left of site 3 9 right of site 5 9 top of site 4 10 bottom of site 4 8
#     site 5 9 left of site 4 9 right of site 6 9 top of site 5 10 bottom of site 5 8
#     site 6 9 left of site 5 9 right of site 7 9 top of site 6 10 bottom of site 6 8
#     site 7 9 left of site 6 9 right of site 8 9 top of site 7 10 bottom of site 7 8
#     site 8 9 left of site 7 9 right of site 9 9 top of site 8 10 bottom of site 8 8
#     site 9 9 left of site 8 9 right of site 10 9 top of site 9 10 bottom of site 9 8
#     site 10 9 left of site 9 9 right of site 11 9 top of site 10 10 bottom of site 10 8
#     site 11 9 left of site 10 9 right of site 12 9 top of site 11 10 bottom of site 11 8
#     site 12 9 left of site 11 9 right of site 13 9 top of site 12 10 bottom of site 12 8
#     site 13 9 left of site 12 9 right of site 14 9 top of site 13 10 bottom of site 13 8
#     site 14 9 left of site 13 9 right of site 15 9 top of site 14 10 bottom of site 14 8
#     site 15 9 left of site 14 9 right of site 16 9 top of site 15 10 bottom of site 15 8
#     site 16 9 left of site 15 9 right of site 17 9 top of site 16 10 bottom of site 16 8
#     site 17 9 left of site 16 9 right of site 18 9 top of site 17 10 bottom of site 17 8
#     site 18 9 left of site 17 9 right of site 19 9 top of site 18 10 bottom of site 18 8
#     site 19 9 left of site 18 9 right of site 20 9 top of site 19 10 bottom of site 19 8
#     site 20 9 left of site 19 9 right of site 21 9 top of site 20 10 bottom of site 20 8
#     site 21 9 left of site 20 9 right of site 22 9 top of site 21 10 bottom of site 21 8
#     site 22 9 left of site 21 9 right of site 23 9 top of site 22 10 bottom of site 22 8
#     site 23 9 left of site 22 9 right of site 0 9 top of site 23 10 bottom of site 23 8
#     site 0 10 left of site 23 10 right of site 1 10 top of site 0 11 bottom of site 0 9
#     site 1 10 left of site 0 10 right of site 2 10 top of site 1 11 bottom of site 1 9
#     site 2 10 left of site 1 10 right of site 3 10 top of site 2 11 bottom of site 2 9
#     site 3 10 left of site 2 10 right of site 4 10 top of site 3 11 bottom of site 3 9
#     site 4 10 left of site 3 10 right of site 5 10 top of site 4 11 bottom of site 4 9
#     site 5 10 left of site 4 10 right of site 6 10 top of site 5 11 bottom of site 5 9
#     site 6 10 left of site 5 10 right of site 7 10 top of site 6 11 bottom of site 6 9
#     site 7 10 left of site 6 10 right of site 8 10 top of site 7 11 bottom of site 7 9
#     site 8 10 left of site 7 10 right of site 9 10 top of site 8 11 bottom of site 8 9
#     site 9 10 left of site 8 10 right of site 10 10 top of site 9 11 bottom of site 9 9
#     site 10 10 left of site 9 10 right of site 11 10 top of site 10 11 bottom of site 10 9
#     site 11 10 left of site 10 10 right of site 12 10 top of site 11 11 bottom of site 11 9
#     site 12 10 left of site 11 10 right of site 13 10 top of site 12 11 bottom of site 12 9
#     site 13 10 left of site 12 10 right of site 14 10 top of site 13 11 bottom of site 13 9
#     site 14 10 left of site 13 10 right of site 15 10 top of site 14 11 bottom of site 14 9
#     site 15 10 left of site 14 10 right of site 16 10 top of site 15 11 bottom of site 15 9
#     site 16 10 left of site 15 10 right of site 17 10 top of site 16 11 bottom of site 16 9
#     site 17 10 left of site 16 10 right of site 18 10 top of site 17 11 bottom of site 17 9
#     site 18 10 left of site 17 10 right of site 19 10 top of site 18 11 bottom of site 18 9
#     site 19 10 left of site 18 10 right of site 20 10 top of site 19 11 bottom of site 19 9
#     site 20 10 left of site 19 10 right of site 21 10 top of site 20 11 bottom of site 20 9
#     site 21 10 left of site 20 10 right of site 22 10 top of site 21 11 bottom of site 21 9
#     site 22 10 left of site 21 10 right of site 23 10 top of site 22 11 bottom of site 22 9
#     site 23 10 left of site 22 10 right of site 0 10 top of site 23 11 bottom of site 23 9
#     site 0 11 left of site 23 11 right of site 1 11 top of site 0 12 bottom of site 0 10
#     site 1 11 left of site 0 11 right of site 2 11 top of site 1 12 bottom of site 1 10
#     site 2 11 left of site 1 11 right of site 3 11 top of site 2 12 bottom of site 2 10
#     site 3 11 left of site 2 11 right of site 4 11 top of site 3 12 bottom of site 3 10
#     site 4 11 left of site 3 11 right of site 5 11 top of site 4 12 bottom of site 4 10
#     site 5 11 left of site 4 11 right of site 6 11 top of site 5 12 bottom of site 5 10
#     site 6 11 left of site 5 11 right of site 7 11 top of site 6 12 bottom of site 6 10
#     site 7 11 left of site 6 11 right of site 8 11 top of site 7 12 bottom of site 7 10
#     site 8 11 left of site 7 11 right of site 9 11 top of site 8 12 bottom of site 8 10
#     site 9 11 left of site 8 11 right of site 10 11 top of site 9 12 bottom of site 9 10
#     site 10 11 left of site 9 11 right of site 11 11 top of site 10 12 bottom of site 10 10
#     site 11 11 left of site 10 11 right of site 12 11 top of site 11 12 bottom of site 11 10
#     site 12 11 left of site 11 11 right of site 13 11 top of site 12 12 bottom of site 12 10
#     site 13 11 left of site 12 11 right of site 14 11 top of site 13 12 bottom of site 13 10
#     site 14 11 left of site 13 11 right of site 15 11 top of site 14 12 bottom of site 14 10
#     site 15 11 left of site 14 11 right of site 16 11 top of site 15 12 bottom of site 15 10
#     site 16 11 left of site 15 11 right of site 17 11 top of site 16 12 bottom of site 16 10
#     site 17 11 left of site 16 11 right of site 18 11 top of site 17 12 bottom of site 17 10
#     site 18 11 left of site 17 11 right of site 19 11 top of site 18 12 bottom of site 18 10
#     site 19 11 left of site 18 11 right of site 20 11 top of site 19 12 bottom of site 19 10
#     site 20 11 left of site 19 11 right of site 21 11 top of site 20 12 bottom of site 20 10
#     site 21 11 left of site 20 11 right of site 22 11 top of site 21 12 bottom of site 21 10
#     site 22 11 left of site 21 11 right of site 23 11 top of site 22 12 bottom of site 22 10
#     site 23 11 left of site 22 11 right of site 0 11 top of site 23 12 bottom of site 23 10
#     site 0 12 left of site 23 12 right of site 1 12 top of site 0 13 bottom of site 0 11
#     site 1 12 left of site 0 12 right of site 2 12 top of site 1 13 bottom of site 1 11
#     site 2 12 left of site 1 12 right of site 3 12 top of site 2 13 bottom of site 2 11
#     site 3 12 left of site 2 12 right of site 4 12 top of site 3 13 bottom of site 3 11
#     site 4 12 left of site 3 12 right of site 5 12 top of site 4 13 bottom of site 4 11
#     site 5 12 left of site 4 12 right of site 6 12 top of site 5 13 bottom of site 5 11
#     site 6 12 left of site 5 12 right of site 7 12 top of site 6 13 bottom of site 6 11
#     site 7 12 left of site 6 12 right of site 8 12 top of site 7 13 bottom of site 7 11
#     site 8 12 left of site 7 12 right of site 9 12 top of site 8 13 bottom of site 8 11
#     site 9 12 left of site 8 12 right of site 10 12 top of site 9 13 bottom of site 9 11
#     site 10 12 left of site 9 12 right of site 11 12 top of site 10 13 bottom of site 10 11
#     site 11 12 left of site 10 12 right of site 12 12 top of site 11 13 bottom of site 11 11
#     site 12 12 left of site 11 12 right of site 13 12 top of site 12 13 bottom of site 12 11
#     site 13 12 left of site 12 12 right of site 14 12 top of site 13 13 bottom of site 13 11
#     site 14 12 left of site 13 12 right of site 15 12 top of site 14 13 bottom of site 14 11
#     site 15 12 left of site 14 12 right of site 16 12 top of site 15 13 bottom of site 15 11
#     site 16 12 left of site 15 12 right of site 17 12 top of site 16 13 bottom of site 16 11
#     site 17 12 left of site 16 12 right of site 18 12 top of site 17 13 bottom of site 17 11
#     site 18 12 left of site 17 12 right of site 19 12 top of site 18 13 bottom of site 18 11
#     site 19 12 left of site 18 12 right of site 20 12 top of site 19 13 bottom of site 19 11
#     site 20 12 left of site 19 12 right of site 21 12 top of site 20 13 bottom of site 20 11
#     site 21 12 left of site 20 12 right of site 22 12 top of site 21 13 bottom of site 21 11
#     site 22 12 left of site 21 12 right of site 23 12 top of site 22 13 bottom of site 22 11
#     site 23 12 left of site 22 12 right of site 0 12 top of site 23 13 bottom of site 23 11
#     site 0 13 left of site 23 13 right of site 1 13 top of site 0 14 bottom of site 0 12
#     site 1 13 left of site 0 13 right of site 2 13 top of site 1 14 bottom of site 1 12
#     site 2 13 left of site 1 13 right of site 3 13 top of site 2 14 bottom of site 2 12
#     site 3 13 left of site 2 13 right of site 4 13 top of site 3 14 bottom of site 3 12
#     site 4 13 left of site 3 13 right of site 5 13 top of site 4 14 bottom of site 4 12
#     site 5 13 left of site 4 13 right of site 6 13 top of site 5 14 bottom of site 5 12
#     site 6 13 left of site 5 13 right of site 7 13 top of site 6 14 bottom of site 6 12
#     site 7 13 left of site 6 13 right of site 8 13 top of site 7 14 bottom of site 7 12
#     site 8 13 left of site 7 13 right of site 9 13 top of site 8 14 bottom of site 8 12
#     site 9 13 left of site 8 13 right of site 10 13 top of site 9 14 bottom of site 9 12
#     site 10 13 left of site 9 13 right of site 11 13 top of site 10 14 bottom of site 10 12
#     site 11 13 left of site 10 13 right of site 12 13 top of site 11 14 bottom of site 11 12
#     site 12 13 left of site 11 13 right of site 13 13 top of site 12 14 bottom of site 12 12
#     site 13 13 left of site 12 13 right of site 14 13 top of site 13 14 bottom of site 13 12
#     site 14 13 left of site 13 13 right of site 15 13 top of site 14 14 bottom of site 14 12
#     site 15 13 left of site 14 13 right of site 16 13 top of site 15 14 bottom of site 15 12
#     site 16 13 left of site 15 13 right of site 17 13 top of site 16 14 bottom of site 16 12
#     site 17 13 left of site 16 13 right of site 18 13 top of site 17 14 bottom of site 17 12
#     site 18 13 left of site 17 13 right of site 19 13 top of site 18 14 bottom of site 18 12
#     site 19 13 left of site 18 13 right of site 20 13 top of site 19 14 bottom of site 19 12
#     site 20 13 left of site 19 13 right of site 21 13 top of site 20 14 bottom of site 20 12
#     site 21 13 left of site 20 13 right of site 22 13 top of site 21 14 bottom of site 21 12
#     site 22 13 left of site 21 13 right of site 23 13 top of site 22 14 bottom of site 22 12
#     site 23 13 left of site 22 13 right of site 0 13 top of site 23 14 bottom of site 23 12
#     site 0 14 left of site 23 14 right of site 1 14 top of site 0 15 bottom of site 0 13
#     site 1 14 left of site 0 14 right of site 2 14 top of site 1 15 bottom of site 1 13
#     site 2 14 left of site 1 14 right of site 3 14 top of site 2 15 bottom of site 2 13
#     site 3 14 left of site 2 14 right of site 4 14 top of site 3 15 bottom of site 3 13
#     site 4 14 left of site 3 14 right of site 5 14 top of site 4 15 bottom of site 4 13
#     site 5 14 left of site 4 14 right of site 6 14 top of site 5 15 bottom of site 5 13
#     site 6 14 left of site 5 14 right of site 7 14 top of site 6 15 bottom of site 6 13
#     site 7 14 left of site 6 14 right of site 8 14 top of site 7 15 bottom of site 7 13
#     site 8 14 left of site 7 14 right of site 9 14 top of site 8 15 bottom of site 8 13
#     site 9 14 left of site 8 14 right of site 10 14 top of site 9 15 bottom of site 9 13
#     site 10 14 left of site 9 14 right of site 11 14 top of site 10 15 bottom of site 10 13
#     site 11 14 left of site 10 14 right of site 12 14 top of site 11 15 bottom of site 11 13
#     site 12 14 left of site 11 14 right of site 13 14 top of site 12 15 bottom of site 12 13
#     site 13 14 left of site 12 14 right of site 14 14 top of site 13 15 bottom of site 13 13
#     site 14 14 left of site 13 14 right of site 15 14 top of site 14 15 bottom of site 14 13
#     site 15 14 left of site 14 14 right of site 16 14 top of site 15 15 bottom of site 15 13
#     site 16 14 left of site 15 14 right of site 17 14 top of site 16 15 bottom of site 16 13
#     site 17 14 left of site 16 14 right of site 18 14 top of site 17 15 bottom of site 17 13
#     site 18 14 left of site 17 14 right of site 19 14 top of site 18 15 bottom of site 18 13
#     site 19 14 left of site 18 14 right of site 20 14 top of site 19 15 bottom of site 19 13
#     site 20 14 left of site 19 14 right of site 21 14 top of site 20 15 bottom of site 20 13
#     site 21 14 left of site 20 14 right of site 22 14 top of site 21 15 bottom of site 21 13
#     site 22 14 left of site 21 14 right of site 23 14 top of site 22 15 bottom of site 22 13
#     site 23 14 left of site 22 14 right of site 0 14 top of site 23 15 bottom of site 23 13
#     site 0 15 left of site 23 15 right of site 1 15 top of site 0 16 bottom of site 0 14
#     site 1 15 left of site 0 15 right of site 2 15 top of site 1 16 bottom of site 1 14
#     site 2 15 left of site 1 15 right of site 3 15 top of site 2 16 bottom of site 2 14
#     site 3 15 left of site 2 15 right of site 4 15 top of site 3 16 bottom of site 3 14
#     site 4 15 left of site 3 15 right of site 5 15 top of site 4 16 bottom of site 4 14
#     site 5 15 left of site 4 15 right of site 6 15 top of site 5 16 bottom of site 5 14
#     site 6 15 left of site 5 15 right of site 7 15 top of site 6 16 bottom of site 6 14
#     site 7 15 left of site 6 15 right of site 8 15 top of site 7 16 bottom of site 7 14
#     site 8 15 left of site 7 15 right of site 9 15 top of site 8 16 bottom of site 8 14
#     site 9 15 left of site 8 15 right of site 10 15 top of site 9 16 bottom of site 9 14
#     site 10 15 left of site 9 15 right of site 11 15 top of site 10 16 bottom of site 10 14
#     site 11 15 left of site 10 15 right of site 12 15 top of site 11 16 bottom of site 11 14
#     site 12 15 left of site 11 15 right of site 13 15 top of site 12 16 bottom of site 12 14
#     site 13 15 left of site 12 15 right of site 14 15 top of site 13 16 bottom of site 13 14
#     site 14 15 left of site 13 15 right of site 15 15 top of site 14 16 bottom of site 14 14
#     site 15 15 left of site 14 15 right of site 16 15 top of site 15 16 bottom of site 15 14
#     site 16 15 left of site 15 15 right of site 17 15 top of site 16 16 bottom of site 16 14
#     site 17 15 left of site 16 15 right of site 18 15 top of site 17 16 bottom of site 17 14
#     site 18 15 left of site 17 15 right of site 19 15 top of site 18 16 bottom of site 18 14
#     site 19 15 left of site 18 15 right of site 20 15 top of site 19 16 bottom of site 19 14
#     site 20 15 left of site 19 15 right of site 21 15 top of site 20 16 bottom of site 20 14
#     site 21 15 left of site 20 15 right of site 22 15 top of site 21 16 bottom of site 21 14
#     site 22 15 left of site 21 15 right of site 23 15 top of site 22 16 bottom of site 22 14
#     site 23 15 left of site 22 15 right of site 0 15 top of site 23 16 bottom of site 23 14
#     site 0 16 left of site 23 16 right of site 1 16 top of site 0 17 bottom of site 0 15
#     site 1 16 left of site 0 16 right of site 2 16 top of site 1 17 bottom of site 1 15
#     site 2 16 left of site 1 16 right of site 3 16 top of site 2 17 bottom of site 2 15
#     site 3 16 left of site 2 16 right of site 4 16 top of site 3 17 bottom of site 3 15
#     site 4 16 left of site 3 16 right of site 5 16 top of site 4 17 bottom of site 4 15
#     site 5 16 left of site 4 16 right of site 6 16 top of site 5 17 bottom of site 5 15
#     site 6 16 left of site 5 16 right of site 7 16 top of site 6 17 bottom of site 6 15
#     site 7 16 left of site 6 16 right of site 8 16 top of site 7 17 bottom of site 7 15
#     site 8 16 left of site 7 16 right of site 9 16 top of site 8 17 bottom of site 8 15
#     site 9 16 left of site 8 16 right of site 10 16 top of site 9 17 bottom of site 9 15
#     site 10 16 left of site 9 16 right of site 11 16 top of site 10 17 bottom of site 10 15
#     site 11 16 left of site 10 16 right of site 12 16 top of site 11 17 bottom of site 11 15
#     site 12 16 left of site 11 16 right of site 13 16 top of site 12 17 bottom of site 12 15
#     site 13 16 left of site 12 16 right of site 14 16 top of site 13 17 bottom of site 13 15
#     site 14 16 left of site 13 16 right of site 15 16 top of site 14 17 bottom of site 14 15
#     site 15 16 left of site 14 16 right of site 16 16 top of site 15 17 bottom of site 15 15
#     site 16 16 left of site 15 16 right of site 17 16 top of site 16 17 bottom of site 16 15
#     site 17 16 left of site 16 16 right of site 18 16 top of site 17 17 bottom of site 17 15
#     site 18 16 left of site 17 16 right of site 19 16 top of site 18 17 bottom of site 18 15
#     site 19 16 left of site 18 16 right of site 20 16 top of site 19 17 bottom of site 19 15
#     site 20 16 left of site 19 16 right of site 21 16 top of site 20 17 bottom of site 20 15
#     site 21 16 left of site 20 16 right of site 22 16 top of site 21 17 bottom of site 21 15
#     site 22 16 left of site 21 16 right of site 23 16 top of site 22 17 bottom of site 22 15
#     site 23 16 left of site 22 16 right of site 0 16 top of site 23 17 bottom of site 23 15
#     site 0 17 left of site 23 17 right of site 1 17 top of site 0 18 bottom of site 0 16
#     site 1 17 left of site 0 17 right of site 2 17 top of site 1 18 bottom of site 1 16
#     site 2 17 left of site 1 17 right of site 3 17 top of site 2 18 bottom of site 2 16
#     site 3 17 left of site 2 17 right of site 4 17 top of site 3 18 bottom of site 3 16
#     site 4 17 left of site 3 17 right of site 5 17 top of site 4 18 bottom of site 4 16
#     site 5 17 left of site 4 17 right of site 6 17 top of site 5 18 bottom of site 5 16
#     site 6 17 left of site 5 17 right of site 7 17 top of site 6 18 bottom of site 6 16
#     site 7 17 left of site 6 17 right of site 8 17 top of site 7 18 bottom of site 7 16
#     site 8 17 left of site 7 17 right of site 9 17 top of site 8 18 bottom of site 8 16
#     site 9 17 left of site 8 17 right of site 10 17 top of site 9 18 bottom of site 9 16
#     site 10 17 left of site 9 17 right of site 11 17 top of site 10 18 bottom of site 10 16
#     site 11 17 left of site 10 17 right of site 12 17 top of site 11 18 bottom of site 11 16
#     site 12 17 left of site 11 17 right of site 13 17 top of site 12 18 bottom of site 12 16
#     site 13 17 left of site 12 17 right of site 14 17 top of site 13 18 bottom of site 13 16
#     site 14 17 left of site 13 17 right of site 15 17 top of site 14 18 bottom of site 14 16
#     site 15 17 left of site 14 17 right of site 16 17 top of site 15 18 bottom of site 15 16
#     site 16 17 left of site 15 17 right of site 17 17 top of site 16 18 bottom of site 16 16
#     site 17 17 left of site 16 17 right of site 18 17 top of site 17 18 bottom of site 17 16
#     site 18 17 left of site 17 17 right of site 19 17 top of site 18 18 bottom of site 18 16
#     site 19 17 left of site 18 17 right of site 20 17 top of site 19 18 bottom of site 19 16
#     site 20 17 left of site 19 17 right of site 21 17 top of site 20 18 bottom of site 20 16
#     site 21 17 left of site 20 17 right of site 22 17 top of site 21 18 bottom of site 21 16
#     site 22 17 left of site 21 17 right of site 23 17 top of site 22 18 bottom of site 22 16
#     site 23 17 left of site 22 17 right of site 0 17 top of site 23 18 bottom of site 23 16
#     site 0 18 left of site 23 18 right of site 1 18 top of site 0 19 bottom of site 0 17
#     site 1 18 left of site 0 18 right of site 2 18 top of site 1 19 bottom of site 1 17
#     site 2 18 left of site 1 18 right of site 3 18 top of site 2 19 bottom of site 2 17
#     site 3 18 left of site 2 18 right of site 4 18 top of site 3 19 bottom of site 3 17
#     site 4 18 left of site 3 18 right of site 5 18 top of site 4 19 bottom of site 4 17
#     site 5 18 left of site 4 18 right of site 6 18 top of site 5 19 bottom of site 5 17
#     site 6 18 left of site 5 18 right of site 7 18 top of site 6 19 bottom of site 6 17
#     site 7 18 left of site 6 18 right of site 8 18 top of site 7 19 bottom of site 7 17
#     site 8 18 left of site 7 18 right of site 9 18 top of site 8 19 bottom of site 8 17
#     site 9 18 left of site 8 18 right of site 10 18 top of site 9 19 bottom of site 9 17
#     site 10 18 left of site 9 18 right of site 11 18 top of site 10 19 bottom of site 10 17
#     site 11 18 left of site 10 18 right of site 12 18 top of site 11 19 bottom of site 11 17
#     site 12 18 left of site 11 18 right of site 13 18 top of site 12 19 bottom of site 12 17
#     site 13 18 left of site 12 18 right of site 14 18 top of site 13 19 bottom of site 13 17
#     site 14 18 left of site 13 18 right of site 15 18 top of site 14 19 bottom of site 14 17
#     site 15 18 left of site 14 18 right of site 16 18 top of site 15 19 bottom of site 15 17
#     site 16 18 left of site 15 18 right of site 17 18 top of site 16 19 bottom of site 16 17
#     site 17 18 left of site 16 18 right of site 18 18 top of site 17 19 bottom of site 17 17
#     site 18 18 left of site 17 18 right of site 19 18 top of site 18 19 bottom of site 18 17
#     site 19 18 left of site 18 18 right of site 20 18 top of site 19 19 bottom of site 19 17
#     site 20 18 left of site 19 18 right of site 21 18 top of site 20 19 bottom of site 20 17
#     site 21 18 left of site 20 18 right of site 22 18 top of site 21 19 bottom of site 21 17
#     site 22 18 left of site 21 18 right of site 23 18 top of site 22 19 bottom of site 22 17
#     site 23 18 left of site 22 18 right of site 0 18 top of site 23 19 bottom of site 23 17
#     site 0 19 left of site 23 19 right of site 1 19 top of site 0 20 bottom of site 0 18
#     site 1 19 left of site 0 19 right of site 2 19 top of site 1 20 bottom of site 1 18
#     site 2 19 left of site 1 19 right of site 3 19 top of site 2 20 bottom of site 2 18
#     site 3 19 left of site 2 19 right of site 4 19 top of site 3 20 bottom of site 3 18
#     site 4 19 left of site 3 19 right of site 5 19 top of site 4 20 bottom of site 4 18
#     site 5 19 left of site 4 19 right of site 6 19 top of site 5 20 bottom of site 5 18
#     site 6 19 left of site 5 19 right of site 7 19 top of site 6 20 bottom of site 6 18
#     site 7 19 left of site 6 19 right of site 8 19 top of site 7 20 bottom of site 7 18
#     site 8 19 left of site 7 19 right of site 9 19 top of site 8 20 bottom of site 8 18
#     site 9 19 left of site 8 19 right of site 10 19 top of site 9 20 bottom of site 9 18
#     site 10 19 left of site 9 19 right of site 11 19 top of site 10 20 bottom of site 10 18
#     site 11 19 left of site 10 19 right of site 12 19 top of site 11 20 bottom of site 11 18
#     site 12 19 left of site 11 19 right of site 13 19 top of site 12 20 bottom of site 12 18
#     site 13 19 left of site 12 19 right of site 14 19 top of site 13 20 bottom of site 13 18
#     site 14 19 left of site 13 19 right of site 15 19 top of site 14 20 bottom of site 14 18
#     site 15 19 left of site 14 19 right of site 16 19 top of site 15 20 bottom of site 15 18
#     site 16 19 left of site 15 19 right of site 17 19 top of site 16 20 bottom of site 16 18
#     site 17 19 left of site 16 19 right of site 18 19 top of site 17 20 bottom of site 17 18
#     site 18 19 left of site 17 19 right of site 19 19 top of site 18 20 bottom of site 18 18
#     site 19 19 left of site 18 19 right of site 20 19 top of site 19 20 bottom of site 19 18
#     site 20 19 left of site 19 19 right of site 21 19 top of site 20 20 bottom of site 20 18
#     site 21 19 left of site 20 19 right of site 22 19 top of site 21 20 bottom of site 21 18
#     site 22 19 left of site 21 19 right of site 23 19 top of site 22 20 bottom of site 22 18
#     site 23 19 left of site 22 19 right of site 0 19 top of site 23 20 bottom of site 23 18
#     site 0 20 left of site 23 20 right of site 1 20 top of site 0 21 bottom of site 0 19
#     site 1 20 left of site 0 20 right of site 2 20 top of site 1 21 bottom of site 1 19
#     site 2 20 left of site 1 20 right of site 3 20 top of site 2 21 bottom of site 2 19
#     site 3 20 left of site 2 20 right of site 4 20 top of site 3 21 bottom of site 3 19
#     site 4 20 left of site 3 20 right of site 5 20 top of site 4 21 bottom of site 4 19
#     site 5 20 left of site 4 20 right of site 6 20 top of site 5 21 bottom of site 5 19
#     site 6 20 left of site 5 20 right of site 7 20 top of site 6 21 bottom of site 6 19
#     site 7 20 left of site 6 20 right of site 8 20 top of site 7 21 bottom of site 7 19
#     site 8 20 left of site 7 20 right of site 9 20 top of site 8 21 bottom of site 8 19
#     site 9 20 left of site 8 20 right of site 10 20 top of site 9 21 bottom of site 9 19
#     site 10 20 left of site 9 20 right of site 11 20 top of site 10 21 bottom of site 10 19
#     site 11 20 left of site 10 20 right of site 12 20 top of site 11 21 bottom of site 11 19
#     site 12 20 left of site 11 20 right of site 13 20 top of site 12 21 bottom of site 12 19
#     site 13 20 left of site 12 20 right of site 14 20 top of site 13 21 bottom of site 13 19
#     site 14 20 left of site 13 20 right of site 15 20 top of site 14 21 bottom of site 14 19
#     site 15 20 left of site 14 20 right of site 16 20 top of site 15 21 bottom of site 15 19
#     site 16 20 left of site 15 20 right of site 17 20 top of site 16 21 bottom of site 16 19
#     site 17 20 left of site 16 20 right of site 18 20 top of site 17 21 bottom of site 17 19
#     site 18 20 left of site 17 20 right of site 19 20 top of site 18 21 bottom of site 18 19
#     site 19 20 left of site 18 20 right of site 20 20 top of site 19 21 bottom of site 19 19
#     site 20 20 left of site 19 20 right of site 21 20 top of site 20 21 bottom of site 20 19
#     site 21 20 left of site 20 20 right of site 22 20 top of site 21 21 bottom of site 21 19
#     site 22 20 left of site 21 20 right of site 23 20 top of site 22 21 bottom of site 22 19
#     site 23 20 left of site 22 20 right of site 0 20 top of site 23 21 bottom of site 23 19
#     site 0 21 left of site 23 21 right of site 1 21 top of site 0 22 bottom of site 0 20
#     site 1 21 left of site 0 21 right of site 2 21 top of site 1 22 bottom of site 1 20
#     site 2 21 left of site 1 21 right of site 3 21 top of site 2 22 bottom of site 2 20
#     site 3 21 left of site 2 21 right of site 4 21 top of site 3 22 bottom of site 3 20
#     site 4 21 left of site 3 21 right of site 5 21 top of site 4 22 bottom of site 4 20
#     site 5 21 left of site 4 21 right of site 6 21 top of site 5 22 bottom of site 5 20
#     site 6 21 left of site 5 21 right of site 7 21 top of site 6 22 bottom of site 6 20
#     site 7 21 left of site 6 21 right of site 8 21 top of site 7 22 bottom of site 7 20
#     site 8 21 left of site 7 21 right of site 9 21 top of site 8 22 bottom of site 8 20
#     site 9 21 left of site 8 21 right of site 10 21 top of site 9 22 bottom of site 9 20
#     site 10 21 left of site 9 21 right of site 11 21 top of site 10 22 bottom of site 10 20
#     site 11 21 left of site 10 21 right of site 12 21 top of site 11 22 bottom of site 11 20
#     site 12 21 left of site 11 21 right of site 13 21 top of site 12 22 bottom of site 12 20
#     site 13 21 left of site 12 21 right of site 14 21 top of site 13 22 bottom of site 13 20
#     site 14 21 left of site 13 21 right of site 15 21 top of site 14 22 bottom of site 14 20
#     site 15 21 left of site 14 21 right of site 16 21 top of site 15 22 bottom of site 15 20
#     site 16 21 left of site 15 21 right of site 17 21 top of site 16 22 bottom of site 16 20
#     site 17 21 left of site 16 21 right of site 18 21 top of site 17 22 bottom of site 17 20
#     site 18 21 left of site 17 21 right of site 19 21 top of site 18 22 bottom of site 18 20
#     site 19 21 left of site 18 21 right of site 20 21 top of site 19 22 bottom of site 19 20
#     site 20 21 left of site 19 21 right of site 21 21 top of site 20 22 bottom of site 20 20
#     site 21 21 left of site 20 21 right of site 22 21 top of site 21 22 bottom of site 21 20
#     site 22 21 left of site 21 21 right of site 23 21 top of site 22 22 bottom of site 22 20
#     site 23 21 left of site 22 21 right of site 0 21 top of site 23 22 bottom of site 23 20
#     site 0 22 left of site 23 22 right of site 1 22 top of site 0 23 bottom of site 0 21
#     site 1 22 left of site 0 22 right of site 2 22 top of site 1 23 bottom of site 1 21
#     site 2 22 left of site 1 22 right of site 3 22 top of site 2 23 bottom of site 2 21
#     site 3 22 left of site 2 22 right of site 4 22 top of site 3 23 bottom of site 3 21
#     site 4 22 left of site 3 22 right of site 5 22 top of site 4 23 bottom of site 4 21
#     site 5 22 left of site 4 22 right of site 6 22 top of site 5 23 bottom of site 5 21
#     site 6 22 left of site 5 22 right of site 7 22 top of site 6 23 bottom of site 6 21
#     site 7 22 left of site 6 22 right of site 8 22 top of site 7 23 bottom of site 7 21
#     site 8 22 left of site 7 22 right of site 9 22 top of site 8 23 bottom of site 8 21
#     site 9 22 left of site 8 22 right of site 10 22 top of site 9 23 bottom of site 9 21
#     site 10 22 left of site 9 22 right of site 11 22 top of site 10 23 bottom of site 10 21
#     site 11 22 left of site 10 22 right of site 12 22 top of site 11 23 bottom of site 11 21
#     site 12 22 left of site 11 22 right of site 13 22 top of site 12 23 bottom of site 12 21
#     site 13 22 left of site 12 22 right of site 14 22 top of site 13 23 bottom of site 13 21
#     site 14 22 left of site 13 22 right of site 15 22 top of site 14 23 bottom of site 14 21
#     site 15 22 left of site 14 22 right of site 16 22 top of site 15 23 bottom of site 15 21
#     site 16 22 left of site 15 22 right of site 17 22 top of site 16 23 bottom of site 16 21
#     site 17 22 left of site 16 22 right of site 18 22 top of site 17 23 bottom of site 17 21
#     site 18 22 left of site 17 22 right of site 19 22 top of site 18 23 bottom of site 18 21
#     site 19 22 left of site 18 22 right of site 20 22 top of site 19 23 bottom of site 19 21
#     site 20 22 left of site 19 22 right of site 21 22 top of site 20 23 bottom of site 20 21
#     site 21 22 left of site 20 22 right of site 22 22 top of site 21 23 bottom of site 21 21
#     site 22 22 left of site 21 22 right of site 23 22 top of site 22 23 bottom of site 22 21
#     site 23 22 left of site 22 22 right of site 0 22 top of site 23 23 bottom of site 23 21
#     site 0 23 left of site 23 23 right of site 1 23 top of site 0 0 bottom of site 0 22
#     site 1 23 left of site 0 23 right of site 2 23 top of site 1 0 bottom of site 1 22
#     site 2 23 left of site 1 23 right of site 3 23 top of site 2 0 bottom of site 2 22
#     site 3 23 left of site 2 23 right of site 4 23 top of site 3 0 bottom of site 3 22
#     site 4 23 left of site 3 23 right of site 5 23 top of site 4 0 bottom of site 4 22
#     site 5 23 left of site 4 23 right of site 6 23 top of site 5 0 bottom of site 5 22
#     site 6 23 left of site 5 23 right of site 7 23 top of site 6 0 bottom of site 6 22
#     site 7 23 left of site 6 23 right of site 8 23 top of site 7 0 bottom of site 7 22
#     site 8 23 left of site 7 23 right of site 9 23 top of site 8 0 bottom of site 8 22
#     site 9 23 left of site 8 23 right of site 10 23 top of site 9 0 bottom of site 9 22
#     site 10 23 left of site 9 23 right of site 11 23 top of site 10 0 bottom of site 10 22
#     site 11 23 left of site 10 23 right of site 12 23 top of site 11 0 bottom of site 11 22
#     site 12 23 left of site 11 23 right of site 13 23 top of site 12 0 bottom of site 12 22
#     site 13 23 left of site 12 23 right of site 14 23 top of site 13 0 bottom of site 13 22
#     site 14 23 left of site 13 23 right of site 15 23 top of site 14 0 bottom of site 14 22
#     site 15 23 left of site 14 23 right of site 16 23 top of site 15 0 bottom of site 15 22
#     site 16 23 left of site 15 23 right of site 17 23 top of site 16 0 bottom of site 16 22
#     site 17 23 left of site 16 23 right of site 18 23 top of site 17 0 bottom of site 17 22
#     site 18 23 left of site 17 23 right of site 19 23 top of site 18 0 bottom of site 18 22
#     site 19 23 left of site 18 23 right of site 20 23 top of site 19 0 bottom of site 19 22
#     site 20 23 left of site 19 23 right of site 21 23 top of site 20 0 bottom of site 20 22
#     site 21 23 left of site 20 23 right of site 22 23 top of site 21 0 bottom of site 21 22
#     site 22 23 left of site 21 23 right of site 23 23 top of site 22 0 bottom of site 22 22
#     site 23 23 left of site 22 23 right of site 0 23 top of site 23 0 bottom of site 23 22
# 

# In[97]:

print successful_flip, misfire
plt.imshow(lattice,cmap='gist_gray_r')


# Out[97]:

#     46886 53114
# 

#     <matplotlib.image.AxesImage at 0xb008ccac>

# image file:

# In[ ]:



