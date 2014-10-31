
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

# In[2]:

#import scipy.integrate as spyint
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
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


# In[10]:

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


# In[24]:

plt.plot(dist, r_m_array)
plt.title('r_m vs distance')
plt.xlabel('distance s in m')
plt.ylabel('distance to closest approach r_m in m')


# Out[24]:

#     <matplotlib.text.Text at 0xb0131fcc>

# image file:

# In[28]:

plt.plot(dist*1e9,theta)
plt.title('theta vs distance')
plt.xlabel('distance s in m')
plt.ylabel(r'$\theta$ in rads')


# Out[28]:

#     <matplotlib.text.Text at 0xaff84bcc>

# image file:

# In[19]:

delta_dist = dist[2] - dist[3]
diff = np.gradient(theta,delta_dist)

c = s/np.sin(theta)
sigma = c/np.abs(diff)
sigma_theory = (q*q/(4.0*E))**2*(1.0/np.sin(theta/2))**4


# In[31]:

plt.hold(True)
plt.semilogy(theta,sigma)
plt.semilogy(theta,sigma_theory)

plt.ylabel(r'$\sigma(\Omega)$')
plt.xlabel(r'$\theta$ (in rads)')
plt.title(r'scattering cross section vs $\theta$')
plt.legend(['Numerical Result','Theoretical Result'],loc=7)
plt.show()


# Out[31]:

# image file:

# In[32]:

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
        
    plt.plot(dist*1e9,theta, label=v)    
    theta = np.zeros(len(dist))
    
plt.legend(loc='upper right')
plt.title(r'variation of scattering angle $\theta$ with initial velocity in m/s')
plt.xlabel('distance s in m')
plt.ylabel(r'$\theta$ in rads')


# Out[32]:

#     <matplotlib.text.Text at 0xafd9cc4c>

# image file:

# In[33]:

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
        
    plt.plot(dist*1e9,theta, label = m)
    theta = np.zeros(len(dist))
    
plt.legend(loc='center right')
plt.title(r'variation of scattering angle $\theta$ with mass of scattered particle')
plt.xlabel('distance s in m')
plt.ylabel(r'$\theta$ in rads')


# Out[33]:

#     <matplotlib.text.Text at 0xafde842c>

# image file:

# In[ ]:



