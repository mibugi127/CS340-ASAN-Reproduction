#include <stdlib.h>
#include <stdio.h>

int main(void) {
    int * volatile p = (int *)malloc(sizeof(int));
    
    printf("Before free 1\n");
    free(p);
    
    printf("Before free 2\n");
    free(p);
    
    return 0;
}