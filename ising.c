#include <stdio.h>
#include <stdlib.h>
//#include <time.h>

void main()
{
	
	int spin[100] = { 0 };
	int neighbour_table[200] = {0};
	int i; // print counter, random integer load counter
	int j; // monte carlo time counter
	int temp = 0;
	int sum_magnetization = 0;
	for (i = 0; i < 100; i++)
	{
		temp = rand()%100;
		if (temp>50)
		{
			spin[i] = -1;
		}
		else
		{
			spin[i] = +1;
		}
	}
	for (i = 0; i < 100; i++)
	{
		neighbour_table[2*i] = i-1;
		neighbour_table[2*i+1] = i+1;
	}
	for (i = 0; i < 100; ++i)
	{
		printf("%d and %d are the neighbours of %d\n", neighbour_table[2*i], neighbour_table[2*i+1], i);
	}
	for (i = 0; i < 100; i++)
	{
		sum_magnetization += spin[i];
	}
	printf("sum magnetization = %d\n",sum_magnetization);
	for (i = 1; i < 99; i++)
	{
		temp = spin[i-1]*spin[i] + spin[i]*spin[i+1];
		printf("neighbour energy = %i at site %i \n",temp,i);
	}
	return;
}

#define sum_magnetization(typedef struct )
#define neighbour_table()
#define sum_energy()
#define neighbour_energy()
/*
the algorithm is
mctime
choose a site at random
check energy
flip it
check energy
if post_e - pre_e < 0
go on
if post_e - pre_e > 0
temp = rand() b/w 0 and 1
if temp < exp(bj*delta) 
go on
else
flip back

int pre_flip_e
int post_flip_e
int mctime
int site
int delta
for (mctime = 0; mctime < 1000; mctime++)
{
	site = rand()%100;
	pre_flip_e = neighbour_energy(site);
	spin[site] = -spin[site];
	post_flip_e = neighbour_energy(site);
	delta = post_flip_e - pre_flip_e;
	if delta < 0
	{
		//go on
	}
	else
	{
		temp = rand()%100;
		if temp < exp(bj*delta)
		{
			//go on
		}
		else
		{
			spin[site] = -spin[site];
		}
	}
}
*/