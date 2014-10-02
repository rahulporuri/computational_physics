
# first we initialize the position and momentum of the particles
# then we define an interaction potential u(r), in our case the lennard-jones potantial, and we calculate the force on particles due to a lennard-jones potential. this force is a function of r, the distance between two objects.
# 
# for particle i,
#     we calculate the distances r_ij
#     we calculate the angles theta_ij
#     we measure the forces by calling the function for the values r_ij
#     we take the x, y components of these forces using cos & sin theta_ij and save them in 2 arrays i.e force in the x direction and force in the y direction. either we save them in an array and then add them up or keep adding pxdot and pydot having initialized them properly on the fly.
# we do this for all particles and save the total force pxdot and pydot for each of these particles in 2 arrays.
# 
# we now update the momentum using the velocity verlet method, using the forces pxdot and pydot for px and py correspondingly. mind you, this is to be done for all particles at once. do not update the particle momenta or positions in the i loop!
# 
# !! one cycle would therefore contain distance and angle measurement, force measurement and components for all particles in the system followed by an update to the positions and momenta of all particles at once !!

# http://www.sklogwiki.org/SklogWiki/index.php/Lennard-Jones_model //
# 
# http://www.sklogwiki.org/SklogWiki/index.php/Argon //
# 
# we intend to use \epsilon/k_B = 119.8 K and \sigma = 0.3405 nm
# 

# In[32]:

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import nano, pico, N_A, m_p
get_ipython().magic(u'matplotlib inline')


# In[29]:

atoms = np.zeros([9,2,2])
# atoms[i] refers to the ith particle
# atoms[i][0] refers to the particle's x,y positions : atoms[i][0][0], atoms[i][0][1]
# atoms[i][1] refers to the particle's x,y momenta : atoms[i][1][0], atoms[i][1][1]


# In[30]:

for i in xrange(9):
    atoms[i][0][0] = i%3
    atoms[i][0][1] = i/3
    atoms[i][1][0] = 1
    atoms[i][1][1] = 1
atoms = atoms*nano


# In[42]:

# for a potential [(alpha/r)^6-(alpha/r)^12], the force is the negative derivative of this potential.
def force(r):
    return 24*e*(2*(sigma/r)**13-(sigma/r)**7)/sigma


# In[48]:

forcex = np.zeros(len(atoms))
forcey = np.zeros(len(atoms))

sigma = 0.3405*nano
e = 997/N_A
#def force_all():
for i in xrange(len(atoms)):
#    rij = []
#    thetaij = []
    pxdot = 0
    pydot = 0
    for j in xrange(len(atoms)):
        if j != i :
            r = np.sqrt(np.power((atoms[i][0][0] - atoms[j][0][0]),2) + np.power((atoms[i][0][1] - atoms[j][0][1]),2))
            theta = np.arctan((atoms[j][0][1] - atoms[i][0][1])/(atoms[j][0][0] - atoms[i][0][0]))
            #print i, j
            #print "distance", r
            #print "angle", theta, theta*180/np.pi
            #note that theta is now in radians and has to be converted to degrees before being used in np.cos or np.sin
    #        rij.append(r)
    #        thetaij.append(theta)
            theta = theta*180/np.pi
            pxdot += force(r)*np.cos(theta)
            pydot += force(r)*np.sin(theta)
    forcex[i] = pxdot
    forcey[i] = pydot
    #return forcex, forcey


# In[49]:

print forcex, forcey


# Out[49]:

#     [ -3.74475435e-14  -1.01698213e-13  -3.74475435e-14  -1.27041436e-14
#       -7.96383878e-14  -1.27041436e-14  -3.74475435e-14  -1.01698213e-13
#       -3.74475435e-14] [ -6.06566019e-14  -5.56196639e-14  -5.05827259e-14   7.27231147e-30
#        5.52202634e-30   0.00000000e+00   6.06566019e-14   5.56196639e-14
#        5.05827259e-14]
# 

