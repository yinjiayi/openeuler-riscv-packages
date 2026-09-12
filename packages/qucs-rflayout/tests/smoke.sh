#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- qucs-rflayout
test -x /usr/bin/qucsrflayout
version_output=$(/usr/bin/qucsrflayout --version)
grep -Fx -- 'Qucs-RFlayout 2.1.2' <<<"$version_output"
