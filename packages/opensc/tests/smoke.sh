#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$(rpm -q --qf '%{VERSION}-%{RELEASE}' opensc)" = "0.23.0-8"
opensc-tool --version
# OpenSC 0.23.0 prints usage and exits 2; --help has no separate success path.
help_status=0
help_text=$(pkcs11-tool --help 2>&1) || help_status=$?
test "$help_status" = 2
grep -q -- '--write-object' <<< "$help_text"
test -f /usr/lib64/opensc-pkcs11.so
echo "Installed OpenSC supplier version and CLI smoke passed; token/card hardware is unverified."
