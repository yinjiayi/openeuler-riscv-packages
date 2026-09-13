#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmodbus libmodbus-devel
rpm -q --provides libmodbus | grep -F 'libmodbus.so.5()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libmodbus-smoke.c" <<'EOF'
#include <modbus/modbus.h>

int main(void) {
    modbus_t *context = modbus_new_tcp("127.0.0.1", 1502);
    if (context == NULL)
        return 1;
    modbus_set_slave(context, 1);
    modbus_close(context);
    modbus_free(context);
    return 0;
}
EOF
cc "$smoke_dir/libmodbus-smoke.c" -o "$smoke_dir/libmodbus-smoke" \
  $({ pkg-config --cflags --libs libmodbus; })
"$smoke_dir/libmodbus-smoke"
