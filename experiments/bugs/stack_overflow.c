#include <stdio.h>
#include <string.h>

void cause_stack_overflow() {
    char buffer[4];
    
    memset(buffer, 'A', 10);
    
    printf("Buffer: %s\n", buffer);
}

int main() {
    cause_stack_overflow();
    return 0;
}