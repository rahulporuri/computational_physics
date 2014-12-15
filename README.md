computational physics
====

implemented so far
- classical scattering
-- need to correct the codes to fix the difference between the theoretical and simulated values.
- ising model in 1d and 2d
-- to be implemented in C/C++, followed by an implementation using MPI.
- molecular dynamics using the velocity verlet algorithm
-- need to correct the radial distribution function to consider constant bin size instead of leaving it up to matplotlib.pyplot.hist
-- correct the parallelized implementation to measure force
- NVT hard ball using monte carlo
-- correct the radial distribution function
- NVT and NPT using monte carlo
-- correct the radial distribution function
-- correct the parallized implementation to measure force
- RK2 and RK4 to study a simple harmonic oscillator

to implement
- quantum scattering
- anharmonic oscillator using RK4, coupled harmonic oscillator and n-coupled harmonic oscillator
- unbrella sampling and the free energy of a polymer
- entropic sampling, entropy of an ising model and it's free energy
- differential equation solver i.e solutions to the wave equation and the heat equation
