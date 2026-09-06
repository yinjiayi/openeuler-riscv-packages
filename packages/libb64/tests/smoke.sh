#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libb64 libb64-devel
test -x /usr/bin/b64
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <b64/cdecode.h>
#include <b64/cencode.h>
#include <string.h>

int main(void)
{
    const char input[] = "hello world";
    char encoded[64] = {0};
    char decoded[64] = {0};
    base64_encodestate encoder;
    base64_decodestate decoder;
    size_t encoded_len;

    base64_init_encodestate(&encoder);
    encoded_len = base64_encode_block(input, strlen(input), encoded, &encoder);
    encoded_len += base64_encode_blockend(encoded + encoded_len, &encoder);
    base64_init_decodestate(&decoder);
    base64_decode_block(encoded, encoded_len, decoded, &decoder);
    return strcmp(input, decoded) == 0 ? 0 : 1;
}
EOF
${CC:-cc} -std=c99 -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  -lb64 -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
