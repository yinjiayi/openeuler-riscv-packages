/* SPDX-License-Identifier: ISC
 * Copyright (c) 2026 yinjiayi
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */
/* Package-added functional ABI checks, not an upstream or scientific suite. */
#include <libred.h>
#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define REQUIRE(c) do { if (!(c)) { fprintf(stderr, "FAIL line %d: %s\n", __LINE__, #c); exit(1); } } while (0)

int main(void)
{
    double r, g, b, x, y, x0, y0, x1, y1, dx, dy, t, elevation;
    long temperature;
    errno = 0;
    REQUIRE(libred_get_colour(999, &r, &g, &b) == -1 && errno == EDOM);
    errno = 0;
    REQUIRE(libred_get_colour_xy(999, &x, &y) == -1 && errno == EDOM);
    /* Exercise every table row and an interpolated point in every interval. */
    for (temperature = 1000; temperature <= 40000; temperature += 50) {
        REQUIRE(libred_get_colour(temperature, &r, &g, &b) == 0);
        REQUIRE(isfinite(r) && isfinite(g) && isfinite(b));
        REQUIRE(r >= 0 && r <= 1.000000000001 && g >= 0 && g <= 1.000000000001 && b >= 0 && b <= 1.000000000001);
        REQUIRE(libred_get_colour_xy(temperature, &x, &y) == 0);
        REQUIRE(isfinite(x) && isfinite(y) && x > 0 && y > 0 && x + y < 1);
    }
    REQUIRE(libred_get_colour(6500, &r, &g, &b) == 0);
    REQUIRE(fabs(r - 1) < 1e-12 && fabs(g - 1) < 1e-12 && fabs(b - 1) < 1e-12);
    REQUIRE(libred_get_colour_xy(6500, &x0, &y0) == 0);
    REQUIRE(fabs(x0 - 0.312727) < 1e-12 && fabs(y0 - 0.329023) < 1e-12);
    t = libred_get_temperature_xy(x0, y0, &dx, &dy);
    REQUIRE(isfinite(t) && fabs(t - 6500) < 1e-6 && fabs(dx) < 1e-12 && fabs(dy) < 1e-12);
    REQUIRE(fabs(libred_get_temperature_xy(x0, y0, NULL, NULL) - 6500) < 1e-6);
    t = libred_get_temperature(r, g, b, NULL, NULL, NULL, NULL);
    REQUIRE(isfinite(t) && t >= 1000 && t <= 40000);
    REQUIRE(libred_get_colour_xy(6600, &x1, &y1) == 0);
    REQUIRE(libred_get_colour_xy(6550, &x, &y) == 0);
    REQUIRE(fabs(x - (x0 + x1) / 2) < 1e-12 && fabs(y - (y0 + y1) / 2) < 1e-12);
    REQUIRE(libred_get_colour_xy(40000, &x0, &y0) == 0);
    REQUIRE(libred_get_colour_xy(50000, &x, &y) == 0);
    REQUIRE(fabs(x - x0) < 1e-12 && fabs(y - y0) < 1e-12);
    REQUIRE(libred_solar_elevation(0, 0, &elevation) == 0);
    REQUIRE(isfinite(elevation) && elevation >= -90 && elevation <= 90);
    REQUIRE(LIBRED_IS_NIGHTTIME(-30) && LIBRED_IS_DAYTIME(30));
    REQUIRE(LIBRED_IS_BLUE_HOUR(-5) && LIBRED_IS_GOLDEN_HOUR(0));
    puts("PASS libred package-added full-table/interpolation/errors/shared-static functional consumer");
    return 0;
}
