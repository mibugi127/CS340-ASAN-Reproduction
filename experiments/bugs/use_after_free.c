#include <stdlib.h>

int main(void) {
    volatile int *p = (volatile int *)malloc(sizeof(int));
    *p = 1;
    free((void *)p);
    return *p;
}