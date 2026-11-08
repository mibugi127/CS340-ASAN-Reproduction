#include <stdio.h>

int main(void) {
    volatile double s = 0.0;
    for (long i = 0; i < 100000000L; i++)
        s += (double)(i % 97);
    printf("%f\n", s);
    return 0;
}