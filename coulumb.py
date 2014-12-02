#Coulumb Scattering
#Sivaramakrishnan H
#EP11B024

import math
from gaussxw import gaussxw
from numpy import ones,arange


def f(u):
    return (s/(1-V(u)/E-(s*s)*(u*u))**0.5)
def V(u):
    return k*u

wr_file = open('op_values.txt', 'w')

#Define s
#s=1e-15

#Define l,V,E

e_ch = 1.67e-19 #electronic charge
m = 1.6e-27     #mass of proton
alp = 9e9       #coulumb constant

z1 = 1 * e_ch
z2 = 1 * e_ch
k = alp*z1*z2
#V=k*z1*z2*u
E=1e3 * e_ch    # 1 keV



#Define a and b

n=3
til_w = ones(n,float)
til_x = ones(n,float)


#Define w and x

x,w = gaussxw(n)

#Define til_w and til_x



#Integration

for q in arange(2.5e-15,1e-10,2.5e-15):
    s=q
    psi = 0
    l=(2*m*E*s*s)**0.5
    a = 0
    b = (1/(2*E*s*s))*(-k+(k*k+4*E*E*s*s)**0.5)
    for i in range(n):
        til_w[i] = w[i] * (b-a)*0.5
        til_x[i] = ((b-a)*x[i]+(b+a))*0.5
    for j in range(n):
        psi = psi + til_w[j] * f(til_x[j])
    theta = 180*(math.pi- 2*psi)/math.pi
    line = str(s)+','+str(theta)
    #print line
    wr_file.write(line+'\n')

wr_file.close()
    
