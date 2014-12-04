#include <stdio.h>
#include <stdlib.h>

/*
the main function should start with void main(){... return}
while subroutines should start with int main(){... return out}
the main function can also be defined as int main(){... return 0}
*/

void main()
{
	//float a;
	//int a;
	//int n;
	//n = 10;
	//int spin[n]; // not preferred because we will not be changing the actual value at the memory location. array[][], array[][][] for 2d and 3d respectively.
	int spin[10] = { 1,2 }; // the rest of the elemends in the array will be set to zero by default unless specified!
	// int array[size] = {0}; if you intend to initialize the whole array to be zero
	//spin[n] = { 1,2 };
	int i;
	//int *spins[n]; //** and *** for 2d and 3d arrays
	//a = 10;
	//printf("%d\n",a);
	// spin = (int*) malloc(n*sizeof(int))
	//spin[n] = { 1,2,3 };
	for (i = 0; i < 10; i++)
	{
		printf("%d\n", spin[i]);
	}
	return;
}

/*
in the printf statement - 
	c for a single character
	s for a string
	d or i for integer where as 
	f for float
*/