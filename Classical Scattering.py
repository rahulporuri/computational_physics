
# Numerical solution to Classical Scattering
# ==============
# 
# We attempt to numerically solve the classical scattering problem for a central potantial of the type \frac{k}{r}. To start with, we assumed that the particle being scattered and the particle causing the scattering are the same i.e protons. Later on in the analysis, we study how the scattering differs when the mass of the particle being scattered varies. 
# 
# We solved the integral 
# 
# $$\theta = \pi - 2\int_{0}^{u_m}\frac{sdu}{((1-\frac{V}{E})-s^2 u^2)^{1/2}}$$
# 
# using the gaussian quadrature method. The predefined quadrature function in the scipy.integrate library was used.
# 
# We solved the following quadratic equation using the np.roots function to obtain r_m which is the distance to point of closest approach.
# 
# $$\frac{dr}{dt} = (\frac{2}{m})^{1/2}(E-V-\frac{l^2}{2mr^2})^{1/2}$$
# 
# 

# the analysis is as follows - 
# 
# 1. the dependence of $r_m$ on s
# 2. the variation of $\theta$ with s 
# 3. plot the scattering function $\sigma(\Omega)$ against s and comparison with the theoretical value
# 4. variation in the $\theta$ vs s plot with change in velocity
# 5. variation in the $\theta$ vs s plot with change in mass of scattered particle

# In[36]:

import scipy.integrate as spyint
import numpy as np
import matplotlib.pyplot as plt
#get_ipython().magic(u'matplotlib inline')
import warnings
warnings.filterwarnings('ignore')
# python -W ignore foo.py - to supress the accuracy warnings that pop up during the quadrature routine

def func(u,s):
    return (s/(1-(k*u)/E-(s*s)*(u*u))**0.5)

m = 1.67262178*1e-27 #mass of proton in kg
q = 1.60217657*1e-19 #charge of proton in coulombs
k = q*q*9e+09

v = 3e+05
E = (1.0/2.0)*m*v*v

dist = np.linspace(1e-15,1e-10,100)
theta = np.zeros(len(dist))
r_m_array = np.zeros(len(dist))

print "computing roots of the quadratic equation to obtain r_m and computing theta using gaussian quadrature"

# In[37]:

for i in xrange(len(dist)):
    s = dist[i]
    l = m*s*v
    
    coeff = [E, -k, -(l*l)/(2*m)]
    r_m = np.roots(coeff)[0]
    
    b = 1/r_m
    psi = spyint.quadrature(func, 0, b, args= [s], maxiter=50)[0]
    
    I = np.pi - 2*psi
    theta[i] = I
    r_m_array[i] = r_m


# In[38]:

print "showing variation of r_m vs dist from horizontal axis"

plt.plot(dist, r_m_array)
plt.show()


# Out[38]:

# image file:

# In[39]:

print "showing variation of theta vs distance from horizontal axis"

plt.plot(dist*1e9,theta)
plt.show()


# Out[39]:

# image file:

# In[40]:

print "computing scattering cross section"

delta_dist = dist[2] - dist[3]
diff = np.gradient(theta,delta_dist)

c = s/np.sin(theta)
sigma = c/np.abs(diff)
sigma_theory = (k/(8*E*E*np.sin(theta/2)))**2


# In[41]:

plt.hold(True)
plt.semilogy(theta,sigma)
plt.semilogy(theta,sigma_theory)

plt.ylabel(r'$\sigma$ (in $m^{-2}$)')
plt.xlabel(r'$\theta$ (in rads)')
plt.title(r'Classical Scaterring')
plt.legend(['Numerical Result','Theoretical Result'],loc=7)
plt.show()


# Out[41]:

# image file:

# In[42]:

print "computing variation of scattering angle for different velocities"

V = np.linspace(3e+04, 3e+05,5)
plt.hold(True)
for v in V:
    for i in xrange(len(dist)):
        s = dist[i]
        E = (1.0/2.0)*m*v*v
        l = m*s*v
        
        coeff = [E, -k, -(l*l)/(2*m)]
        r_m = np.roots(coeff)[0]
        
        b = 1/r_m
        psi = spyint.quadrature(func, 0, b, args= [s], maxiter=50)[0]
        
        I = np.pi - 2*psi
        theta[i] = I
        
    plt.plot(dist*1e9,theta)    
    theta = np.zeros(len(dist))

plt.show()
# Out[42]:

# image file:

# In[43]:

print "computing variation of scattering angle for different masses"

m_p = 1.67262178*1e-27 #mass of proton in kg
M = np.linspace(m_p*1e-03, m_p,4)
plt.hold(True)
for m in M:
    for i in xrange(len(dist)):
        s = dist[i]
        E = (1.0/2.0)*m*v*v
        l = m*s*v
        
        coeff = [E, -k, -(l*l)/(2*m)]
        r_m = np.roots(coeff)[0]
        
        b = 1/r_m
        psi = spyint.quadrature(func, 0, b, args= [s], maxiter=50)[0]
        
        I = np.pi - 2*psi
        theta[i] = I
        
    plt.plot(dist*1e9,theta)    
    theta = np.zeros(len(dist))

plt.show()
# Out[43]:

# image file:

# In[ ]:



