/* SPDX-License-Identifier: MIT */
#include <stdio.h>

static unsigned long read_counter(void)
{
#if defined(__x86_64__)
    unsigned int low;
    unsigned int high;
    __asm__ volatile("rdtsc" : "=a"(low), "=d"(high));
    return ((unsigned long)high << 32) | low;
#elif defined(__riscv)
#error "golden failure: x86-only counter lacks a RISC-V implementation"
#else
    return 0;
#endif
}

int main(void)
{
    printf("%lu\n", read_counter());
    return 0;
}
