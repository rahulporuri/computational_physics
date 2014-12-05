#include <stdio.h>
#include <stdlib.h>
//#include <time.h>

void main()
{
	
	int spin[100] = { 0 }; // the rest of the elemends in the array will be set to zero by default unless specified!
	// int array[size] = {0}; if you intend to initialize the whole array to be zero
	//spin[n] = { 1,2 };
	int neighbour_table[200] = {0};
	int i; // print counter, random integer load counter
	int j; // monte carlo time counter
	int temp = 0;
	int sum_magnetization = 0;
	//clock_t t;// (void)
	//t = clock();
	//int *spins[n]; //** and *** for 2d and 3d arrays
	//a = 10;
	//printf("%d\n",a);
	// spin = (int*) malloc(n*sizeof(int))
	//spin[n] = { 1,2,3 };
	for (i = 0; i < 100; i++)
	{
		//printf("%d\n", spin[i]);
		//fputs("Hello, World!\n",stdout);
		//spin[i] = rand()%100;
		temp = rand()%100;// we get numbers between 0 and 100!
		//temp = rand()%10; had i done this, i would've gotten numbers between 0 and 9.
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
	
	/*for (i = 0; i < 100; i++)
	{
		printf("%d\n", spin[i]);
		//fputs("Hello, World!\n",stdout);
	//	spin[i] = rand();
	}*/
/*
	for (i = 0; i < 100; i++)
	{
		//printf("%d\n", spin[i]);
		//fputs("Hello, World!\n",stdout);
	//	spin[i] = rand();
		sum_magnetization += spin[i];
	}

	printf("sum magnetization = %d\n",sum_magnetization);

	for (i = 1; i < 99; i++)
	{
		temp = spin[i-1]*spin[i] + spin[i]*spin[i+1];
		printf("neighbour energy = %i at site %i \n",temp,i);
	}
	//fputs(sum_energy,stdout); no!
/*	for (j=0; j < 1000; j++)
	{

	}*/
	return;
}