# In[53]:

step = 1.*np.power(10,6)
#while t < np.power(10,5):
for i in xrange(len(atoms)):
    # first momentum half step
    atoms[i][1][0] = atoms[i][1][0] + forcex[i]*step/2 # px update
    atoms[i][1][1] = atoms[i][1][1] + forcey[i]*step/2 # py update
    # position update full step
    atoms[i][0][0] = atoms[i][0][0] + atoms[i][1][0]*step # x update
    atoms[i][0][1] = atoms[i][0][1] + atoms[i][1][1]*step # y update
    # second momentum half step
    atoms[i][1][0] = atoms[i][1][0] + forcex[i]*step/2 # px update
    atoms[i][1][1] = atoms[i][1][1] + forcey[i]*step/2 # py update


# In[54]:

atoms


# Out[54]:

#     array([[[ -1.77238082e-02,  -2.93283606e-02],
#             [ -3.64475810e-08,  -5.96566626e-08]],
#     
#            [[ -4.98492064e-02,  -2.68098866e-02],
#             [ -1.00698315e-07,  -5.46197195e-08]],
#     
#            [[ -1.77238062e-02,  -2.42914125e-02],
#             [ -3.64475810e-08,  -4.95827765e-08]],
#     
#            [[ -5.35208348e-03,   1.00000200e-03],
#             [ -1.17041563e-08,   1.00000000e-09]],
#     
#            [[ -3.88192716e-02,   1.00000200e-03],
#             [ -7.86384675e-08,   1.00000000e-09]],
#     
#            [[ -5.35208148e-03,   1.00000200e-03],
#             [ -1.17041563e-08,   1.00000000e-09]],
#     
#            [[ -1.77238082e-02,   3.13283646e-02],
#             [ -3.64475810e-08,   6.16566626e-08]],
#     
#            [[ -4.98492064e-02,   2.88098906e-02],
#             [ -1.00698315e-07,   5.66197195e-08]],
#     
#            [[ -1.77238062e-02,   2.62914165e-02],
#             [ -3.64475810e-08,   5.15827765e-08]]])

# In[ ]:




# In[ ]:

def force():
    force_matrix = np.zeros([len(atoms),2])
    for site in xrange(len(atoms)):
        force_matrix[site] = force_particle(site)
    return force_matrix

def force_particle(site):
    temp = 0
    for i in xrange(len(atoms)):
        if i != site:
            temp += ((a/r)**12 - (a/r)**6)
            


# In[131]:

e = 119.8*1.3806488/np.power(10,23)
#e = 1
#e = 997/N_A
sigma = 1
#sigma = 0.3405 # units of nm
#m_p = 1.67262178/np.power(10,27)
#m = 1
#m = np.power(10,6)*m_p

r = np.linspace(0.1,10,100)
#r = np.linspace(0.01,10,1000) # units of nm

force = 24*e*(2*(sigma/r)**12-(sigma/r)**6)/r
#acc = (24.*e**(2.*(sigma/r)**12-(sigma/r)**6)/r)/m
#energy = 4.*e*((sigma/r)**12-(sigma/r)**6)

#plt.hold(True)
plt.plot(force)
#plt.plot(energy)
#plt.plot(acc)
#plt.ylim([-10,10])
plt.xlim([0,2])
#print force


# Out[131]:

#     (0, 2)

# image file:

# In[ ]:

# plot the force wrt r
# we have e and sigma as the parameters in force and sigma should have the units of r.


# In[5]:

print 1./np.power(10,9)


# Out[5]:

#     1e-09
# 

# In[9]:

from scipy.constants import nano, pico


# In[12]:

l = 50.*pico


# In[13]:

print l


# Out[13]:

#     5e-11
# 

# In[14]:

print np.linspace(100*pico,nano,10)


# Out[14]:

