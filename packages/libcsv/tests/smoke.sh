#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.c" <<'EOF'
#include <csv.h>
#include <stdio.h>

static void field(void *data, size_t len, void *count) {
  (void)data;
  (void)len;
  ++*(unsigned int *)count;
}

static void row(int terminator, void *count) {
  (void)terminator;
  ++*(unsigned int *)count;
}

int main(void) {
  struct csv_parser parser;
  unsigned int count = 0;
  const char input[] = "alpha,beta\ngamma,delta\n";

  if (csv_init(&parser, CSV_STRICT) != 0)
    return 1;
  if (csv_parse(&parser, input, sizeof(input) - 1, field, row, &count) !=
      sizeof(input) - 1) {
    csv_free(&parser);
    return 2;
  }
  if (csv_fini(&parser, field, row, &count) != 0) {
    csv_free(&parser);
    return 3;
  }
  csv_free(&parser);
  return count == 6 ? 0 : 4;
}
EOF

${CC:-cc} ${CFLAGS:-} "$tmpdir/smoke.c" -lcsv -o "$tmpdir/smoke"
"$tmpdir/smoke"
