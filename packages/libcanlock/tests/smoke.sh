#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libcanlock libcanlock-devel
command -v canlock
command -v canlock-mhp
command -v canlock-hfp
pkg-config --print-errors --exists libcanlock-3 libcanlock-hp-3 || {
  printf '%s\n' 'Installed pkg-config metadata could not be resolved.' >&2
  printf '%s\n' 'Installed metadata files:' >&2
  ls -l /usr/lib64/pkgconfig/libcanlock*.pc >&2
  printf '%s\n' 'pkg-config search path:' >&2
  pkg-config --variable=pc_path pkg-config >&2 || true
  exit 1
}

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'C'
#include <libcanlock-3/canlock.h>
#include <libcanlock-3/canlock-hp.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    const unsigned char secret[] = "0123456789abcdef0123456789abcdef";
    const unsigned char message[] = "<rva23@example.org>";
    const char header[] = "Cancel-Lock: sha256:example\r\n\r\n";
    char *key = cl_get_key(CL_SHA256, secret, sizeof(secret) - 1,
                           message, sizeof(message) - 1);
    char *lock = cl_get_lock(CL_SHA256, secret, sizeof(secret) - 1,
                             message, sizeof(message) - 1);
    char *field = cl_hp_get_field(header, sizeof(header) - 1, "Cancel-Lock");
    char *key_string = NULL;
    char *lock_string = NULL;
    int ok = key != NULL && lock != NULL &&
             cl_split(key, &key_string) == CL_SHA256 &&
             cl_split(lock, &lock_string) == CL_SHA256 &&
             cl_verify(CL_SHA256, key_string, lock_string) == 0 &&
             field != NULL && strstr(field, "sha256:example") != NULL;
    free(key);
    free(lock);
    free(field);
    return ok ? 0 : 1;
}
C

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags libcanlock-3 libcanlock-hp-3) \
  "$smoke_dir/smoke.c" \
  $(pkg-config --libs libcanlock-3 libcanlock-hp-3) \
  -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
