#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libseccomp libseccomp-devel python3-libseccomp
scmp_sys_resolver read | grep -E '^[0-9]+$'
python3 -c 'import seccomp; assert seccomp.system_arch() != 0'
