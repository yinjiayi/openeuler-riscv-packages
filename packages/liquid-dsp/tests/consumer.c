/* SPDX-License-Identifier: MIT
 * Copyright (c) 2026 yinjiayi
 * Downstream installed-interface acceptance, not an upstream test replacement.
 */
#include <complex.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <liquid/liquid.h>

int main(void)
{
    if (strcmp(liquid_libversion(), "1.8.3") != 0 ||
        liquid_libversion_number() != LIQUID_VERSION_NUMBER)
        return 1;
    float complex input[8] = {1.0f}, output[8] = {0};
    if (fft_run(8, input, output, LIQUID_FFT_FORWARD, 0) != LIQUID_OK)
        return 2;
    for (unsigned i = 0; i < 8; ++i)
        if (!isfinite(crealf(output[i])) || !isfinite(cimagf(output[i])) ||
            cabsf(output[i] - 1.0f) > 1e-5f)
            return 3;
    unsigned char message[] = "123456789";
    unsigned key = crc_generate_key(LIQUID_CRC_32, message, 9);
    if (!crc_validate_message(LIQUID_CRC_32, message, 9, key))
        return 4;
    message[4] ^= 1;
    if (crc_validate_message(LIQUID_CRC_32, message, 9, key))
        return 5;
    puts("downstream installed version/FFT impulse/CRC corruption checks passed");
    return 0;
}
