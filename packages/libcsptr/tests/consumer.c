/* SPDX-License-Identifier: MIT
 * Copyright (c) 2026 yinjiayi
 * Downstream interface/regression checks, not an upstream test replacement.
 */
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <csptr/array.h>

static int calls;
static int expected[3] = {7, 11, 13};
static int token = 2026;

static void destroy_element(void *ptr, void *meta)
{
    s_meta_array *array_meta = meta;
    assert(calls >= 0 && calls < 3);
    assert(*(int *) ptr == expected[calls]);
    assert(array_meta != NULL);
    assert(array_meta->nmemb == 3 && array_meta->size == sizeof(int));
    assert(*(int *) (array_meta + 1) == token);
    ++calls;
}

static void inspect(int *a)
{
    assert(a != NULL);
    assert(array_length(a) == 3);
    assert(array_type_size(a) == sizeof(int));
    assert(*(int *) array_user_meta(a) == token);
    for (size_t i = 0; i < 3; ++i)
        assert(a[i] == expected[i]);
}

int main(void)
{
    int *a = shared_ptr(int[3], {7, 11, 13}, destroy_element,
                       {&token, sizeof(token)});
    inspect(a);
    int *b = sref(a);
    assert(a == b);
    sfree(a);
    assert(calls == 0);
    inspect(b);
    sfree(b);
    assert(calls == 3);
    calls = 0;
    a = shared_arr(int, 3, {7, 11, 13}, destroy_element,
                   {&token, sizeof(token)});
    inspect(a);
    b = sref(a);
    sfree(a);
    assert(calls == 0);
    inspect(b);
    sfree(b);
    assert(calls == 3);
    calls = 0;
    a = unique_ptr(int[3], {7, 11, 13}, destroy_element,
                   {&token, sizeof(token)});
    inspect(a);
    sfree(a);
    assert(calls == 3);
    puts("libcsptr downstream array API regression: PASS");
    return 0;
}
