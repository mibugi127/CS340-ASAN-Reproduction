#include <stdio.h>
#include <stdlib.h>

#define CHUNK_MB 32
#define ROUNDS 3
#define PAGE 4096

int main(void) {
    size_t chunk = (size_t)CHUNK_MB * 1024 * 1024;
    unsigned char acc = 0;

    for (int r = 0; r < ROUNDS; r++) {
        volatile unsigned char *p = malloc(chunk);
        if (!p) {
            fprintf(stderr, "allocation failed\n");
            return 1;
        }
        for (size_t i = 0; i < chunk; i += PAGE)
            p[i] = (unsigned char)(i + r);
        acc ^= p[(size_t)r * PAGE % chunk];
        free((void *)p);
    }

    printf("%u\n", (unsigned)acc);
    return 0;
}
