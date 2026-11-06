#include <stdio.h>

#define N 500

static double a[N][N], b[N][N], c[N][N];

int main(void) {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            a[i][j] = i + j;
            b[i][j] = i - j;
        }
    for (int i = 0; i < N; i++)
        for (int k = 0; k < N; k++)
            for (int j = 0; j < N; j++)
                c[i][j] += a[i][k] * b[k][j];
    printf("%f\n", c[0][0]);
    return 0;
}