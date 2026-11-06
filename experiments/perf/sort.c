#include <stdio.h>
#include <stdlib.h>

#define N 1000000

static int cmp(const void *x, const void *y) {
    int a = *(const int *)x, b = *(const int *)y;
    return (a > b) - (a < b);
}

int main(void) {
    int *v = (int *)malloc(N * sizeof(int));
    unsigned seed = 12345;
    for (int i = 0; i < N; i++) {
        seed = seed * 1103515245u + 12345u;
        v[i] = (int)(seed >> 16);
    }
    qsort(v, N, sizeof(int), cmp);
    printf("%d\n", v[N / 2]);
    free(v);
    return 0;
}