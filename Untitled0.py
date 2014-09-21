
#     https://docs.python.org/2/library/random.html - random number generators in python.

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


# Out[11]:

#     the mean of the random.random output is 0.508082509051 
#     the variance of the random.random output is 0.0828779728855 
#     the mean of the random.uniform output is 0.50030226968 
#     the variance of the random.uniform output is 0.0824666758476
# 

# image file:

# In[17]:

z = [1,2,3,4,5,6,7]
print np.random.choice(z)


# Out[17]:

#     2
# 

# In[45]:

spins = np.zeros([12,12])
for i in xrange(0,12):
    for j in xrange(0,12):
        tmp = np.random.random()
        if tmp > 1./2:
            spins[i,j] = 1
        elif tmp < 1./2:
            spins[i,j] = -1
            
print spins
plt.imshow(spins)


# Out[45]:

#     [[ 1. -1. -1. -1. -1. -1. -1.  1.  1. -1.  1. -1.]
#      [ 1.  1. -1.  1. -1. -1.  1. -1.  1. -1.  1. -1.]
#      [ 1. -1. -1. -1. -1. -1.  1.  1.  1.  1. -1. -1.]
#      [ 1. -1.  1.  1.  1. -1.  1.  1.  1.  1.  1. -1.]
#      [-1. -1.  1. -1.  1.  1. -1. -1.  1.  1.  1. -1.]
#      [-1.  1. -1.  1.  1. -1.  1. -1.  1.  1.  1.  1.]
#      [ 1. -1. -1. -1.  1.  1.  1. -1.  1.  1.  1. -1.]
#      [ 1.  1.  1. -1.  1.  1. -1. -1. -1. -1. -1.  1.]
#      [-1. -1.  1. -1. -1. -1. -1. -1. -1. -1.  1.  1.]
#      [ 1.  1. -1. -1.  1.  1. -1. -1.  1.  1.  1.  1.]
#      [-1. -1.  1. -1.  1.  1.  1.  1.  1.  1. -1.  1.]
#      [ 1. -1.  1. -1. -1.  1.  1. -1. -1. -1. -1. -1.]]
# 

#     <matplotlib.image.AxesImage at 0xaf9c238c>

# image file:

# In[49]:

spins[11,11]


# Out[49]:

#     -1.0

# In[*]:

import numpy as np
import matplotlib.pyplot as plt
posns = np.arange(0,144)
m = []
for i in xrange(144):
    tmp = np.random.choice(posns)
    m.append(posns)


# In[ ]:



