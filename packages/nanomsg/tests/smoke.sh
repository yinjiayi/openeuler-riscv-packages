#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- nanomsg nanomsg-devel
rpm -q --provides nanomsg | grep -F 'libnanomsg.so.6()(64bit)'
nanocat --help >/dev/null

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/nanomsg-smoke.c" <<'EOF'
#include <nanomsg/nn.h>
#include <nanomsg/pair.h>
#include <string.h>

int main(void) {
    static const char message[] = "RVA23";
    char buffer[sizeof message] = {0};
    int timeout = 2000;
    int receiver = nn_socket(AF_SP, NN_PAIR);
    int sender = nn_socket(AF_SP, NN_PAIR);
    if (receiver < 0 || sender < 0)
        return 1;
    if (nn_setsockopt(receiver, NN_SOL_SOCKET, NN_RCVTIMEO,
                      &timeout, sizeof timeout) < 0 ||
        nn_bind(receiver, "inproc://openeuler-rva23-smoke") < 0 ||
        nn_connect(sender, "inproc://openeuler-rva23-smoke") < 0 ||
        nn_send(sender, message, sizeof message, 0) != (int) sizeof message ||
        nn_recv(receiver, buffer, sizeof buffer, 0) != (int) sizeof message ||
        memcmp(message, buffer, sizeof message) != 0)
        return 1;
    return nn_close(sender) < 0 || nn_close(receiver) < 0;
}
EOF
cc $({ pkg-config --cflags nanomsg; }) \
  "$smoke_dir/nanomsg-smoke.c" -o "$smoke_dir/nanomsg-smoke" \
  $({ pkg-config --libs nanomsg; })
"$smoke_dir/nanomsg-smoke"
