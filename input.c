#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <time.h>
#include <math.h>
void rand_str(char *dest, size_t length) {
    char charset[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    while (length-- > 0) {
        size_t index = (double) rand() / RAND_MAX * (sizeof charset - 1);
        *dest++ = charset[index];
    }
    *dest = '\0';
}


int main()
{
int rows=1000000;
int n[rows];
double p[rows];
srand(time(0)); 
 for(int i = 0; i<rows; i++) {
       n[i]=rand();
       p[i]=(double) n[i]; 
       char str[] = { [89] = '\1' };
	   rand_str(str, sizeof str - 1);
       printf("%0.0f %s\n", p[i],str); 
   }
return 0;
}