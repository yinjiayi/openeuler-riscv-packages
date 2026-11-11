/* SPDX-License-Identifier: MIT
 * Copyright (c) 2026 yinjiayi
 * Downstream representative API checks, not the upstream test suite.
 */
#include <json.h>
#include <stdio.h>
#include <string.h>

#define REQUIRE(x) do { if (!(x)) { fprintf(stderr, "check failed: %s\n", #x); return 1; } } while (0)
struct events { unsigned count[JSON_NULL + 1]; };
static int event(void *ctx, int type, const char *data, uint32_t len)
{
    struct events *e = ctx;
    if (type < JSON_NONE || type > JSON_NULL) return 1;
    e->count[type]++;
    if (type == JSON_KEY && (len != 1 || data[0] != 'x')) return 1;
    return 0;
}
struct output { char data[128]; size_t length; };
static int output(void *ctx, const char *data, uint32_t len)
{
    struct output *o = ctx;
    if (o->length + len >= sizeof(o->data)) return 1;
    memcpy(o->data + o->length, data, len);
    o->length += len; o->data[o->length] = 0;
    return 0;
}
int main(void)
{
    static const char text[] = "{\"x\":[1,true,false,null,\"z\"]}";
    json_parser p; struct events e = {{0}}; uint32_t used = 0;
    REQUIRE(json_parser_init(&p, NULL, event, &e) == 0);
    REQUIRE(json_parser_string(&p, text, 7, &used) == 0 && used == 7);
    for (size_t i = 7; i < sizeof(text) - 1; ++i)
        REQUIRE(json_parser_char(&p, (unsigned char)text[i]) == 0);
    REQUIRE(json_parser_is_done(&p));
    REQUIRE(e.count[JSON_OBJECT_BEGIN] == 1 && e.count[JSON_OBJECT_END] == 1);
    REQUIRE(e.count[JSON_ARRAY_BEGIN] == 1 && e.count[JSON_ARRAY_END] == 1);
    REQUIRE(e.count[JSON_KEY] == 1 && e.count[JSON_INT] == 1);
    REQUIRE(e.count[JSON_TRUE] == 1 && e.count[JSON_FALSE] == 1);
    REQUIRE(e.count[JSON_NULL] == 1 && e.count[JSON_STRING] == 1);
    REQUIRE(json_parser_free(&p) == 0);
    REQUIRE(json_parser_init(&p, NULL, NULL, NULL) == 0);
    REQUIRE(!json_parser_is_done(&p));
    REQUIRE(json_parser_string(&p, "{]", 2, &used) != 0);
    REQUIRE(json_parser_free(&p) == 0);
    json_printer pr; struct output o = {{0}, 0};
    REQUIRE(json_print_init(&pr, output, &o) == 0);
    REQUIRE(json_print_args(&pr, json_print_raw, JSON_OBJECT_BEGIN,
                           JSON_KEY, "x", -1, JSON_INT, "1", -1,
                           JSON_OBJECT_END, -1) == 0);
    REQUIRE(strcmp(o.data, "{\"x\":1}") == 0);
    REQUIRE(json_print_free(&pr) == 0);
    puts("libjson downstream API checks passed");
    return 0;
}
