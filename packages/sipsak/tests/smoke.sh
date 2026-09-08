#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- sipsak
installed_version=$(rpm -q --qf '%{VERSION}' sipsak)
version_output=$(sipsak --version)
grep -F "${installed_version}" <<<"${version_output}"
grep -F 'SRV_SUPPORT(ARES)' <<<"${version_output}"
