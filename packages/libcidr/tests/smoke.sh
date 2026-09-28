#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libcidr libcidr-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libcidr.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    CIDR *address = cidr_from_str("192.0.2.1/24");
    CIDR *network;
    CIDR *ipv6;
    char *text;
    if (!address || strncmp(cidr_version(), CIDR_VERSION, strlen(CIDR_VERSION)))
        return 1;
    network = cidr_addr_network(address);
    if (!network)
        return 2;
    text = cidr_to_str(network, CIDR_NOFLAGS);
    if (!text || strcmp(text, "192.0.2.0/24"))
        return 3;
    free(text);
    cidr_free(network);
    cidr_free(address);
    ipv6 = cidr_from_str("2001:db8::1/64");
    if (!ipv6 || cidr_get_proto(ipv6) != CIDR_IPV6)
        return 4;
    cidr_free(ipv6);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -lcidr -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
cidrcalc 192.0.2.1/24 >"$smoke_dir/cidrcalc.out"
grep -Fq '192.0.2.0/24' "$smoke_dir/cidrcalc.out"