#     [  1.00000000e-10   2.00000000e-10   3.00000000e-10   4.00000000e-10
#        5.00000000e-10   6.00000000e-10   7.00000000e-10   8.00000000e-10
#        9.00000000e-10   1.00000000e-09]
# 

# In[33]:

sigma = 0.3405*nano
print sigma
e = 997/N_A
print e


# Out[33]:

#     3.405e-10
#     1.65555730427e-21
# 

# In[39]:

r = np.linspace(10*pico,1*nano,100)
sigma = 0.3405*nano
plt.plot(24*e*((sigma/r)**13-(sigma/r)**7)/sigma)
plt.xlim([0,2])
#plt.ylim([-50000,50000])


# Out[39]:

#     (0, 2)

# image file:

# In[40]:

24*e*((sigma/r)**13-(sigma/r)**7)/sigma


# Out[40]:

#     array([  9.65074530e+09,   1.17806945e+06,   6.05319047e+03,
#              1.43806934e+02,   7.90581129e+00,   7.38893078e-01,
#              9.95986721e-02,   1.75516507e-02,   3.79542237e-03,
#              9.64455292e-04,   2.79229948e-04,   9.00267910e-05,
#              3.17650927e-05,   1.21002151e-05,   4.92253336e-06,
#              2.11982749e-06,   9.59281262e-07,   4.53351791e-07,
#              2.22562544e-07,   1.12969146e-07,   5.90374043e-08,
#              3.16419190e-08,   1.73282134e-08,   9.66055242e-09,
#              5.46194470e-09,   3.11863854e-09,   1.78941114e-09,
#              1.02531211e-09,   5.81579230e-10,   3.22174020e-10,
#              1.70163626e-10,   8.13617667e-11,   3.00411334e-11,
#              1.04410684e-12,  -1.46484213e-11,  -2.24451671e-11,
#             -2.56076194e-11,  -2.61079595e-11,  -2.51380516e-11,
#             -2.34146055e-11,  -2.13638273e-11,  -1.92340313e-11,
#             -1.71647575e-11,  -1.52293982e-11,  -1.34615629e-11,
#             -1.18713961e-11,  -1.04556566e-11,  -9.20390588e-12,
#             -8.10226728e-12,  -7.13566752e-12,  -6.28913229e-12,
#             -5.54849627e-12,  -4.90075432e-12,  -4.33419663e-12,
#             -3.83841742e-12,  -3.40425334e-12,  -3.02368589e-12,
#             -2.68972909e-12,  -2.39631455e-12,  -2.13818122e-12,
#             -1.91077325e-12,  -1.71014771e-12,  -1.53289255e-12,
#             -1.37605437e-12,  -1.23707550e-12,  -1.11373934e-12,
#             -1.00412315e-12,  -9.06557363e-13,  -8.19590641e-13,
#             -7.41959797e-13,  -6.72564015e-13,  -6.10442717e-13,
#             -5.54756567e-13,  -5.04771168e-13,  -4.59843048e-13,
#             -4.19407622e-13,  -3.82968829e-13,  -3.50090214e-13,
#             -3.20387232e-13,  -2.93520607e-13,  -2.69190600e-13,
#             -2.47132043e-13,  -2.27110039e-13,  -2.08916230e-13,
#             -1.92365566e-13,  -1.77293481e-13,  -1.63553443e-13,
#             -1.51014817e-13,  -1.39560998e-13,  -1.29087777e-13,
#             -1.19501918e-13,  -1.10719899e-13,  -1.02666821e-13,
#             -9.52754386e-14,  -8.84853116e-14,  -8.22420591e-14,
#             -7.64966988e-14,  -7.12050652e-14,  -6.63272951e-14,
#             -6.18273721e-14])

# In[ ]:

def sum_force(site):
    for i in xrange(len(atoms)):
        if site != i:
            np.dist(atoms[i][0]-atoms[site][0])

