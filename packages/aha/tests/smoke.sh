#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- aha
installed_version=$(rpm -q --qf '%{VERSION}' aha)
aha --version | grep -F "$installed_version"
output=$(printf '\033[31mred\033[0m\n' | aha --no-header)
grep -F 'color:red' <<< "$output"
grep -F '>red<' <<< "$output"
