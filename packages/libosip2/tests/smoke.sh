#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libosip2 libosip2-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <osip2/osip.h>
#include <osipparser2/osip_uri.h>
#include <osipparser2/osip_port.h>
#include <string.h>

int main(void) {
    osip_t *core = 0;
    osip_uri_t *uri = 0;
    char *text = 0;
    int ok;
    if (osip_init(&core) != 0 || !core) return 1;
    if (osip_uri_init(&uri) != 0 || !uri) return 2;
    if (osip_uri_parse(uri, "sip:alice@example.org") != 0) return 3;
    if (osip_uri_to_str(uri, &text) != 0 || !text) return 4;
    ok = strcmp(text, "sip:alice@example.org") == 0;
    osip_free(text);
    osip_uri_free(uri);
    osip_release(core);
    return ok ? 0 : 5;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libosip2) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
