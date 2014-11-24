#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>
#include <string.h>
#define LENGTH 6        /* system+boundary layer size is LENGTH*LENGTH */
#define BUFSIZE (LENGTH-2)*(LENGTH-2)        /* system size*/
#define TEMP   1.0         /* TEMP in units of interaction and k_B */
#define WARM   1000  
#define MCS    1250

int    total_energy( int [][LENGTH], int [] , int []);
int    total_mag( int [][LENGTH]);

double ran3( long int *);
float  fpow (float , float);
float  mag_analytic(float);
/* total number of processes "nworkers", identity of each process "rank" */
int	nworkers, rank, NP;
int spin[LENGTH][LENGTH];
int nbr1[LENGTH];
int nbr2[LENGTH];
long int iseed=-35433454;
/* structure defining the variables of the grid topology */
typedef struct GRID_INFO_TYPE{
int p;
MPI_Comm comm;
MPI_Comm row_comm;
MPI_Comm col_comm;
int q;
int my_row;
int my_col;
int my_rank;
}GRID_INFO_TYPE;

void   print_config (GRID_INFO_TYPE* grid, int [][LENGTH] , int );
/* set up the grid-topology */
void Setup_grid(GRID_INFO_TYPE* grid);
void initialize(GRID_INFO_TYPE* grid, int [][LENGTH], int [] , int []);
void mcmove(GRID_INFO_TYPE* grid, int[][LENGTH] , int [] , int [] );
/* communicate the state of the spins at the boundaries to neighbors */
void boundary(GRID_INFO_TYPE* grid, int[][LENGTH] , int [] , int [] );
int coordinates[2];

