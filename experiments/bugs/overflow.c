#include <stdlib.h>
#include <stdio.h>

int main() {
    volatile int *arr = (int *)malloc(10 * sizeof(int));
    
    for (int i = 0; i < 10; i++) {
        arr[i] = i;
    }
    
    arr[20] = 42; 
    
    printf("Value: %d\n", arr[20]);
    
    free((void*)arr);
    return 0;
}