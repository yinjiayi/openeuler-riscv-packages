/* SPDX-License-Identifier: Apache-2.0 */
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

static uint64_t probe_zba(uint64_t base, uint64_t index) {
    uint64_t result;
    __asm__ volatile("sh1add %0, %1, %2" : "=r"(result) : "r"(index), "r"(base));
    return result;
}

static uint64_t probe_zbb(uint64_t lhs, uint64_t rhs) {
    uint64_t result;
    __asm__ volatile("andn %0, %1, %2" : "=r"(result) : "r"(lhs), "r"(rhs));
    return result;
}

static uint64_t probe_zbs(uint64_t value, uint64_t bit) {
    uint64_t result;
    __asm__ volatile("bset %0, %1, %2" : "=r"(result) : "r"(value), "r"(bit));
    return result;
}

int main(void) {
    const uint64_t zba = probe_zba(7, 5);
    const uint64_t zbb = probe_zbb(UINT64_C(0xff), UINT64_C(0x0f));
    const uint64_t zbs = probe_zbs(0, 7);
    if (zba != 17 || zbb != UINT64_C(0xf0) || zbs != UINT64_C(0x80)) {
        fprintf(stderr, "RVA23 extension probe failed: zba=%" PRIu64
                        " zbb=%" PRIu64 " zbs=%" PRIu64 "\n",
                zba, zbb, zbs);
        return 1;
    }
    puts("RVA23 representative instruction probe: pass (Zba/Zbb/Zbs)");
    return 0;
}

