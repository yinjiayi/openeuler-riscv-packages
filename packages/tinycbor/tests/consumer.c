/* SPDX-License-Identifier: MIT
 * Copyright (c) 2026 yinjiayi
 * Downstream installed API acceptance, not an upstream test case. */
#ifdef USE_CMAKE_EXPORT
# include <tinycbor/cbor.h>
#else
# include <cbor.h>
#endif
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    uint8_t buf[128];
    CborEncoder encoder, map;
    CborParser parser;
    CborValue root, item, value;
    int64_t number = 0;
    bool flag = false;
    cbor_encoder_init(&encoder, buf, sizeof(buf), 0);
    assert(cbor_encoder_create_map(&encoder, &map, 2) == CborNoError);
    assert(cbor_encode_text_stringz(&map, "n") == CborNoError);
    assert(cbor_encode_int(&map, 42) == CborNoError);
    assert(cbor_encode_text_stringz(&map, "ok") == CborNoError);
    assert(cbor_encode_boolean(&map, true) == CborNoError);
    assert(cbor_encoder_close_container_checked(&encoder, &map) == CborNoError);
    size_t len = cbor_encoder_get_buffer_size(&encoder, buf);
    assert(len == 9);
    assert(memcmp(buf, "\xa2\x61n\x18\x2a\x62ok\xf5", 9) == 0);
    assert(cbor_parser_init(buf, len, 0, &parser, &root) == CborNoError);
    assert(cbor_value_is_map(&root));
    assert(cbor_value_map_find_value(&root, "n", &value) == CborNoError);
    assert(cbor_value_get_int64(&value, &number) == CborNoError && number == 42);
    assert(cbor_value_map_find_value(&root, "ok", &value) == CborNoError);
    assert(cbor_value_get_boolean(&value, &flag) == CborNoError && flag);
    assert(cbor_value_enter_container(&root, &item) == CborNoError);
    while (!cbor_value_at_end(&item))
        assert(cbor_value_advance(&item) == CborNoError);
    assert(cbor_value_leave_container(&root, &item) == CborNoError);
    assert(cbor_value_get_next_byte(&root) == buf + len);
    puts("downstream installed API passed");
    return 0;
}
