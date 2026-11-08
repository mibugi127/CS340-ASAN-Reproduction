#include <stdio.h>

int main(void) {
    volatile int a[4];
    a[4] = 1;
    printf("%d\n", a[4]);
    return 0;
}