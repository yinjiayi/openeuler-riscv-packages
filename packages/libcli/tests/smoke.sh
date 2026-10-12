#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libcli libcli-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat > "$smoke_dir/smoke.c" <<'EOF'
#include <libcli.h>
#include <string.h>

static int called;

static int probe(struct cli_def *cli, const char *command, char **argv, int argc) {
    (void)cli;
    if (strcmp(command, "probe") != 0 || argc != 1 || strcmp(argv[0], "RVA23") != 0)
        return CLI_ERROR;
    called++;
    return CLI_OK;
}

int main(void) {
    struct cli_def *cli = cli_init();
    if (cli == NULL) return 1;
    if (cli_register_command(cli, NULL, "probe", probe,
                             PRIVILEGE_UNPRIVILEGED, MODE_EXEC, NULL) == NULL) return 2;
    if (cli_run_command(cli, "probe RVA23") != CLI_OK || called != 1) return 3;
    if (cli_done(cli) != CLI_OK) return 4;
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -lcli -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
