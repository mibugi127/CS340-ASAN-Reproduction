#include <stdlib.h>
#include <stdio.h>

int main(void) {
    int *a = (int *)malloc(4 * sizeof(int));
    a[4] = 42;
    printf("%d\n", a[4]);
    free(a);
    return 0;
}