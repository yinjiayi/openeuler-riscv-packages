#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmnl libmnl-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libmnl/libmnl.h>
int main(void) {
    char buffer[MNL_SOCKET_BUFFER_SIZE];
    struct nlmsghdr *header = mnl_nlmsg_put_header(buffer);
    header->nlmsg_type = 0x10;
    return header->nlmsg_len == MNL_NLMSG_HDRLEN &&
           mnl_nlmsg_get_payload_len(header) == 0 ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libmnl) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
