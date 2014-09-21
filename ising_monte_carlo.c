#include <stdio.h>
#include <math.h>

'''

initialise array
N = 10^5 (iterations over lattice size) and n = 144 (lattice size)
for i < N 
	for i < n
		calculate energy
		random no. generator -> to choose site!
		flip spin and calculate energy
		if energy diff < 0
			flip
		if energy diff > 0
			random no. generator -> to flip with probability
			if '''' > exp(betaXdeltaE)
				flip
			else 
				dont flip
	calculate energy
	save data in file

function to calculate energy at every iteration

shashi says!
> initialise 1) cold start and 2) hot start
> neighbor table
here we initialise 4 arrays which store the positions of the l, r, u & b positions of every position i in the initialised array.
---> r = (i+1+L)%L
---> l = (i-1+L)%N
---> u = (i+L)%N
---> b = (i-L+N)%N
where i is the position of the site in the 1D array. for N sites.
> MC sweep
> declare rand. no. generator
> probability
> energy or observable measurement and write

'''

'''
in python - 
1. checked the random.random and random.uniform distrubutions
2. checked the random.choice distribution to choose one of the array elements
'''

---> we initialise the spin lattice
spins = np.zeros(12,12)
for i in xrange(12):
	for j in xrange(12):
		tmp = np.random.random()
		if tmp > 1./2:
			spins[i,j] = +1
		elif tmp < 1./2:
			spins[i,j] = -1

plt.ion()
plt.imshow(spins)

kB = 6.023*1e-23
T = 500
beta = kB*T
energy = []

---> function to sum the interaction energy b/w nearest neighbors
def sum_neighbors(array, site):
	return array[site%12-1, site/12]*array[site%12, site/12] + array[site%12+1, site/12]*array[site%12, site/12] + array[site%12, site/12-1]*array[site%12, site/12] + array[site%12, site/12 + 1]*array[site%12, site/12]

---> the monte carlo routine
flip_posn = np.arange(144) # the position on the lattice we choose to flip!
for i in xrange(100000):
	for i in xrange(144):
		site = np.random.choice()
		initial_e = sum_neighbors(spins,site)
		spins[site%12, site/12] = -spins[site%12, site/12]
		final_e = sum_neighbors(spins,site)
		if initial_e - final_e < 0 :
			#move to next cycle
		elif initial_e - final_e < 0 :
			temp = np.random.random()
			if temp < np.exp(-beta*(initial_e - final_e)):
				# move to next cycle
			elif temp > np.exp(-beta*(initial_e - final_e)):
				spins[site%12, site/12] = -spins[site%12, site/12]
	# measure energy of the system
	energy.append("")