/*****************************************************************************
                      C-DAC Tech Workshop : hyPACK-2013 
                         October 15-18, 2013 

 Example               : omp-matmat-three-parallel.c

 Objective             : Matrix - Matrix Multiplication using

                  	 OpenMP three PARALLEL for directive and Private Clause

 Input                 :  Size of Matrices(i.e Size of Matrix A and Matrix B) ie in terms of
                  	  CLASS where CLASS A :1024; CLASS B: 2048 and CLASS C: 4096
                  	  Number of Threads .

 Output                : Number of Threads
                  	 Total Memory Utilized for the Matrix - Matrix Computation
                  	 Total Time Taken for Matrix - Matrix Computaion.
	                                            
 Created               : August-2013

 E-mail                : hpcfte@cdac.in     

************************************************************************/

#include <stdio.h>
#include <sys/time.h>
#include <omp.h>
#include <stdlib.h>

/*              Function declaration            */ 
void Matrix_Multiplication_Three(double **Matrix_A,double **Matrix_B,double **Result,int N_size,int Total_threads);


/* Main Program */
main(int  argc , char * argv[])
{
	int             CLASS_SIZE,N_size, i,j,k,Total_threads,THREADS;
	double          Total_overhead = 0.0;
	double         **Matrix_A, **Matrix_B, **Result;
        double           memoryused=0.0;
        int             iteration;
 	FILE            *fp;
	char            * CLASS;

       /* Checking for the command line arguments */        
        if( argc != 3 ){

           printf("\t\t Very Few Arguments\n ");
           printf("\t\t Syntax : exec <Size of Matrix(Square matrix)> <Threads>\n");
           exit(-1);
        }
        else {
           N_size = atoi(argv[1]);
           THREADS = atoi(argv[2]);
        }
        Total_threads = THREADS;   		
        printf("\n\t\t Matrix Size :  %d",N_size);
        printf("\n\t\t Threads     :  %d",Total_threads);
        printf("\n");
	
	/* Matrix_A Elements */

	Matrix_A = (double **) malloc(sizeof(double *) * N_size);
	for (i = 0; i < N_size; i++) {
		Matrix_A[i] = (double *) malloc(sizeof(double) * N_size);
		for (j = 0; j < N_size; j++)
		{
		//	srand48((unsigned int)N_size);
		//	Matrix_A[i][j] = (double)(rand()%10);
			Matrix_A[i][j] = i+j;
		}
			
	}

	/* Matrix_B Elements */

	Matrix_B = (double **) malloc(sizeof(double *) * N_size);
	for (i = 0; i < N_size; i++) {
		Matrix_B[i] = (double *) malloc(sizeof(double) * N_size);
		for (j = 0; j < N_size; j++)
		{
	        //	 srand48((unsigned int)N_size);
                  //      Matrix_B[i][j] = (double)(rand()%10);
			Matrix_B[i][j] = i+j;
		}
	
	}

	/* Dynamic Memory Allocation */

	Result = (double **) malloc(sizeof(double *) * N_size);

	for (i = 0; i < N_size; i++) 
		Result[i] = (double *) malloc(sizeof(double) * N_size);

        memoryused = (3*(N_size*N_size))*sizeof(double);
	
	/* Function Calling   */
       Matrix_Multiplication_Three(Matrix_A,Matrix_B,Result,N_size,Total_threads);
	/* Free Memory     */
 
	free(Matrix_A);
	free(Matrix_B);
	free(Result);


}/* Main function end    */

/* Functions implementation   */

void Matrix_Multiplication_Three(double **Matrix_A,double **Matrix_B,double **Result,int N_size,int Total_threads)
{
	int             i,j,k;	
//	gettimeofday(&TimeValue_Start, &TimeZone_Start);
	
        /* set the no. of threads */
	omp_set_num_threads(Total_threads);
	
	/* OpenMP Three For Directive :Fork a team of threads giving them their own copies of variables    
         * Spawn a parallel region explicitly scoping all variables 
        */ 
	#pragma omp parallel for private (j,k) shared (Matrix_A,Matrix_B,Result,N_size) num_threads(Total_threads) 
	for (i = 0; i < N_size; i = i + 1)
	{
        #pragma omp parallel for private(k) shared (Matrix_A,Matrix_B,Result,N_size) num_threads(Total_threads) 	
		for (j = 0; j < N_size; j = j + 1)
		{
		 		Result[i][j]=0.0;
        	    #pragma omp parallel for private(k) shared (Matrix_A,Matrix_B,Result,N_size) num_threads(Total_threads)
				for (k = 0; k < N_size; k = k + 1)
					Result[i][j] = Result[i][j] + Matrix_A[i][k] * Matrix_B[k][j];

		}
     }/* end of parallel section */

}

