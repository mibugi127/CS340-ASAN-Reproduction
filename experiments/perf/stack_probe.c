#include <stdio.h>

static long vmstk_kb(void) {
    FILE *f = fopen("/proc/self/status", "r");
    char line[256];
    long kb = -1;
    if (!f) return -1;
    while (fgets(line, sizeof(line), f))
        if (sscanf(line, "VmStk: %ld kB", &kb) == 1) break;
    fclose(f);
    return kb;
}

int main(void) {
    volatile char buf[16][64];
    for (int i = 0; i < 16; i++) buf[i][0] = (char)i;
    printf("VmStk_kB=%ld\n", vmstk_kb());
    return 0;
}