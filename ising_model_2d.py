
# coding: utf-8

                    https://docs.python.org/2/library/random.html - random number generators in python.
                
# In[11]:

import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
plt.ion()

x = []
for i in xrange(10000):
    tmp = np.random.random()
    x.append(tmp)

plt.hist(x,100);

y = []
for i in xrange(10000):
    tmp = np.random.uniform(0,1)
    y.append(tmp)

print "the mean of the random.random output is", np.mean(x), "\n" "the variance of the random.random output is", np.var(x), "\n" "the mean of the random.uniform output is", np.mean(y), "\n" "the variance of the random.uniform output is", np.var(y)
    
plt.subplot(121)
plt.hist(x,100);
plt.subplot(122)
plt.hist(y,100);


# In[94]:

array = np.arange(144)
a = []
for i in xrange(14400):
    tmp = np.random.choice(array)
    a.append(tmp)
plt.hist(a,144);


# In[95]:

#---> we initialise the spin lattice
#---> random start
spins = np.zeros([12,12])
for i in xrange(12):
	for j in xrange(12):
		tmp = np.random.random()
		if tmp > 1./2:
			spins[i,j] = +1
		elif tmp < 1./2:
			spins[i,j] = -1
            
plt.imshow(spins)


# In[34]:

import numpy as np
import matplotlib.pyplot as plt
import time
get_ipython().magic(u'matplotlib inline')

kB = 6.023*1e-23
T = 500
beta = kB*T
energy = []

#---> function to sum the interaction energy b/w nearest neighbors
def sum_neighbors(array, site):
	if site < 132:
		return array[(site-1)%12, site/12]*array[site%12, site/12] + array[(site+1)%12, site/12]*array[site%12, site/12] + array[site%12, site/12-1]*array[site%12, site/12] + array[site%12, site/12 + 1]*array[site%12, site/12]
	if site > 131:
		site = 143-site
		return array[(site-1)%12, site/12]*array[site%12, site/12] + array[(site+1)%12, site/12]*array[site%12, site/12] + array[site%12, site/12-1]*array[site%12, site/12] + array[site%12, site/12 + 1]*array[site%12, site/12]


# In[88]:

spins = np.ones([12,12])
plt.imshow(spins,cmap='gist_gray_r')
successful_flip = 0
misfire = 0
flip_posn = np.arange(144)
for i in xrange(10000):
    site = np.random.choice(flip_posn)
    #print "site to flip", site, "x,y", site%12, site/12
    initial_e = sum_neighbors(spins,site)
    #print initial_e
    spins[site%12,site/12] = -spins[site%12,site/12]
    final_e = sum_neighbors(spins,site)
    #print final_e
    #print np.exp()
    if final_e - initial_e < 0:
    #    print "flip!"
        successful_flip += 1
    else :
        tmp = np.random.random()
        if tmp < np.exp(-(final_e-initial_e)):
    #        print "flip!"
            successful_flip += 1
        else:
            spins[site%12,site/12] = -spins[site%12,site/12]
    #        print "no flip!"
            misfire += 1


# In[90]:

print successful_flip, misfire
plt.imshow(spins,cmap='gist_gray_r')


# In[3]:

import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[27]:

spins = np.ones(200)
#accepted_moves = 0
#global_e = []

beta = 1
J = 0.5

def energy_local(site):
    if site == 0:
        return spins[site]*spins[site+1]
    elif site == len(spins)-1 :
        return spins[site]*spins[site-1]
    else :
        return spins[site]*spins[site-1] + spins[site]*spins[site+1]

def global_energy():
    #return beta*J*spins[:]*spins[:-1]
    temp = 0
    for i in xrange(len(spins)-1):
        temp += spins[i]*spins[i+1]
    return beta*J*temp

for n in xrange(-3,3):
    beta = np.power(10,n)
    plt.hold(True)
    plt.legend(loc='upper right')
    global_e = []
    accepted_moves = 0
    for i in xrange(1000):        
        site = np.random.choice(np.linspace(0,199,200))
        pre_flip_e = energy_local(site)
        spins[site] = -spins[site]
        post_flip_e = energy_local(site)
        if post_flip_e - pre_flip_e < 0:
            global_e.append(global_energy())
            accepted_moves += 1
        else :
            temp = np.random.random()
            if temp < np.exp(-beta*J*(post_flip_e - pre_flip_e)):
                global_e.append(global_energy())
                accepted_moves += 1
            else :
                spins[site] = -spins[site]
                global_e.append(global_energy())
    print "accepted_moves", accepted_moves, "n", n
    plt.plot(global_e,label=n)


# In[29]:

plt.plot(global_e,label=n)
plt.legend(loc = 'upper right')


# In[ ]:



