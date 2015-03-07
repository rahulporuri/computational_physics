import numpy as np
import matplotlib.pyplot as plt

a = 100
alist = np.arange(0,a+1,1)
anotherlist = np.zeros(iterations)
count = 0.
iterations = 100
for i in xrange(iterations):
    tempx = np.random.choice(alist)
    tempy = np.random.choice(alist)
    if tempx**2 + tempy**2 < (a**2)+1:
        count += 1.
    anotherlist[i] = count/(i+1)*4.


print anotherlist[-1]
plt.plot(anotherlist)
plt.show()
'''
a = 100
alist = np.arange(0,a+1,1)
andanotherlist = []
for iterations in [10+1,10**2+1,10**3+1,10**4+1,10**5+1,10**6+1]:
    #anotherlist = np.zeros(iterations)
    count = 0.
    #iterations = 100
    for i in xrange(iterations):
        tempx = np.random.choice(alist)
        tempy = np.random.choice(alist)
        if tempx**2 + tempy**2 < (a**2)+1:
            count += 1.
        #anotherlist[i] = count/(i+1)*4.
    andanotherlist.append(count/iterations*4.)

plt.plot(andanotherlist,'o')

a = 1000
alist = np.arange(0,a+1,1)
andanotherlist = []
for iterations in [10+1,10**2+1,10**3+1,10**4+1,10**5+1,10**6+1]:
    #anotherlist = np.zeros(iterations)
    count = 0.
    #iterations = 100
    for i in xrange(iterations):
        tempx = np.random.choice(alist)
        tempy = np.random.choice(alist)
        if tempx**2 + tempy**2 < (a**2)+1:
            count += 1.
        #anotherlist[i] = count/(i+1)*4.
    andanotherlist.append(count/iterations*4.)

plt.plot(andanotherlist,'o')
'''
