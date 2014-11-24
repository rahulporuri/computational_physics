/*
*   This program evaluates the trapezoidal rule estimate
*   for an integral of F(x). In this case, F(x) is exp(x)
*   evaluated for the interval of 0 to 1. Each case provides
*   2X increase in precision. Therefore each result should be
*   similar but, not the same.
*
*   Testing for Nps 1 ... 11 should execute programs.
*   Testing for Nps 12 and above should stop the program.
*
*   This program requires the following call(s)
*             MPI_Init
*             MPI_Comm_rank
*             MPI_Comm_size
*             MPI_Abort
*             MPI_Finalize
*
*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "mpi.h"

#define F(x) (exp(x))
main (int argc, char **argv) 
{
double	TN, SUM, X, H,T1,T2,DH,res,
	A = 0.0,
	B = 1.0;
int	nworkers, whoami, i, errcode;

    /* Initialize MPI */
MPI_Init(&argc, &argv);
    /* Find out this processor number */
MPI_Comm_rank(MPI_COMM_WORLD, &whoami);
    /* Find out the number of processors */
MPI_Comm_size(MPI_COMM_WORLD, &nworkers);
DH=(B-A)/nworkers;

whoami = whoami + 1;
T1=A+(whoami-1)*DH;
T2=A+whoami*DH;
H=(T2-T1)/50.0;
SUM = 0.0;
for (i = 0; i <=49; i++)
     SUM = SUM+F(T1+H*i)+F(T1+H*(i+1));
TN = SUM*H;
printf("whoami %d\t, T1= %f\t, T2= %f\t, TN %f \n", whoami-1, T1, T2, TN);
//MPI_Bcast (&TN,1,MPI_DOUBLE, 1, MPI_COMM_WORLD);
MPI_Reduce (&TN, &res,1,MPI_DOUBLE, MPI_SUM, 1, MPI_COMM_WORLD);

if(whoami==2)printf("Integral = %10.6f\n",res);
MPI_Finalize();
}

