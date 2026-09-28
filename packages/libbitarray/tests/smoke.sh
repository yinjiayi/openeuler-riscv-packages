#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libbitarray libbitarray-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'C'
#include <bit_array.h>

int main(void) {
  BIT_ARRAY *bits = bit_array_create(65);
  if (!bits || bit_array_length(bits) != 65) return 1;
  bit_array_set_bit(bits, 0);
  bit_array_set_bit(bits, 64);
  if (!bit_array_get_bit(bits, 0) ||
      !bit_array_get_bit(bits, 64) ||
      bit_array_get_bit(bits, 1)) return 2;
  bit_array_clear_bit(bits, 64);
  if (bit_array_get_bit(bits, 64)) return 3;
  bit_array_free(bits);
  return 0;
}
C
gcc "$smoke_dir/smoke.c" -lbitarr -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
