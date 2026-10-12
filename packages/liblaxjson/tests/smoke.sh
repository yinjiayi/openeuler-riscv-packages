#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- liblaxjson liblaxjson-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/check.c" <<'EOF'
#include <laxjson.h>
#include <string.h>

struct counts { int properties, numbers, true_values, objects, ends; };

static int on_string(struct LaxJsonContext *ctx, enum LaxJsonType type,
                     const char *value, int length) {
    struct counts *n = ctx->userdata;
    if (type != LaxJsonTypeProperty || length != 1 || value[0] != 'x') return 1;
    ++n->properties;
    return 0;
}
static int on_number(struct LaxJsonContext *ctx, double value) {
    struct counts *n = ctx->userdata;
    if (value != 1.0) return 1;
    ++n->numbers;
    return 0;
}
static int on_primitive(struct LaxJsonContext *ctx, enum LaxJsonType type) {
    struct counts *n = ctx->userdata;
    if (type != LaxJsonTypeTrue) return 1;
    ++n->true_values;
    return 0;
}
static int on_begin(struct LaxJsonContext *ctx, enum LaxJsonType type) {
    struct counts *n = ctx->userdata;
    if (type != LaxJsonTypeObject) return 1;
    ++n->objects;
    return 0;
}
static int on_end(struct LaxJsonContext *ctx, enum LaxJsonType type) {
    struct counts *n = ctx->userdata;
    if (type != LaxJsonTypeObject) return 1;
    ++n->ends;
    return 0;
}
int main(void) {
    const char input[] = "{\"x\":1}";
    struct counts n = {0};
    struct LaxJsonContext *ctx = lax_json_create();
    if (!ctx) return 1;
    ctx->userdata = &n;
    ctx->string = on_string;
    ctx->number = on_number;
    ctx->primitive = on_primitive;
    ctx->begin = on_begin;
    ctx->end = on_end;
    if (lax_json_feed(ctx, strlen(input), input) != LaxJsonErrorNone) return 2;
    if (lax_json_eof(ctx) != LaxJsonErrorNone) return 3;
    lax_json_destroy(ctx);
    return n.properties == 1 && n.numbers == 1 && n.true_values == 0 &&
           n.objects == 1 && n.ends == 1 ? 0 : 4;
}
EOF
cc "$smoke_dir/check.c" -llaxjson -o "$smoke_dir/check"
"$smoke_dir/check"
