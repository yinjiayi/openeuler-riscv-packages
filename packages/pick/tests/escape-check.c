/* SPDX-License-Identifier: MIT */
/* Functional length regression only, not a memory-safety or native claim. */
#define main pick_program_main
#include "../pick.c"
#undef main
#include <assert.h>

int
main(void)
{
    static const struct {
        const char *text;
        size_t length;
    } cases[] = {
        { "", 0 },
        { "plain", 0 },
        { "\033", 0 },
        { "\033[", 2 },
        { "\033[31", 4 },
        { "\033]title", 7 },
        { "\033[31m", 5 },
        { "\033]title\a", 8 }
    };
    size_t i;
    for (i = 0; i < sizeof(cases) / sizeof(cases[0]); i++)
        assert(skipescseq(cases[i].text) == cases[i].length);
    puts("PASS pick eight escape-length regressions");
    return 0;
}