main (int argc, char **argv) 
{
/* Allocate memory for the  structure grid */
GRID_INFO_TYPE *grid = (GRID_INFO_TYPE *)malloc(sizeof(GRID_INFO_TYPE));
    /* Initialize MPI */
MPI_Init(&argc, &argv);
    /* Find out this process number */
MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    /* Find out the number of processes */
MPI_Comm_size(MPI_COMM_WORLD, &nworkers);

Setup_grid(grid);

   int itime;
   int i;
   int big_energy,E;
   int big_mag,M;
   double E_per_spin;
   double M_per_spin;
   NP=sqrt(nworkers);
   iseed=iseed*(rank+1);
     itime = 0;
     big_energy = 0;
     big_mag = 0;
/* get started */
   initialize(grid,spin, nbr1, nbr2);
	boundary(grid,spin, nbr1, nbr2);

/* warm up system */
     for (i = 1 ; i <= WARM; i++) 
     { 
	     itime = i;
	     mcmove(grid,spin, nbr1, nbr2);
	boundary(grid,spin, nbr1, nbr2);
     }

/* do Monte Carlo steps and collect stuff for averaging */
     for (i = (WARM + 1) ; i <= MCS; i++) 
     { 
  	itime = i;
	mcmove(grid,spin, nbr1, nbr2);
	if(i!=MCS)boundary(grid,spin, nbr1, nbr2);
	   big_mag = big_mag + total_mag(spin);
	   big_energy = big_energy + total_energy(spin,nbr1,nbr2);
     }
     printf("Mag  %f rank %d time %d\n", 1.0*big_mag/(MCS-WARM), rank, MCS-WARM);
     MPI_Reduce (&big_mag, &M,1,MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD); /* process 0 adds total magentization from each process to find the net magnetization. */ 
     MPI_Reduce (&big_energy, &E,1,MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
     if(rank==0)
     {
      M_per_spin = (float)M/((MCS - WARM)*(nworkers*(LENGTH-2)*(LENGTH-2)));
      E_per_spin = (float)E/((MCS - WARM)*nworkers*((LENGTH-2)*(LENGTH-2)));

// finish off 
     printf("Mag  %d Mag/spin %lf rank %d\n",M, M_per_spin, rank);
     printf("Energy  %d Energy/spin %lf rank %d\n",E, E_per_spin, rank);
     printf("Analytic: Mag/spin %f, Energy/spin -2 to 0\n", mag_analytic(TEMP));
     printf("Temperature %lf, Edge length of system %d \n", TEMP , LENGTH);
     printf("No. of warm-up steps %d, No. of MCS %d \n", WARM , MCS);

     }
print_config(grid, spin, itime ); 
MPI_Finalize();  /* exit all MPI functions */
}

void initialize(GRID_INFO_TYPE* grid,int spin[][LENGTH], int nbr1[], int nbr2[])
{
 int i, ix, iy,m,n,mt,nt,tag=50; float sd;
  char message[100];
     for (iy = 0 ; iy <LENGTH; iy++) /* start with random spins */
     for (ix = 0 ; ix <LENGTH; ix++)
     { sd=ran3(&iseed);
       if( sd>0.5 )spin[ix][iy] = 1; 
       if( sd <= 0.5 )spin[ix][iy] = -1; }
     for (i = 1 ; i < LENGTH-1 ; i++)  /* set up neighbor list */ 
     {
       nbr1[i] = i - 1;
       nbr2[i] = i + 1;
      }
}

int total_mag( int spin[][LENGTH] )        /* total magnetization */
{
	int i, ix, iy,cx,cy;
	int foom;
        foom = 0;
        for (iy =1  ; iy < LENGTH-1; iy++) /* start magnetized all spins = 1 */
        for (ix = 1 ; ix < LENGTH-1; ix++)
 	     foom = foom + spin[ix][iy];
 	return(foom);
}

int total_energy( int spin[][LENGTH] , int nbr1[] , int nbr2[])
{                                             /* total energy */
	int ix, iy, cx, cy;
	int fooe;
	fooe = 0;
              for (iy =1  ; iy < LENGTH-1; iy++) /* start magnetized all spins = 1 */
              for (ix =1 ; ix < LENGTH-1; ix++)
		 fooe = fooe - spin[ix][iy] * spin[ix][nbr1[iy]]
		             - spin[ix][iy] * spin[nbr2[ix]][iy];
	 return(fooe);
}

void mcmove(GRID_INFO_TYPE* grid, int spin[][LENGTH], int nbr1[] , int nbr2[])
{

/* ONE MONTE CARLO STEP by Metropolis: Flip probability 1 if Enew < Eold, 
   else prob is exp -(Enew-Eold)/T.  Simplified here since only there 
   are five cases in d=2 for external field = 0.
   FLIP WITH prob1   prob2    1.0     1.0     1.0   (Below spins called)
               +       -       -       -       -           ss2
             + + +   + + +   + + -   + + -   - + -      ss1 ss0 ss3
               +       +       +       -       -           ss4          */

  int i, ix, iy, cx, cy,m,n,nt,mt,tag=50;
  int ixpick, iypick;
  int ss0, ss1, ss2, ss3, ss4, de;
  int flag;
  long int idum;
  double prob1 , prob2;
 int *U1,*D1,*R1,*L1;
  char message[100];
/* arrays to recieve the spin configuration from neighbors */
     U1=(int *)malloc(LENGTH*sizeof(int));
     D1=(int *)malloc(LENGTH*sizeof(int));
     R1=(int *)malloc(LENGTH*sizeof(int));
     L1=(int *)malloc(LENGTH*sizeof(int));
   MPI_Status status;
  MPI_Cart_shift(grid->comm,0,-1,&m,&n);
  MPI_Recv(U1,LENGTH, MPI_INT,n,tag,MPI_COMM_WORLD,&status); /* receive U1 buffer with dimension LENGTH of type MPI_INT from process "n" with "tag" */
  MPI_Cart_shift(grid->comm,0,1,&m,&n);
  MPI_Recv(D1,LENGTH, MPI_INT,n,tag,MPI_COMM_WORLD,&status);
  MPI_Cart_shift(grid->comm,1,-1,&m,&n);
  MPI_Recv(L1,LENGTH, MPI_INT,n,tag,MPI_COMM_WORLD,&status);
  MPI_Cart_shift(grid->comm,1,1,&m,&n);
  MPI_Recv(R1,LENGTH, MPI_INT,n,tag,MPI_COMM_WORLD,&status);
  prob1 = exp(-8.0/TEMP);
  prob2 = exp(-4.0/TEMP);
  for (i = 1 ; i < LENGTH-1; i++)
  {
   spin[i][0]=U1[i];
   spin[i][LENGTH-1]=D1[i];
   spin[0][i]=R1[i];
   spin[LENGTH-1][i]=L1[i];
//   if(grid->my_rank==12)printf("mcmove-1 %d %d %d \n",i, U1[i],D1[i]);
  }
	free(U1);
	free(D1);
	free(L1);
	free(R1);
        //    print_config (grid,spin,i);
  for (i = 1 ; i <= (LENGTH-1)*(LENGTH-1) ; i++)
  {
	  ixpick = floor((LENGTH-2) * ran3(&idum)+0.5);	  
	  iypick = floor((LENGTH-2) * ran3(&idum)+0.5);	  
      ss0 = spin [ixpick]       [iypick]       ;     
      ss1 = spin [nbr1[ixpick]] [iypick]       ;
      ss2 = spin [ixpick]       [nbr1[iypick]] ;
      ss3 = spin [nbr2[ixpick]] [iypick]       ;
      ss4 = spin [ixpick]       [nbr2[iypick]] ;

      de =  2*ss0*(ss1+ss2+ss3+ss4);

      flag = 1;                     /* flip spin if flag = 1 */

             if ( (de == 8) && (ran3(&idum) > prob1)
			||    
         	  (de == 4) && (ran3(&idum) > prob2) )     
	     flag = 0;
	 
       spin[ixpick][iypick] = (1 - 2*flag )*spin[ixpick][iypick];
  }

}

void boundary(GRID_INFO_TYPE* grid, int spin[][LENGTH], int nbr1[] , int nbr2[])
{
 int i,*U2,*D2,*R2,*L2,m,n,tag=50;
     U2=(int *)malloc(LENGTH*sizeof(int));
     D2=(int *)malloc(LENGTH*sizeof(int));
     R2=(int *)malloc(LENGTH*sizeof(int));
     L2=(int *)malloc(LENGTH*sizeof(int));
/* put  the spins at the left, right, up and down boundaries into separate arrays */
     for (i = 1 ; i < LENGTH-1 ; i++)    
     {  U2[i]=spin[i][1];
       D2[i]=spin[i][LENGTH-2];
       L2[i]=spin[1][i];
       R2[i]=spin[LENGTH-2][i];
      }
/*
send the boundary arrays to appropriate neighbor process
Remeber 0 is up and down and  1 is left and right. 
*/
       MPI_Cart_shift(grid->comm,0,-1,&m,&n); /* find the neighbor process down the current one */ 
       MPI_Send(U2,LENGTH, MPI_INT,n,tag,MPI_COMM_WORLD); /* send U2 buffer with dimension LENGTH of type MPI_INT to  process "n" with "tag" */
       MPI_Cart_shift(grid->comm,0,1,&m,&n);
       MPI_Send(D2,LENGTH, MPI_INT,n,tag,MPI_COMM_WORLD);
       MPI_Cart_shift(grid->comm,1,1,&m,&n);
       MPI_Send(R2,LENGTH, MPI_INT,n,tag,MPI_COMM_WORLD);
       MPI_Cart_shift(grid->comm,1,-1,&m,&n);
       MPI_Send(L2,LENGTH, MPI_INT,n,tag,MPI_COMM_WORLD);
	free(U2);
	free(D2);
	free(L2);
	free(R2);
}

void print_config(GRID_INFO_TYPE *grid, int spin[][LENGTH] , int itime )
{
   int ix , iy, i,buf[(LENGTH-2)],buf1[LENGTH-2],tag=147,n,mp,np;
   char fname[30],message[50];
   float cx[1];
   FILE* fpr;
   MPI_Status status;
   if(grid->my_rank!=0)/* if rank is not zero pack all spins into a 1-d array */
   {
         i=0;
        for (iy =1  ; iy < LENGTH-1; iy++) 
       {
        for (ix = 1 ; ix < LENGTH-1; ix++)
            { 
		buf[i]=spin[iy][ix]; 
		i++;
	    }
         }
         MPI_Send(buf,BUFSIZE,MPI_INT,0,tag,MPI_COMM_WORLD); /* send it to process 0 */
   }
   else  /* if the rank is zero */
  { fpr=fopen("config","w");  /* open the file */
     for (iy =1  ; iy < LENGTH-1; iy++) /* print the own configuration*/
     {
     for (ix = 1 ; ix < LENGTH-1; ix++)
       { 
        fprintf(fpr,"%d \t", spin[iy][ix]);
       }
        fprintf(fpr," \n");
     }
     for (n=1 ; n<nworkers;n++)
     {
        sprintf(message,"process-%d \n",n);
        fprintf(fpr," %s \n", message);
        MPI_Recv(buf1,BUFSIZE, MPI_INT,n,tag,MPI_COMM_WORLD,MPI_STATUS_IGNORE); /* receive from all other processes */ 
        for(i=0; i<(LENGTH-2);i++)
        {
         for (ix = i*(LENGTH-2) ; ix < (i+1)*(LENGTH-2); ix++)
           { 
            fprintf(fpr,"%d \t", buf1[ix]);
            printf("%d \t%d \t\n", ix, buf1[ix]);
           }
            fprintf(fpr," \n");
        }
    }
    fclose(fpr);
  }
}


#define Tc 2.2691853142130216092 

float mag_analytic(float temp)     /* analytic solution for magnetization */
{
 int i;
 float mag;
   if (temp >= Tc) mag = 0.0;
   else            mag = fpow( (1.0-pow(sinh(2.0/temp),-4)) , 0.125);
 return(mag);
}

float fpow ( float x , float power )     /* raises to a noninteger power */
{
 float thing;
 thing = exp ( power * log ( x ) );
 return(thing);
}

#include <stdlib.h>         
#define MBIG 1000000000
#define MSEED 161803398              /* portable random number generator */
#define MZ 0                         /* from numerical recipes book */
#define FAC (1.0/MBIG)
 
double ran3(long *idum)
{
  static int inext,inextp;
  static long ma[56];
  static int iff=0;
  long mj,mk;
  int i,ii,k;
  
  if (*idum < 0 || iff == 0){
      iff=1;
      mj = labs(MSEED-labs(*idum));
      mj %= MBIG;
      ma[55]=mj;
      mk=1;
      for (i=1;i<=54;i++){
          ii=(21*i) % 55;
          ma[ii]=mk;
          mk=mj-mk;
          if (mk < MZ) mk += MBIG;
          mj =ma[ii];
      }
      for (k=1;k<=4;k++)
          for (i=1;i<=55;i++) {
              ma[i] -= ma[1+(i+30) % 55];
              if (ma[i] < MZ) ma[i] += MBIG;
          }
      inext=0;
      inext=31;
      *idum=1;
  }
  if (++inext == 56) inext=1; 
  if (++inextp == 56) inextp=1; 
  mj =ma[inext]-ma[inextp];
  if (mj < MZ) mj += MBIG;
  ma[inext] =mj;
  return mj*FAC;
}


void Setup_grid(GRID_INFO_TYPE* grid){
int dimensions[2];
int periods[2];
int varying_coords[2];
MPI_Comm   localname;

MPI_Comm_size(MPI_COMM_WORLD, (&grid->p)); /* get the total number of processes */
grid->q=(int)sqrt((double) grid->p);  /* square grid  */ 
dimensions[0]=dimensions[1]=grid->q;   /* dimension of the grid */
periods[0]=periods[1]=1;  /*  periodic if 1 and non-periodic if 0 */

MPI_Cart_create(MPI_COMM_WORLD, 2, dimensions, periods, 1, &(grid->comm)); /* create a grid communicator from the "Comm_world" , having dimension 2, reorder the process to processor mapping */

MPI_Comm_rank(grid->comm, &(grid->my_rank));
MPI_Cart_coords(grid->comm, grid->my_rank,2,coordinates);
grid->my_row=coordinates[0];
grid->my_col=coordinates[1];
varying_coords[0]=0;varying_coords[1]=1;
MPI_Cart_sub(grid->comm,varying_coords,&(grid->row_comm));
varying_coords[0]=1;varying_coords[1]=0;
MPI_Cart_sub(grid->comm,varying_coords,&(grid->col_comm));

}

