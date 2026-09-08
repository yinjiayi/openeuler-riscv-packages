#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.c" <<'EOF'
#include <http_parser.h>
#include <string.h>

static int completed(http_parser *parser) {
  int *flag = parser->data;
  *flag = 1;
  return 0;
}

int main(void) {
  const char request[] = "GET /repo HTTP/1.1\r\nHost: localhost\r\n\r\n";
  http_parser parser;
  http_parser_settings settings;
  int complete = 0;
  http_parser_init(&parser, HTTP_REQUEST);
  http_parser_settings_init(&settings);
  parser.data = &complete;
  settings.on_message_complete = completed;
  size_t parsed = http_parser_execute(&parser, &settings, request,
                                      sizeof(request) - 1);
  return parsed == sizeof(request) - 1 && complete && parser.method == HTTP_GET
             ? 0
             : 1;
}
EOF

${CC:-cc} ${CFLAGS:-} "$tmpdir/smoke.c" -lhttp_parser -o "$tmpdir/smoke"
"$tmpdir/smoke"
